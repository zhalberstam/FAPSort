import random
import csv

# Constants
WORKSHOP_CAPACITY = 12
TOTAL_CAPACITY = 24
DAYS = 3
WORKSHOPS_PER_DAY = 2

class Student:
    def __init__(self, name, email, preferences):
        self.name = name
        self.email = email
        self.preferences = preferences
        self.assignments = [[] for _ in range(DAYS)]

class Workshop:
    def __init__(self, name):
        self.name = name
        self.assigned_students = [[] for _ in range(DAYS * WORKSHOPS_PER_DAY)]

def read_input_data(filename):
    students = []
    workshops = set()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            name = row['Name']
            email = row['Email Address']
            preferences = [
                [row[f'Workshop Batch {i} [First Choice]'], row[f'Workshop Batch {i} [Second Choice]'],
                 row[f'Workshop Batch {i} [Third Choice]'], row[f'Workshop Batch {i} [Fourth Choice]'],
                 row[f'Workshop Batch {i} [Fifth Choice]'], row[f'Workshop Batch {i} [Sixth Choice]']]
                for i in range(1, 4)
            ]
            students.append(Student(name, email, preferences))
            workshops.update(sum(preferences, []))
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
                if len(workshop.assigned_students[day*2 - 2 + session]) < WORKSHOP_CAPACITY and preference not in [w.name for w in student.assignments[day-1]]:
                    workshop.assigned_students[day*2 - 2 + session].append(student)
                    student.assignments[day-1].append(workshop)
                    break

def output_results(students, output_filename):
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Day 1 Morning', 'Day 1 Afternoon', 'Day 2 Morning', 'Day 2 Afternoon', 'Day 3 Morning', 'Day 3 Afternoon'])
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

def main():
    input_filename = 'FAP_Workshop_Preferences_Dummy_Data.tsv'
    output_filename = 'workshop_assignments.csv'
    
    students, workshops = read_input_data(input_filename)
    
    for day in range(1, DAYS + 1):
        assign_workshops(students, workshops, day)
    
    output_results(students, output_filename)

if __name__ == "__main__":
    main()
