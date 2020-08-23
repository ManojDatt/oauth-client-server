# Generated by Django 3.0.9 on 2020-08-22 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('task_name', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('priority', models.CharField(choices=[('HIGHT', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('MODERATE', 'MODERATE')], max_length=20)),
                ('complete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Todos',
            },
        ),
    ]
