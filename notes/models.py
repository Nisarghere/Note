from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes", null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update= models.DateTimeField(auto_now=True, null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    shared_to = models.ManyToManyField(User, related_name="shared_notes",through="NoteShare", blank=True)
    #img = models.ImageField(upload_to="profiles/", blank=True, null=True)
    attachment= models.FileField(upload_to="attachments/", blank=True, null=True)

       
    def __str__(self):
        return self.title
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    
    def __str__(self):
        return self.user.username   

class NoteShare(models.Model):
    PERMISSION_CHOICES=[
        ("view", "view only"),
        ("edit", "edit only"),
    ]
    
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default="view")
    
    class Meta:
        unique_together = ("note", "user")  # avoid duplicates

    def __str__(self):
        return f"{self.user.username} - {self.note.title} ({self.permission})"
        
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
