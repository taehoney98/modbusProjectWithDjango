# Generated by Django 3.1.3 on 2022-03-23 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_value', models.IntegerField(default=0)),
                ('register_input', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Digital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coil_value', models.BooleanField(default=False)),
            ],
        ),
    ]
