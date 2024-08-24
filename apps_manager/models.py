from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.apk']
  if not ext in valid_extensions:
    raise ValidationError(u'File not supported!')
 
class App(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file_path = models.FileField(upload_to='apk_files/',validators=[validate_file_extension])
    first_screen_screenshot_path = models.ImageField(upload_to='screenshots/',default='notfound')
    second_screen_screenshot_path = models.ImageField(upload_to='screenshots/',default='notfound')
    video_recording_path = models.FileField(upload_to='videos/',default='notfound')
    ui_hierarchy = models.TextField()
    screen_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
