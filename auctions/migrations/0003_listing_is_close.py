# Generated by Django 5.0.7 on 2024-08-07 23:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_listing_watchlist_delete_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="is_close",
            field=models.BooleanField(default=False),
        ),
    ]
