from lxml import html
import requests
import json
import re
import urllib
from movie import Movie
import glob
import sys
import datetime

def remove_all_punctuation(string):
    r_string = re.sub('\W+', '', string)

    return r_string


def strip_whitespace(string):
    r_string = string.strip()

    return r_string


def to_string(tree_element_list):
    return strip_whitespace(tree_element_list[0])


def to_href(tree_element_list):
    return tree_element_list[0].attrib['href']


def make_new_list(source, add_date, output_file_name):

    tree = html.parse(source)

    with open(output_file_name, 'w') as output_file:
        n = len(tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/b'))

        for i in range(1, n + 1):
            if i % 500 == 0:
                print 'Finished', i, 'of', n

            xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/b[' + str(i) + ']/text()')
            year = remove_all_punctuation(xp[0])
            # year = remove_all_punctuation(to_string(xp))

            xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/b[' + str(i) + ']/a')
            title = strip_whitespace(xp[0].text)
            nflx = xp[0].attrib['href']

            m = re.search('http://movies\.netflix\.com/WiMovie/(.*)/(\d+)\?trkid=(\d+)', nflx.strip())
            if m is not None:
                nflx_search, nflxid, trkid = m.groups()
            else:
                nflx_search, nflxid, trkid = None, None, None

            xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/i[' + str(i) + ']/a')
            imdb = xp[0].attrib['href']
            m = re.search('http://www\.imdb\.com/search/title\?title=(.*)', imdb.strip())
            if m is not None:
                imdb_search = m.groups()[0]
            else:
                imdb_search = None

            xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/i[' + str(i) + ']')
            rating_runtime = strip_whitespace(xp[0].text)

            try:
                rating, runtime = rating_runtime.split(',')
                runtime_val, runtime_unit = runtime.strip().split()[:2]
                runtime_val = int(runtime_val)
            except:
                print rating_runtime
                print rating
                print runtime
                print runtime_val
                print runtime_unit
                raise

            if runtime_unit.lower().strip() == 'minutes':
                # it's a movie, not a series
                item_type = 'movie'
            else:
                item_type = 'series'

            item = {'version': '0',
                    'type': item_type,
                    'date added': add_date,
                    'title': title,
                    'year': year,
                    'rating': rating,
                    'runtime': runtime_val,
                    'runtime unit': runtime_unit,
                    'Netflix ID': nflxid,
                    'IMDB title search': imdb_search}

            print >> output_file, json.dumps(item)


def add_movies_from_full_list(source, observe_date, movies, max_add=None):

    tree = html.parse(source)

    base_element = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]')[0]

    # xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/b')
    xp = base_element.xpath('b')
    n = len(xp)

    if n == 0:
        print 'WARNING - bad source:', source
        xp = tree.xpath('//*[@id="Blog1"]/div[1]/div[1]/div[1]/text()')
        if re.search('Sorry, the page you were looking for in this blog does not exist.', xp[0]) is not None:
            print 'WARNING - bad url:', xp[0].strip()
        return

    added = 0

    for i in range(1, n + 1):
        if max_add is not None:
            if added >= max_add:
                print 'added maximum number of movies to list'
                break

        if i % 500 == 0:
            print 'Finished', i, 'of', n

        # xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/b[' + str(i) + ']/a')
        xp = base_element.xpath('b[' + str(i) + ']/a')
        title = strip_whitespace(xp[0].text)
        nflx = xp[0].attrib['href']

        m = re.search('http://movies\.netflix\.com/WiMovie/(.*)/(\d+)\?trkid=(\d+)', nflx.strip())
        if m is not None:
            nflx_search, nflxid, trkid = m.groups()
        else:
            nflx_search, nflxid, trkid = None, None, None

        if nflxid not in movies:
            # new movie - get the rest of the details and add it
            added += 1

            #xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/b[' + str(i) + ']/text()')
            xp = base_element.xpath('b[' + str(i) + ']/text()')
            year = remove_all_punctuation(xp[0])

            # xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/i[' + str(i) + ']/a')
            xp = base_element.xpath('i[' + str(i) + ']/a')
            imdb = xp[0].attrib['href']
            m = re.search('http://www\.imdb\.com/search/title\?title=(.*)', imdb.strip())
            if m is not None:
                imdb_search = m.groups()[0]
            else:
                imdb_search = None

            #xp = tree.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]/i[' + str(i) + ']')
            xp = base_element.xpath('i[' + str(i) + ']')
            rating_runtime = strip_whitespace(xp[0].text)
            rating, runtime = rating_runtime.split(',')
            match = re.search('(\d+)\s+(\w+)\s*', runtime)
            if match is not None:
                runtime, runtime_unit = match.groups()
                runtime = int(runtime)
                runtime_unit = runtime_unit.lower().strip()
            else:
                runtime, runtime_unit = None, None

            if runtime_unit == 'minutes':
                # it's a movie, not a series
                item_type = 'movie'
            else:
                item_type = 'series'

            m = Movie(nflx_id=nflxid,
                      title=title,
                      year=year,
                      rating=rating,
                      runtime=runtime,
                      runtime_unit=runtime_unit,
                      imdb_search=imdb_search,
                      movie_type=item_type)

            m.add_observation(observe_date)

            movies[m.nflx_id] = m

        else:
            # we've seen this movie before, so  add onto the observed date list
            movies[nflxid].add_observation(observe_date)


def write_list_to_file(movies, movie_file_name):
    with open(movie_file_name, 'w') as output_file:
        for m in movies.values():
            print >> output_file, m._json


def main():

    movie_file_name = 'movies.json'

    # load the existing list
    movies = dict()

    with open(movie_file_name, 'r') as movie_file:
        for line in movie_file:
            m = Movie.from_json(line)
            id = m.nflx_id
            movies[id] = m

    # add new movies
    for file_name in glob.glob('data/*'):
        match = re.search('alpha_list_(.*)\.html', file_name)
        formatted_date = match.groups()[0]
        d = datetime.datetime.strptime(formatted_date, '%a_%b_%d_%Y')

        source   = file_name
        observe_date = d.strftime('%Y-%m-%d')
        max_add = None

        add_movies_from_full_list(source, observe_date, movies, max_add)

    write_list_to_file(movies, movie_file_name)

if __name__ == "__main__":
    main()