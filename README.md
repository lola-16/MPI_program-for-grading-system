# Parallel Grading System with MPI

This Python script simulates a parallel grading system using the `mpi4py` library. It demonstrates the use of MPI's `broadcast`, `scatter`, and `reduce` operations to distribute data and calculate statistics in parallel.

## Goal

The goal of this project is to simulate a parallel grading system where:

* A master process broadcasts grading criteria to all worker processes.
* The master process scatters student scores to the worker processes.
* Worker processes calculate local grades.
* The results are reduced to the master process to compute final class statistics (average, highest, and lowest grade). [cite: 14]

## Task Description

The task involves simulating a grading system with the following specifications:

* Number of students: 8
* Number of processes: 4
* Each process handles 2 students.
* Each student has scores for 3 quizzes and 1 assignment. [cite: 15]

The script calculates the final grade for each student based on predefined weights for quizzes and assignments and then computes the class average, highest grade, and lowest grade.

## Requirements

* Python 3.x
* `mpi4py` library (install using `pip install mpi4py`)
* MPI implementation (e.g., MPICH, Open MPI)

## Usage

1.  Save the Python script (e.g., `grading_system.py`).
2.  Run the script using the `mpiexec` command (or the appropriate MPI launcher for your system).  
    For example, to run with 4 processes:

    ```bash
    mpiexec -n 4 python grading_system.py
    ```

## Code Explanation

The script performs the following steps:

1.  **Initialization:**
    * Imports the necessary libraries (`mpi4py.MPI`, `numpy`).
    * Initializes the MPI communicator and gets the number of processes (`size`) and the rank of the current process (`rank`).
2.  **Broadcast Grading Criteria:**
    * The master process (rank 0) defines the `grading_criteria` (weights for quizzes and assignments).
    * `comm.bcast()` is used to broadcast the `grading_criteria` to all processes. [cite: 2, 3]
3.  **Scatter Student Scores:**
    * The master process simulates student quiz and assignment scores using `numpy.random.randint()`.
    * `comm.scatter()` is used to distribute the student scores (quizzes and assignments) to the worker processes, ensuring each process receives an equal chunk of the data. [cite: 6, 7]
4.  **Calculate Local Final Grades:**
    * Each process calculates the final grade for the students it received, based on the broadcasted `grading_criteria`.
5.  **Reduce to Calculate Statistics:**
    * `comm.reduce()` is used to calculate the global sum, maximum, and minimum of the final grades across all processes. [cite: 10, 11]
6.  **Print Results:**
    * The master process (rank 0) calculates the average grade from the global sum and prints the final class statistics (average, highest, and lowest grade).

## Example Output
Final Class Statistics:

Average Grade: 81.54
Highest Grade: 96.90
Lowest Grade : 56.50
