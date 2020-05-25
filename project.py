"""
File: project.py
-------------------------
This program uses statistical analysis to recommend IBS BFSU elective courses for the user based on their interests;
reads in the answers from the user, and then uses Pearson's R value to calculate the correlation of different courses
based on the data previously collected; ends with when the user has got the recommendations.
"""

import pandas as pd
import numpy as np
from simpleimage import SimpleImage
from colorama import init
from termcolor import colored
init(autoreset=True)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
HUM_COURSES = 'Humanistic Courses.csv'
HUM_COURSES_RATINGS = 'Humanistic Courses Ratings.csv'
SPE_COURSES = 'Specialization Courses.csv'
SPE_COURSES_RATINGS = 'Specialization Courses Ratings.csv'
CORE_COURSES_PIC = 'Core Courses.png'
CURR_UNDERGRAD_PIC = 'Curriculum for Undergraduates.png'

def greet_user():
    print(colored("\nWelcome to the Elective Course recommendation system for IBS BFSU.", 'red', attrs=['bold']))
    print(colored("This program uses statistical analysis to provide you with accurate suggestions for choosing your elective courses.", 'cyan', attrs=['bold']))
    choice = first_step()
    return choice

def first_step():
    ans = 0
    while ans != '3':
        ans = input(str("\nEnter 1 to view Undergrad Curriculum \nEnter 2 to view Core Courses \n"
                    "Enter 3 to proceed with the recommendations \nEnter value here: "))
        if ans == '1' or '2':
            show_pic(ans)
        if ans == '3':
            break
    choice = hum_or_spe()
    return choice

def show_pic(ans):
    if ans == '1':
        image = SimpleImage(CURR_UNDERGRAD_PIC)
        image.show()
    if ans == '2':
        image = SimpleImage(CORE_COURSES_PIC)
        image.show()

def hum_or_spe():
    print(colored("\nLet's begin!", 'cyan', attrs=['bold']))
    while True:
        ans = input("\nEnter 0 to go back to the start \nEnter 1 for Humanistic Courses \n"
                "Enter 2 for Specialized Courses \nEnter value here: ")
        if ans == '1' or ans == '2' or ans == '0':
            break
    return ans

def rec_hum_courses():
    print(colored("\nLet's start with your interests", 'cyan', attrs=['bold']))
    while True:
        ans = input("\nEnter 1 if you like Humanities \nEnter 2 if you like Social Sciences \nEnter value here: ")
        if ans == '1' or ans == '2':
            break
    if ans == '1':
        recs = rec_system(HUM_COURSES, HUM_COURSES_RATINGS, 'Chinese Contemporary and modern literature', 4)
    if ans == '2':
        recs = rec_system(HUM_COURSES, HUM_COURSES_RATINGS, 'Public Communication and Critical Thinking', 4)
    return recs

def rec_spe_courses():
    print(colored("\nLet's start with your interests", 'cyan', attrs=['bold']))
    while True:
        ans = input("\nEnter 1 if you like Accounting \nEnter 2 if you like Finance \nEnter 3 if you like Marketing \n"
                "Enter 4 if you like Management \nEnter 5 if you like General Business \nEnter value here: ")
        if ans == '1' or ans == '2' or ans == '3' or ans == '4' or ans == '5' or ans == '0':
            break
    if ans == '1':
        recs = rec_system(SPE_COURSES, SPE_COURSES_RATINGS, 'International Investment Analysis', 7)
    if ans == '2':
        recs = rec_system(SPE_COURSES, SPE_COURSES_RATINGS, 'International Finance', 7)
    if ans == '3':
        recs = rec_system(SPE_COURSES, SPE_COURSES_RATINGS, 'Consumer Behavior', 7)
    if ans == '4':
        recs = rec_system(SPE_COURSES, SPE_COURSES_RATINGS, 'Brand Management', 7)
    if ans == '5':
        recs = rec_system(SPE_COURSES, SPE_COURSES_RATINGS, 'International Business', 7)
    return recs

def rec_system(courses, rating, subject, num_recs):
    courses = pd.read_csv(courses)
    ratings = pd.read_csv(rating)
    mat_stud_courses = ratings.pivot_table(index=['studentID'], columns=['course'], values='rating')
    #print(mat_stud_courses)
    #print(pearsons_correlation_coefficient(mat_stud_courses['China on the Screen'], mat_stud_courses['The Chinese Economy ']))
    recs = get_recs(subject, mat_stud_courses, num_recs)
    return recs

def pearsons_correlation_coefficient(pri_course, sec_course):
    pri_course_cor = pri_course - pri_course.mean()
    sec_course_cor = sec_course - sec_course.mean()
    stand_dev_pri_sec_course = np.sqrt(np.sum(pri_course_cor ** 2) * np.sum(sec_course_cor ** 2))
    r = np.sum(pri_course_cor * sec_course_cor) / stand_dev_pri_sec_course
    return r

def get_recs(course_name, matrix, num):
    reviews = []
    for title in matrix.columns:
        #if title == course_name:
            #continue
        cor = pearsons_correlation_coefficient(matrix[course_name], matrix[title])
        if np.isnan(cor):
            continue
        else:
            reviews.append((title, cor))
    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:num]

def main():
    """
    This program uses statistical analysis to recommend IBS BFSU elective courses
    for the user based on their interests; reads in the answers from the user, and then uses
    Pearson's R value to measure the linear correlation between two variables X and Y,
    based on the data previously collected; ends with when the user has got the recommendations.
    """
    choice = greet_user()
    while choice == '0':
        choice = first_step()
    if choice == '1':
        recs = rec_hum_courses()
        print(colored("\nHere are your recommendations for choosing Humanistic Courses "
                      "with the respective correlation values: \n", 'cyan', attrs=['bold']))
    if choice == '2':
        recs = rec_spe_courses()
        print(colored("\nHere are your recommendations for choosing Specialized Courses "
                      "with the respective correlation values: \n", 'cyan', attrs=['bold']))
    for courses in recs:
        print(courses)
    print(colored("\nNote: \nIf the value is near +1, then the course is STRONGLY recommended. "
                  "\nIf the value is near 0, the course is MODERATELY recommended. "
                  "\nIf the value is near -1, then the course is NOT recommended", 'red', attrs=['bold']))
    print(colored("\nThank you for using this program.", 'cyan', attrs=['bold']))

if __name__ == '__main__':
    main()