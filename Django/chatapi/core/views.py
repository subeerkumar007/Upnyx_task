from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import secrets
from django.db.models import F

from .serializers import RegisterSerializer, LoginSerializer, ChatRequestSerializer
from .models import AuthToken, User, Chat


def _extract_token_from_request(request, fallback_data: dict | None = None) -> str | None:
    auth_header = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION")
    if auth_header and auth_header.lower().startswith("token "):
        return auth_header.split(" ", 1)[1].strip()
    if fallback_data is not None:
        return fallback_data.get("token")
    return None


class RegisterView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Registration successful", "username": user.username, "tokens": user.tokens},
                status=status.HTTP_201_CREATED,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        # Optionally invalidate old tokens; here we keep only one active token
        AuthToken.objects.filter(user=user).delete()
        token_key = secrets.token_hex(32)
        token = AuthToken.objects.create(user=user, key=token_key)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class ChatView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        token_key = _extract_token_from_request(request, serializer.validated_data)
        if not token_key:
            return Response({"error": "Authentication token required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = AuthToken.objects.select_related("user").get(key=token_key)
        except AuthToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        user: User = token.user
        message: str = serializer.validated_data["message"]

        # Deduct 100 tokens atomically if user has enough
        updated_rows = User.objects.filter(id=user.id, tokens__gte=100).update(tokens=F("tokens") - 100)
        if updated_rows == 0:
            return Response({"error": "Insufficient tokens"}, status=status.HTTP_400_BAD_REQUEST)

        # Refresh tokens value
        user.refresh_from_db(fields=["tokens"])

        # Dummy AI response
        ai_response = "This is a dummy AI response."

        # Persist chat
        chat = Chat.objects.create(user=user, message=message, response=ai_response)

        return Response(
            {"response": ai_response, "remaining_tokens": user.tokens, "chat_id": chat.id},
            status=status.HTTP_200_OK,
        )


class BalanceView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        token_key = _extract_token_from_request(request)
        if not token_key:
            return Response({"error": "Authentication token required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = AuthToken.objects.select_related("user").get(key=token_key)
        except AuthToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"tokens": token.user.tokens}, status=status.HTTP_200_OK)


