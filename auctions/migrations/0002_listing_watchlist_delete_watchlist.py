# Generated by Django 5.0.7 on 2024-08-02 07:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Watchlist",
        ),
    ]
