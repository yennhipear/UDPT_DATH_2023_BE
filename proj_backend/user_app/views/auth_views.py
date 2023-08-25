from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt, datetime
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


from ..models.user import User
from ..serializers.user_serializers import UserSerializer

JWT_SECRET_KEY = settings.JWT_SECRET_KEY


class RegisterView(APIView):
    def post(self, request):
        print('register', request.user)
        email = request.data['email']
        password = request.data['password']
        displayname = request.data['displayname']
        if not email:
            return Response({'message': 'Email is required!'})
        if not password:
            return Response({'message': 'Password is required!'})
        if not displayname:
            return Response({'message': 'Display name is required!'})
        
        user = UserSerializer(User.objects.filter(Email=email), many=True).data
        if len(user) > 0:
            return Response({'message': 'Email already exists!'})

        user = User()
        user.DisplayName = displayname
        user.Email = email
        user.Password = make_password(password)
        user.AboutMe = 'My name is ' + displayname
        user.Location = 'Viet Nam'
        user.RoleID = 0
        user.RoleName = 'User'
        user.Status = 1
        user.Level = 1
        user.save()

        return Response({'message': 'Register successfully!'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if not email:
            return Response({'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'message': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(Email=email).values().first()
        if user is None:
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user['Password']):
            return Response({'message': 'Incorrect password!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.pop('Password')
        # payload = {
        #     'id': user['ID'],
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow(),
        #     'user': user
        # }
        # token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
            'token': '',
            'user': user
        }
        return Response({
            'message': 'Login successfully!',
            'data': response.data
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successfully!'
        }
        return response

class UserView(APIView):
    def get(self, request):
        print(request.user)
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(ID=payload['id']).values().first()
        user.pop('Password')
        return Response(user)