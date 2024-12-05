from celery import shared_task
from django.core.mail import send_mail
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_password_reset_email(email, reset_link):
    """
    Send a password reset email asynchronously.
    """
    subject = "Reset Your Password"
    message = f"Click the link below to reset your password:\n\n{reset_link}"
    from_email = "no-reply@example.com"

    try:
        send_mail(subject, message, from_email, [email])
        return f"Password reset email sent to {email}"
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {e}")
        return f"Failed to send password reset email to {email}"

@shared_task
def log_failed_login(email, ip_address):
    """
    Log failed login attempts asynchronously.
    """
    attempts = cache.get(f"{email}_failed_attempts", 0) + 1
    cache.set(f"{email}_failed_attempts", attempts, timeout=3600)

    if attempts >= 5:
        # Lock the account for 1 hour
        cache.set(f"{email}_locked", True, timeout=3600)
        logger.warning(f"Account locked for {email} after {attempts} failed login attempts.")

    logger.info(f"Failed login attempt for {email} from IP {ip_address}. Attempts: {attempts}")
