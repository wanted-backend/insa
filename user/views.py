import json
import bcrypt
import jwt
import re

from django.http        import JsonResponse, HttpResponse
from django.views       import View

from .models            import User
from insa.settings import SECRET_KEY

class SignUpView(View):
	validation = {
		'password': lambda password: False if not re.match('\w{6,15}', password) else True
	}

	def post(self, request):
		try:
			data = json.loads(request.body)
			
			# 빈 문자열 검사
			for value in data.values():
				if value == '':
					return HttpResponse(status=401)

			# 비밀번호 숫자, 영문 조합으로 6자리 이상인지 검증
			for value, validator in self.validation.items():
				if not validator(data[value]):
					return HttpResponse(status=401)

			User.objects.create(
				email = data['email'],
				name = data['name'],
				password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
				agreement = data['agreement']
			)
			return JsonResponse({'message':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'message': 'INVALID_KEYS'}, status=401)

class LogInView(View):
	def post(self, request):
		data = json.loads(request.body)
		try:
			if User.objects.filter(email=data['email']).exists():
				user = User.objects.get(email=data['email'])

				if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
					token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
					return JsonResponse({'token': token.decode('utf-8')}, status=200)
				return HttpResponse(status=401)
		except KeyError:
			return JsonResponse({'users':'invalid'}, status=401)
