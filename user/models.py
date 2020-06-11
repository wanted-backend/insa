from django.db import models

class User(models.Model):

    country = models.ForeignKey('company.Country', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=500)
    password = models.CharField(max_length=500)
    agreement = models.BooleanField(default=0)
    contact = models.CharField(max_length=50, null=True)
    image_url = models.URLField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fail_count = models.IntegerField(default=0)
    deleted = models.BooleanField(default=0)
    job_position = models.CharField(max_length=100, null=True)
    user_bookmark = models.ManyToManyField('company.Position', through='company.Bookmark', related_name='user_bookmark')

    class Meta:
        db_table = 'users'

class Security(models.Model):

    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    user_ip = models.CharField(max_length=100)
    browser = models.CharField(max_length=1000)
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'securities'

class Want(models.Model):

    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey('company.Company', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wants'

class Matchup_career(models.Model):

    year = models.CharField(max_length=50)

    class Meta:
        db_table = 'matchup_careers'

class Exception(models.Model):

    company = models.ForeignKey('company.Company', on_delete=models.SET_NULL, null=True)
    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'exceptions'

class Matchup_skill(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    skill = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'matchup_skills'

class Matchup_job(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    job_text = models.ForeignKey('Job_text', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'matchup_jobs'

class Job_text(models.Model):

    is_working = models.CharField(max_length=50)
    text = models.CharField(max_length=50)
    agreement = models.BooleanField(default=0)

    class Meta:
        db_table = 'job_texts'

class Resume_role(models.Model):
    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey('company.Role', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'resume_roles'

class Resume(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    job_category = models.ForeignKey('company.Job_category', on_delete=models.SET_NULL, null=True)
    matchup_career = models.ForeignKey('Matchup_career', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=500, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=0)
    is_matchup = models.BooleanField(default=0)
    image_url = models.URLField(max_length=2000, null=True)
    title = models.CharField(max_length=150, null=True)
    income = models.IntegerField(default=0)
    total_work = models.IntegerField(default=0, null=True)
    is_job_category = models.BooleanField(default=0)
    roles = models.ManyToManyField('company.Role', through='Resume_role', related_name='resume_resume_role')

    class Meta:
        db_table = 'resumes'

class Resume_file(models.Model):

    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    resume_file = models.FilePathField(path='/user/resumes')

    class Meta:
        db_table = 'resume_files'

class Career(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    start_year = models.CharField(max_length=30, null=True)
    start_month = models.CharField(max_length=30, null=True)
    end_year = models.CharField(max_length=30, null=True)
    end_month = models.CharField(max_length=30, null=True)
    is_working = models.BooleanField(default=0)
    company = models.CharField(max_length=100, null=True)
    position = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'careers'

class Result(models.Model):

    career = models.ForeignKey('Career', on_delete=models.SET_NULL, null=True)
    start_year = models.CharField(max_length=30, null=True)
    start_month = models.CharField(max_length=30, null=True)
    end_year = models.CharField(max_length=30, null=True)
    end_month = models.CharField(max_length=30, null=True)
    title = models.CharField(max_length=300, null=True)
    content = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'results'

class Education(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    start_year = models.CharField(max_length=30, null=True)
    start_month = models.CharField(max_length=30, null=True)
    end_year = models.CharField(max_length=30, null=True)
    end_month = models.CharField(max_length=30, null=True)
    school = models.CharField(max_length=100, null=True)
    is_working = models.BooleanField(default=0)
    specialism = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'educations'


class Award(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    date_year = models.CharField(max_length=30, null=True)
    date_month = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'awards'

class Language(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    linguistic = models.ForeignKey('Linguistic', on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'languages'

class Linguistic(models.Model):

    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'linguistics'

class Level(models.Model):

    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'levels'

class Test(models.Model):

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300, null=True)
    score = models.CharField(max_length=150, null=True)
    date = models.DateField(null=True)

    class Meta:
        db_table = 'tests'

class Link(models.Model):

    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    url = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'links'
