from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    phone_number = PhoneNumberField(required=False)
    
    def validate_email(self, email):
        """
        Check that the email is unique (case-insensitive)
        """
        print(f"DEBUG: Validating email: {email}")  # Debug print
        
        if User.objects.filter(email__iexact=email).exists():
            print(f"DEBUG: Email {email} already exists!")  # Debug print
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )
        
        print(f"DEBUG: Email {email} is available")  # Debug print
        return email.lower()  # Normalize email to lowercase
    
    def validate(self, data):
        """
        Cross-field validation
        """
        print(f"DEBUG: Full validation data: {data}")  # Debug print
        
        # Call parent validation first
        data = super().validate(data)
        
        # Additional validation for email (backup check)
        email = data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                'email': 'A user with this email address already exists.'
            })
            
        return data
    
    def validate_phone_number(self, phone_number):
        """
        Check that the phone number is unique if provided
        """
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return phone_number
    
    def custom_signup(self, request, user):
        """
        Save additional fields to the user
        """
        print(f"DEBUG: custom_signup called for user: {user.email}")  # Debug print
        
        phone_number = self.validated_data.get('phone_number')
        if phone_number:
            user.phone_number = phone_number
            try:
                user.save(update_fields=['phone_number'])
                print(f"DEBUG: Phone number saved successfully")  # Debug print
            except IntegrityError as e:
                print(f"DEBUG: IntegrityError in custom_signup: {e}")  # Debug print
                raise serializers.ValidationError(
                    "Unable to save phone number. It may already exist."
                )
    
    def save(self, request):
        """
        Create the user with proper error handling
        """
        print(f"DEBUG: save() method called")  # Debug print
        print(f"DEBUG: validated_data: {self.validated_data}")  # Debug print
        
        try:
            user = super().save(request)
            print(f"DEBUG: User created successfully: {user.email}")  # Debug print
            return user
        except IntegrityError as e:
            print(f"DEBUG: IntegrityError in save(): {e}")  # Debug print
            
            # This shouldn't happen if validation works properly, but just in case
            if 'email' in str(e):
                raise serializers.ValidationError({
                    'email': 'A user with this email address already exists.'
                })
            elif 'phone_number' in str(e):
                raise serializers.ValidationError({
                    'phone_number': 'A user with this phone number already exists.'
                })
            else:
                raise serializers.ValidationError({
                    'non_field_errors': 'Registration failed due to duplicate data.'
                })