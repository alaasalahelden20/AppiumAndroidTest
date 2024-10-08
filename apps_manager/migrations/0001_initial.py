# Generated by Django 5.1 on 2024-08-20 02:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('apk_file_path', models.FileField(upload_to='apk_files/')),
                ('first_screen_screenshot_path', models.ImageField(upload_to='screenshots/')),
                ('second_screen_screenshot_path', models.ImageField(upload_to='screenshots/')),
                ('video_recording_path', models.FileField(upload_to='videos/')),
                ('ui_hierarchy', models.TextField()),
                ('screen_changed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
