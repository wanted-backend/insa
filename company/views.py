import json
import random
import config
import urllib
import requests
import datetime
import monthdelta
import math

from django.http            import JsonResponse, HttpResponse
from django.views           import View
from django.db.models       import Q, Count, F
from django.core.exceptions import ObjectDoesNotExist
from django.utils           import timezone

from datetime               import date
# from iamport                import Iamport

from utils                  import login_decorator, login_check
from user.models            import User, Matchup_skill, Want, Matchup_career, Resume, Career, Education
from company.models         import (Company, City, Foundation_year, Employee, Industry, Workplace, Position, Company_matchup,
                                    Role, Position_workplace, Country, Tag, Company_tag, Bookmark, Image, Volunteers, Like, Theme,
                                    Reading, Proposal, Category , Network , Position_item , Matchup_item , Item , Expiration , Temp)


def getGPS_coordinates_for_KAKAO(address):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'KakaoAK {}'.format(config.MYAPP_KEY['MYAPP_KEY'])
    }
    address = address.encode("utf-8")
    p = urllib.parse.urlencode({'query': address})
    api = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params=p)
    lat = api.json()['documents'][0]['x']
    lng = api.json()['documents'][0]['y']
    city = api.json()['documents'][0]['address']['region_1depth_name']
    result = [lat, lng, city]
    return result

class EmployeeView(View):
    def get(self, request):
        employees = Employee.objects.all()
        data = [
            {
                'id':employee.id,
                'employee':employee.number
            } for employee in employees
        ]
        return JsonResponse({'employees':data}, status=200)

class CountryView(View):
    def get(self, request):
        countries = Country.objects.all()
        data = [
            {
                'id':country.id,
                'country':country.name
            } for country in countries
        ]
        return JsonResponse({'countries':data}, status=200)

class CityView(View):
    def get(self, request):
        cities = City.objects.all()
        data = [
            {
                'id':city.id,
                'city':city.name
            } for city in cities
        ]
        return JsonResponse({'cities':data}, status=200)

class CompanyRegister(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Company.objects.filter(user_id=request.user.id).exists():
                return JsonResponse({'MESSAGE': 'INVALID'}, status=401)

            Company(
                user_id = request.user.id,
                name = data['name'],
                registration_number = int(data['registration_number']),
                revenue = int(data['revenue']),
                industry = Industry.objects.get(name=data['industry']),
                employee = Employee.objects.get(number=data['employee']),
                description = data['description'],
                foundation_year = Foundation_year.objects.get(name=data['foundation_year']),
                email = data['email'],
                contact_number = data['contact_number'],
                website = data['website'],
                keyword = data['keyword'],
                recommender = data['recommender'],
			).save()

            address = data['address']
            coordinates = getGPS_coordinates_for_KAKAO(address)
            Workplace.objects.create(
                company_id = Company.objects.get(user_id=request.user.id).id,
                city = City.objects.get(name=data['city']),
                country = Country.objects.get(name=data['country']),
                address = address,
                represent = data['represent'],
                lat = coordinates[0],
                lng = coordinates[1]
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID USER'}, status=401)

    @login_decorator
    def get(self, request):
        try:
            user = request.user
            company = Company.objects.get(user_id=user.id)
            workplace = Workplace.objects.filter(company_id=company.id)
            data = [
                {
                    'id':company.id,
                    'name':company.name,
                    'description':company.description,
                    'website':company.website,
                    'workplace':[(
                                place.city.country.name,
                                place.city.name,
                                place.address,
                                place.represent
                            ) for place in workplace],
                    'registration_number':company.registration_number,
                    'revenue':company.revenue,
                    'industry':company.industry.name,
                    'employee':company.employee.number,
                    'foundation_year':company.foundation_year.name,
                    'email':company.email,
                    'contact_number':company.contact_number,
                    'keyword':company.keyword,
                }
            ]
            return JsonResponse({'company':data}, status=200)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

class WorkplaceView(View):
    @login_decorator
    def get(self, request):
        try:
            company = Company.objects.get(user_id=request.user.id)
            workplace = Workplace.objects.filter(company_id=company.id)
            data = [
                {
                    'id':place.id,
                    'company_id':place.company.id,
                    'company':place.company.name,
                    'address':place.address,
                    'lat':place.lat,
                    'lng':place.lng,
                    'represent':place.represent
                } for place in workplace
            ]
            return JsonResponse({'company':data}, status=200)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            address = data['address']
            coordinates = getGPS_coordinates_for_KAKAO(address)
            city = City.objects.get(name=coordinates[2])
            company = Company.objects.get(user_id=request.user.id)
            Workplace.objects.create(
                company_id = Company.objects.get(user_id=request.user.id).id,
                city_id = city.id,
                country_id = city.country.id,
                address = address,
                lat = coordinates[0],
                lng = coordinates[1]
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

class CompanyInfomationModify(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            company = Company.objects.get(user_id=request.user.id)
            company.description = data['description']
            company.website = data['website']
            company.registration_number = data['registration_number']
            company.revenue = data['revenue']
            company.industry.name = Industry.objects.get(name=data['industry']).name
            company.employee.number = Employee.objects.get(number=data['employee']).number
            company.foundation_year.name = Foundation_year.objects.get(name=data['foundation_year']).name
            company.email = data['email']
            company.contact_number = data['contact_number']
            company.keyword = data['keyword']
            company.industry.save()
            company.employee.save()
            company.foundation_year.save()
            company.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class CompanyLogo(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            company = Company.objects.get(user_id=request.user.id)
            company.image_url = data['image_url']
            company.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

class CompanyImages(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            company = Company.objects.get(user_id=request.user.id)
            Image.objects.create(
                company_id=company.id,
                image_url='/static/'+data['image_url']
            )
            images = company.image_set.filter(company_id=company.id)
            data = [
                {
                    'id':image.id,
                    'company_id':image.company.id,
                    'image':image.image_url
                } for image in images
            ]
            return JsonResponse({'image':data}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

    @login_decorator
    def get(self, request):
        company = Company.objects.prefetch_related('image_set').get(user_id=request.user.id)
        images = company.image_set.filter(company_id=company.id)
        data = [
            {
                'id':image.id,
                'company_id':image.company.id,
                'image':image.image_url
            } for image in images
        ]
        return JsonResponse({'images': data}, status=200)

class CompanyImageModify(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'image_id' in data:
                image_id = data['image_id']
                company = Company.objects.prefetch_related('image_set').get(user_id=request.user.id)
                image = company.image_set.get(id=image_id)
                image.image_url = data['image_url']
                image.save()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class CompanyImageDelete(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'image_id' in data:
                image_id = data['image_id']
                company = Company.objects.prefetch_related('image_set').get(user_id=request.user.id)
                images = company.image_set.filter(company_id=company.id)
                if images.count() == 2:
                    return JsonResponse({'MESSAGE': '더 이상 삭제할 수 없습니다. 이미지는 최소 2장 이상 업로드 해주세요.'}, status=401)
                Image.objects.get(id=image_id).delete()
                data = [
                    {
                        'id':image.id,
                        'company_id':image.company.id,
                        'image':image.image_url
                    } for image in images
                ]
                return JsonResponse({'image':data}, status=200)
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class CompanyPosition(View):
    @login_decorator
    def get(self, request, position_id):
        company = Company.objects.get(user_id=request.user.id)
        position = Position.objects.get(id=position_id)
        address = Workplace.objects.get(company_id=company.id, represent=True)
        is_always = '상시' if position.always==True else position.expiry_date
        is_entry_min = 0 if position.entry==True else position.min_level
        is_entry_max = 1 if position.entry==True else position.max_level
        is_preferred = None if position.preferred==True else position.preferred
        try:
            data = [
                {
                    'id':position.id,
                    'company_id':company.id,
                    'company':company.name,
                    'name':position.name,
                    'role':{position.role.id:position.role.name},
                    'description':position.description,
                    'responsibility':position.responsibility,
                    'preferred':is_preferred,
                    'benefit':position.benefit,
                    'expiry_date':is_always,
                    'address':address.address,
                    'min_level':is_entry_min,
                    'max_level':is_entry_max
                }
            ]
            return JsonResponse({'position':data}, status=200)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)
        except Position.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID POSITION'}, status=401)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            address = data['address']
            coordinates = getGPS_coordinates_for_KAKAO(address)
            city = City.objects.get(name=coordinates[2])
            company = Company.objects.get(user_id=request.user.id)
            workplace = Workplace.objects.get(company_id=company.id, represent=True)
            place = Workplace.objects.create(
                company_id = Company.objects.get(user_id=request.user.id).id,
                city_id = city.id,
                country_id = city.country.id,
                address = address,
                lat = coordinates[0],
                lng = coordinates[1]
            )
            company = Company.objects.get(user_id=request.user.id)
            place = Workplace.objects.get(company_id=company.id, represent=True)
            is_entry_min = 0 if data['entry']==True else data['min_level']
            is_entry_max = 1 if data['entry']==True else data['max_level']
            is_always = None if data['always']==True else data['expiry_date']
            is_preferred = None if data['preferred']==True else data['preferred']

            position = Position.objects.create(
                company_id = company.id,
                workplace_id = place.id if place else workplace.id,
                min_level = int(is_entry_min),
                max_level = is_entry_max,
                entry = data['entry'],
                mim_wage = int(data['mim_wage']),
                max_wage = int(data['max_wage']),
                expiry_date = is_always,
                always = data['always'],
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
            for role in data['role']:
                positions = Position.objects.get(id=position.id)
                positions.role = Role.objects.get(id=int(role))
                positions.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

def get_reward_currency(company_id):
    place = Workplace.objects.get(company_id=company_id)
    currency = place.country.english_currency
    reward = format(position.total, ',')

    if position.country.id == 3 or position.country.id == 4 or position.country.id == 6:
        total_reward = reward + currency
        return total_reward
    else:
        total_reward = currency + reward
        return total_reward

class PositionList(View):
    @login_decorator
    def get(self, request):
        user = request.user
        company = Company.objects.prefetch_related('position_set', 'image_set').get(user_id=user.id)
        print(company.id)
        positions = company.position_set.filter(company_id=company.id)
        workplace = Workplace.objects.filter(company_id=company.id)
        data = [
            {
                'id' : position.id,
                'image' : position.company.image_set.first().image_url if position.company.image_set.first() else None,
                'name' : position.name,
                'company' : position.company.name,
                'city' : workplace.first().city.name,
                'country' : workplace.first().country.name,
                'total_reward' :get_reward_currency(company.id)
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
        except ValueError:
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

def get_reward_currency(position_id):
    position = Position.objects.get(id=position_id)
    currency = position.country.english_currency
    reward   = format(position.total, ',')

    if position.country.id == 3 or position.country.id == 4 or position.country.id == 6:
        total_reward = reward + currency
        return total_reward

    else:
        total_reward = currency + reward
        return total_reward

class DetailView(View):
    @login_check
    def get(self, request, position_id):
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 8))
        
        try:
            user_id = request.user.id
        except:
            user_id = None

        try:
            position = (
                Position
                .objects
                .select_related('company', 'role')
                .prefetch_related('position_workplace_set')
                .get(id = position_id)
            )
            workplace =  position.position_workplace_set.get().workplace

            position_list = [
                {
                    'id' : position_id,
                    'detail_images' : [image.image_url for image in position.company.image_set.all()],
                    'name' : position.name,
                    'company' : position.company.name,
                    'city' : position.city.name if position.city else None,
                    'country' : position.country.name,
                    'tag' : [tag_list.tag.name for tag_list in position.company.company_tag_set.all()],
                    'bookmark' : Bookmark.objects.filter(Q(user_id = user_id) & Q(position_id = position_id)).exists(),
                    'applied' : Volunteers.objects.filter(Q(user_id = user_id) & Q(position_id = position_id)).exists(),
                    'reward' :{
                        'referrer':get_reward_currency(position.id),
                        'volunteer':get_reward_currency(position.id)
                    },
                    'body' :{
                        'description' : position.description,
                        'main_task' : position.responsibility,
                        'qualification' : position.qualification,
                        'preffered' : position.preferred,
                        'benefit' : position.benefit
                    },
                    'info' :{
                        'always' :{
                            'value' : position.always,
                            'expiry_date' : position.expiry_date
                        },
                        'location' :{
                            'full_location' : workplace.address,
                            'lat' : workplace.lat,
                            'lng' : workplace.lng,
                        },
                        'company' :{
                            'image' : position.company.image_url,
                            'name' : position.company.name,
                            'industry_name' : position.company.industry.name
                        }
                    },
                    'recommendation' :[
                        {
                            'id' : item.id,
                            'image' : item.company.image_set.first().image_url,
                            'name' : item.name,
                            'company' : item.company.name,
                            'city' : item.city.name if item.city else None,
                            'country' : item.country.name,
                            'reward' : get_reward_currency(position.id)
                        } for item in Position.objects.order_by('?')
                            if item.role.job_category_id == position.role.job_category_id
                    ] [offset : limit]
                }
            ]
            return JsonResponse({'position' : position_list}, status = 200)

        except Position.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_POSITION'}, status = 400)

class PositionBookmarkView(View):
    @login_decorator
    def post(self, request, position_id):

        try:
            if Bookmark.objects.filter(Q(user_id = request.user.id) & Q(position_id = position_id)).exists():
                Bookmark.objects.filter(Q(user_id = request.user.id) & Q(position_id = position_id)).delete()
                return JsonResponse({'message' : False}, status = 200)

            Position.objects.get(id = position_id).bookmarks.add(User.objects.get(id = request.user.id))
            return JsonResponse({'message' : True}, status = 200)

        except Position.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_POSITION'}, status = 400)

class PositionApplyView(View):
    @login_decorator
    def post(self, request, position_id):
        try:
            data = json.loads(request.body)

            Volunteers.objects.create(
                position_id = position_id,
                user_id = request.user.id,
                resume_id = data['resume']
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

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
            "id"                      : position.id,
            "image"                   : position.company.image_set.all().first().image_url,
            "name"                    : position.name,
            "company"                 : position.company.name,
            "city"                    : position.city.name if position.city else None,
            "country"                 : position.city.country.name if position.city else None,
            "total_reward"            : get_reward_currency(position.id)
        } for position in themes_list[offset:limit]]

        return JsonResponse({"theme_top":themetop, "theme_list":themelist},status=200)

class HomeView(View):

    @login_decorator
    def get(self,request):

        user = request.user
        roles = Resume.objects.filter(user_id=user.id).first().job_category_id if Resume.objects.filter(user_id=user.id) else None # 목데이터 실제 테스트시 1이 아닌 user.id
        themes = Theme.objects.prefetch_related('position_set').all()
        positions = Position.objects.select_related('company').prefetch_related('position_workplace_set','role').all()
        network_item = Position_item.objects.filter(
            Q(start_date__lte =date.today()) &
            Q(end_date__gte   =date.today()) &
            Q(item_id=2))     if Position_item.objects.filter(
                Q(start_date__lte =date.today()) &
                Q(end_date__gte   =date.today()) &
                Q(item_id=2))     else None

        network_ad = [{
            "id"             : item.id,
            "img"            : item.image_url,
            "title"          : item.title,
            "subTitle"       : item.description,
        }for item in network_item.order_by('?')][:4] if network_item else ''

        user_recomended_position = [{
            "id"             : position.id,
            "image"          : position.company.image_set.first().image_url,
            "name"           : position.name,
            "company"        : position.company.name,
            "city"           : position.city.name if position.city else None,
            "country"        : position.city.country.name if position.city else None,
            "total_reward"   : get_reward_currency(position.id),
        }for position in positions.order_by('?') if position.role.job_category_id == roles][:4] if roles else ''

        new_employment = [{
            "id"             : position.id,
            "image"          : position.company.image_set.first().image_url,
            "name"           : position.name,
            "company"        : position.company.name,
            "city"           : position.city.name if position.city else None,
            "country"        : position.city.country.name if position.city else None,
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

        if len(recommendations_of_the_week) == 0 :

            recommendations_of_the_week = [{
                "id"           : reco.id,
                "image"        : reco.company.image_set.first().image_url,
                "name"         : reco.name,
                "company"      : reco.company.name,
                "city"         : reco.city.name if reco.city else None,
                "country"      : reco.city.country.name if reco.city else None,
                "total_reward" : get_reward_currency(reco.id),
            }for reco in positions.order_by('?')][:4]

        return JsonResponse({"network_item"        : network_ad,
                             "position_recommend"  : user_recomended_position,
                             "new_employment"      : new_employment,
                             "theme_list"          : theme_list,
                             "Recommendation_week" : recommendations_of_the_week,
                            },status=200)

class CompanyRequestResume(View):
    @login_decorator
    def get(self, request):
        try:
            company = Company.objects.get(user_id=request.user.id)
            requests = Company_matchup.objects.filter(company_id=company.id, status=True)
            data = [
                {
                    'id':request.id,
                    'resume_id':request.resume.id,
                    'name':request.resume.user.name,
                    'description':request.resume.description,
                    'career':request.resume.matchup_career.year,
                    'skills':list(Matchup_skill.objects.filter(resume_id=request.resume.id).values()),
                    'work_info':list(Career.objects.filter(resume_id=request.resume.id).values()),
                    'education':list(Education.objects.filter(resume_id=request.resume.id).values('school'))
                } for request in requests
            ]
            return JsonResponse({'resume':data}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)
        except Company.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID COMPANY'}, status=401)

class PositionAdvertisement(View):
    def get(self, request):
        advertisement_list = (
            Position_item
            .objects
            .select_related('position')
            .filter(
                Q(start_date__lte = date.today()) &
                Q(end_date__gte = date.today()) &
                Q(item_id = 1) &
                Q(is_valid=True)
            )
        )
        position_list =[
            {
                'id' : position.position.id,
                'image' : position.position.company.image_set.first().image_url,
                'company_logo' : position.position.company.image_url,
                'name' : position.position.name,
                'company' : position.position.company.name,
                'location' : position.position.city.name if position.position.city else None,
                'country' : position.position.country.name,
                'total_reward' : get_reward_currency(position.position.id)
            } for position in advertisement_list
        ]

        return JsonResponse({'advertisement' : position_list}, status = 200)


class PositionMain(View):
    def sort_position(self, sort_by, year_filter):
        sort = {
            'latest' : year_filter.order_by('-created_at'),
            'popularity' : year_filter.annotate(count = Count('volunteers')).order_by('-count'),
            'compensation' : year_filter.order_by(F('total') * F('country__exchange_rate'))
        }
        return sort[sort_by]

    def filter_year(self, year, sort_by, city_filter):
        year_filter = city_filter.filter(Q(min_level__lte = year) & Q(max_level__gte = year))
        year = {
            -1 : city_filter,
             0 : city_filter.filter(Q(entry = True) | Q(min_level = 0)),
            10 : city_filter.filter(min_level__lte = year)
        }.get(year, year_filter)

        return self.sort_position(sort_by, year)

    def filter_city(self, city, year, sort_by, country_filter):
        if city == ['all']:
            city_filter = country_filter
        else:
            city_filter = country_filter.filter(city__name__in = city)

        return self.filter_year(year, sort_by, city_filter)

    def filter_country(self, country, city, year, sort_by, position_filter):
        if country == 'all':
            country_filter = position_filter
        else:
            country_filter = position_filter.filter(country__name = country)

        return self.filter_city(city, year, sort_by, country_filter)

    def keyword_search(self, country, city, year, sort_by, keyword):
        if keyword:
            keyword_list = keyword.split(' ')
            keyword_filter = Q()

            for keyword in keyword_list:
                keyword_filter.add(Q(name__icontains = keyword), Q.OR)
                keyword_filter.add(Q(company__name__icontains = keyword), Q.OR)

            position_filter = Position.objects.filter(keyword_filter).distinct()
        else:
            position_filter = Position.objects.all()

        return self.filter_country(country, city, year, sort_by, position_filter)

    def get(self, request):
        sort_by = request.GET.get('sort_by', 'latest')
        country = request.GET.get('country', '한국')
        city    = request.GET.getlist('city', ['all'])
        year    = int(request.GET.get('year', -1))
        limit   = int(request.GET.get('limit', 20))
        offset  = int(request.GET.get('offset', 0))
        keyword = request.GET.get('keyword', None)

        position_filter = self.keyword_search(country, city, year, sort_by, keyword)

        position_list =[
            {
                'id' : position.id,
                'image' : position.company.image_set.first().image_url,
                'name' : position.name,
                'company' : position.company.name,
                'city' : position.city.name if position.city else None,
                'country' : position.country.name,
                'total_reward' : get_reward_currency(position.id),
            } for position in position_filter[offset : offset + limit]
        ]

        return JsonResponse({'position' : position_list}, status = 200)

class JobAdPosition(View):

    @login_decorator
    def get(self,request):

        try:
            user = request.user
            company_positions = Company.objects.prefetch_related('position_set').get(user_id=1).position_set.all()
            # 테스트할때 기업회원 로그인 후 회사 정보 입력해야 함
            positions = [{
                "id"            : position.id,
                "name"          : position.name,
                "image"         : position.company.image_set.all().first().image_url,
                "city"          : position.city.name if position.city else None,
                "country"       : position.country.name if position.city else None,
                "total_reward"  : get_reward_currency(position.id)
            }for position in company_positions]
        except:
            return JsonResponse({ "positions" : '' },status=200)
        return JsonResponse({ "positions" : positions },status=200)

class JobAdPurchase(View):
    
    @login_decorator
    def get(self,request):

        network = Network.objects.filter(item_id=1)

        network_item = [{
            "id"               : item.id,
            "period"           : item.period,
            "displayed_amount" : item.displayed_amount,
            "item_id"          : item.item_id,
        }for item in network]

        return JsonResponse({ "item" : network_item },status=200)

    @login_decorator
    def post(self,request):

        data = json.loads(request.body)
        
        if Position_item.objects.filter(Q(position_id=data['position_id']) & Q(start_date=data['start_date']) & 
                                        Q(end_date=data['end_date'])).exists():
            
            return JsonResponse({"message" : "이미 해당 포지션에 구매한 아이템이 존재합니다."} , status=400)

        front = 'http://192.168.219.108:3000' # 준영님 주소

        request_url = "https://kapi.kakao.com/v1/payment/ready"

        headers1 = {
            'Authorization'   : "KakaoAK " + "adb7eb79eb94d1702a3c84bff005e31c",
            "Content-type"    : 'application/application/x-www-form-urlencoded;charset=utf-8',
        }

        params1 = {
            'cid'             : "TC0ONETIME",
            'partner_order_id': '1001',
            'partner_user_id' : 'wanted',
            'item_name'       : data['position_name'], # 아이템 명 불러오기,
            'quantity'        : 1, # 아이템 불러오기,
            'total_amount'    : 100, # 아이템 불러오기,
            'tax_free_amount' : 0,
            'vat_amount'      : 10,
            'approval_url'    : front + '/dashboard/ad?match=home', # 결제성공시 리다이렉트
            'fail_url'        : front, # 실패
            'cancel_url'      : front, # 취소
        }

        response = requests.post(request_url,params=params1,headers=headers1)
        response = json.loads(response.text)

        res = {
            'tid'            : response['tid'],
            'redirect'       : response['next_redirect_pc_url'],
            'created_at'     : response['created_at'],
        }
        
        item = Position_item.objects.create(
            position   = Position.objects.get(id=data['position_id']),
            item       = Item.objects.get(id=1),     # 1 직무상단 2 네트워크
            expiration = Expiration.objects.get(id=1),  # 1 사용전 # 2 사용중 # 3 사용완료 디폴트 1이 들어와야 함
            start_date = data['start_date'],
            end_date   = data['end_date'],
        )

        Temp.objects.create(
            item = Position_item.objects.get(id=item.id),
            tid  = response['tid']
        )

        return JsonResponse({ "response" : res },status=200)

class JobAdPurchased(View):

    @login_decorator
    def post(self,request):

        data = json.loads(request.body)
        
        tid = Temp.objects.get()
        
        request_url = "https://kapi.kakao.com/v1/payment/approve"

        headers1 = {
            'Authorization'   : "KakaoAK " + "adb7eb79eb94d1702a3c84bff005e31c",
            "Content-type"    : 'application/application/x-www-form-urlencoded;charset=utf-8',
        }

        params1 = {
            'cid'             : "TC0ONETIME",
            'tid'             : tid.tid, # tid 넘겨 받을 방법 찾아야 함
            'partner_order_id': '1001',
            'partner_user_id' : 'wanted',
            'pg_token'        : data['pg_token'],
            'total_amount'    : 100,
        }
        
        
        response = requests.post(request_url,params=params1,headers=headers1)
        response = json.loads(response.text)
        Is_Paid = False

        if 'aid' in response:
            Is_Paid       = True
            Paid          = Position_item.objects.get(id=tid.item.id)
            Paid.is_valid = True
            Paid.save()
            
        Temp.objects.all().delete()
        
        return JsonResponse({"is_Paid" : Is_Paid },status=200)

class NetworkAd(View):

    def post(self,request):

        data = json.loads(request.body)

        try:
            Position_item.objects.create(
                company    = Company.objects.get(Q(name=data['company_name'])|
                                                 Q(email=data['email'])).id,
                item       = data['item_id'],
                expiration = data['expiration'],
                start_date = data['start_date'],
                end_date   = data['end_data'],
                image_url  = data['image_url'],
                title      = data['title'],
                description= data['description'],
            )
        except:
            return JsonResponse({"message" : "회사이름이나 이메일이 올바른지 확인해주세요"},status=400)
        return HttpResponse(status=200)

class MatchUpItem(View):

    @login_decorator
    def get(self,request):

        item = Matchup_item.objects.all()

        plans = [{
            "name"             : plan.name,
            "displayed_amount" : plan.displayed_amount,
            "price_amount"     : plan.price_amount,
            "count"            : plan.count,
            "days"             : plan.days,
        }for plan in item]

        return JsonResponse({"plans" : plans} , status=200)
class JobAdState(View):

    @login_decorator
    def get(self,request):

        user = request.user
        company = Company.objects.get(user_id=user.id)
        item = Position_item.objects.filter(company_id=company.id)

        state = [{
            "item"          : stat.item.name, # 1 직무상단 2 네트워크 광고
            "position_name" : stat.position.name,
            "exp"           : stat.expiration.name, # 1 사용전 2 사용중 3 사용완료
            "start_date"    : stat.start_date,
            "end_date"      : stat.end_date,
            "click"         : stat.click,
        }for stat in item]

        return JsonResponse({"response" : state},status=200)

class MatchUpItemPurchased(View):
    
    @login_decorator
    def post(self,request):

        data = json.loads(request.body)

        DEFAULT_TEST_IMP_KEY = 'imp_apikey'
        DEFAULT_TEST_IMP_SECRET = ('ekKoeW8RyKuT0zgaZsUtXXTLQ4AhPFW3ZGseDA6bkA5lamv9O'
                           'qDMnxyeB9wqOsuO9W3Mx9YSJ4dTqJ3f')


    # def get(self,request):



class CompanyReadingResume(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'resume_id' in data:
                resume_id = data['resume_id']
                resume = Resume.objects.get(id=resume_id)
                company = Company.objects.get(user_id=request.user.id)
                if Reading.objects.filter(company_id=company.id, resume_id=resume_id, read=True).exists():
                    return JsonResponse({'MESSAGE':'열람한 이력서'}, status=401)
                Reading.objects.create(
                    company_id=company.id,
                    resume_id=resume.id,
                    read=True,
                )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class CompanyProposalsResume(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'resume_id' in data:
                resume_id = data['resume_id']
                resume = Resume.objects.get(id=resume_id)
                company = Company.objects.get(user_id=request.user.id)
                if Proposal.objects.filter(company_id=company.id, resume_id=resume.id).exists():
                    return JsonResponse({'MESSAGE':'이미 요청됨'}, status=401)
                Proposal.objects.create(
                    company_id = company.id,
                    resume_id = resume.id,
                    user_id = resume.user.id
                )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
            return JsonResponse({'MESSAGE': 'INVALID'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

class PositionFilter(View):
    def get(self, request):
        city_by_country = [
            {
                'country' : country.name,
                'city' : [city.name for city in country.city_set.all()]
            } for country in Country.objects.all()]

        career = [level.year for level in Matchup_career.objects.all()]

        return JsonResponse({'country_city' : city_by_country, 'career' : career}, status=200)

class TagView(View):
    def get(self, request):
        tag_list = [
            {
                category.name : [tag.name for tag in category.tag_set.all()]
            } for category in Category.objects.all()
        ]

        return JsonResponse({'tag_list' : tag_list}, status = 200)

class TagSearch(View):
    def get(self, request):
        tag    = request.GET.get('tag', None)
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 20))

        if not tag:
            return JsonResponse({'message' : 'INVALID_TAG_NAME'}, status = 400)

        tag_search = Position.objects.filter(company__company_tag__tag__name = tag).order_by('-created_at')

        search_list = [
            {
                'id' : position.id,
                'image' : position.company.image_set.first().image_url,
                'name' : position.name,
                'company' : position.company.name,
                'city' : position.city.name if position.city else None,
                'country' : position.country.name,
                'total_reward' : get_reward_currency(position.id)
            } for position in tag_search[offset : offset + limit]
        ]

        return JsonResponse({'position' : search_list}, status = 200)

class CompanyMatchupSearch(View):
    def filter_year(self, year_from, year_to, country_filter):
        if (Q(year_from == 0) & Q(year_to == 20)):
            year_filter = country_filter
        else:
            year_filter = country_filter.filter(Q(total_work__gte=year_from) & Q(total_work__lte=year_to))

        return year_filter

    def filter_country(self, country, year_from, year_to, keyword_filter):
        if country == ['all']:
            country_filter = keyword_filter
        else:
            country_filter = keyword_filter.filter(user__country__name__in=country)

        return self.filter_year(year_from, year_to, country_filter)

    def keyword_search(self, keyword, country, year_from, year_to, resume_list):
        if keyword:
            keyword_list = keyword.split(' ')
            keyword_filter = Q()

            for keyword in keyword_list:
                keyword_filter.add(Q(career__company__icontains = keyword), Q.OR)
                keyword_filter.add(Q(education__school__icontains = keyword), Q.OR)
                keyword_filter.add(Q(matchup_skill__skill__icontains = keyword), Q.OR)
                keyword_filter.add(Q(description__icontains = keyword), Q.OR)

            keyword_filter = resume_list.filter(keyword_filter)
        else:
            keyword_filter = resume_list

        return self.filter_country(country, year_from, year_to, keyword_filter)

    def select_resume_list(self, keyword, country, year_from, year_to, resume_list, company_id):
        resume = Resume.objects.all()

        resume_list = {
            1 : resume.filter(company_matchup__company_id = company_id),
            2 : resume.filter(like__company_id = company_id),
            3 : resume.filter(Q(reading__company_id = company_id) & Q(reading__read = 0)),
            4 : resume.filter(Q(reading__company_id = company_id) & Q(reading__read = 1)),
            5 : resume.filter(proposal__company_id = company_id)
            }.get(resume_list, resume)
    
        return self.keyword_search(keyword, country, year_from, year_to, resume_list)

    def get_duration(self, end_year, end_month, start_year, start_month):
        day = 1
        end_date = datetime.datetime(int(end_year), int(end_month), day)
        start_date = datetime.datetime(int(start_year), int(start_month), day)

        return monthdelta.monthmod(start_date, end_date)[0].months

    @login_decorator
    def get(self, request):
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 10))
        country     = request.GET.getlist('country', ['한국'])
        year_from   = int(request.GET.get('year_from', 0))
        year_to     = int(request.GET.get('year_to', 20))
        keyword     = request.GET.get('keyword', None)
        resume_list = int(request.GET.get('list', -1))

        try:
            company_id    = Company.objects.get(user_id = request.user.id).id
            resume_search = self.select_resume_list(keyword, country, year_from, year_to, resume_list, company_id)
            total_amount  = len(resume_search)

            resume_list = [
                {
                    'id' : resume.id,
                    'name' : resume.user.name,
                    'role': [role.role.name for role in resume.resume_role_set.all()],
                    'total_career' : resume.total_work,
                    'career' : [
                        {
                            'company' : career.career_set.company,
                            'duration' : self.get_duration(
                                            career.career_set.end_year, career.career_set.end_month,
                                            career.career_set.start_year, career.career_set.start_month
                                        )
                        } for career in resume.career_set.all()
                    ],
                    'description' : resume.description,
                    'skill' : [skill.matchup_skill.skill for skill in resume.matchup_skill_set.all()],
                    'school' : resume.education_set.first().school,
                    'specialism' : resume.education_set.first().specialism,
                    'liked' : Like.objects.filter(
                                                Q(company_id = company_id) & 
                                                Q(resume_id = resume.id) & 
                                                Q(status = 1)
                                                ).exists(),
                    'requested' : Company_matchup.objects.filter(
                                                            Q(company_id = company_id) 
                                                            & Q(resume_id = resume.id)
                                                            )
                } for resume in resume_search.order_by('-created_at')[offset : offset + limit]
            ]

            return JsonResponse({'resume_search' : resume_list, 'total_amount' : total_amount}, status = 200)

        except Company.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_COMPANY'}, status = 401)

class ApplicantView(View):
    @login_decorator
    def get(self, request):

        user        = request.user
        category    = request.GET.get('category', None)
        offset      = int(request.GET.get('offset','0'))
        limit       = int(request.GET.get('limit','10'))

        data        = []
        companies   = (
            Company
            .objects
            .prefetch_related('position_set')
            .get(user_id = user.id)
        )

        for position in companies.position_set.values('id'):
            volunteers = (
                Volunteers.objects
                .filter(position_id=position['id'])
                .order_by('-created_at')
                .values('id','user__name','resume__id','resume__is_matchup' )
            )
            for user in list(volunteers):
                if category == 'matchup':
                    if user['resume__is_matchup']==True:
                        user['user__name']=list(user['user__name'])[0]
                        data.append(user)
                else:
                    user['user__name']=list(user['user__name'])[0]
                    data.append(user)

        return JsonResponse({'volunteer':data[offset:offset+limit],'max_length':len(data)}, status=200)

class ApplicantDetailView(View):

    @login_decorator
    def get(self, request, volunteer_id):

        volunteers = (
            Volunteers.objects
            .select_related('user','resume')
            .get(id=volunteer_id)
        )

        data = {
            "name"      : list(volunteers.user.name)[0],
            "created_at": volunteers.created_at,
            "is_matchup": volunteers.resume.is_matchup
        }

        return JsonResponse({'data':data}, status=200)

    @login_decorator
    def delete(self, request, volunteer_id):

        volunteers = Volunteers.objects.get(id=volunteer_id)
        volunteers.delete()

        return HttpResponse(status = 200)
