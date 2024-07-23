import csv
import random
from datetime import datetime, timedelta

# Constants
NUM_STUDENTS = 100
WORKSHOPS_BATCH1 = ["Dana's Dancing", "Texaco's Tunes", "Joe's Clothes", "Avi's Art", "Elyse's Energy", "Zach's Wax"]
WORKSHOPS_BATCH2 = ["Joy's Voice", "Max's Music", "Lollie's Trolly", "AJ's Wordplay", "Em's Kin", "Adam's Architecture"]
WORKSHOPS_BATCH3 = ["Bimba's Limbo", "Crystal's Whistles", "Ria's Rave", "Priya's Party", "Keren's Cartwheels", "Gabby's Great's"]

def generate_name():
    first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William"]
    last_names = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Moore", "Anderson", "Thomas", "Jackson"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_email(name):
    return f"{name.lower().replace(' ', '.')}@college.harvard.edu"

def generate_preferences(workshops):
    return random.sample(workshops, len(workshops))

def generate_dummy_data(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        
        # Write header
        header = ["Timestamp", "Email Address", "Name"]
        for batch in range(1, 4):
            for choice in range(1, 7):
                header.append(f"Workshop Batch {batch} [{'First' if choice == 1 else 'Second' if choice == 2 else 'Third' if choice == 3 else 'Fourth' if choice == 4 else 'Fifth' if choice == 5 else 'Sixth'} Choice]")
        writer.writerow(header)
        
        # Generate data for each student
        start_time = datetime.now()
        for _ in range(NUM_STUDENTS):
            name = generate_name()
            email = generate_email(name)
            timestamp = (start_time + timedelta(minutes=random.randint(0, 60))).strftime("%m/%d/%Y %H:%M:%S")
            
            row = [timestamp, email, name]
            row.extend(generate_preferences(WORKSHOPS_BATCH1))
            row.extend(generate_preferences(WORKSHOPS_BATCH2))
            row.extend(generate_preferences(WORKSHOPS_BATCH3))
            
            writer.writerow(row)

if __name__ == "__main__":
    output_filename = "FAP_Workshop_Preferences_Dummy_Data.tsv"
    generate_dummy_data(output_filename)
    print(f"Dummy data has been generated and saved to {output_filename}")
