# Generated by Django 3.2.9 on 2021-11-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField(blank=True, null=True)),
                ('sfirstname', models.CharField(blank=True, max_length=25, null=True)),
                ('ssecondname', models.CharField(blank=True, max_length=25, null=True)),
                ('sage', models.IntegerField(blank=True, null=True)),
                ('smajor', models.CharField(blank=True, max_length=50, null=True)),
                ('saddress', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'students',
                'managed': False,
            },
        ),
    ]