from datetime import datetime as dt
from functools import reduce


def set_id():
    return (i for i in range(100000000))


def with_genres(n, movies):
    return list(filter(lambda x: len(x.genres) >= n, movies))


def popular(numero, movies):  # rating [2]
    return list(map(lambda x: x.title, list(filter(lambda x: x.rating > numero, movies))))


def tops_of_genre(genero, movies):
    tienen_genero = [movie for movie in movies if genero in movie.genres]
    tienen_genero.sort(reverse=True, key=lambda x: x.rating)
    return list(map(lambda x: x.title, tienen_genero[:10]))


def actor_rating(nombre, movies, cast):
    peliculas = [i.movie for i in cast if i.name == nombre]
    ratings = [movie.rating for movie in movies if movie.title in peliculas]
    return sum(ratings) / (len(ratings))


def compare_actors(nombre1, nombre2, movies, cast):
    if actor_rating(nombre1, movies, cast) > actor_rating(nombre2, movies, cast):
        print(nombre1)
    else:
        print(nombre1)


def movies_of(nombre, cast):
    actor = filter(lambda x: x.name == nombre, cast)
    return list(map(lambda x: (x.movie, x.name), actor))


def from_year(ano, movies):
    return list(map(lambda x: x.title, list(filter(lambda x: x.release.year == ano, movies))))


class Cast:

    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = []
        for arg in args:
            self.genres.append(arg)

if __name__ == "__main__":
    with open('movies.txt', 'r', encoding="utf-8") as f:
        movies = [Movie(*line.strip("\n").split(",")[1:])
                  for line in f]  # Se omite el primer valor que es el
        print(popular(8, movies))
        print(tops_of_genre("Action", movies))

    with open('cast.txt', 'r') as f:
        cast = [Cast(*line.strip("\n").split(",")) for line in f]
        print(actor_rating("Hugh Jackman", movies, cast))
        print(movies_of("Hugh Jackman", cast))
        print(from_year(2016, movies))
