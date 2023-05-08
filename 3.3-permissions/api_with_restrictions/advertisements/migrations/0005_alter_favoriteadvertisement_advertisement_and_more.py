# Generated by Django 4.1.7 on 2023-05-08 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisements', '0004_alter_favoriteadvertisement_advertisement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteadvertisement',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='advertisements.advertisement'),
        ),
        migrations.AlterField(
            model_name='favoriteadvertisement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
