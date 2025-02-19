# Generated by Django 5.1.6 on 2025-02-19 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSubstitute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroceryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PackagingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('grocery_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grocery_type_items', to='pantry.grocerytype')),
                ('substitute_key', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='food_substitute_ingredients', to='pantry.foodsubstitute')),
            ],
        ),
        migrations.CreateModel(
            name='GroceryListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_grocery_list_items', to='pantry.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=64)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_tags', to='pantry.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('room', models.CharField(choices=[('kitchen', 'Kitchen'), ('basement', 'Basement'), ('overflow', 'Overflow')], default='kitchen', max_length=64)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('room__in', ['kitchen', 'basement', 'overflow'])), name='room_exists')],
            },
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multi_use', models.BooleanField(default=False)),
                ('amount_left', models.CharField(choices=[('high', 'High'), ('medium', 'Med'), ('low', 'Low')], default='high', max_length=64, null=True)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('date_expires', models.DateField(null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_items', to='pantry.ingredient')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_items', to='pantry.location')),
                ('packaging_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packaging_type_items', to='pantry.packagingtype')),
            ],
        ),
    ]
