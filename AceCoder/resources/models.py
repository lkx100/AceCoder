from django.db import models

class PostTag(models.Model):
    post_tag = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.post_tag

class Post(models.Model):
    tittle = models.CharField(max_length = 200)
    created_on = models.DateField()
    edited_on = models.DateField()
    description = models.CharField(max_length = 200)
    post = models.TextField()
    banner = models.ImageField(upload_to = 'gallery/', blank = True, null = True)
    pictures = models.ImageField(upload_to = 'gallery/', blank = True, null = True)
    author = models.CharField(max_length = 100)
    tags = models.ManyToManyField(PostTag)

    def __str__(self):
        return f"\"{self.tittle[:20]}.... \" by {self.author}" if len(self.tittle) > 20 else f"\"{self.tittle}\" by {self.author}"
    

class SubPost(models.Model):
    tittle = models.CharField(max_length = 200)
    link = models.URLField(default = '')
    parent_post = models.ManyToManyField(Post)

    def __str__(self):
        return self.tittle
