from __future__ import annotations


class Movie:
    def __init__(self, movie_id: int, title: str, genres: str) -> None:
        self.movieId = movie_id
        self.title = title
        self.genres = genres
