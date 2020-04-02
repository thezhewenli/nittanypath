# Generated by Django 2.2.5 on 2020-03-29 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityMemberProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_name', models.TextField()),
                ('age', models.PositiveSmallIntegerField()),
                ('legal_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('home_zipcode', models.CharField(max_length=5)),
                ('home_street_address', models.TextField()),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UniversityMember',
        ),
    ]
