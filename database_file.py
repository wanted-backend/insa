import os
import django
import csv
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insa.settings")
django.setup(	)

from company.models import *
from user.models import *

CSV_PATH = './csv/expirations.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Expiration.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/industries.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Industry.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/employees.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Employee.objects.create(
            number = row['number']
        )
        print(row)

CSV_PATH = './csv/foundation_years.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Foundation_year.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/categories.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Category.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/countries.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Country.objects.create(
            name = row['name'],
            number = row['number'],
            currency = row['currency'],
            english_currency = row['english_currency']
        )
        print(row)

CSV_PATH = './csv/cities.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        City.objects.create(
            country = Country.objects.get(id=row['countries_id']),
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/companies.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        updated_at = None if row['updated_at'] == '' else row['updated_at']
        Company.objects.create(
            foundation_year = Foundation_year.objects.get(id=row['foundation_years_id']),
            employee = Employee.objects.get(id=row['employees_id']),
            industry = Industry.objects.get(id=row['industries_id']),
            name = row['name'],
            registration_number = row['registration_number'],
            revenue = row['revenue'],
            description = row['description'],
            email = row['email'],
            contact_number = row['contact_number'],
            website = row['website'],
            keyword = row['keyword'],
            recommender = row['recommender'],
            image_url = row['image_url'],
            created_at = row['created_at'],
            updated_at = updated_at,
            deleted = row['deleted']
        )
        print(row)

CSV_PATH = './csv/tags.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Tag.objects.create(
            name = row['name'],
            category = Category.objects.get(id=row['categories_id'])
        )
        print(row)

CSV_PATH = './csv/companies_tags.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Company_tag.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            tag = Tag.objects.get(id=row['tags_id'])
        )
        print(row)

CSV_PATH = './csv/images.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Image.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            image_url = row['image_url']
        )
        print(row)

CSV_PATH = './csv/workplaces.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        cities_id = None if row['cities_id'] == "" else City.objects.get(id=row['cities_id'])

        Workplace.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            city = cities_id,
            address = row['address'],
            lat = row['lat'],
            lng = row['lng'],
            represent = row['represent']
        )
        print(row)

CSV_PATH = './csv/themes.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Theme.objects.create(
            title = row['title'],
            description = row['description'],
            image_url = row['image_url'],
            inner_image_url = row['inner_image_url'],
            inner_description = row['inner_description']
        )
        print(row)

CSV_PATH = './csv/items.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Item.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/networks.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Network.objects.create(
            item = Item.objects.get(id=row['items_id']),
            name = row['name'],
            period = row['period'],
            displayed_amount = row['displayed_amount'],
            price_amount = row['price_amount']
        )
        print(row)

CSV_PATH = './csv/job_categories.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Job_category.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/roles.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Role.objects.create(
            job_category = Job_category.objects.get(id=row['job_categories_id']),
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/matchup_items.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Matchup_item.objects.create(
            name = row['name'],
            price_amount = row['price_amount'],
            displayed_amount = row['displayed_amount'],
            count = row['count'],
            days = row['days']
        )
        print(row)

CSV_PATH = './csv/positions.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        expiry_date = None if row['expiry_date'] == '' else row['expiry_date']
        preferred = None if row['preferred'] == '' else row['preferred']
        themes_id = None if row['themes_id'] == '' else Theme.objects.get(id=row['themes_id'])

        Position.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            theme = themes_id,
            role = Role.objects.get(id=row['roles_id']),
            min_level = row['min_level'],
            max_level = row['max_level'],
            entry = row['entry'],
            mim_wage = row['mim_wage'],
            max_wage = row['max_wage'],
            expiry_date = expiry_date,
            always = row['always'],
            name = row['name'],
            description = row['description'],
            responsibility = row['responsibility'],
            qualification = row['qualification'],
            preferred = preferred,
            benefit = row['benefit'],
            created_at = row['created_at'],
            updated_at = row['updated_at'],
            referrer = row['referrer'],
            volunteer = row['volunteer'],
            total = row['total']
        )
        print(row)

CSV_PATH = './csv/positions_workplaces.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Position_workplace.objects.create(
            position = Position.objects.get(id=row['positions_id']),
            workplace = Workplace.objects.get(id=row['workplaces_id'])
        )
        print(row)

CSV_PATH = './csv/matchup_careers.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Matchup_career.objects.create(
            year = row['year']
        )
        print(row)

CSV_PATH = './csv/linguistics.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Linguistic.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/levels.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Level.objects.create(
            name = row['name']
        )
        print(row)

CSV_PATH = './csv/job_texts.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Job_text.objects.create(
            is_working = row['is_working'],
            text = row['text'],
            agreement = row['agreement']
        )
        print(row)
