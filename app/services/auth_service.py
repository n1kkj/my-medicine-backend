from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.conf import settings
import logging

from app.models import User

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def is_logged_in(request):
        """Проверка статуса входа пользователя"""
        try:
            if request.user.is_authenticated:
                user = User.objects.get(pk=request.user.pk)
                return {
                    'is_authenticated': True,
                    'user_id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'surname': user.surname,
                    'phone': user.phone,
                    'subscribe': user.subscribe,
                }
            return {'is_authenticated': False}
        except Exception as e:
            logger.error(f'Error checking login status: {e}')
            return {'is_authenticated': False}

    @staticmethod
    def logout(request):
        """Выход из системы"""
        try:
            auth_logout(request)
            return {'success': True}
        except Exception as e:
            logger.error(f'Error during logout: {e}')
            return {'success': False}

    @staticmethod
    def login(request, email, password):
        """Вход в систему"""
        try:
            if not (email_user := User.objects.filter(email=email).first()):
                raise Exception('Неверные учетные данные')
            user = authenticate(request, username=email_user.username, password=password)
            if user is not None:
                auth_login(request, user)

                if not user.is_active:
                    AuthService._send_verification_email(user)
                    raise Exception('Пожалуйста, подтвердите ваш email.')

                return {
                    'success': True,
                    'user_id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'surname': user.surname,
                    'phone': user.phone,
                    'subscribe': user.subscribe,
                }
            raise Exception('Неверные учетные данные')
        except Exception as e:
            logger.error(f'Login error: {e}')
            raise

    @staticmethod
    def register(email, password, **kwargs):
        """Регистрация нового пользователя"""
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                is_active=False,
                first_name=kwargs.get('name'),
                surname=kwargs.get('surname'),
                phone=kwargs.get('phone'),
                subscribe=kwargs.get('subscribe', False),
            )

            AuthService._send_verification_email(user)

            return {'success': True, 'user_id': user.id, 'email': user.email}
        except Exception as e:
            logger.error(f'Registration error: {e}')
            raise

    @staticmethod
    def _send_verification_email(user):
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

    @staticmethod
    def send_password_reset_email(email):
        """Отправка письма для сброса пароля"""
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
            return True
        except User.DoesNotExist:
            logger.error(f'User with email {email} not found')
            raise Exception('Пользователь с таким email не найден')
        except Exception as e:
            logger.error(f'Error sending password reset email: {e}')
            raise

    @staticmethod
    def is_email_verified(request):
        """Проверка подтверждения email"""
        return request.user.is_authenticated and request.user.is_active

    @staticmethod
    def resend_verification_email(request):
        """Повторная отправка письма с подтверждением"""
        if request.user.is_authenticated and not request.user.is_active:
            AuthService._send_verification_email(request.user)
            return True
        raise Exception('Email уже подтвержден или пользователь не аутентифицирован')
