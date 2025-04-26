from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .models import ResetUserPasswordCode
from rest_framework.decorators import action

from users.serializers import (
    CustomUserLoginSerializer,
    CustomUserRegisterSerializer,
    CustomUserChangePasswordSerializer,
    CreateResetPasswordCodeSerializer,
    ResetPasswordCodeSerializer,
    ActivateResetPasswordSerializer,
)

from .utils import logout_user_sessions


class SessionLoginView(APIView):
    template_name = 'users/login.html'

    def get_renderers(self):
        if self.request.method == 'GET':
            return [TemplateHTMLRenderer()]
        return [JSONRenderer()]

    def get(self, request, format=None):  # noqa: A002
        return Response(template_name=self.template_name)

    def post(self, request, format=None):  # noqa: A002
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if user is not None:
            login(request, user)
            return Response({'success': True})
        return Response(
            {'success': False, 'non_field_errors': 'Wrong email or password'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

class CustomUserRegisterView(APIView):
    template_name = 'users/sign_up.html'

    def get_renderers(self):
        if self.request.method == 'GET':
            return [TemplateHTMLRenderer()]
        return [JSONRenderer()]

    def get(self, request, format=None):  # noqa: A002
        return Response(template_name=self.template_name)

    def post(self, request, format=None):  # noqa: A002
        serializer = CustomUserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response({'success': True})


class SessionLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):  # noqa: A002
        logout(request)
        return Response({'success': True}, status=status.HTTP_200_OK)


class CustomUserChangePasswordView(APIView):

    template_name = 'users/change_password.html'
    permission_classes = [IsAuthenticated]

    def get_renderers(self):
        if self.request.method == 'GET':
            return [TemplateHTMLRenderer()]
        return [JSONRenderer()]

    def get(self, request, format=None):  # noqa: A002
        return Response(template_name=self.template_name)

    def post(self, request, format=None):   # noqa: A002
        serializer = CustomUserChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['password1']
        user = request.user
        user.set_password(new_password)
        user.save()
        logout_user_sessions(user=user)
        return Response({'success': True}, status=status.HTTP_200_OK)


class CustomUserCreateResetPasswordView(APIView):
    template_name = 'users/change_password.html'

    def get_renderers(self):
        if self.request.method == 'GET':
            return [TemplateHTMLRenderer()]
        return [JSONRenderer()]

    def get(self, request, format=None):  # noqa: A002
        return Response(template_name=self.template_name)

    def post(self, request, format=None):  # noqa: A002
        serializer = CreateResetPasswordCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.instance


class ResetPasswordView(mixins.RetrieveModelMixin,
                        GenericViewSet):

    queryset = ResetUserPasswordCode.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateResetPasswordCodeSerializer
        return ResetPasswordCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateResetPasswordCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password = serializer.save()
        serializer = ResetPasswordCodeSerializer(reset_password)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def activate_reset_password(self, request, pk=None):
        serializer = ActivateResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password_code = self.get_object()
        if serializer.validated_data['reset_password_code'] == password_code.reset_password_code:
            return Response({'success': True})
        return Response({'success': False})
