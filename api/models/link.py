from __future__ import annotations


class Link:
    def __init__(self, movie_id: int, imdb_id: str, tmdb_id: str) -> None:
        self.movieId = movie_id
        self.imdbId = imdb_id
        self.tmdbId = tmdb_id
