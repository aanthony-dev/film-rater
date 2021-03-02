import os
import urllib.request
import gzip
import shutil

def retrieve_db():
    print('Downloading Databases From IMDB ... \n')

    name_data_url = 'https://datasets.imdbws.com/name.basics.tsv.gz'
    crew_data_url = 'https://datasets.imdbws.com/title.crew.tsv.gz'
    rating_data_url = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
    title_data_url = 'https://datasets.imdbws.com/title.basics.tsv.gz'

    urllib.request.urlretrieve(name_data_url, './data/name_data.tsv.gz')
    urllib.request.urlretrieve(crew_data_url, './data/crew_data.tsv.gz')
    urllib.request.urlretrieve(rating_data_url, './data/rating_data.tsv.gz')
    urllib.request.urlretrieve(title_data_url, './data/title_data.tsv.gz')

    with gzip.open('./data/name_data.tsv.gz', 'rb') as f_in:
        with open('./data/name_data.tsv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    with gzip.open('./data/crew_data.tsv.gz', 'rb') as f_in:
        with open('./data/crew_data.tsv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    with gzip.open('./data/rating_data.tsv.gz', 'rb') as f_in:
        with open('./data/rating_data.tsv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    with gzip.open('./data/title_data.tsv.gz', 'rb') as f_in:
        with open('./data/title_data.tsv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove('./data/name_data.tsv.gz')
    os.remove('./data/crew_data.tsv.gz')
    os.remove('./data/rating_data.tsv.gz')
    os.remove('./data/title_data.tsv.gz')
    
    print('Latest database downloaded.')
