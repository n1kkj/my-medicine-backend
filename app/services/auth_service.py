from urllib.parse import urljoin

from django.contrib.auth import login as auth_login
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
    def is_logged_in(email):
        """Проверка статуса входа пользователя"""
        user = User.objects.filter(username=email).first()
        if (not user) or (not user.is_active):
            return {'is_authenticated': False}
        return {
            'is_authenticated': True,
            'user_id': user.id,
            'email': user.email,
            'surname': user.surname,
            'phone': user.phone,
            'subscribe': user.subscribe,
        }

    @staticmethod
    def login(request, email, password):
        """Вход в систему"""
        try:
            user = User.objects.filter(username=email).first()

            if user is not None and user.check_password(password):
                auth_login(request, user)

                if not user.is_active:
                    AuthService._send_verification_email(user)
                    raise Exception('Пожалуйста, подтвердите ваш email.')

                return {
                    'success': True,
                    'user_id': user.id,
                    'email': user.email,
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
                is_active=False,
                first_name=kwargs.get('name'),
                surname=kwargs.get('surname'),
                phone=kwargs.get('phone'),
                subscribe=kwargs.get('subscribe', False),
            )
            user.set_password(password)
            user.save()

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
            url = urljoin(settings.BASE_URL, f'/api/auth/verify-email/{uid}/{token}/')
            subject = 'Подтвердите ваш email'
            message = f'Для подтверждения email перейдите по ссылке: {url}'
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
            url = urljoin(settings.BASE_URL, f'/api/auth/reset-password-form/{uid}/{token}/')
            message = f'Для сброса пароля перейдите по ссылке: {url}'
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
    def is_email_verified(email: str):
        """Проверка подтверждения email"""
        user = User.objects.filter(username=email).first()
        if not user:
            return False
        return user.is_active

    @staticmethod
    def resend_verification_email(email):
        """Повторная отправка письма с подтверждением"""
        user = User.objects.filter(username=email).first()
        if not user:
            return False
        if not user.is_active:
            AuthService._send_verification_email(user)
            return True
        raise Exception('Email уже подтвержден или пользователь не аутентифицирован')
