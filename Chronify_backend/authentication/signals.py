from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver
from django.core.cache import cache
from .tasks import log_failed_login, send_password_reset_email
from .tasks import send_password_reset_email


@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    user_agent = request.META['HTTP_USER_AGENT']
    print(f"User logged in from {ip} using {user_agent}")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


@receiver(user_login_failed)
def track_failed_logins(sender, credentials, request, **kwargs):
    email = credentials.get('email')
    ip_address = request.META.get('REMOTE_ADDR')
    log_failed_login.delay(email, ip_address)

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        reset_link = self.request.build_absolute_uri('/password-reset-confirm/')
        send_password_reset_email.delay(email, reset_link)
        return super().form_valid(form)


@shared_task
def cleanup_expired_tokens():
    """
    Periodically remove expired tokens.
    """
    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
    from datetime import datetime

    tokens_deleted = OutstandingToken.objects.filter(expires_at__lt=datetime.now()).delete()
    logger.info(f"Deleted {tokens_deleted[0]} expired tokens.")
