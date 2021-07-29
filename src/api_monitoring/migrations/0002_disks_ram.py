# Generated by Django 3.2.5 on 2021-07-08 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_monitoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('path', models.CharField(max_length=100)),
                ('size', models.IntegerField()),
                ('used', models.IntegerField()),
                ('free', models.IntegerField()),
                ('percent_used', models.IntegerField()),
                ('current_write_speed', models.IntegerField()),
                ('current_read_speed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('type', models.CharField(max_length=50)),
                ('used', models.IntegerField()),
                ('percent_used', models.IntegerField()),
            ],
        ),
    ]
