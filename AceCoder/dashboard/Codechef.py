import requests
import re
import json
from bs4 import BeautifulSoup
import pandas as pd

class CodechefTools:

    def __init__(self, codechef_handle: str) -> None:
        self.codechef_handle = codechef_handle
        self.url = f"https://www.codechef.com/users/{codechef_handle}"
        self.result = requests.get(self.url)
        self.script_text = self.result.text
        # Parse the HTML content using BeautifulSoup
        self.soup = BeautifulSoup(self.script_text, 'html.parser')

    def account_exists(self) -> bool:
        # Use regular expression to find the JavaScript array containing ratings
        self.match = re.search(r"var all_rating = (\[.*?\]);", self.script_text, re.DOTALL)
        if self.match:
            return True
        else:
            print(f"User names {self.codechef_handle} doesnot exists!")
            return False
        
    def fetch_num_of_contests(self) -> int:
        contests_text = self.soup.find('h3', string=lambda t: 'Contests' in t).text
        num_contests = int(contests_text.split('(')[1].split(')')[0])
        return num_contests
    
    def fetch_num_of_problems(self) -> int:
        problems_solved_text = self.soup.find('h3', string=lambda t: 'Total Problems Solved' in t).text
        num_practice_problems = int(problems_solved_text.split(': ')[1])
        return num_practice_problems
    
    def fetch_num_of_plagarisms(self) -> int:
        ratings = self.feth_details()
        counts = 0
        for contest in ratings:
            if contest['penalised_in']: counts+=1

        return counts
    
    def stars(self):
        ratings = self.feth_details()
        curr_rating = int(ratings[-1]['rating'])
        if curr_rating < 1400:
            return 1
        elif curr_rating < 1600:
            return 2
        elif curr_rating < 1800:
            return 3
        elif curr_rating < 2000:
            return 4
        elif curr_rating < 2200:
            return 5
        elif curr_rating < 2400:
            return 6
        else:
            return 7

    def feth_details(self) -> list:
        # Extract the ratings data as a JSON array
        ratings_json = self.match.group(1)
        # Convert the JSON array to a Python list
        self.ratings = json.loads(ratings_json)
        return self.ratings
    
    def pd_fetch(self) -> pd.DataFrame:
        data = self.feth_details()

        rows = []

        for contest in data:
            row = {
                "Contest": contest['code'],
                "Rating": contest['rating'],
                "Rank": contest['rank'],
                "Plagarised": "No" if contest["penalised_in"] == None else "Yes"
            }
            rows.append(row)

        df = pd.DataFrame(rows)

        return(df)
    
    def fetch_contest_problems(self) -> dict:
        contests_section = self.soup.find_all('div', class_='content')
        contest_problems = {}
        
        for section in contests_section:
            # print("Section:", section)  # Debugging line to print the section
            h5_tag = section.find('h5')
            if h5_tag:
                contest_name = h5_tag.text.strip()
                paragraphs = section.find_all('p')
                if len(paragraphs) > 0:
                    problems = paragraphs[0].find_all('span', style=lambda value: value and 'font-size: 12px' in value)
                    problem_list = [problem.text.strip() for problem in problems]
                    contest_problems[contest_name] = problem_list
                else:
                    print(f"No problems found for contest {contest_name}")
            else:
                # print("No 'h5' tag found in this section")
                continue
            # print("-"*32)

        return contest_problems
    
if __name__ == "__main__":
    obj = CodechefTools("sweshikreddy")
    obj.account_exists()
    details = obj.fetch_contest_problems()
    for arr in details.values():
        print(", ".join(arr))