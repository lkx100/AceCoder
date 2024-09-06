# AceCoder/dashboard/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Student, Codechef_database
# from .Codechef import CodechefTools

# @receiver(post_save, sender=Student) # Trigerred as soon as created
# def create_codechef_database(sender, instance, created, **kwargs):
#     if created and instance.codechef_id: # If Student is created and Student.codechef_id exists
#         codechef_obj = CodechefTools(instance.codechef_id) # Creates an Codechef_obj for that student
#         if codechef_obj.account_exists():
#             details = codechef_obj.feth_details()[-1] # Fetches last contest data
#             Codechef_database.objects.create( # Creates an object of Codechef_database for that Student.
#                 last_contest = details['code'],
#                 latest_rating = details['rating'],
#                 latest_rank = details['rating'],
#                 student = instance,
#                 no_of_contests = codechef_obj.fetch_num_of_contests(),
#                 no_of_problems = codechef_obj.fetch_num_of_problems(),
#                 plagarisms = codechef_obj.fetch_num_of_plagarisms(),
#                 stars = codechef_obj.stars(),
#             )