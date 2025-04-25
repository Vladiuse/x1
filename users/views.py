from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import CustomUserLoginSerializer


class SessionLoginView(APIView):
    template_name = 'users/login.html'

    def get_renderers(self):
        if self.request.method == 'GET':
            return [TemplateHTMLRenderer()]
        return [JSONRenderer()]

    def get(self, request, format=None):
        return Response(template_name=self.template_name)

    def post(self, request, format=None):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request, email=serializer.validated_data['email'], 
            password=serializer.validated_data['password'],
        )
        if user is not None:
            login(request, user)
            return Response({'success': True})
        return Response({'success': False, 'message': 'Wrong email or password'},
                        status=status.HTTP_401_UNAUTHORIZED)
