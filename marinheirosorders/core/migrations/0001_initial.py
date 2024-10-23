# Generated by Django 5.1.2 on 2024-10-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('dish_name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('dish_note', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('table_number', models.IntegerField()),
                ('waiter', models.CharField(max_length=100)),
                ('is_outside', models.BooleanField(default=False)),
                ('order_note', models.TextField(blank=True)),
                ('dishes', models.ManyToManyField(related_name='orders', to='core.dish')),
            ],
        ),
    ]