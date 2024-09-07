import logging
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.text import slugify

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Log the extra_data for debugging
        logger.debug(f"Extra data: {sociallogin.account.extra_data}")

        # Attempt to get the email from the user object first
        email = sociallogin.user.email

        # If the email is not set on the user object, try to get it from extra_data
        if not email:
            email = sociallogin.account.extra_data.get('email', '')
            if not email:
                print(f"Email not found in extra_data: {sociallogin.account.extra_data}")
                raise ValidationError("Email not found in extra_data.")
            sociallogin.user.email = email
            sociallogin.user.save()
            logger.debug(f"Email set from extra_data: {email}")

        email_domain = email.split('@')[1] if email else ''

        # Skip the rest of the method if the user is new and the email domain is gmail.com
        if sociallogin.user.pk is None:
            logger.debug("New user")
            if email_domain == 'gmail.com':
                logger.debug("Skipping pre_social_login for new Gmail user.")
                return

        logger.debug(f"Processing email: {email}")

        if not email or '@' not in email:
            raise ValidationError("Invalid email address.")