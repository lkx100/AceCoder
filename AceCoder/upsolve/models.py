from django.db import models

'''
All_Problem_Tags = [
    'basics', 'math', 'arrays', 'trees', 'bitmask'
]
'''

class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag


class Contest(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    contest = models.CharField(max_length=50)
    link = models.URLField()
    solution_link = models.URLField(default='')
    date = models.DateField()
    duration = models.SmallIntegerField()

    def __str__(self):
        return self.name

class Problem(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="problems")
    problem_link = models.URLField(default='')
    rating = models.IntegerField(null=True, blank=True)
    problem_tags = models.ManyToManyField(Tag, related_name="tags")
    def __str__(self):
        return self.name