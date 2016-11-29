import json
import numpy
from collections import Counter

input_file_name = 'movies.json'
output_file_name = 'movies.stats.csv'

max_lines = None
stats = dict()
processed_movie_ids = set()

n = sum([1 for line in open(input_file_name, 'r')])

with open(input_file_name, 'r') as input_file:
    for line_number, line in enumerate(input_file):
        if max_lines is not None:
            if line_number > max_lines:
                break

        if line_number % 1000 == 0:
            print 'Finished ' + str(line_number) + ' of ' + str(n)

        movie = json.loads(line)

        id = movie['Netflix ID']
        assert id not in processed_movie_ids, 'ERROR - this movie is in the data twice: ' + id
        processed_movie_ids.add(id)

        for d in movie['dates observed']:
            stats.setdefault(d, {'type': list(), 'genre': list()})
            stats[d]['type'].append(movie['type'])
            stats[d]['genre'].append(movie['genre'])

m = 100
delimiter = '|'

with open(output_file_name, 'w') as output_file:
    header  = ['date', '# movies', '# series', 'total films'] + reduce(lambda x,y: x+ y, [['genre ' + str(i), '# genre ' + str(i)] for i in range(1,m+1)])
    print >>output_file, delimiter.join(header)
    for d, counts in sorted(stats.iteritems()):
        type_counter = Counter(counts['type'])
        print_data = [d, type_counter['movie'], type_counter['series'], sum(type_counter.values())]

        genre_counter = Counter(counts['genre'])
        for genre, count in genre_counter.most_common(m):
            print_data.extend([genre, count])

        print_data_is_short = True if len(print_data) < len(header) else False

        if print_data_is_short:
            print_data.append('')
            print_data_is_short = True if len(print_data) < len(header) else False

        print_data = map(lambda s: str(s), print_data)
        print >> output_file, delimiter.join(print_data)

