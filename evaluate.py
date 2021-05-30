import os
import time
from queue import Queue
from threading import Thread

import concurrent.futures

import pandas as pd
import numpy as np

from requests import *

##############################################################################

#TODO:
#       remove non-films from consideration (episodes, shorts etc.)
#       include main cast member(s) in consideration
#       develop final rating estimate formula:
#           - roles have different weight towards final rating
#	          affected by number of films for each person? (consistency?)
#           - consider genre?
#           - determine measurement uncertainty?

##############################################################################

if not os.path.exists('./data'):
    os.makedirs('./data')
if os.path.isfile('./data/name_data.tsv'):
    update = input('Database detected,download latest version? y/n: ')
    if update == 'y':
       retrieve_db()
else:
    retrieve_db()

##############################################################################

names = []
scores = []

names.append(input('Director: '))
director_nconst = ''

names.append(input('Writer: '))
writer_nconst = ''

def search(name):
    for row in name_db.itertuples(index=False):
        if row[1] == name:
            nconst = row[0]
            break
    films = []
    for row in crew_db.itertuples(index=False):
        if nconst in row[1]:
            films.append(row[0])
    sum = 0
    num_films = len(films)
    for row in rating_db.itertuples(index=False):
        if row[0] in films:
            sum += row[1]
            films.remove(row[0])

    return sum / num_films

initial_time = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
    name_db = pd.read_csv('./data/name_data.tsv', delimiter='\t', usecols=[0, 1])
    crew_db = pd.read_csv('./data/crew_data.tsv', delimiter='\t', usecols=[0, 1])
    rating_db = pd.read_csv('./data/rating_data.tsv', delimiter='\t', usecols=[0, 1])
    futures = [executor.submit(search, name) for name in names]

    completion_time = time.perf_counter()

    for future in futures:
        scores.append(future.result())


print(f'Returned in: {completion_time - initial_time:.2f} seconds.')
print(f'{names[0]} Director Score:  {(scores[0]):.2f}')
print(f'{names[1]} Writer Score: {(scores[1]):.2f}')

##############################################################################
