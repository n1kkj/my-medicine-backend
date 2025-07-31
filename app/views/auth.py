from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from app.serializers.user import (
    UserSerializer,
    SuccessResponseSerializer,
    ErrorResponseSerializer,
    EmailVerifiedResponseSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    LoginSerializer,
    CheckAuthResponseSerializer,
)
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(method='get', responses={200: CheckAuthResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['get'])
    def check_auth(self, request):
        """Проверка статуса входа пользователя"""
        return AuthService.is_logged_in(request)

    @swagger_auto_schema(method='post', responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Выход из системы"""
        return AuthService.logout(request)

    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={
            200: UserSerializer,
            401: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
            400: ErrorResponseSerializer,
        },
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Вход в систему"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        return AuthService.login(request, email, password)

    @swagger_auto_schema(
        method='post', request_body=RegisterSerializer, responses={200: UserSerializer, 400: ErrorResponseSerializer}
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Регистрация нового пользователя"""
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.pop('email')
        password = serializer.validated_data.pop('password')

        return AuthService.register(email, password, **serializer.validated_data)

    @swagger_auto_schema(
        method='post',
        request_body=PasswordResetSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer},
    )
    @action(detail=False, methods=['post'])
    def send_password_reset(self, request):
        """Отправка письма для сброса пароля"""
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        AuthService.send_password_reset_email(email)
        return Response()

    @swagger_auto_schema(method='get', responses={200: EmailVerifiedResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['get'])
    def check_email_verified(self, request):
        """Проверка подтверждения email"""
        is_verified = AuthService.is_email_verified(request)
        return Response({'is_verified': is_verified})

    @swagger_auto_schema(method='post', responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        """Повторная отправка письма с подтверждением"""
        AuthService.resend_verification_email(request)
        return Response({'success': True})
