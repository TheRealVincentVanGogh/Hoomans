import pandas as pd
import names
import random
import time
import copy

min_reproduction_age = 18
initial_men = 5
initial_female = 5
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
    attributes = []

    first_name, last_name = get_name(gender)
    age = 0
    virgin = True

    attributes.append(first_name)
    attributes.append(last_name)
    attributes.append(gender)
    attributes.append(age)
    attributes.append(virgin)

    return attributes


def initialize_population():
    global population
    for men in range(0, initial_men):
        hooman_attributes = create_hooman('male')
        #print(hooman_attributes)
        population.loc[len(population), :] = hooman_attributes

    for female in range(0, initial_female):
        hooman_attributes = create_hooman('female')
        #print(hooman_attributes)
        population.loc[len(population), :] = hooman_attributes

def agify(df):
    for index, row in df.iterrows():
        df.at[index, 'Age'] = df.at[index, 'Age'] + 1

def reproduce(df):
    for index, row in df.iterrows():
        first_name = df.at[index, 'First Name']
        last_name = df.at[index, 'Last Name']
        age = df.at[index, 'Age']
        gender = df.at[index, 'Gender']

        if age >= min_reproduction_age and gender == 'male':
            female_pop = df.loc[df['Gender'] == 'female']
            mate = female_pop.sample()
            mate = mate.reset_index(drop=True)
            print(mate)
            mate_first_name = mate.at[0, 'First Name']
            mate_last_name = mate.at[0, 'Last Name']
            print(f"{first_name} {last_name} did the deed with {mate_first_name} {mate_last_name}")


def simulate_year(df):
    agify(df)
    reproduce(df)
    print(population)

def main():
    global population
    initialize_population()
    print(population)

    while True:
        simulate_year(population)
        #time.sleep(1)
    

main()