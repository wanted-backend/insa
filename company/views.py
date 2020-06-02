import json

from django.http        import JsonResponse, HttpResponse
from django.views       import View

from utils         import login_decorator
from company.models     import *

class CompanyRegister(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		try:
			user = request.user
			Company(
					user_id = Company.objects.get(user_id=user.id),
					name = data['name'],
					location = City.objects.get(name=data['city']),
					address = data['address'],
					registration_number = data['registration_number'],
					revenue = data['revenue'],
					industry = Industry.objects.get(name=data['industry']),
					employee = Employee.objects.get(name=data['employee']),
					description = data['description'],
					foundation_year = Foundation_year.objects.get(name=data['foundation_year']),
					email = data['email'],
					contact_number = data['contact_number'],
					website = data['website'],
					keyword = data['keyword'],
					recommender = data['recommender'],
					image_url = data['image_url']
			).save()
			return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'MESSAGE': 'INVALID KEYS'}, status=401)

	@login_decorator
	def get(self, request):
		user = request.user
		company = Company.objects.get(user_id=user.id)
		data = [
			{
				'name':company.name,
				'country':company.city.country.name,
				'location':company.city.name,
				'address':company.address,
				'registration_number':company.registration_number,
				'revenue':company.revenue,
				'industry':company.industry.name,
				'employee':company.employee.name,
				'description':company.description,
				'foundation_year':company.foundation_year.name,
				'email':company.email,
				'contact_number':company.contact_number,
				'website':company.website,
				'keyword':company.keyword,
				'recommender':company.recommender,
				'image_url':company.image_url
			}
		]
		return JsonResponse({'company':data}, status=200)

class ThemeTop(View):
    
    def get(self,request,theme_id):
        
        themes = Theme.objects.get(id=theme_id)
        
        themetop = {
			"theme_title"             : themes.title,
            "theme_description"       : themes.description,
            "theme_inner_image"       : themes.inner_image_url,
            "theme_inner_description" : themes.inner_description,
		}
        
        return JsonResponse({"theme_top" : themetop},status=200)

class ThemeList(View):
    
    def get(self,request,theme_id):
        
        offset = int(request.GET.get('offset'))
        limit  = int(request.GET.get('limit'))
        themes = Position.objects.filter(theme_id=theme_id)

        themelist = [{
            "item_id"       : position.id,
            "item_image"    : Image.objects.filter(company_id=position.company.id)[0].image_url,
			"item_title"    : position.name,
            "item_company"  : position.company.name,
            "item_location" : Workplace.objects.filter(company_id=position.company.id)[0].city.name,
            "item_country"  : Workplace.objects.filter(company_id=position.company.id)[0].city.country.name,
            "item_reward"   : position.total
		} for position in themes[offset:offset + limit-1]]
        
        return JsonResponse({"theme_list":themelist},status=200)
    
# class HomeView(View):
    
#     @login_decorator
#     def get(self,request):
        
#         position_recommend = Position.objects.filter()