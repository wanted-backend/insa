import json
import bcrypt
import jwt
import re
import time

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from datetime           import datetime

from .models            import User, Security
from insa.settings      import SECRET_KEY

class UserRegisterView(View):
	validation = {
		'password': lambda password: re.match('\w{6,15}', password)
	}

	def post(self, request):
		try:
			data = json.loads(request.body)
			
			# 빈 문자열 검사
			for value in data.values():
				if value == '':
					return JsonResponse({'MESSAGE':'입력 정보를 확인해주세요'}, status=401)

			# 비밀번호 숫자, 영문 조합으로 6자리 이상인지 검증(특수문자는 선택)
			for value, validator in self.validation.items():
				if not validator(data[value]):
					return JsonResponse({'MESSAGE':'영문자, 숫자만 사용하여 6자 이상 입력해주세요.'}, status=401)

			User.objects.create(
				email = data['email'],
				name = data['name'],
				password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
				agreement = data['agreement']
			)
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class AdminRegisterView(View):
	validation = {
		'password': lambda password: re.match('\w{6,15}', password)
	}

	def post(self, request):
		try:
			data = json.loads(request.body)
			
			# 빈 문자열 검사
			for value in data.values():
				if value == '':
					return JsonResponse({'MESSAGE':'입력 정보를 확인해주세요'}, status=401)

			# 비밀번호 숫자, 영문 조합으로 6자리 이상인지 검증(특수문자는 선택)
			for value, validator in self.validation.items():
				if not validator(data[value]):
					return JsonResponse({'MESSAGE':'영문자, 숫자만 사용하여 6자 이상 입력해주세요.'}, status=401)

			User.objects.create(
				name = data['name'],
				position = data['position'],
				contact = data['contact'],
				email = data['email'],
				password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
			)
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class LogInView(View):
	def post(self, request):
		data = json.loads(request.body)
		try:
			if User.objects.filter(email=data['email']).exists():
				user = User.objects.get(email=data['email'])

				if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
					token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
					print('로그인 유저는 ',user.id)
					Security.objects.create(
						user_id = user.id,
						user_ip = request.META['REMOTE_ADDR'],
						browser = request.META['HTTP_USER_AGENT'],
						date = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
					)
					return JsonResponse({'token': token.decode('utf-8')}, status=200)
				return HttpResponse(status=401)
		except KeyError:
			return JsonResponse({'MESSAGE':'USER INVALID'}, status=401)
