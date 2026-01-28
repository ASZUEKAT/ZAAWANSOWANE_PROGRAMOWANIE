from __future__ import annotations


class Rating:
    def __init__(
        self,
        user_id: int,
        movie_id: int,
        rating: float,
        timestamp: int,
    ) -> None:
        self.userId = user_id
        self.movieId = movie_id
        self.rating = rating
        self.timestamp = timestamp
