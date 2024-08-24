import pandas as pd
import time
from django.core.management import BaseCommand
from dashboard.models import Student
from dashboard.Codechef import CodechefTools

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        codechef_handles = pd.read_excel("static\Codechef_Credentials\Codechef_details(Staters 146).xlsx")
        n = len(codechef_handles)
        branch = {
            '3': "CSE",
            '4': "ECE",
            '8': "Ai&Ds",
        }

        try:
            for index, row in list(codechef_handles.iterrows())[564:]:
                roll_no = str(row['Roll No'])
                name = row['Name']
                codechef_id = row['Codechef Id']

                student, created = Student.objects.get_or_create(
                    roll_no=roll_no,
                    name=name,
                    department=branch.get(roll_no[5], "Unknown"),
                    defaults={'codechef_id': codechef_id, 'year': '2'}
                )
                if created:
                    print(f"Created new student: {name} - {roll_no}")
                else:
                    print(f"Updated existing student: {name} - {roll_no}")

                codechef_obj = CodechefTools(codechef_id)
                if codechef_obj.account_exists():
                    details = codechef_obj.feth_details()[-1]
                    student.last_contest = details['code']
                    student.latest_rating = details['rating']
                    student.latest_rank = details['rank']
                    student.no_of_contests = codechef_obj.fetch_num_of_contests()
                    student.no_of_problems = codechef_obj.fetch_num_of_problems()
                    student.plagarisms = codechef_obj.fetch_num_of_plagarisms()
                    student.contest_problems = ", ".join(codechef_obj.fetch_contest_problems().get(details['name'], []))
                    student.stars = codechef_obj.stars()
                    student.save()
                    print(f"Success! -> {name} details added to Student!")
                else:
                    print(f"Failed! -> {name} details not added to Student!")

                print(f"{index+1} out of {n} done! --> {((index+1)/n)*100}% completed.")
                print("-"*32)
        except Exception as e:
            print(f"Error occurred! --> {e}")

        print("Script ended!")