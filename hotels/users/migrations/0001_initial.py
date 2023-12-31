# Generated by Django 4.2.5 on 2023-09-16 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(0, 'Admin'), (1, 'Maid Supervisor'), (2, 'Supervisor'), (3, 'Guest')])),
                ('permission_type', models.IntegerField(choices=[(0, 'Create Work Oder Cleaning'), (1, 'Create Work Oder Maid Req'), (2, 'Create Work Oder Technician Req'), (3, 'Create Work Oder Amenity Req')])),
            ],
            options={
                'unique_together': {('user_type', 'permission_type')},
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(0, 'Admin'), (1, 'Maid Supervisor'), (2, 'Supervisor'), (3, 'Guest')], default=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
