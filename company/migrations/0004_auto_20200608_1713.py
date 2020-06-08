# Generated by Django 3.0.6 on 2020-06-08 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('company', '0003_auto_20200608_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='companies_matchup',
        ),
        migrations.RemoveField(
            model_name='company',
            name='companies_reading',
        ),
        migrations.RemoveField(
            model_name='company_matchup',
            name='matchup',
        ),
        migrations.RemoveField(
            model_name='like',
            name='matchup',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='matchup',
        ),
        migrations.RemoveField(
            model_name='reading',
            name='matchup',
        ),
        migrations.AddField(
            model_name='company_matchup',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AddField(
            model_name='like',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AddField(
            model_name='reading',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AlterField(
            model_name='company',
            name='companies_like_matchup',
            field=models.ManyToManyField(related_name='companies_resumes', through='company.Like', to='user.Resume'),
        ),
    ]