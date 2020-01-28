import pandas as pd
import matplotlib.pyplot as plt
import names
import random
import time
import copy

max_homo_chance = 50
max_age = 50
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
    'Homo'
    ]
    )

def random_gender():
    isMale = bool(random.getrandbits(1))
    if isMale == True:
        return 'male'
    elif isMale == False:
        return 'female'

def get_name(gender):
    ''' Generates a full name split into first + last, array format '''
    return names.get_full_name(gender=gender).split(" ", 1)

def get_first_name(my_gender):
    ''' Generates exclusively a first name based on gender '''
    return names.get_first_name(gender=my_gender)

def create_hooman(gender, lastname=''):
    ''' Initiates human attributes, returns as list '''
    attributes = []
 
    if lastname == '':
        first_name, last_name = get_name(gender)
    else:
        first_name = get_first_name(gender)
        last_name = lastname
    age = random.randint(1,10)
    virgin = True
    homo = False

    attributes.append(first_name)
    attributes.append(last_name)
    attributes.append(gender)
    attributes.append(age)
    attributes.append(virgin)
    attributes.append(homo)

    return attributes


def initialize_population():
    ''' Initializes a human for each amount specified '''
    global population
    for men in range(0, initial_men):
        hooman_attributes = create_hooman('male')
        #print(hooman_attributes)
        population.loc[len(population), :] = hooman_attributes

    for female in range(0, initial_female):
        hooman_attributes = create_hooman('female')
        #print(hooman_attributes)
        population.loc[len(population), :] = hooman_attributes

def initialize_child(last_name):
    ''' Initialize a human child inheriting a lastname.'''
    ''' Adds child to population table '''
    global population

    child_attributes = create_hooman(random_gender(), lastname=last_name)
    population.loc[len(population), :] = child_attributes

def agify(df):
    ''' For each human row, increases age by one year '''
    for index, row in df.iterrows():
        df.at[index, 'Age'] = df.at[index, 'Age'] + 1

def reproduce(df):
    ''' For each male human, 1/6 chance of trying to reproduce '''
    for index, row in df.iterrows():
        if random.randint(0, 5) == 0:
            # Gather my information
            first_name = df.at[index, 'First Name']
            last_name = df.at[index, 'Last Name']
            age = df.at[index, 'Age']
            gender = df.at[index, 'Gender']
            homo = df.at[index, 'Homo']

            if age >= min_reproduction_age and gender == 'male' and homo == False:
                # Filter population by female
                female_pop = df.loc[df['Gender'] == 'female']
                # Choose random human from female_pop
                mate = female_pop.sample()

                # Update virginity as appropriate
                df.at[mate.index, 'Virgin'] = False
                df.at[index, 'Virgin'] = False

                mate = mate.reset_index(drop=True)

                # Gather mate's first name and last name
                mate_first_name = mate.at[0, 'First Name']
                mate_last_name = mate.at[0, 'Last Name']
                print(f"{first_name} {last_name} did the deed with {mate_first_name} {mate_last_name}")
                initialize_child(last_name)

def check_death(df):
    for index, row in df.iterrows():
        try:
            if df.at[index, 'Age'] >= max_age:
                print(f"{df.at[index, 'First Name']} {df.at[index, 'Last Name']} died at age {df.at[index, 'Age']}!")
                df = df.drop(index, inplace=True)
        except:
            pass

def homo_conversion(df):
    for index, row in df.iterrows():
        if random.randint(0, max_homo_chance) == 0:
            # Convert hooman to homo.
            if df.at[index, 'Homo'] == False:
                df.at[index, 'Homo'] = True

def graph_homo(df):
    labels = ['No Homo', 'Homo']
    sizes = [len(df["Homo"]) - sum(df["Homo"]), sum(df["Homo"])]
    colors = ['yellowgreen', 'lightskyblue']
    patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.pause(.001)
    plt.draw()

def graph_family(df):
    #df['Last Name'].value_counts().plot.bar()
    #df.groupby('Homo').size().plot.bar()
    #df['Homo'].hist()
    pd.value_counts(df['Last Name']).plot.bar()

def graph_gender(df):
    df.groupby('Gender').Age.hist()

def graph_age(df):
    df.groupby('Age').Age.hist()

def simulate_year(df):
    ''' Simulate one year of life '''
    #df = df.reset_index(drop=True)
    #df.reset_index(drop=True, inplace=True)
    check_death(df)
    agify(df)
    reproduce(df)
    homo_conversion(df)
    #graph_homo(df)
    #graph_family(df)
    #graph_gender(df)
    #graph_age(df)
    #print(population)

def main():
    ''' Initialize humans + simulate years '''
    global population
    initialize_population()
    print(population)

    while population.empty == False:
        simulate_year(population)
        #time.sleep(0.2)
    

main()