from django.core.management import BaseCommand
from dashboard.models import Student, Codechef_database
from dashboard.Codechef import CodechefTools
import time

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        all_students = Student.objects.all()
        n = len(all_students)

        print("-"*32 + " AceCoder Codechef Details Updater " + "-"*32)
        print("Script started...")

        for index,student in enumerate(all_students):
            codechef_obj = CodechefTools(student.codechef_id)
            print(f"Updating details of {student.name} - {student.codechef_id}...")
            if codechef_obj.account_exists():
                details = codechef_obj.feth_details()[-1]  # Fetches last contest data
                codechef_db, created = Codechef_database.objects.get_or_create(student=student)
                codechef_db.last_contest = details['code']
                codechef_db.latest_rating = details['rating']
                codechef_db.latest_rank = details['rank']
                codechef_db.no_of_contests = codechef_obj.fetch_num_of_contests()
                codechef_db.no_of_problems = codechef_obj.fetch_num_of_problems()
                codechef_db.plagarisms = codechef_obj.fetch_num_of_plagarisms()
                codechef_db.stars = codechef_obj.stars()
                codechef_db.save()
                print(f"Success! -> {student.name} details updated!")
            else:
                print(f"Failed! -> {student.name} details not updated!")
            print(f"{index+1} out of {n} done!")
            # print("Cooldown 10 sec...")
            # time.sleep(10)
            print("-"*28)

        print("Script ended!")