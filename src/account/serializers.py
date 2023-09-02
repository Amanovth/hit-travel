from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from .models import User


class RegisterAPIViewSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, max_length=68, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name', 'password', 'confirm_password']

    def save(self, *args, **kwargs):
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        phone = self.validated_data['phone']

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        if password != confirm_password:
            raise serializers.ValidationError({'response': False, 'password': _("Password doesn't match.")})
        user.set_password(password)
        user.save()
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()

    class Meta:
        fields = ['email', 'code']


class SendAgainCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        style={'input_type': 'email'},
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class PasswordResetUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Password do not much')
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'Password do not much'})
        return attrs


class UpdateProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo']


class PersonalInfoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_joined', 'last_login', 'photo',
                  'balance', 'bonuses']

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            photo_url = obj.photo.url
            return request.build_absolute_uri(photo_url)
        return None

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%Y/%m/%d %H:%M")

    def get_last_login(self, obj):
        if obj.last_login:
            return obj.last_login.strftime("%Y/%m/%d %H:%M")
