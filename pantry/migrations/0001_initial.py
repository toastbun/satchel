# Generated by Django 5.1.4 on 2025-02-08 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('temperature_controlled', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('room', models.CharField(choices=[('kitchen', 'Kitchen'), ('basement', 'Basement')], default='kitchen', max_length=64)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('room__in', ['kitchen', 'basement'])), name='room_exists')],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_expires', models.DateField(null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_items', to='pantry.ingredient')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_items', to='pantry.location')),
            ],
        ),
    ]
