# Generated by Django 4.1.5 on 2023-01-19 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('preferred_currency', models.CharField(max_length=10)),
                ('scammer_flag', models.CharField(max_length=5)),
                ('scammer_count', models.IntegerField(default=0)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_name', models.CharField(max_length=255)),
                ('cost', models.CharField(max_length=50)),
                ('expiration', models.CharField(max_length=100)),
                ('group_link', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('slots', models.IntegerField(default=0)),
                ('slots_taken', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('members', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs_joined', to='share_app.customer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions_owned', to='share_app.customer')),
            ],
        ),
    ]