import json
import bcrypt
import jwt
import re
import time

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from partial_date       import PartialDateField
from datetime           import datetime

from utils              import login_decorator
from insa.settings      import SECRET_KEY
from company.models     import Company, Company_matchup, Proposal
from .models            import User, Security, Resume, Career, Result, Education, Award, Language,\
                                Test, Link, Level, Linguistic, Resume_file, Want, Matchup

class UserEmailExists(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'True'}, status=200)
            return JsonResponse({'MESSAGE':'False'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class UserRegisterView(View):
    validation = {
		'password': lambda password: re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$", password)
	}

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 이메일입니다.'}, status=401)

			# 빈 문자열 검사
            for value in data.values():
                if value == '':
                    return JsonResponse({'MESSAGE':'입력 정보를 확인해주세요'}, status=401)

			# 비밀번호 숫자, 영문, 특수문자 조합으로 6자리 이상인지 검증
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
        'password': lambda password: re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$", password)
    }

    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 이메일입니다.'}, status=401)

			# 빈 문자열 검사
            for value in data.values():
                if value == '':
                    return JsonResponse({'MESSAGE':'입력 정보를 확인해주세요'}, status=401)

			# 비밀번호 숫자, 영문, 특수문자 조합으로 6자리 이상인지 검증
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
                return JsonResponse({'MESSAGE':'INVALID'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE':'USER INVALID'}, status=401)

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

class ResumeMainView(View):

    @login_decorator
    def get(self, request):
        user = request.user
        resumeMain = Resume.objects.filter(user_id=user.id).values('id','title', 'created_at', 'status')
        for resume in resumeMain:
            if resume['title'] == None:
                resume['title']=""
            if resume['status'] == False:
                resume['status']="작성 완료"
            else:
                resume['status']="작성 중"

        return JsonResponse({'data':list(resumeMain)}, status=200)

class ResumeView(View):

    @login_decorator
    def get(self, request):
        user = request.user
        resume = Resume.objects.create()
        resume.user_id = user.id
        resume.status = True
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
    def delete(self, request, main_resume_id):
        data = Resume.objects.get(id=main_resume_id)
        data.delete()

        return HttpResponse(status=200)

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
            resume.status=data['status']
            resume.save()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'keyerror'}, status=401)

class ResumeDetailView(View):

    @login_decorator
    def get(self, request, main_resume_id):

        category = request.GET.get('category', None)

        def classification(affiliation_method):
                class_list = affiliation_method.objects.create()
                class_list.resume_id = main_resume_id
                class_list.save()

                data={
                    'id':class_list.id,
                    'resume_id':int(main_resume_id)
                }

                return data

        if category == 'career':
            data = classification(Career)
        elif category == 'education':
            data = classification(Education)
        elif category == 'award':
            data = classification(Award)
        elif category == 'language':
            data = classification(Language)
        elif category == 'link':
            data = classification(Link)

        return JsonResponse({'data':data}, status=200)

    @login_decorator
    def delete(self, request, main_resume_id):

        data = json.loads(request.body)
        category = request.GET.get('category', None)

        def remove(kind):
            row = kind.objects.get(id=data['id'])
            row.delete()

        if category == 'career':
            remove(Career)
        elif categroy == 'education':
            remove(Education)
        elif category == 'award':
            remove(Award)
        elif category == 'language':
            remove(Language)
        elif category == 'link':
            remove(Link)
        return HttpResponse(status=200)

class ResumeDetailWriteView(View):

    @login_decorator
    def get(self, request, main_resume_id):
         user = request.user

         category = request.GET.get('category', None)

         def year_month(theme_set, theme):

             data=[]
             for index,element in enumerate(theme_set):
                 start_year = theme.objects.filter(resume_id=main_resume_id).values('start_year')[index]
                 start_month = theme.objects.filter(resume_id=main_resume_id).values('start_month')[index]
                 end_year = theme.objects.filter(resume_id=main_resume_id).values('end_year')[index]
                 end_month = theme.objects.filter(resume_id=main_resume_id).values('end_month')[index]
                 start = [start_year['start_year'], start_month['start_month']]
                 end = [end_year['end_year'], end_month['end_month']]

                 element['start']= start
                 element['end']= end
                 data.append(element)

             return data

         if category == 'career':
             data= []
             elements = Career.objects.filter(resume_id=main_resume_id).values('id', 'resume_id', 'is_working', 'company', 'position')
             datas = year_month(elements, Career)

             for data_list in datas:
                 result = Result.objects.filter(career_id=data_list['id']).values('id','career_id','title','content')

                 for index,element in enumerate(result):
                     start_year = Result.objects.filter(career_id=data_list['id']).values('start_year')[index]
                     start_month = Result.objects.filter(career_id=data_list['id']).values('start_month')[index]
                     end_year = Result.objects.filter(career_id=data_list['id']).values('end_year')[index]
                     end_month = Result.objects.filter(career_id=data_list['id']).values('end_month')[index]
                     start = [start_year['start_year'], start_month['start_month']]
                     end = [end_year['end_year'], end_month['end_month']]

                     element['start']= start
                     element['end']= end

                 data_list['result']=list(result)
                 data.append(data_list)

         elif category == 'award':
             data = []
             elements = Award.objects.filter(resume_id=main_resume_id).values('id','resume_id','name','content')

             for index,element in enumerate(elements):
                 year = Award.objects.filter(resume_id=main_resume_id).values('date_year')[index]
                 month = Award.objects.filter(resume_id=main_resume_id).values('date_month')[index]
                 date = [year['date_year'], month['date_month']]
                 element['date']=date
                 data.append(element)

         elif category == 'education':

             elements = Education.objects.filter(resume_id=main_resume_id).values('id','is_working','school','specialism','subject')
             data = year_month(elements, Education)

         elif category == 'language':
             data = Language.objects.filter(resume_id=main_resume_id).values()
         elif category == 'link':
             data = Link.objects.filter(resume_id=main_resume_id).values()

         return JsonResponse({'data':list(data)}, status=200)

    @login_decorator
    def post(self, request, main_resume_id):
        data = json.loads(request.body)
        user = request.user

        category = request.GET.get('category', None)

        if category == 'career':
            for index_data in data:

                careers = Career.objects.get(id=index_data['id'])
                careers.start_year = index_data['start'][0]
                careers.start_month = index_data['start'][1]
                careers.end_year = index_data['end'][0]
                careers.end_month = index_data['end'][1]
                careers.is_working = index_data['is_working']
                careers.company = index_data['company']
                careers.position = index_data['position']
                careers.save()

                for element in index_data['result']:
                    results = Result.objects.get(id=element['id'])
                    results.title = element['title']
                    results.content = element['content']
                    results.start_year = element['start'][0]
                    results.start_month = element['start'][1]
                    results.end_year = element['end'][0]
                    results.end_month = element['end'][1]
                    results.end = element['end']
                    results.save()

        elif category == 'award':
            for index_data in data:
                awards = Award.objects.get(id=index_data['id'])
                awards.date_year = index_data['date'][0]
                awards.date_month = index_data['date'][1]
                awards.name = index_data['name']
                awards.content = index_data['content']
                awards.save()

        elif category == 'education':
            for index_data in data:
                educations = Education.objects.get(id=index_data['id'])
                educations.start_year = index_data['start'][0]
                educations.start_month = index_data['start'][1]
                educations.end_year = index_data['end'][0]
                educations.end_month = index_data['end'][1]
                educations.end = index_data['end']
                educations.is_working = index_data['is_working']
                educations.school = index_data['school']
                educations.specialism = index_data['specialism']
                educations.subject = index_data['subject']
                educations.save()

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

        return HttpResponse(status=200)

class CareerResultView(View):

    @login_decorator
    def get(self, request, main_career_id):

        results = Result.objects.create()
        results.career_id = main_career_id
        results.save()

        data={
            'id':results.id,
            'career_id':int(main_career_id)
        }

        return JsonResponse({'data':data}, status=200)

    @login_decorator
    def delete(self, request, main_career_id):

        row = Result.objects.get(id=data['id'])
        row.delete()

        return HttpResponse(status=200)

class CompanyLikedResumes(View):
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

class CompanyRequestsResume(View):
    @login_decorator
    def get(self, request):
        matchup = Matchup.objects.get(user_id=request.user.id)
        requests_resume = Company_matchup.objects.filter(matchup_id=matchup.id)
        data = [
            {
                'name':request.company.name,
                'logo':request.company.image_url,
                'date':request.created_at
            } for request in requests_resume
        ]
        return JsonResponse({'is_resume_request':data}, status=200)

class CompanyInterviewResume(View):
    @login_decorator
    def get(self, request):
        matchup = Matchup.objects.get(user_id=request.user.id)
        interviews = Proposal.objects.filter(matchup_id=matchup.id)
        data = [
            {
                'name':interview.company.name,
                'logo':interview.company.image_url,
                'date':interview.created_at
            } for interview in interviews
        ]
        return JsonResponse({'is_resume_request':data}, status=200)
