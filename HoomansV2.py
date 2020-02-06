import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import names
import random
import time
import copy
import threading

professions = ['Farmer', 'None', 'None', 'None', 'None']
food_history = []
seconds = []
current_second = 0
population_history = []
starting_food = 10
food = 20
max_homo_chance = 150
max_age = 100
min_reproduction_age = 18
initial_men = 10
initial_female = 10
population = pd.DataFrame(
    columns=[
    'First Name', 
    'Last Name',
    'Gender',
    'Age',
    'Hunger',
    'Virgin',
    'Homo',
    'Profession'
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

def random_profession():
    ''' Chooses random profession from global list '''
    return random.choice(professions)

def create_hooman(gender, lastname=''):
    ''' Initiates human attributes, returns as list '''
    attributes = []
 
    if lastname == '':
        first_name, last_name = get_name(gender)
    else:
        first_name = get_first_name(gender)
        last_name = lastname
    age = random.randint(1,5)
    hunger = starting_food
    virgin = True
    homo = False
    profession = random_profession()

    attributes.append(first_name)
    attributes.append(last_name)
    attributes.append(gender)
    attributes.append(age)
    attributes.append(hunger)
    attributes.append(virgin)
    attributes.append(homo)
    attributes.append(profession)

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

    child_attributes = [create_hooman(random_gender(), lastname=last_name)]
    child = pd.DataFrame(child_attributes, columns=['First Name', 'Last Name', 'Gender', 'Age', 'Hunger', 'Virgin', 'Homo', 'Profession'])
    population = population.append(child, ignore_index=True)

def agify(df):
    ''' For each human row, increases age by one year '''
    for index, row in df.iterrows():
        df.at[index, 'Age'] = df.at[index, 'Age'] + 1

def reproduce(df):
    ''' For each male human, 1/6 chance of trying to reproduce '''
    for index, row in df.iterrows():
        if random.randint(0, 6) == 0:
            # Gather my information
            first_name = df.at[index, 'First Name']
            last_name = df.at[index, 'Last Name']
            age = df.at[index, 'Age']
            gender = df.at[index, 'Gender']
            homo = df.at[index, 'Homo']
            hunger = df.at[index, 'Hunger']
            profession = df.at[index, 'Profession']

            if age >= min_reproduction_age and gender == 'male' and homo == False and hunger >= 2:
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

def check_death_age(df):
    ''' Checks each row/human for an age above 50 then kills '''
    indexNames = df[ df['Age'] == max_age ].index
    for index in indexNames:
        print(f"{df.at[index, 'First Name']} {df.at[index, 'Last Name']} died at age {df.at[index, 'Age']}!")
    df = df.drop(indexNames, inplace=True)

def check_death_food(df):
    ''' Checks each row/human for food <= 0 then kills '''
    indexNames = df[ df['Hunger'] <= 0 ].index
    for index in indexNames:
        print(f"{df.at[index, 'First Name']} {df.at[index, 'Last Name']} died at age {df.at[index, 'Age']}!")
    df = df.drop(indexNames, inplace=True)

def check_death(df):
    ''' runs all death checks '''
    check_death_age(df)
    check_death_food(df)

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

def graph_population_history(i):
    global current_second
    global population
    global food_history
    global food
    #time.sleep(1)
    current_second += 1
    seconds.append(current_second)

    food_history.append(food)

    population_history.append(population.count(axis=0))
    plt.xlabel('Time (Seconds)')
    plt.ylabel('# People/Food')
    plt.plot(seconds, population_history, color='skyblue', label='Population' if i == 0 else "")
    plt.plot(seconds, food_history, color='chartreuse', label='Food' if i == 0 else "")
    plt.legend()

def animate_population_graph():
    fig = plt.figure()
    ani = FuncAnimation(fig, graph_population_history, interval=1000)
    plt.tight_layout()
    plt.show()

def basic_energy(df):
    ''' Simulates basic caloric usage by living. '''
    for index, row in df.iterrows():
        df.at[index, 'Hunger'] -= 1

def eat(df):
    ''' simulates eating food to restore hunger. '''
    global food
    for index, row in df.iterrows():
        if food >= 2 and df.at[index, 'Hunger'] < 2:
            food -= 2
            df.at[index, 'Hunger'] += 2

def food_restoration():
    ''' simulates magical food gain to central store '''
    global food
    food += random.randint(5, 10)

def survive(df):
    ''' Handles all energy '''
    food_restoration()
    basic_energy(df)
    eat(df)

def work_farmer(index, df):
    ''' Farmer work '''
    ''' Farmers produce 1 - 5 food per year'''
    global food
    food += random.randint(2, 5)

def work_profession(df):
    ''' All profession work '''
    for index, row in df.iterrows():
        if df.at[index, 'Age'] >= 18:
            if df.at[index, 'Profession'] == 'Farmer':
                work_farmer(index, df)


def simulate_year(df):
    ''' Simulate one year of life '''
    #df = df.reset_index(drop=True)
    #df.reset_index(drop=True, inplace=True)
    survive(df)
    check_death(df)
    agify(df)
    reproduce(df)
    homo_conversion(df)
    work_profession(df)

    #graph_homo(df)
    #graph_family(df)
    #graph_gender(df)
    #graph_age(df)
    print(population)
    print(f"Population: {len(df)}")
    print(f"Food: {food}")

def main():
    ''' Initialize humans + simulate years '''
    global population
    initialize_population()
    print(population)
    graphing_thread = threading.Thread(target = animate_population_graph)
    graphing_thread.start()
    time.sleep(5)

    while population.empty == False:
        simulate_year(population)
        #time.sleep(0.5)
    

main()