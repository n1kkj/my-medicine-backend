from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from app.models import User
from app.serializers.user import (
    UserSerializer,
    SuccessResponseSerializer,
    ErrorResponseSerializer,
    EmailVerifiedResponseSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    LoginSerializer,
    CheckAuthResponseSerializer,
    EmailSerializer,
)
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method='post',
        request_body=EmailSerializer,
        responses={200: CheckAuthResponseSerializer, 400: ErrorResponseSerializer},
    )
    @action(detail=False, methods=['post'])
    def check_auth(self, request):
        """Проверка статуса входа пользователя"""
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        return Response(AuthService.is_logged_in(email))

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

        return Response(AuthService.login(request, email, password))

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

        return Response(AuthService.register(email, password, **serializer.validated_data))

    @swagger_auto_schema(
        method='get',
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        },
    )
    @action(detail=False, methods=['get'], url_path='verify-email/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)')
    def verify_email(self, request, uidb64, token):
        """Подтверждение email пользователя"""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Неверная ссылка подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({'success': True, 'message': 'Email успешно подтвержден!'}, status=status.HTTP_200_OK)
            return Response({'success': True, 'message': 'Email уже был подтвержден ранее.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Неверная ссылка подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        request_body=EmailSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer},
    )
    @action(detail=False, methods=['post'], url_path='send-password-reset')
    def send_password_reset(self, request):
        """Отправка письма для сброса пароля"""
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        AuthService.send_password_reset_email(email)
        return Response()

    @swagger_auto_schema(
        method='post',
        request_body=EmailSerializer,
        responses={200: EmailVerifiedResponseSerializer, 400: ErrorResponseSerializer},
    )
    @action(detail=False, methods=['post'])
    def check_email_verified(self, request):
        """Проверка подтверждения email"""
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        is_verified = AuthService.is_email_verified(email)
        return Response({'is_verified': is_verified})

    @swagger_auto_schema(
        method='post',
        request_body=EmailSerializer,
        responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer},
    )
    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        """Повторная отправка письма с подтверждением"""
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        AuthService.resend_verification_email(email)
        return Response({'success': True})

    @swagger_auto_schema(
        method='post',
        request_body=PasswordResetSerializer,
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
        },
    )
    @action(detail=False, methods=['post'], url_path='reset-password/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)')
    def reset_password(self, request, uidb64, token):
        """Сброс пароля по токену из письма"""
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Неверная ссылка для сброса пароля'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Неверный токен для сброса пароля'}, status=status.HTTP_400_BAD_REQUEST)

        # Устанавливаем новый пароль
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({'success': True, 'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='reset-password-form/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)')
    def reset_password_form(self, request, uidb64, token):
        """Отображение формы для сброса пароля"""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            valid_link = default_token_generator.check_token(user, token)
            error = None if valid_link else 'Неверный токен для сброса пароля'
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            valid_link = False
            error = 'Неверная ссылка для сброса пароля'

        return render(
            request,
            'password_reset_form.html',
            {'uidb64': uidb64, 'token': token, 'error': error, 'valid_link': valid_link},
        )
