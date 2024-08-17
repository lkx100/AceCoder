from django.db import models

class Post(models.Model):
    tittle = models.CharField(max_length = 200)
    created_on = models.DateField()
    edited_on = models.DateField()
    description = models.CharField(max_length = 200)
    post = models.TextField()
    banner = models.ImageField(upload_to = 'gallery/', blank = True, null = True)
    pictures = models.ImageField(upload_to = 'gallery/', blank = True, null = True)
    author = models.CharField(max_length = 100)

    def __str__(self):
        return f"\"{self.tittle[:20]}.... \" by {self.author}" if len(self.tittle) > 20 else f"\"{self.tittle}\" by {self.author}"
