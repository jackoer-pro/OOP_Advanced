#  Base Class 
import json
import os
DATA_FILE = "school.json"
class Person:
    def __init__(self, name, dob, hometown):
        self.name = name
        self.dob = dob  # date of birth as string
        self.hometown = hometown
        self.email = f"{name}.{dob.replace('-', '')}@gmail.com"


# ===== Student =====
class Student(Person):
    def __init__(self, name, dob, hometown, subjects, is_leader=False):
        super().__init__(name, dob, hometown)
        self.subjects = subjects
        self.is_leader = is_leader


# ===== Teacher =====
class Teacher(Person):
    def __init__(self, name, dob, hometown, subject):
        super().__init__(name, dob, hometown)
        self.subject = subject
    def show_students(self):
        with open(DATA_FILE,"r") as f:
            data=json.load(f)
        for t in data["teachers"]:
            if self.subject==t["subject"]:
                print(f"\n{self.subject} Teacher: {self.name}")
                if not t["students"]:
                    print("  (No students)")
                for s in t["students"]:
                    print(f"  - {s['name']} ({s['role']}), DOB: {s['dob']}, Hometown: {s['hometown']}, Subjects: {', '.join(s['subjects'])}")
# Teachers 
teachers = [
    Teacher("Mr Linh", "1988-05-12", "HN", "Math"),
    Teacher("Ms Mai", "1989-08-20", "HN", "Physics"),
    Teacher("Mr Nam", "1987-02-14", "HN", "Chemistry"),
    Teacher("Ms Hoa", "1990-11-05", "HN", "English")
]
available_subjects=[t.subject for t in teachers]

# Create Json data base forever
def init_json():
    if os.path.exists(DATA_FILE):
        return
    data = {
        "teachers": [
            {"name": t.name, "subject": t.subject, "students": []}
            for t in teachers
        ]
    }

    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)
def check_existing_student(student, existing_students):
    return any(
        s["name"]==student["name"] and
        s["dob"] == student["dob"] and
        s["hometown"] == student["hometown"]
        for s in existing_students
    )

def register_student():
    print("\n--- Student Registration ---")
    name = input("Name: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")
    hometown = input("Hometown: ")

    print("Available subjects:", ", ".join(available_subjects))
    subjects = []
    while len(subjects) < 2:
        sub = input("Choose subject (or 'done'): ")
        if sub == "done":
            break
        if sub in available_subjects and sub not in subjects:
                subjects.append(sub)
        else:
            print("Invalid or duplicated subject")

    if not subjects:
        print("❌ Must choose at least one subject")
        return 
    leader_choice = input("Do you want to be a leader? (yes/no): ").lower()
    is_leader = leader_choice == "yes"
    new_student={
        "name":name,
        "dob": dob,
        "hometown": hometown,
        "subjects": subjects,
        "role": "Leader" if is_leader else "Student"
    }
    with open(DATA_FILE,"r") as f:
        data=json.load(f)
    for t in data["teachers"]:
        if t["subject"] in subjects:
            if not check_existing_student(new_student,t["students"]):
                t["students"].append(new_student)
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)
    print(f"✅ {name} registered successfully")
def remove_from_subject():
    name = input("Student name: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")
    print("Available subjects:", ", ".join(available_subjects))
    subject = input("Which subject do you want to remove yourself from? ")

    if subject not in available_subjects:
        print("❌ Invalid subject")
        return

    removed = False
    with open(DATA_FILE,"r") as f:
        data = json.load(f)

    for t in data["teachers"]:
        if t["subject"] == subject:
            original_len = len(t["students"])
            t["students"] = [
                s for s in t["students"]
                if not (s["name"].strip() == name.strip() and s["dob"] == dob)
            ]
            if len(t["students"]) < original_len:
                removed = True

    with open(DATA_FILE,"w") as f:
        json.dump(data, f, indent=4)

    if removed:
        print(f"✅ {name} removed from {subject}")
    else:
        print(f"❌ Student not found in {subject}")

    print(f"🗑️  {name} deleted")
def reset_semester():
    confirm = input("⚠️ Reset ALL students for new semester? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Cancelled")
        return

    # Read existing JSON
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Clear students for all teachers
    for t in data["teachers"]:
        t["students"] = []

    # Write back to JSON
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ New semester started")
init_json()

while True:
    print("""
1. Register student
2. Show teachers
3. Delete ONE student
4. New semester (reset all)
5. Exit
""")
    choice = input("Choose: ")
    if choice == "1":
        register_student()
    elif choice == "2":
        for t in teachers:
            t.show_students()
    elif choice == "3":
        remove_from_subject()
    elif choice == "4":
        reset_semester()
    elif choice == "5":
        break

