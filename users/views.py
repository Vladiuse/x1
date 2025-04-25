from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import CustomUserLoginSerializer, CustomUserRegisterSerializer


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
