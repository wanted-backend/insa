import json
import bcrypt
import jwt
import re
import time

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from partial_date       import PartialDateField

from utils              import login_decorator
from .models            import User, Security, Resume, Career, Result, Education, Award, Language, Test, Link, Level, Linguistic, Resume_file, Want

from insa.settings      import SECRET_KEY
from utils              import login_decorator

class UserEmailExists(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'True'}, status=200)
            return JsonResponse({'MESSAGE':'False'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

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
                job_position = data['job_position'],
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

class ResumeView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        resume = Resume.objects.create()
        resume.user_id = user.id
        resume.save()

        print(resume.id)

        data ={
                'id':resume.id,
                'user_id':user.id
        }
        return JsonResponse({'data':data}, status=200)

class UserResumeWriteView(View):

    @login_decorator
    def get(self, request, main_resume_id):
        user = request.user
        title_number = Resume.objects.filter(user_id=user.id)

        resume = Resume.objects.get(id=main_resume_id)

        def judgment(element, affiliation):
            if element == None:
                outcome=affiliation
            else:
                outcome=element
            return outcome

        resume_title = judgment(resume.title, "새로운 문서")
        resume_name = judgment(resume.name, user.name)
        resume_email = judgment(resume.email, user.email)
        resume_contact = judgment(resume.contact, user.contact)

        data = {
                'user_id':user.id,
                'resume_id':main_resume_id,
                'title':resume_title,
                'name':resume_name,
                'email':resume_email,
                'phone':resume_contact,
                'about':resume.description,
                'image':resume.image_url,
            }


        return JsonResponse({'resume':data}, status=200)

    @login_decorator
    def post(self, request, main_resume_id):
        try:
            data = json.loads(request.body)
            user = request.user

            resume = Resume.objects.get(id=main_resume_id)

            resume.id=main_resume_id
            resume.title=data['title']
            resume.name=data['name']
            resume.email=data['email']
            resume.contact=data['phone']
            resume.description=data['about']
            resume.image_url=data['image']
            resume.save()

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'keyerror'}, status=401)

    # @login_decorator
    # def delete(self, request, main_resume_id):
    #    data = json.loads(request.body)
    #    user = request.user

class ResumeDetailView(View):

    @login_decorator
    def get(self, request, main_resume_id):

        category = request.GET.get('category', None)

        def classification( affiliation_method):
                class_list = affiliation_method.objects.create()
                class_list.resume_id = main_resume_id
                class_list.save()

                data={
                    'id':class_list.id,
                    'resume_id':main_resume_id
                }

                return data

        if category == 'career':
            data = classification(Career)
        elif category == 'award':
            data = classification(Award)
        elif category == 'language':
            data = classification(Language)
        elif category == 'link':
            data = classification(Link)

        return JsonResponse({'data':data}, status=200)

class ResumeDetailWriteView(View):

    @login_decorator
    def get(self, request, main_resume_id):
         user = request.user

         category = request.GET.get('category', None)

         if category == 'career':
             data = Career.objects.filter(resume_id=main_resume_id).values()
         elif category == 'award':
             data = Award.objects.filter(resume_id=main_resume_id).values()
         elif category == 'language':
             data = Language.objects.filter(resume_id=main_resume_id).values()
         elif category == 'link':
             data = Link.objects.filter(resume_id=main_resume_id).values()

         return JsonResponse({'career':list(data)}, status=200)

    @login_decorator
    def post(self, request, main_resume_id):
        data = json.loads(request.body)
        user = request.user

        category = request.GET.get('category', None)

        if category == 'career':
            for index_data in data:
                careers = Career.objects.get(id=index_data['id'])
                careers.start = index_data['start']
                careers.end = index_data['end']
                careers.is_working = index_data['is_working']
                careers.company = index_data['company']
                careers.position = index_data['position']
                careers.save()

        elif category == 'award':
            for index_data in data:
                awards = Award.objects.get(id=index_data['id'])
                awards.is_working = index_data['is_working']
                awards.date = index_data['date']
                awards.name = index_data['name']
                awards.content = index_data['content']
                awards.save()

        elif category == 'language':
            for index_data in data:
                 languages = Language.objects.get(id=index_data['id'])
                 languages.lingustic_id = index_data['lingustic_id']
                 languages.level_id = index_data['level_id']
                 languages.save()

        elif category == 'link':
            for index_data in data:
                links = Link.objects.get(id=index_data['id'])
                links.url = index_data['link']

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

class LikedCompanies(View):
    @login_decorator
    def get(self, request):
        companies = Want.objects.filter(user_id=request.user.id)
        data = [
            {
                'name':want.company.name,
                'logo':want.company.image_url,
                'date':want.created_at
            } for want in companies
        ]
        return JsonResponse({'companies':data}, status=200)
