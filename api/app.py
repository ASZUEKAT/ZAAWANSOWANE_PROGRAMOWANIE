from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Optional

from flask import Flask, request
from flask_restful import Api, Resource

from models.link import Link
from models.movie import Movie
from models.rating import Rating
from models.tag import Tag

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

MOVIES_CACHE: Optional[list[Movie]] = None
LINKS_CACHE: Optional[list[Link]] = None
RATINGS_CACHE: Optional[list[Rating]] = None
TAGS_CACHE: Optional[list[Tag]] = None


def _apply_limit(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Optional query param: ?limit=100."""
    raw = request.args.get("limit")
    if raw is None:
        return items

    try:
        limit = int(raw)
    except ValueError:
        return items

    if limit < 0:
        return []

    return items[:limit]


def load_movies() -> list[Movie]:
    global MOVIES_CACHE
    if MOVIES_CACHE is not None:
        return MOVIES_CACHE

    path = DATA_DIR / "movies.csv"
    movies: list[Movie] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append(
                Movie(
                    movie_id=int(row["movieId"]),
                    title=row["title"],
                    genres=row["genres"],
                )
            )

    MOVIES_CACHE = movies
    return movies


def load_links() -> list[Link]:
    global LINKS_CACHE
    if LINKS_CACHE is not None:
        return LINKS_CACHE

    path = DATA_DIR / "links.csv"
    links: list[Link] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            links.append(
                Link(
                    movie_id=int(row["movieId"]),
                    imdb_id=row.get("imdbId", ""),
                    tmdb_id=row.get("tmdbId", ""),
                )
            )

    LINKS_CACHE = links
    return links


def load_ratings() -> list[Rating]:
    global RATINGS_CACHE
    if RATINGS_CACHE is not None:
        return RATINGS_CACHE

    path = DATA_DIR / "ratings.csv"
    ratings: list[Rating] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ratings.append(
                Rating(
                    user_id=int(row["userId"]),
                    movie_id=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"]),
                )
            )

    RATINGS_CACHE = ratings
    return ratings


def load_tags() -> list[Tag]:
    global TAGS_CACHE
    if TAGS_CACHE is not None:
        return TAGS_CACHE

    path = DATA_DIR / "tags.csv"
    tags: list[Tag] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags.append(
                Tag(
                    user_id=int(row["userId"]),
                    movie_id=int(row["movieId"]),
                    tag=row["tag"],
                    timestamp=int(row["timestamp"]),
                )
            )

    TAGS_CACHE = tags
    return tags


app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self) -> dict[str, str]:
        return {"hello": "world"}


class Movies(Resource):
    def get(self) -> list[dict[str, Any]]:
        movies = load_movies()
        data = [m.__dict__ for m in movies]
        return _apply_limit(data)


class Links(Resource):
    def get(self) -> list[dict[str, Any]]:
        links = load_links()
        data = [l.__dict__ for l in links]
        return _apply_limit(data)


class Ratings(Resource):
    def get(self) -> list[dict[str, Any]]:
        ratings = load_ratings()
        data = [r.__dict__ for r in ratings]
        return _apply_limit(data)


class Tags(Resource):
    def get(self) -> list[dict[str, Any]]:
        tags = load_tags()
        data = [t.__dict__ for t in tags]
        return _apply_limit(data)


api.add_resource(Hello, "/hello")
api.add_resource(Movies, "/movies")
api.add_resource(Links, "/links")
api.add_resource(Ratings, "/ratings")
api.add_resource(Tags, "/tags")


if __name__ == "__main__":
    app.run(debug=True)
