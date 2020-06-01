import json

from django.http        import JsonResponse, HttpResponse
from django.views       import View

from utils              import login_decorator
from company.models     import Company, City, Foundation_year, Employee, Industry, Workplace, Position, Role

class CompanyRegister(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		print(data)
		try:
			user = request.user
			print(user.id)
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
			print(data)
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
				benifit = data['benifit'],
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
				'expiry_date':position.expiry_date,
                'always':position.always
			} for position in positions
		]
		return JsonResponse({'company':data}, status=200)
