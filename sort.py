import random
import csv
from collections import defaultdict

# Constants
DAYS = 3
WORKSHOPS_PER_DAY = 2
WORKSHOP_CAPACITY = 17

class Student:
    def __init__(self, name, email, preferences):
        self.name = name
        self.email = email
        self.preferences = preferences
        self.assignments = [[] for _ in range(DAYS)]

class Workshop:
    def __init__(self, name, capacity = WORKSHOP_CAPACITY):
        self.name = name
        self.assigned_students = [[] for _ in range(DAYS * WORKSHOPS_PER_DAY)]
        self.capacity = capacity #some workshops have different capacity

def read_input_data(filename):
    students = []
    workshops = set()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            name = row['Name']
            email = row['Email Address']
            preferences = []
            for i in range(1, DAYS + 1):
                batch_prefs = []
                for j in range(1, 7):  # Assuming 6 choices per batch
                    choice = row.get(f'Workshop Batch {i} [{"First" if j == 1 else "Second" if j == 2 else "Third" if j == 3 else "Fourth" if j == 4 else "Fifth" if j == 5 else "Sixth"} Choice]')
                    if choice:
                        batch_prefs.append(choice)
                        workshops.add(choice)
                preferences.append(batch_prefs)
            students.append(Student(name, email, preferences))
    return students, {workshop: Workshop(workshop) for workshop in workshops}

def assign_workshops(students, workshops, day):
    if day == 1:
        random.shuffle(students)
    elif day == 2:
        students.reverse()
    else:
        random.shuffle(students)

    for session in range(WORKSHOPS_PER_DAY):
        for student in students:
            for preference in student.preferences[day-1]:
                workshop = workshops[preference]
                if len(workshop.assigned_students[day*2 - 2 + session]) < workshop.capacity and preference not in [w.name for w in student.assignments[index] for index in range(day)]: #check if the workshop has been assigned on a previous day
                    workshop.assigned_students[day*2 - 2 + session].append(student)
                    student.assignments[day-1].append(workshop)
                    break
                    
def gale_shapley_assigner(students, workshops, day):
    random.shuffle(students)
    
    unassigned_students = list(students)
    assignments = {students: None for student in students}
    current_assignments = {workshop: [] for workshop in capacities}

    while unassigned_students:
        student = unassigned_students.pop(0)
        workshop = student.preferences[day-1]
        preferences_index[student] += 1
        





def output_results(students, output_filename):
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['Name', 'Email']
        for day in range(1, DAYS + 1):
            for session in ['Morning', 'Afternoon']:
                header.append(f'Day {day} {session}')
        writer.writerow(header)
        
        for student in students:
            row = [student.name, student.email]
            for day in range(DAYS):
                for session in range(WORKSHOPS_PER_DAY):
                    if session < len(student.assignments[day]):
                        workshop = student.assignments[day][session]
                        preference = student.preferences[day].index(workshop.name) + 1
                        row.append(f"{workshop.name} ({preference})")
                    else:
                        row.append("Unassigned")
            writer.writerow(row)

def print_statistics(students, workshops):
    choice_counts = defaultdict(int)
    workshop_scores = defaultdict(int)
    workshop_appearances = defaultdict(int)
    unassigned_count = 0
    total_assignments = DAYS * WORKSHOPS_PER_DAY * len(students)
    
    for student in students:
        for day in range(DAYS):
            for session in range(WORKSHOPS_PER_DAY):
                if session < len(student.assignments[day]):
                    workshop = student.assignments[day][session]
                    preference = student.preferences[day].index(workshop.name) + 1
                    choice_counts[preference] += 1
                    workshop_scores[workshop.name] += preference
                    workshop_appearances[workshop.name] += 1
                else:
                    unassigned_count += 1
    
    print("Assignment Statistics:")
    for choice, count in sorted(choice_counts.items()):
        print(f"Choice {choice}: {count}")
    
    print(f"\nUnassigned slots: {unassigned_count}")
    print(f"Percentage of assignments filled: {((total_assignments - unassigned_count) / total_assignments) * 100:.2f}%")
    
    print("\nWorkshop Popularity (lower score = more popular):")
    workshop_avg_scores = {w: workshop_scores[w] / workshop_appearances[w] 
                           for w in workshop_scores}
    sorted_workshops = sorted(workshop_avg_scores.items(), key=lambda x: x[1])
    
    for workshop, avg_score in sorted_workshops:
        print(f"{workshop}: {avg_score:.2f} (assigned {workshop_appearances[workshop]} times)")

def main():
    input_filename = 'FAP_Workshop_Preferences_Dummy_Data.tsv'
    output_filename = 'workshop_assignments.csv'
    
    students, workshops = read_input_data(input_filename)
    
    for day in range(1, DAYS + 1):
        assign_workshops(students, workshops, day)
    
    output_results(students, output_filename)
    print_statistics(students, workshops)

if __name__ == "__main__":
    main()
