from __future__ import annotations


class Tag:
    def __init__(self, user_id: int, movie_id: int, tag: str, timestamp: int) -> None:
        self.userId = user_id
        self.movieId = movie_id
        self.tag = tag
        self.timestamp = timestamp
