import jwt

from django.http        import JsonResponse

from user.models            import User
from insa.settings      import SECRET_KEY


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)

        if token == None:
            return JsonResponse({"message": "INVALID_LOGIN"}, status=401)
        
        d_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=d_token['id'])
        request.user = user
        return func(self, request, *args, **kwargs)
    return wrapper
