import json
import random
import datetime

from django.http            import JsonResponse, HttpResponse
from django.views           import View
from django.db.models       import Q, Count, F
from django.core.exceptions import ObjectDoesNotExist
from django.utils           import timezone

from utils                  import login_decorator, login_check
from user.models            import User, Matchup_skill, Want, Matchup_career, Resume, Career
from company.models         import (Company, City, Foundation_year, Employee, Industry, Workplace, Position, Company_matchup,
                                    Role, Position_workplace, Country, Tag, Company_tag, Bookmark, Image, Volunteers, Like, Theme,
                                    Reading, Proposal, Category , Network , Position_item)

class CompanyRegister(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		try:
			user = request.user
			Company(
                user_id = user.id,
                name = data['name'],
                registration_number = data['registration_number'],
                revenue = data['revenue'],
                industry = Industry.objects.get(name=data['industry']),
                employee = Employee.objects.get(number=data['employee']),
                description = data['description'],
                foundation_year = Foundation_year.objects.get(name=data['foundation_year']),
                email = data['email'],
                contact_number = data['contact_number'],
                website = data['website'],
                keyword = data['keyword'],
                recommender = data['recommender'],
                image_url = data['image_url']
			).save()

			Workplace.objects.create(
                company_id = Company.objects.get(user_id=user.id).id,
                city = City.objects.get(name=data['city']),
                address = data['address'],
                lat = data['lat'],
                lng = data['lng'],
                represent = data['represent']
            )
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

	@login_decorator
	def get(self, request):
		user = request.user
		company = Company.objects.get(user_id=user.id)
		workplace = Workplace.objects.get(company_id=company.id)
		data = [
			{
				'name':company.name,
				'description':company.description,
				'website':company.website,
				'workplace':workplace.address,
                'city':workplace.city.name,
                'country':workplace.city.country.name,
                'registration_number':company.registration_number,
				'revenue':company.revenue,
				'industry':company.industry.name,
				'employee':company.employee.number,
				'foundation_year':company.foundation_year.name,
				'email':company.email,
				'contact_number':company.contact_number,
				'keyword':company.keyword,
				'image_url':company.image_url
			}
		]
		return JsonResponse({'company':data}, status=200)

class CompanyPosition(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		try:
			user = request.user
			company = Company.objects.get(user_id=user.id)
			is_entry_min = 0 if data['entry']==True else data['min_level']
			is_entry_max = 1 if data['entry']==True else data['max_level']
			is_always = None if data['always']==True else data['expiry_date']
			is_preferred = None if data['preferred']==True else data['preferred']

			Position.objects.create(
				company = company,
				role = Role.objects.get(name=data['role']),
				min_level = is_entry_min,
				max_level = is_entry_max,
				entry = data['entry'],
				mim_wage = data['mim_wage'],
				max_wage = data['mim_wage'],
                expiry_date = is_always,
				always = data['always'],
				workplace = Workplace.objects.get(company_id=company.id),
				name = data['name'],
				description = data['description'],
				responsibility = data['responsibility'],
				qualification = data['qualification'],
				preferred = is_preferred,
				benefit = data['benefit'],
				referrer = data['referrer'],
				volunteer = data['volunteer'],
				total = data['total']
			)
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class PositionList(View):
    @login_decorator
    def get(self, request):
        user = request.user
        company = Company.objects.get(user_id=user.id)
        positions = Position.objects.filter(company_id=company.id)
        data = [
                {
                    'name':position.name,
                    'expiry_date':position.expiry_date if position.expiry_date else position.always,
                } for position in positions
                ]

        return JsonResponse({'company':data}, status=200)

class CompanyLikedResume(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'resume_id' in data:
                resume_id = data['resume_id']
                resume = Resume.objects.get(id=resume_id)
                company = Company.objects.get(user_id=request.user.id)
                like = Like.objects.filter(company_id=company.id, resume_id=resume_id, status=True)
                if like.exists():
                    like.delete()
                    return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                Like.objects.create(
                    company_id=company.id,
                    resume_id=resume_id,
                    status = True
                )
                Want.objects.create(
                    user_id=resume.user.id,
                    company_id=company.id
                )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

    @login_decorator
    def get(self, request):
        try:
            company = Company.objects.get(user_id=request.user.id)
            likes = Like.objects.filter(company_id=company.id, status=True)
            for like in likes:
                data = [
                    {
                        'id':like.resume.user.id,
                        'name':like.resume.user.name,
                        'description':like.resume.description,
                        'role':like.resume.role.name,
                        'career':like.resume.matchup_career.year,
                        'skills':list(Matchup_skill.objects.filter(resume_id=like.resume.id).values()),
                        'work_info':list(Career.objects.filter(resume_id=like.resume.id).values()),
                        'education':like.resume.school,
                    }
                ]
                return JsonResponse({'liked_matchup':data}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)

class MatchupList(View):
    @login_decorator
    def get(self, request):
        resume = Resume.objects.all()
        data = [
            {
                'id':match.user.id,
                'user':match.user.name,
                'role':match.role.name,
                'career':match.matchup_career.year,
                'description':match.description if match.status == True else match.description,
                'skills':list(Matchup_skill.objects.filter(resume_id=match.id).values()),
                'work_info':list(Career.objects.filter(resume_id=match.id).values()),
                'education':match.school
            } for match in resume
        ]
        return JsonResponse({'matchup_list':data}, status=200)

def get_reward_currency(position_id):
            position=Position.objects.get(id=position_id)
            currency=position.country.english_currency
            reward=format(position.total, ',')

            if position.country.id==3 or position.country.id==4 or position.country.id==6:
                total_reward=reward+currency
                return total_reward
            else:
                total_reward=currency+reward
                return total_reward

class DetailView(View):
    @login_check
    def get(self, request, position_id):
        RECOMENDATION_LIMIT=8
        try:
            user_id=request.user.id
        except:
            user_id=None

        position = Position.objects.select_related('company', 'role').prefetch_related('position_workplace_set').get(id=position_id)
        workplace =  position.position_workplace_set.get().workplace
        position_list = [{
            'id':position_id,
            'detail_images':[image.image_url for image in position.company.image_set.all()],
            'name':position.name,
            'company':position.company.name,
            'city':position.city.name if position.city else None,
            'country':position.country.name,
            'tag':[tag_list.tag.name for tag_list in position.company.company_tag_set.all()],
            'bookmark':Bookmark.objects.filter(Q(user_id=user_id) & Q(position_id=position_id)).exists(),
            'reward' :{
                'referrer':get_reward_currency(position.id),
                'volunteer':get_reward_currency(position.id)
            },
            'body':{
                'description':position.description,
                'main_task':position.responsibility,
                'qualification':position.qualification,
                'preffered':position.preferred,
                'benefit':position.benefit
            },
            'info':{
                'always':{
                    'value':position.always,
                    'expiry_date':position.expiry_date
                },
                'location':{
                    'full_location':workplace.address,
                    'lat':workplace.lat,
                    'lng':workplace.lng,
                },
                'company':{
                    'image':position.company.image_url,
                    'name':position.company.name,
                    'industry_name':position.company.industry.name
                }
            },
            'recommendation':[{
                'id':item.id,
                'image':item.company.image_set.first().image_url,
                'name':item.name,
                'company':item.company.name,
                'city':item.city.name if item.city else None,
                'country':item.country.name,
                'reward':get_reward_currency(position.id)
                }for item in Position.objects.order_by('?') if item.role.job_category_id==position.role.job_category_id][:RECOMENDATION_LIMIT]
            }]
        return JsonResponse({'position':position_list}, status=200)

class PositionBookmarkView(View):
    @login_decorator
    def get(self, request, position_id):
        try:
            if Bookmark.objects.filter(Q(user_id=request.user.id) & Q(position_id=position_id)).exists():
                Bookmark.objects.filter(Q(user_id=request.user.id) & Q(position_id=position_id)).delete()
                return HttpResponse(status=200)

            Position.objects.get(id=position_id).bookmarks.add(User.objects.get(id=request.user.id))
            return HttpResponse(status=200)

        except Position.DoesNotExist:
            return JsonResponse({'message':'INVALID_POSITION'}, status=400)

class PositionApplyView(View):
    @login_decorator
    def get(self, request, position_id):
        user_id=request.user.id
        user=User.objects.prefetch_related('resume_set').filter(user_id=user_id)

        apply_info:{
            'name':user.name,
            'email':user.email,
            'resume':[{
                'title':resume.title,
                'created_at':resume.created_at,
                'status':True if status==1 else False
            }for resume in user.resume_set.all()]
        }
        return JsonResponse({'apply_info':apply_info}, status=200)

    @login_decorator
    def post(self, request, position_id):
        user_id=request.user.id

        Volunteers.objects.create(
            position_id=position_id,
            user_id=request.user.id,
        )
        return HttpResponse(status=200)


class ThemeList(View):
    
    def get(self,request,theme_id):

        offset = int(request.GET.get('offset'))
        limit  = int(request.GET.get('limit'))
        themes_list = Position.objects.filter(theme_id=theme_id)
        themes = Theme.objects.get(id=theme_id)

        themetop = {
            "theme_title"             : themes.title,
            "theme_description"       : themes.description,
            "theme_inner_image"       : themes.inner_image_url,
            "theme_inner_description" : themes.inner_description,
        }
        
        themelist = [{
            "id"          : position.id,
            "image"       : position.company.image_set.all().first().image_url,
            "name"        : position.name,
            "company"     : position.company.name,
            "city"        : position.city.name if position.city else None,
            "country"     : position.city.country.name if position.city else None,
            "total_reward": get_reward_currency(position.id)
		} for position in themes_list[offset:limit]]

        return JsonResponse({"theme_top":themetop, "theme_list":themelist},status=200)

class HomeView(View):

    @login_check
    def get(self,request):

        user = request.user
        roles = Resume.objects.get(user_id=user.id) if Resume.objects.filter(user_id=user.id).exists() else None
        mathced_position = Position.objects.filter(role_id=roles.role.id) if roles != None else None
        themes = Theme.objects.prefetch_related('position_set').all()
        positions = Position.objects.select_related('company').prefetch_related('position_workplace_set').all()
        
        user_recomended_position = [{
            "id"             : position.id,
            "image"          : position.company.image_set.first().image_url,
            "name"           : position.name,
            "company"        : position.company.name,
            "city"           : position.city.name,
            "country"        : position.city.country.name,
            "total_reward"   : get_reward_currency(position.id),
        }for position in mathced_position if position.role.job_category_id == roles.role.job_category_id][:4] if roles != None else ''

        new_employment = [{
            "id"             : position.id,
            "image"          : position.company.image_set.first().image_url,
            "name"           : position.name,
            "company"        : position.company.name,
            "city"           : position.city.name,
            "country"        : position.city.country.name,
            "total_reward"   : get_reward_currency(position.id),
        }for position in positions.order_by('created_at')[:4]]

        theme_list = [{
            "id"             : theme.id,
            "image"          : theme.image_url,
            "title"          : theme.title,
            "desc"           : theme.description,
            "logos"          : list(set([logos.company.image_url for logos in theme.position_set.all()]))
        }for theme in themes[:4]]

        recommendations_of_the_week = [{
            "id"             : recommend.id,
            "image"          : recommend.company.image_set.first().image_url,
            "name"           : recommend.name,
            "company"        : recommend.company.name,
            "city"           : recommend.city.name if recommend.city else None,
            "country"        : recommend.city.country.name if recommend.city else None,
            "total_reward"   : get_reward_currency(recommend.id),
        }for recommend in positions.order_by('?')if recommend.created_at.isocalendar()[1] == datetime.date.today().isocalendar()[1]][:4]

        return JsonResponse({"position_recommend"  : user_recomended_position,
                             "new_employment"      : new_employment,
                             "theme_list"          : theme_list,
                             "Recommendation_week" : recommendations_of_the_week,
                            },status=200)

# class RequestResume(View):
#     @login_decorator
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             if 'matchup_id' in data:
#                 matchup_id = data['matchup_id']
#                 matchup = Matchup.objects.get(id=matchup_id)
#                 company = Company.objects.get(user_id=request.user.id)
#                 if matchup.resume.is_matchup == True:
#                     if Company_matchup.objects.filter(company_id=company.id, matchup_id=matchup_id, status=True).exists():
#                         return JsonResponse({'MESSAGE':'이미 요청됨'}, status=401)
#                     Company_matchup.objects.create(
#                         company_id=company.id,
#                         matchup_id=matchup_id,
#                         status = True
#                     )
#                     return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
#                 return JsonResponse({'MESSAGE': 'INVALID'}, status=401)
#         except KeyError:
#             return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

# class RequestMatchupList(View):
#     @login_decorator
#     def get(self, request):
#         try:
#             company = Company.objects.get(user_id=request.user.id)
#             requests = Company_matchup.objects.filter(company_id=company.id, status=True)
#             for request in requests:
#                 matchup = Matchup.objects.prefetch_related('matchup_skill_set','work_information_set').get(user_id=request.matchup.user.id)
#                 data = [
#                     {
#                         'id':request.id,
#                         'name':request.matchup.user.name,
#                         'description':request.matchup.description,
#                         'role':request.matchup.role.name,
#                         'career':request.matchup.matchup_career.year,
#                         'work_info':[{work.name:[work.start, work.end]} for work in matchup.work_information_set.filter(matchup_id=matchup.id)],
#                         'work_skills':[work.skill for work in matchup.matchup_skill_set.filter(matchup_id=matchup.id)],
#                         'education':request.matchup.school,
#                     }
#                 ]
#                 return JsonResponse({'is_resume_request':data}, status=200)
#         except ValueError:
#             return JsonResponse({'MESSAGE': 'INVALID'}, status=401)

class PositionAdvertisement(View):
    def get(self, request):
        advertisement=[{
            'id':position.position.id,
            'image':position.position.company.image_set.first().image_url,
            'company_logo':position.position.company.image_url,
            'name':position.position.name,
            'company':position.position.company.name,
            'location': position.position.city.name if position.position.city else None,
            'country':position.position.country.name,
            'total_reward':get_reward_currency(position.position.id)
        }for position in Position_item.objects.select_related('position').filter(
                                                                            Q(start_date__lt=timezone.now()) &
                                                                            Q(end_date__gt=timezone.now()) &
                                                                            Q(item_id=1)
                                                                            )]

        return JsonResponse({'advertisement':advertisement}, status=200)

class PositionMain(View):
    def sort_position(self, sort_by, year_filter):
        sort={
            'latest':year_filter.order_by('-created_at'),
            'popularity':year_filter.annotate(count=Count('volunteers')).order_by('-count'),
            'compensation':year_filter.order_by(F('total')*F('country__exchange_rate'))
        }
        for key in sort:
            if sort_by==key:
                position_filter=sort[key]
                return position_filter

    def filter_year(self, year, sort_by, city_filter):
        if year==0:
            year_filter=city_filter.filter(entry=True)
        elif year==-1:
            year_filter=city_filter
        else:
            year_filter=city_filter.filter(Q(min_level__gte=year) & Q(max_level__lte=year))
        return self.sort_position(sort_by, year_filter)

    def filter_city(self, city, year, sort_by, country_filter):
        if city=='all':
            city_filter=country_filter
        else:
            city_filter=country_filter.filter(city__name__in=city)
        return self.filter_year(year, sort_by, city_filter)

    def filter_country(self, country, city, year, sort_by, position_filter):
        if country=='all':
            country_filter=position_filter
        else:
            country_filter=position_filter.filter(country__name=country)
        return self.filter_city(city, year, sort_by, country_filter)

    def keyword_search(self, country, city, year, sort_by, keyword):
        if keyword!=None:
            keyword_list = keyword.split(' ')
            keyword_filter = Q()
            for keyword in keyword_list:
                keyword_filter.add(Q(name__icontains=keyword), Q.OR)
                keyword_filter.add(Q(company__name__icontains=keyword), Q.OR)

            position_filter=Position.objects.filter(keyword_filter)
        else:
            position_filter=Position.objects.all()
        return self.filter_country(country, city, year, sort_by, position_filter)

    def get(self, request):
        sort_by=request.GET.get('sort_by', 'latest')
        country=request.GET.get('country', '한국')
        city=request.GET.getlist('city', 'all')
        year=int(request.GET.get('year', -1))
        limit=int(request.GET.get('limit', 20))
        offset=int(request.GET.get('offset', 0))
        keyword=request.GET.get('keyword', None)
        
        position_filter=self.keyword_search(country, city, year, sort_by, keyword)
        position_list=[{
            'id':position.id,
            'image':position.company.image_set.first().image_url,
            'name':position.name,
            'company':position.company.name,
            'city':position.city.name if position.city else None,
            'country':position.country.name,
            'total_reward':get_reward_currency(position.id),
            }for position in position_filter[offset:offset+limit]]

        return JsonResponse({'position':position_list}, status=200)

class JobAdPosition(View):

    @login_decorator
    def get(self,request):
        
        try:
            user = request.user
            company_positions = Company.objects.prefetch_related('position_set').get(user_id=user.id).position_set.all()
            # 테스트할때 기업회원 로그인 후 회사 정보 입력해야 함
            positions = [{
                "id"            : position.id,
                "name"          : position.name,
                "image"         : position.company.image_set.all().first().image_url,
                "city"          : position.city.name if position.city else None,
                "country"       : position.country.name if postion.city else None,
                "total_reward"  : get_reward_currency(postion.id)
            }for position in company_positions]
        except:
            return JsonResponse({ "positions" : '' },status=200)
        return JsonResponse({ "positions" : positions },status=200)

class JobAdItem(View):
    
    @login_decorator
    def post(self,request):
        
        data = json.loads(request.body)

        me = 'http://localhost:8000'
        
        request_url = "https://kapi.kakao.com/v1/payment/ready"
        
        headers1 = {
            'Authorization' : "KakaoAK " + "adb7eb79eb94d1702a3c84bff005e31c",
            "Content-type"  : 'application/application/x-www-form-urlencoded;charset=utf-8',
        }
        
        params1 = {
            'cid' : "TC0ONETIME",
            'partner_order_id': '1001',
            'partner_user_id': 'wanted',
            'item_name': data['name'],
            'quantity': data['period'],
            'total_amount': data['item_price'],
            'tax_free_amount': 0,
            'vat_amount' : int(int(data['include_tax']) - int(data['item_price'])),
            'approval_url': me + '/kakaopay/purchase',
            'fail_url': me,
            'cancel_url': me,
        }

        response = requests.post(request_url,params=params1,headers=headers1)
        response = json.loads(response.text)
       
        return JsonResponse({"response" : response},status=200)
        
class JobAdPurchased(View):
    
    def post(self,request):
        
        data = json.loads(request.body)
        
        for items in data:
            
            Position_item.objects.create(
                position   = items['postions_id'],
                item       = items['item_id'],     # 1 직무상단 2 네트워크 
                expiration = items['expiration'],  # 1 사용전 # 2 사용중 # 3 사용완료 디폴트 1이 들어와야 함
                start_date = items['start_date'],
                end_date   = items['end_date'],
            )
        
        return HttpResponse(status=200)
        
# class ReadingMatchup(View):
#     @login_decorator
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             if 'matchup_id' in data:
#                 matchup_id = data['matchup_id']
#                 matchup = Matchup.objects.get(id=matchup_id)
#                 company = Company.objects.get(user_id=request.user.id)
#                 if Reading.objects.filter(company_id=company.id, matchup_id=matchup_id, read=True).exists():
#                     return JsonResponse({'MESSAGE':'열람한 이력서'}, status=401)
#                 Reading.objects.create(
#                     company_id=company.id,
#                     matchup_id=matchup.id,
#                     read=True,
#                     interview=False
#                 )
#                 return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
#         except KeyError:
#             return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

# class ReadingMatchupList(View):
#     @login_decorator
#     def get(self, request):
#         try:
#             company = Company.objects.get(user_id=request.user.id)
#             reading = Reading.objects.prefetch_related('matchup').filter(company_id=company.id)
#             data = [
#                 {
#                     'id':read.id,
#                     'name':read.matchup.user.name,
#                     'description':read.matchup.description,
#                     'role':read.matchup.role.name,
#                     'career':read.matchup.matchup_career.year,
#                     'work_info':[{work.name:[work.start, work.end]} for work in Work_information.objects.filter(matchup_id=read.matchup.id)],
#                     'work_skills':[work.skill for work in Matchup_skill.objects.filter(matchup_id=read.matchup.id)],
#                     'education':read.matchup.school,
#                 } for read in reading
#             ]
#             return JsonResponse({'reading_matchup':data}, status=200)
#         except ValueError:
#             return JsonResponse({'MESSAGE': 'INVALID'}, status=401)

# class ProposalView(View):
#     @login_decorator
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             Proposal.objects.create(
#                 company_id = Company.objects.get(user_id=request.user.id).id,
#                 matchup_id = Matchup.objects.get(id=data['matchup_id']).id,
#                 position_id = Position.objects.get(id=data['position_id']).id,
#                 content = data['content'],
#                 title = data['title'],
#                 start = data['start'],
#                 end = data['end'],
#                 place = data['place'],
#                 stock = data['stock']
#             )

#             return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
#         except KeyError:
#             return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

#     @login_decorator
#     def get(self, request):
#         interviews = Proposal.objects.filter(company_id=Company.objects.get(user_id=request.user.id).id)
#         data = [
#             {
#                 'id':interview.id,
#                 'name':interview.matchup.user.name,
#                 'description':interview.matchup.description,
#                 'role':interview.matchup.role.name,
#                 'career':interview.matchup.matchup_career.year,
#                 'work_info':[{work.name:[work.start, work.end]} for work in Work_information.objects.filter(matchup_id=interview.matchup.id)],
#                 'work_skills':[work.skill for work in Matchup_skill.objects.filter(matchup_id=interview.matchup.id)],
#                 'education':interview.matchup.school
#             } for interview in interviews
#         ]
#         return JsonResponse({'interview_proposal':data}, status=200)

class MainFilter(View):
    def get(self, request):
        country=[{
            country.name:[city.name for city in country.city_set.all()] 
            }for country in Country.objects.all()],
        career_level=[level.year for level in Matchup_career.objects.all()]
        
        
        return JsonResponse({'country':country, 'career':career_level}, status=200)

class TagView(View):
    def get(self, request):
        tag_list=[{
            category.name:[tag.name for tag in category.tag_set.all()]
        }for category in Category.objects.all()]
        return JsonResponse({'tag_list':tag_list}, status=200)

class TagSearch(View):
    def get(self, request):
        tag=request.GET.get('tag', None)
        offset=int(request.GET.get('offset', 0))
        limit=int(request.GET.get('limit', 20))

        if tag==None:
            return JsonResponse({'message':'INVALID_TAG_NAME'})

        tag_search=Position.objects.filter(company__company_tag__tag__name=tag).order_by('-created_at')
        search_list=[{
            'id':position.id,
            'image':position.company.image_set.first().image_url,
            'name':position.name,
            'company':position.company.name,
            'city':position.city.name if position.city else None,
            'country':position.country.name,
            'total_reward':get_reward_currency(position.id)
            }for position in tag_search[offset:offset+limit]]

        return JsonResponse({'position':search_list}, status=200)
