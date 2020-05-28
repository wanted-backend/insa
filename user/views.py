import json
import bcrypt
import jwt

from django.http        import JsonResponse, HttpResponse
from django.views       import View

from .models            import User
from wetargram.settings import SECRET_KEY

class SignUpView(View):
	def post(self, request):
		data = json.loads(request.body)
		User(
			email = data['email'],
			name = data['nmae'],
			password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
			agreement = data['agreement']
        ).save()
		return JsonResponse({'message':'success'}, status=200)
