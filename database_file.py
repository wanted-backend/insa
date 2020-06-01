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
django.setup()

from company.models import *
from user.models import *

CSV_PATH = './csv/expirations.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Expiration.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/industries.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Industry.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/employees.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Employee.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/foundation_years.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Foundation_year.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/categories.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Category.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/countries.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Country.objects.create(
            name = row['name'],
            number = row['number'],
            currency = row['currency'],
            english_currency = row['english_currency']
        )

CSV_PATH = './csv/cities.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        City.objects.create(
            country = Country.objects.get(id=row['countries_id']),
            name = row['name']
        )

CSV_PATH = './csv/companies.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Company.objects.create(
            city = City.objects.get(id=row['cities_id']),
            foundation_year = Foundation_year.objects.get(id=row['foundation_years_id']),
            employee = Employee.objects.get(id=row['employees_id']),
            industry = Industry.objects.get(id=row['industries_id']),
            name = row['name'],
            workplace = Workplace.objects.get(id=row['workplaces_id']),
            address = row['address'],
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
            updated_at = row['updated_at']
        )

CSV_PATH = './csv/tags.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Tag.objects.create(
            category = Category.objects.get(id=row['categories_id']),
            name = row['name']
        )

CSV_PATH = './csv/companies_tags.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Tag.objects.create(
            category = Category.objects.get(id=row['categories_id']),
            tag = Tag.objects.get(id=row['tags_id'])
        )

CSV_PATH = './csv/images.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Tag.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            image_url = row['image_url']
        )

CSV_PATH = './csv/workplaces.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Workplace.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            city = Company.objects.get(id=row['cities_id']),
            address = row['address'],
            lat = row['lat'],
            lng = row['lng']
        )

CSV_PATH = './csv/themes.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Workplace.objects.create(
            title = row['title'],
            description = row['address'],
            image_url = row['image_url'],
            inner_image_url = row['inner_image_url'],
            inner_description = row['inner_description']
        )

CSV_PATH = './csv/items.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Item.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/networks.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Network.objects.create(
            item = Item.objects.get(id=row['items_id']),
            name = row['name'],
            period = row['period'],
            displayed_amount = row['displayed_amount'],
            price_amount = row['price_amount']
        )

CSV_PATH = './csv/job_categories.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Job_category.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/roles.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Role.objects.create(
            item = Job_category.objects.get(id=row['job_categories_id']),
            name = row['name']
        )

CSV_PATH = './csv/matchup_items.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Network.objects.create(
            name = row['name'],
            displayed_amount = row['displayed_amount'],
            price_amount = row['price_amount'],
            count = row['count'],
            days = row['days']
        )

CSV_PATH = './csv/positions.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Position.objects.create(
            company = Company.objects.get(id=row['companies_id']),
            theme = Theme.objects.get(id=row['themes_id']),
            role = Role.objects.get(id=row['roles_id']),
            min_level = row['min_level'],
            max_level = row['max_level'],
            entry = row['entry'],
            min_wage = row['min_wage'],
            max_wage = row['max_wage'],
            expiry_date = row['expiry_date'],
            always = row['always'],
            name = row['name'],
            description = row['description'],
            responsibility = row['responsibility'],
            qualification = row['qualification'],
            preferred = row['preferred'],
            benifit = row['benifit'],
            created_at = row['created_at'],
            updated_at = row['updated_at'],
            referrer = row['referrer'],
            volunteer = row['volunteer'],
            total = row['total']
        )

CSV_PATH = './csv/positions_workplaces.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Position_workplace.objects.create(
            position = Position.objects.get(id=row['positions_id']),
            workplace = Workplace.objects.get(id=row['workplaces_id'])
        )

CSV_PATH = './csv/matchup_careers.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Matchup_career.objects.create(
            year = row['year']
        )

CSV_PATH = './csv/linguistics.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Linguistic.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/levels.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Level.objects.create(
            name = row['name']
        )

CSV_PATH = './csv/job_texts.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Job_text.objects.create(
            is_working = row['is_working'],
            text = row['text'],
            agreement = row['agreement']
        )