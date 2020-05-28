import os
import django
import csv
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "willy.settings")
django.setup()

from company.models import *
from user.models import *

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
            code = row['code'],
            currency = row['currency'],
            english_currency = row['english_currency']
        )

CSV_PATH = './csv/locations.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Location.objects.create(
            country = Country.objects.get(id=row['countries_id']),
            name = row['name']
        )

CSV_PATH = './csv/companies.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        print(row)
        Company.objects.create(
            location = Location.objects.get(id=row['locations_id']),
            foundation_year = Foundation_year.objects.get(id=row['foundation_years_id']),
            employee = Employee.objects.get(id=row['employees_id']),
            industry = Industry.objects.get(id=row['industries_id']),
            name = row['name'],
            address = row['address'],
            registration_number = row['registration_number'],
            revenue = row['revenue'],
            description = row['description'],
            email = row['email'],
            contact_number = row['contact_number'],
            website = row['website']
        )