import jwt

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.common import MiddlewareMixin

SECRET_KEY = "django-insecure-o4@s$4=sk*^dnyi9l&9xtt!r-45sv&4%7hr-9jy2o_ii57$1b3"

class TokenAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.secret_key = SECRET_KEY

    def process_request(self, request):
        # Get the token from the request header
        token = request.META['HTTP_AUTHORIZATION']

        # Check if the token is present
        if not token:
            return JsonResponse({'error': 'Unauthorized'})

        # Split the token into the prefix and the token
        prefix, token = token.split()

        # Check if the prefix is valid
        if prefix != 'Bearer':
            return JsonResponse({'error': 'Invalid token'})

        # Decode the token
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'})
        except jwt.InvalidSignatureError:
            return JsonResponse({'error': 'Invalid token'})

        # Get the user from the database
        user = get_user_model().objects.get(username=payload['email'])

        # Set the user on the request
        request.user = user

    def get_response(self, request):
        return self.get_response(request)