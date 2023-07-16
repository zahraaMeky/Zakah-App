# Generated by Django 3.2.7 on 2021-09-28 15:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ar', models.CharField(blank=True, max_length=500, null=True)),
                ('name_en', models.CharField(blank=True, max_length=500, null=True)),
                ('logo', models.ImageField(upload_to='uploads/')),
                ('city', models.CharField(blank=True, max_length=300, null=True)),
                ('phone', models.CharField(blank=True, max_length=300, null=True)),
                ('website', models.CharField(blank=True, max_length=300, null=True)),
                ('device_id', models.CharField(blank=True, max_length=300, null=True)),
                ('charity_id', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='Sub_types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_type_ar', models.CharField(blank=True, max_length=300, null=True)),
                ('sub_type_en', models.CharField(blank=True, max_length=300, null=True)),
                ('sub_id', models.CharField(blank=True, max_length=300, null=True)),
                ('type_id', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name_plural': 'Sub Zakah types',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
                ('money', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('device_id', models.CharField(blank=True, max_length=300, null=True)),
                ('trans_id', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name_plural': 'Donate Transaction',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_ar', models.CharField(blank=True, max_length=100, null=True)),
                ('type_en', models.CharField(blank=True, max_length=100, null=True)),
                ('charity_id', models.CharField(blank=True, max_length=300, null=True)),
                ('type_id', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name_plural': 'Zakah types',
            },
        ),
    ]