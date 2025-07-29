from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
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
)

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(method='get', responses={200: CheckAuthResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['get'])
    def check_auth(self, request):
        """Проверка статуса входа пользователя"""
        try:
            if request.user.is_authenticated:
                user = User.objects.get(pk=request.user.pk)
                serializer = UserSerializer(user)
                return Response({'is_authenticated': True, **serializer.data})
            return Response({'is_authenticated': False})
        except Exception as e:
            logger.error(f'Error checking login status: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='post', responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Выход из системы"""
        try:
            auth_logout(request)
            return Response({'success': True})
        except Exception as e:
            logger.error(f'Error during logout: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

        try:
            print(email, password)
            user = User.objects.filter(email=email).first()
            if user is not None:
                pass_check = check_password(password, user.password)
                if not pass_check:
                    return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
            if user is not None:
                auth_login(request, user)

                if not user.is_active:
                    self._send_verification_email(user)
                    return Response({'error': 'Пожалуйста, подтвердите ваш email.'}, status=status.HTTP_403_FORBIDDEN)

                serializer = UserSerializer(user)
                return Response({'success': True, **serializer.data})
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f'Login error: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post', request_body=RegisterSerializer, responses={200: UserSerializer, 400: ErrorResponseSerializer}
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Регистрация нового пользователя"""
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=serializer.validated_data['email'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False,
                name=serializer.validated_data.get('name'),
                surname=serializer.validated_data.get('surname'),
                phone=serializer.validated_data.get('phone'),
                subscribe=serializer.validated_data.get('subscribe', False),
            )

            self._send_verification_email(user)

            user_serializer = UserSerializer(user)
            return Response({'success': True, **user_serializer.data})
        except Exception as e:
            logger.error(f'Registration error: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            subject = 'Сброс пароля'
            message = f'Для сброса пароля перейдите по ссылке: {settings.BASE_URL}/reset-password/{uid}/{token}/'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({'success': True})
        except User.DoesNotExist:
            logger.error(f'User with email {email} not found')
            return Response({'error': 'Пользователь с таким email не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error sending password reset email: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='get', responses={200: EmailVerifiedResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['get'])
    def check_email_verified(self, request):
        """Проверка подтверждения email"""
        is_verified = request.user.is_authenticated and request.user.is_active
        return Response({'is_verified': is_verified})

    @swagger_auto_schema(method='post', responses={200: SuccessResponseSerializer, 400: ErrorResponseSerializer})
    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        """Повторная отправка письма с подтверждением"""
        if request.user.is_authenticated and not request.user.is_active:
            self._send_verification_email(request.user)
            return Response({'success': True})
        return Response(
            {'error': 'Email уже подтвержден или пользователь не аутентифицирован'}, status=status.HTTP_400_BAD_REQUEST
        )

    def _send_verification_email(self, user):
        """Отправка письма с подтверждением email"""
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            subject = 'Подтвердите ваш email'
            message = f'Для подтверждения email перейдите по ссылке: {settings.BASE_URL}/verify-email/{uid}/{token}/'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f'Error sending verification email: {e}')
            raise
