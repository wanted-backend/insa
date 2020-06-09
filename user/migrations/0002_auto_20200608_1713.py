# Generated by Django 3.0.6 on 2020-06-08 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20200608_1713'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work_information',
            name='matchup',
        ),
        migrations.RemoveField(
            model_name='exception',
            name='matchup',
        ),
        migrations.RemoveField(
            model_name='matchup_job',
            name='matchup',
        ),
        migrations.RemoveField(
            model_name='matchup_skill',
            name='matchup',
        ),
        migrations.AddField(
            model_name='exception',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AddField(
            model_name='matchup_job',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AddField(
            model_name='matchup_skill',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Resume'),
        ),
        migrations.AddField(
            model_name='resume',
            name='income',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resume',
            name='matchup_career',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Matchup_career'),
        ),
        migrations.AddField(
            model_name='resume',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Role'),
        ),
        migrations.AddField(
            model_name='resume',
            name='school',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Matchup',
        ),
        migrations.DeleteModel(
            name='Work_information',
        ),
    ]