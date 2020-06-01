from django.db import models

class Company(models.Model):
	user = models.OneToOneField('user.User', on_delete=models.SET_NULL, null=True)
	foundation_year = models.ForeignKey('Foundation_year', on_delete=models.SET_NULL, null=True)
	employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
	industry = models.ForeignKey('Industry', on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100)
	registration_number = models.IntegerField()
	revenue = models.IntegerField()
	description = models.TextField()
	email = models.EmailField()
	contact_number = models.CharField(max_length=50)
	website = models.TextField(blank=True)
	keyword = models.CharField(max_length=300, null=True)
	recommender = models.CharField(max_length=100, null=True)
	image_url = models.URLField(max_length=2000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField(default=0)
	matchup = models.ManyToManyField('user.Matchup', through='user.Exception')
	tag = models.ManyToManyField('Tag', through='Company_tag')
	company_matchup_items = models.ManyToManyField('Matchup_item', through='Company_matchup_item')

	class Meta:
		db_table = 'companies'

class Image(models.Model):
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
	image_url = models.URLField(max_length=2000, null=True)

	class Meta:
		db_table = 'images'

class Industry(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'industries'

class Employee(models.Model):
	number = models.CharField(max_length=50)

	class Meta:
		db_table = 'employees'

class Foundation_year(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'foundation_years'

class Category(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'categories'

class Tag(models.Model):
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100)

	class Meta:
		db_table = 'tags'

class Company_tag(models.Model):
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
	tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'companies_tags'

class Workplace(models.Model):
        company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, related_name='company')
        country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
        city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
        address = models.CharField(max_length=1000)
        lat = models.DecimalField(max_digits=10, decimal_places=7)
        lng = models.DecimalField(max_digits=10, decimal_places=7)
        represent = models.BooleanField(default=0)

        class Meta:
            db_table = 'workplaces'

class Country(models.Model):
	name = models.CharField(max_length=100)
	number = models.CharField(max_length=30)
	code = models.CharField(max_length=20)
	currency = models.CharField(max_length=10)
	english_currency = models.CharField(max_length=10)

	class Meta:
		db_table = 'countries'

class City(models.Model):
	country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'cities'

class Position(models.Model):
        company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
        theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
        role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
        workplace = models.ForeignKey('Workplace', on_delete=models.SET_NULL, null=True)
        min_level = models.IntegerField(default=0)
        max_level = models.IntegerField(default=0)
        entry = models.BooleanField(default=0)
        mim_wage = models.IntegerField(default=0)
        max_wage = models.IntegerField(default=0)
        expiry_date = models.DateField(null=True)
        always = models.BooleanField(default=0)
        name = models.CharField(max_length=100)
        description = models.TextField()
        responsibility = models.TextField()
        qualification = models.TextField()
        preferred = models.TextField(blank=True, null=True)
        benefit = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        referrer = models.CharField(max_length=50)
        volunteer = models.CharField(max_length=50)
        total = models.CharField(max_length=150)
        item = models.ManyToManyField('Item', through='Position_item')

        class Meta:
            db_table = 'positions'

class Position_workplace(models.Model):
	position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True)
	workplace = models.ForeignKey('Workplace', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'positions_workplaces'

class Bookmark(models.Model):
	position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=0)

	class Meta:
		db_table = 'bookmarks'

class Theme(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	image_url = models.URLField(max_length=2000)
	inner_image_url = models.URLField(max_length=2000)
	inner_description = models.TextField()

	class Meta:
		db_table = 'themes'

class Item(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'items'

class Expiration(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'expirations'

class Position_item(models.Model):
	position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True)
	item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
	expiration = models.ForeignKey('Expiration', on_delete=models.SET_NULL, null=True)
	period = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	used_at = models.DateField(null=True)
	image_url = models.URLField(max_length=2000)
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	click = models.IntegerField(default=0)

	class Meta:
		db_table = 'positions_items'

class Network(models.Model):
	item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=50)
	period = models.IntegerField(default=0)
	displayed_amount = models.IntegerField(default=0)
	price_amount = models.IntegerField(default=0)

	class Meta:
		db_table = 'networks'

class Volunteers(models.Model):
	position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=0)

	class Meta:
		db_table = 'volunteers'

class Like(models.Model):
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=0)

	class Meta:
		db_table = 'like'

class Job_category(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'job_categories'

class Role(models.Model):
	job_category = models.ForeignKey('Job_category', on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'roles'

class Company_matchup(models.Model):
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
	matchup = models.ForeignKey('user.Matchup', on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=0)

	class Meta:
		db_table = 'companies_matchup'

class Reading(models.Model):
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
	matchup = models.ForeignKey('user.Matchup', on_delete=models.SET_NULL, null=True)
	read = models.BooleanField(default=0)
	interview = models.BooleanField(default=0)

	class Meta:
		db_table = 'readings'

class Matchup_item(models.Model):
	name = models.CharField(max_length=50)
	displayed_amount = models.IntegerField(default=0)
	price_amount = models.IntegerField(default=0)
	count = models.IntegerField(default=0)
	days = models.IntegerField(default=0)

	class Meta:
		db_table = 'matchup_items'

class Company_matchup_item(models.Model):
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
	matchup_item = models.ForeignKey('Matchup_item', on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	expiration = models.BooleanField(default=0)

	class Meta:
		db_table = 'companies_matchup_items'

