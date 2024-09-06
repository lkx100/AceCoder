# File: users/backends.py

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
        # Ensure that the email domain is allowed
        email = sociallogin.user.email
        email_domain = email.split('@')[1] if '@' in email else ''
        allowed_domains = settings.ALLOWED_EMAILS
        
        if email_domain not in allowed_domains:
            messages.error(request, "Email domain is not allowed.")
            raise ValidationError("Email domain is not allowed.")
        
        # Ensure that the user exists
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass