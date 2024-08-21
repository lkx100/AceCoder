from django.db import models
from .Codechef import CodechefTools

# Create your models here.
class Student(models.Model): # Model for Student database

    department_options = ( # Options for department field
        ('Ai&Ds', 'Ai&Ds'),
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
    )

    years_options = ( # Options for year field
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )

    sections_options = ( # Options for section field
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
    )

    # Input fields
    name = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=10)
    codechef_id = models.CharField(max_length=100, null=True)
    department = models.CharField(choices=department_options, max_length=5)
    year = models.CharField(choices=years_options, max_length=1)
    section = models.CharField(choices=sections_options, max_length=1)

    # Display name
    def __str__(self) -> str:
        return f"{self.roll_no} - {self.name}"


class Codechef_database(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=True)
    last_contest = models.CharField(max_length=10 ,null=True, blank=True)
    latest_rating = models.IntegerField(null=True, blank=True)
    latest_rank = models.IntegerField(null=True, blank=True)
    no_of_contests = models.IntegerField(null=True, blank=True)
    no_of_problems = models.IntegerField(null=True, blank=True)
    plagarisms = models.IntegerField(null=True, blank=True)
    contest_problems = models.CharField(max_length=1000, null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.student and self.student.codechef_id:
            codechef_obj = CodechefTools(self.student.codechef_id)
            if codechef_obj.account_exists():
                details = codechef_obj.feth_details()[-1]
                self.last_contest = details['code']
                self.last_contest_full = details['name']
                self.latest_rating = details['rating']
                self.latest_rank = details['rank']
                self.no_of_contests = codechef_obj.fetch_num_of_contests()
                self.no_of_problems = codechef_obj.fetch_num_of_problems()
                self.plagarisms = codechef_obj.fetch_num_of_plagarisms()
                contest_problems_list = codechef_obj.fetch_contest_problems().get(self.last_contest_full, [])
                self.contest_problems = ", ".join(contest_problems_list)
                self.stars = codechef_obj.stars()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.student:
            return f"{self.student.roll_no} - {self.student.name}"
        else:
            return f"Student Deleted"
