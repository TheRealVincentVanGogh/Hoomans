import pandas as pd
import names
import random
import time
import copy

initial_men = 2
initial_female = 2
population = pd.DataFrame(
    columns=[
    'First Name', 
    'Last Name',
    'Gender',
    'Age',
    'Virgin',
    ]
    )

def get_name(gender):
    return names.get_full_name(gender=gender).split(" ", 1)

def create_hooman(gender):
    first_name, last_name = get_name(gender)


def initialize_population():
    for men in range(0, initial_men):
        create_hooman('male')
    for female in range(0, initial_female):
        create_hooman('female')

def main():
    

main()