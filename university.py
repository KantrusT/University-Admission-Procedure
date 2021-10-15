from dataclasses import dataclass, astuple, asdict, field

# Reading inputs.
n = int(input())

@dataclass(order=True)
class Department:
    name: str
    id: int #  represents position of gpa related to this dep in the student list.
    applicants_quantity: int = 0
    successful_applicants: list = field(default_factory=list)
    applicants: list = field(default_factory=list)
    size: int = n


@dataclass(order=True)
class Applicant:
    name: str
    scores: list = field(default_factory=list)
    priorities: tuple = field(default_factory=tuple)



#   Assigning applicants to the successful list
def assign_applicants(departments):
    i = 0
    for dep in departments:
        for student in dep.applicants[:]:
            if dep.applicants_quantity < n:
                dep.successful_applicants.append(student)  # Add a student to the list.
                dep.applicants_quantity += 1  # Increment total student number in the department.
                dep.applicants.remove(student)  # delete the applicant from the old list
        i += 1
    for dep in departments:
        sort_applicants(dep)  #  sorting time!


def init_students(applicants):
    j = 0
    applicants = []
    for student in applicants_list:
        name = student[0] + ' ' + student[1]
        scores = [i for i in student[2:6]]
        priorities = {i for i in student[6:9]}
        applicants.append(Applicant(name))
        applicant = applicants[j]
        applicant.scores = scores
        applicant.priorities = priorities
        j += 1


#   Sorts applicants within the department
def sort_applicants(department):
    department.applicants = sorted(department.applicants, key=lambda x: (-max(x[department.id], x[6]), x[0], x[1]))
    if (department.successful_applicants) is not None:
        department.successful_applicants = sorted(department.successful_applicants, key=lambda x: (-max(x[department.id], x[6]), x[0], x[1]))


#   Divides applicants into departments
def divide_applicants(applicants, departments, prior):
    for student in applicants:
        priority = student[prior]
        for dep in departments:
            if dep.name == priority:
                dep.applicants.append(student)  # Add a potential student
                break

    for dep in departments:
        sort_applicants(dep)    #  sorting time!


#   Rearranging and clearing the old lists
def rearrange_applicants(applicants_list, departments):
    applicants_list.clear()
    for dep in departments:
        for appl in dep.applicants:
            applicants_list.append(appl)
        dep.applicants.clear()


#   Main function for sorting applicants
def sorting(applicants, departments):
    prior = 7
    for _ in range (3):
        divide_applicants(applicants, departments, prior)
        assign_applicants(departments)
        rearrange_applicants(applicants, departments)
        prior += 1
        if (prior > 9):
            prior = 9

#   Printing applicants
def printing_applicants(departments):
    for dep in departments:
        print(dep.name)
        for student in dep.successful_applicants:
            print(F'{student[0]} {student[1]} {student[dep.id]}')
        print()


#   Writes to file and prints results
def write_to_file(department, file):
    # write the names on separate lines
    for student in department.successful_applicants:
        # print(F'{student[0]} {student[1]} {student[department.id]}')
        file.write(student[0] + " " + student[1] + " " + str(
            max(student[department.id], student[6])) + '\n')
    file.close()


# Initializing and populating applicants list.
applicants_list = []
with open('applicants.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # we use strip() to get rid of newline symbols
        applicants_list.append(line.strip().split(" "))
    for student in applicants_list:
        for i in range(2, 7):
            student[i] = float(student[i])  # GPA as float
        student.append(student[3])  #   saving chemistry value for the later use
        student[3] = (student[2] + student[3]) / 2    # calculating mean for biotech
        student[2] = (student[4] + student[2]) / 2    #  calculating mean for physics
        student[5] = (student[4] + student[5]) / 2    #  calculating mean for engineering

# Initializing department list.
print(applicants_list)
biotech = Department("Biotech", 3)
chemistry = Department("Chemistry", 10)
engineering = Department("Engineering", 5)
mathematics = Department("Mathematics", 4)
physics = Department("Physics", 2)
departments = [biotech, chemistry, engineering, mathematics, physics]
dep_dict = {'Biotech':3, 'Chemistry':3, 'Engineering':5, 'Mathematics':4, 'Physics':2}

# Dividing and sorting applicants.
sorting(applicants_list, departments)
printing_applicants(departments)

# Writing to filies and printing results
biotech_file = open('biotech.txt', 'w', encoding='utf-8')
write_to_file(departments[0], biotech_file)
chemistry_file = open('chemistry.txt', 'w', encoding='utf-8')
write_to_file(departments[1], chemistry_file)
engineering_file = open('engineering.txt', 'w', encoding='utf-8')
write_to_file(departments[2], engineering_file)
mathematics_file = open('mathematics.txt', 'w', encoding='utf-8')
write_to_file(departments[3], mathematics_file)
physics_file = open('physics.txt', 'w', encoding='utf-8')
write_to_file(departments[4], physics_file)