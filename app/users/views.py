from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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
from django.views.decorators.http import require_http_methods
from common.request_sender import RequestSender
from common.email_sender import EmailSender, EmailData
from common.exceptions import EmailNotSend
from rest_framework.reverse import reverse as rest_reverse


from users.serializers import (
    CustomUserLoginSerializer,
    CustomUserRegisterSerializer,
    CustomUserChangePasswordSerializer,
    CreateResetPasswordCodeSerializer,
    ResetPasswordCodeSerializer,
    ActivateResetPasswordSerializer,
    ResetPasswordSerializer,
)

from .utils import logout_user_sessions

email_sender = EmailSender(request_sender=RequestSender())
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


@require_http_methods(['GET'])
def reset_password(request):
    return render(request, 'users/reset_password.html')

class ResetPasswordView(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):

    queryset = ResetUserPasswordCode.objects.all()
    serializer_class = ResetPasswordCodeSerializer

    def _send_email(self, request,reset_password: ResetUserPasswordCode) -> None:
        email_data = EmailData(
            reset_password_code=reset_password.reset_password_code,
            email=reset_password.email,
            reset_url=rest_reverse('users:deactivate_reset_code', args=[reset_password.pk], request=request),
        )
        email_sender.send_email(email_data=email_data)

    def create(self, request, *args, **kwargs):
        serializer = CreateResetPasswordCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password = serializer.save()
        try:
            self._send_email(request=request, reset_password=reset_password)
        except EmailNotSend:
            return Response(
                {'non_field_errors': 'Ошибка при отправке письма'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        serializer = ResetPasswordCodeSerializer(reset_password,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def activate_reset_password(self, request, pk=None):
        serializer = ActivateResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password_code = self.get_object()
        is_code_correct, message = password_code.check_code(code=serializer.validated_data['reset_password_code'])
        if is_code_correct:
            return Response({'success': True})
        return Response({'success': False, 'message':message }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def reset_password(self, request, pk=None):
        reset_password_code = self.get_object()
        if reset_password_code.is_password_can_be_reset():
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_password = serializer.validated_data['password1']
            user = reset_password_code.user
            user.set_password(new_password)
            user.save()
            logout_user_sessions(user=user)
            reset_password_code.mark_password_reset()
            return Response({'status': True})
        return Response({'success': False, 'message': 'Password cant be reseted'})


def deactivate_reset_code(request, reset_code_id):
    reset_password_code = get_object_or_404(ResetUserPasswordCode, pk=reset_code_id)
    reset_password_code.deactivate()
    if request.user.is_authenticated:
        return redirect(reverse('users:change_password'))
    return redirect(reverse('users:reset_password'))
