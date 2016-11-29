from lxml import html
import requests
import json
import re
import urllib
from movie import Movie
import glob
import sys
import datetime


def write_list_to_file(movies, movie_file_name):
    with open(movie_file_name, 'w') as output_file:
        for m in movies.values():
            print >> output_file, m._json

def main():

    movie_file_name = 'movies.json'

    # load the existing list
    movies = dict()

    n = sum([1 for line in open(movie_file_name, 'r')])

    with open(movie_file_name, 'r') as movie_file:
        for line_number, line in enumerate(movie_file):
            if line_number % 100 == 0:
                print 'Finished', line_number, 'of', n

            m = Movie.from_json(line)
            id = m.nflx_id

            if m.movie_type == 'movie':
                try:
                    query = 'http://www.omdbapi.com/?t=' + urllib.quote(m.title) + '&y=' + urllib.quote(m.year) + '&plot=short&r=json'
                    result = requests.get(query)
                    result = json.loads(result.content)
                    if result['Response'] == 'False':
                        genre = result.get('Error', 'ERROR - no error field found')
                    else:
                        genre = result.get('Genre', 'ERROR - no genre field found')
                except:
                    # something went wrong, probably with the api request - just skip it
                    print 'WARNING - something went wrong with the query:', m.title, m.year
                    genre = 'movie - unknown genre'
            else:
                genre = 'series - unknown genre'

            m.set_genre(genre)

            movies[id] = m

    write_list_to_file(movies, movie_file_name)



if __name__ == "__main__":
    main()