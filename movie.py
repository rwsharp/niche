import json

class Movie:

    def __init__(self, nflx_id=None, title=None, year=None, rating=None, runtime=None, runtime_unit=None, genre=None,
                 imdb_search=None, movie_type=None, add_date=None, observe_date=None):

        self.version = '0'
        self.movie_type = movie_type
        self.nflx_id = nflx_id
        self.dates_observed = [observe_date] if observe_date is not None else list()
        self.add_date = add_date
        self.title = title
        self.year = year
        self.rating = rating
        self.runtime = runtime
        self.runtime_unit = runtime_unit
        self.imdb_search = imdb_search
        self.genre = genre
        self._dict = self.v0_to_dict()
        self._json = json.dumps(self._dict)


    @classmethod
    def from_dict(cls, movie_dict):
        assert movie_dict.get('version', '0') == '0', 'ERROR - wrong version'

        m = cls(nflx_id=movie_dict.get('Netflix ID'),
                title=movie_dict.get('title'),
                year=movie_dict.get('year'),
                rating=movie_dict.get('rating'),
                genre=movie_dict.get('genre'),
                runtime=movie_dict.get('runtime'),
                runtime_unit=movie_dict.get('runtime unit'),
                imdb_search=movie_dict.get('IMDB title search'),
                movie_type=movie_dict.get('type'),
                add_date=movie_dict.get('date added'))

        for d in movie_dict.get('dates observed', list()):
            m.add_observation(d)

        return m


    @classmethod
    def from_json(cls, json_string):
        movie_dict = json.loads(json_string)
        return cls.from_dict(movie_dict)


    def v0_to_dict(self):

        assert self.version == '0', 'ERROR - not a v0 object'

        movie = {'version': self.version,
                'type': self.movie_type,
                'date added': self.add_date,
                'dates observed': self.dates_observed,
                'title': self.title,
                'year': self.year,
                'rating': self.rating,
                'genre': self.genre,
                'runtime': self.runtime,
                'runtime unit': self.runtime_unit,
                'Netflix ID': self.nflx_id,
                'IMDB title search': self.imdb_search}

        return movie


    def add_observation(self, observe_date):
        self.dates_observed.append(observe_date)
        self._json = json.dumps(self._dict)

    def set_genre(self, genre):
        self.genre = genre
        self._dict['genre'] = genre
        self._json = json.dumps(self._dict)
