# Generated by Django 4.1.5 on 2023-01-20 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_app', '0004_subscription_slots_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='scammer_flag',
            field=models.CharField(default=0, max_length=5),
        ),
    ]
