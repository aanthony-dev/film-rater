import os
import time
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

director_name = input('Director: ')
director_nconst = ''

writer_name = input('Writer: ')
writer_nconst = ''

##############################################################################

print('Searching Name Database ... \n')
initial_time = time.perf_counter()
db = pd.read_csv('./data/name_data.tsv', delimiter='\t')

for row in db.itertuples(index=False):
    if row[1] == director_name and director_nconst == '':
        director_nconst = row[0]
    if row[1] == writer_name and writer_nconst == '':
        writer_nconst = row[0]
    if director_nconst != '' and writer_nconst != '':
        break
        
completion_time = time.perf_counter()
print(f'Returned in: {completion_time - initial_time:.2f} seconds.')
print(director_name, director_nconst)
print(writer_name, writer_nconst)
input('Press Enter to Continue ...')

##############################################################################

director_films = []
writer_films = []

print('Searching Crew Database ... \n')
initial_time = time.perf_counter()
db = pd.read_csv('./data/crew_data.tsv', delimiter='\t')

for row in db.itertuples(index=False):
    if director_nconst in row[1]:
        director_films.append(row[0])
    if writer_nconst in row[2]:
        writer_films.append(row[0])

completion_time = time.perf_counter()
print(f'Returned in: {completion_time - initial_time:.2f} seconds.')
print('Director Films:', len(director_films))
print('Writer Films:', len(writer_films))
input('Press Enter to Continue ...')

##############################################################################

director_sum = 0
writer_sum = 0
dtr_film_length = len(director_films)
wtr_film_length = len(writer_films)

print('Searching Rating Database ... \n')
initial_time = time.perf_counter()
db = pd.read_csv('./data/rating_data.tsv', delimiter='\t')

for row in db.itertuples(index=False):
    if row[0] in director_films:
        director_sum += row[1]
        director_films.remove(row[0])
    if row[0] in writer_films:
        writer_sum += row[1]
        writer_films.remove(row[0])

completion_time = time.perf_counter()
print(f'Returned in: {completion_time - initial_time:.2f} seconds.')
print(f'{director_name} Director Score:  {(director_sum / dtr_film_length):.2f}')
print(f'{writer_name} Writer Score: {(writer_sum / wtr_film_length):.2f}')
input('Press Enter to Continue ...')
