from django.shortcuts import render
# In accounts/views.py
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        # Check for existing email before processing
        email = request.data.get('email', '').lower()
        if User.objects.filter(email__iexact=email).exists():
            return Response(
                {'email': ['A user with this email address already exists.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'email' in str(e):
                return Response(
                    {'email': ['A user with this email address already exists.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'non_field_errors': ['Registration failed due to duplicate data.']},
                status=status.HTTP_400_BAD_REQUEST
            )
