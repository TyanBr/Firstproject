import numpy as np
import pandas as pd 
import os as os 
from fuzzywuzzy import fuzz

df = pd.read_csv('Shortage dataset.csv')
checker = df['Special Condition']
checker.fillna("No special conditions attached", inplace = True)
job_List = df['Job types included on the shortage occupations list']



def search(user_Job):
    answer = user_Job
    answer = answer.lower()
    answer = answer.strip()
    score = 0
    best_score = 0
    jobs_title = []
    closest_matching = []
    index = 0 
    closest_index = 0
    for x in job_List:
        score = fuzz.ratio(answer , x)
        jobs_title = [x]
        index = index + 1
        if score > best_score:
            best_score = score
            closest_matching = jobs_title
            closest_index = index
    if (best_score >= 80):
        print("Yes it seems your job is available for sponsorship on a shortage basis")
        #Check to see if there is a special condition if so print it out
        if not checker.iloc[closest_index] == "No special conditions attached":
            print(checker.iloc[closest_index])
    elif (best_score > 50 and best_score < 80):
        print("Did you mean   ", closest_matching)
    else: print("It seems this job does not support a shortage visa")
    return answer, best_score , closest_matching 
            
search('chemistryzad')