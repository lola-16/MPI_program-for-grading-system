from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Define the grading criteria (broadcasted from the master process)
if rank == 0:
    grading_criteria = {
        'quiz_weight': 0.6,
        'assignment_weight': 0.4
    }
else:
    grading_criteria = None

grading_criteria = comm.bcast(grading_criteria, root=0)

# Simulate student scores on the master process
num_students = 8
num_quizzes = 3
if rank == 0:
    all_quiz_scores = np.random.randint(50, 101, size=(num_students, num_quizzes))
    all_assignment_scores = np.random.randint(60, 101, size=num_students)

    # Scatter the student scores to the worker processes
    students_per_process = num_students // size
    quiz_scores = np.array_split(all_quiz_scores, size)
    assignment_scores = np.array_split(all_assignment_scores, size)
else:
    quiz_scores = None
    assignment_scores = None

local_quiz_scores = comm.scatter(quiz_scores, root=0)
local_assignment_scores = comm.scatter(assignment_scores, root=0)

# Calculate local final grades
local_final_grades = []
for i in range(len(local_quiz_scores)):
    weighted_quiz_score = np.mean(local_quiz_scores[i]) * grading_criteria['quiz_weight']
    weighted_assignment_score = local_assignment_scores[i] * grading_criteria['assignment_weight']
    final_grade = weighted_quiz_score + weighted_assignment_score
    local_final_grades.append(final_grade)

local_final_grades = np.array(local_final_grades)

# Calculate local sum, max, and min
local_sum = np.sum(local_final_grades)
local_max = np.max(local_final_grades)
local_min = np.min(local_final_grades)

# Reduce to get global sum, max, and min
global_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)
global_max = comm.reduce(local_max, op=MPI.MAX, root=0)
global_min = comm.reduce(local_min, op=MPI.MIN, root=0)

# Calculate and print statistics on the root process
if rank == 0:
    average_grade = global_sum / num_students
    highest_grade = global_max
    lowest_grade = global_min

    print("\nFinal Class Statistics:")
    print(f"- Average Grade: {average_grade:.2f}")
    print(f"- Highest Grade: {highest_grade:.2f}")
    print(f"- Lowest Grade : {lowest_grade:.2f}")