# CS1350 Week 2 Homework: NumPy Array Operations
# Submission: homework2_lastname_firstname.py
# NOTE: Replace "lastname_firstname" in the filename with your actual last and first name
# 
# Required import for all problems
import numpy as np

# Set random seed for reproducible results
np.random.seed(1350)  # Use course number as seed


# -----------------------------
# Problem 1: Array Creation and Basic Operations (20 points)
# -----------------------------
def problem1():
    """
    Create arrays using different NumPy methods and perform basic operations.
    Returns:
        arr1, arr2, identity, linspace_arr, random_arr
    """
    # a) Create a 1D array of integers from 10 to 50 (inclusive) with step 5
    # Store in variable 'arr1'
    arr1 = np.arange(10, 51, 5)

    # b) Create a 2D array of shape (3, 4) filled with zeros
    # Store in variable 'arr2'
    arr2 = np.zeros((3, 4), dtype=float)

    # c) Create a 3x3 identity matrix
    # Store in variable 'identity'
    identity = np.eye(3, dtype=float)

    # d) Create an array of 10 evenly spaced numbers between 0 and 5
    # Store in variable 'linspace_arr'
    linspace_arr = np.linspace(0, 5, 10)

    # e) Create a random array of shape (2, 5) with values between 0 and 1
    # Store in variable 'random_arr'
    random_arr = np.random.rand(2, 5)

    return arr1, arr2, identity, linspace_arr, random_arr


# -----------------------------
# Problem 2: Array Mathematics and Broadcasting (20 points)
# -----------------------------
def problem2():
    """
    Perform array operations using broadcasting.
    Returns:
        result_add, result_multiply, result_square, column_means, centered_arr
    """
    # Given arrays
    arr_a = np.array([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]])

    arr_b = np.array([10, 20, 30])

    # a) Add arr_b to each row of arr_a (using broadcasting)
    result_add = arr_a + arr_b  # (3,3) + (3,) -> broadcast across columns

    # b) Multiply each column of arr_a by the corresponding element in arr_b
    result_multiply = arr_a * arr_b  # broadcast across columns

    # c) Calculate the square of all elements in arr_a
    result_square = arr_a ** 2

    # d) Calculate the mean of each column in arr_a
    column_means = arr_a.mean(axis=0)

    # e) Subtract the column means from each element in the respective column (centering)
    centered_arr = arr_a - column_means

    return result_add, result_multiply, result_square, column_means, centered_arr


# -----------------------------
# Problem 3: Array Indexing and Slicing (25 points)
# -----------------------------
def problem3():
    """
    Demonstrate array indexing and slicing.
    Returns:
        third_row, last_column, center_subarray, greater_than_15, arr_copy
    """
    # Create a 5x5 array with values from 1 to 25
    arr = np.arange(1, 26).reshape(5, 5)

    # a) Extract the third row
    third_row = arr[2, :]  # zero-based indexing

    # b) Extract the last column
    last_column = arr[:, -1]

    # c) Extract the 2x2 subarray from the center (rows 1-2, columns 1-2)
    # Based on the parenthetical note: rows 1-2 and cols 1-2 -> indices 1:3
    center_subarray = arr[1:3, 1:3]

    # d) Extract all elements greater than 15
    greater_than_15 = arr[arr > 15]

    # e) Replace all even numbers with -1 (create a copy first)
    arr_copy = arr.copy()
    arr_copy[arr_copy % 2 == 0] = -1

    return third_row, last_column, center_subarray, greater_than_15, arr_copy


# -----------------------------
# Problem 4: Statistical Analysis (25 points)
# -----------------------------
def problem4():
    """
    Perform statistical analysis on student scores.
    Returns:
        student_averages, test_averages, student_max_scores, test_std, high_performers
    """
    # Student test scores (rows: students, columns: tests)
    scores = np.array([[85, 90, 78, 92],
                       [79, 85, 88, 91],
                       [92, 88, 95, 89],
                       [75, 72, 80, 78],
                       [88, 91, 87, 94]])

    # a) Calculate the average score for each student (across all tests)
    student_averages = scores.mean(axis=1)

    # b) Calculate the average score for each test (across all students)
    test_averages = scores.mean(axis=0)

    # c) Find the highest score for each student
    student_max_scores = scores.max(axis=1)

    # d) Find the standard deviation of scores for each test
    test_std = scores.std(axis=0, ddof=0)  # population std per instructions

    # e) Identify which students have an average score above 85 (boolean array)
    high_performers = student_averages > 85

    return student_averages, test_averages, student_max_scores, test_std, high_performers


# -----------------------------
# Problem 5: Performance Comparison (10 points)
# (The spec shows problem6 below; we provide both.
#  problem5 implements the comparison, and problem6 calls problem5.)
# -----------------------------
def problem5():
    """
    Compare performance between NumPy arrays and Python lists by squaring elements.
    Returns: dict with timings and speedup.
    """
    import time

    size = 100_000

    # Create Python list and NumPy array with same data
    python_list = list(range(size))
    numpy_array = np.arange(size)

    # Python list approach (list comprehension)
    start_time = time.time()
    list_result = [x * x for x in python_list]
    list_time = time.time() - start_time

    # NumPy array approach (vectorized)
    start_time = time.time()
    array_result = numpy_array ** 2
    numpy_time = time.time() - start_time

    # Validate same result length to avoid "unused variable" lint and sanity check
    assert len(list_result) == array_result.size

    # Calculate speedup
    speedup = list_time / (numpy_time if numpy_time > 0 else np.nan)

    return {
        'list_time': list_time,
        'numpy_time': numpy_time,
        'speedup': speedup,
        'conclusion': f"NumPy is {speedup:.1f}x faster than Python lists for this operation"
    }


# -----------------------------
# Problem 6: Alias to Problem 5 (per provided skeleton)
# -----------------------------
def problem6():
    """Alias/wrapper that performs the same comparison as problem5()."""
    return problem5()


# -----------------------------
# Bonus Challenge (Optional, +25 points)
# -----------------------------
def bonus_challenge():
    """
    Create a simple 10x10 'image' and apply transformations.
    Returns:
        normalized, brightened, negative, thresholded
    """
    # Create a 10x10 array representing a grayscale image
    # Values should be between 0 (black) and 255 (white)
    image = np.random.randint(0, 256, size=(10, 10))

    # a) Normalize the image (scale values to 0-1 range)
    normalized = image / 255.0

    # b) Apply brightness adjustment (increase all values by 50, cap at 255)
    brightened = np.clip(image + 50, 0, 255)

    # c) Create a negative of the image (invert values)
    negative = 255 - image

    # d) Apply threshold (values > 128 become 255, others become 0)
    thresholded = np.where(image > 128, 255, 0)

    return normalized, brightened, negative, thresholded


# -----------------------------
# Self-test harness
# -----------------------------
if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)

    print("Problem 1 Results:")
    p1 = problem1()
    for item in p1:
        print(item)

    print("\nProblem 2 Results:")
    p2 = problem2()
    for item in p2:
        print(item)

    print("\nProblem 3 Results:")
    p3 = problem3()
    for item in p3:
        print(item)

    print("\nProblem 4 Results:")
    p4 = problem4()
    for item in p4:
        print(item)

    print("\nProblem 5 Results:")
    print(problem5())

    print("\nProblem 6 Results:")
    print(problem6())

    # Uncomment if attempting bonus
    # print("\nBonus Challenge Results:")
    # bonus = bonus_challenge()
    # for item in bonus:
    #     print(item)
