from typing import Any, Callable


class Game:
    def __init__(self, title: str, developer: str, release_year: int, genre: str, game_id: str) -> None:
        self.title = title
        self.developer = developer
        self.release_year = release_year
        self.genre = genre
        self.game_id = game_id

    def __repr__(self) -> str:
        return f"{self.title} ({self.developer}, {self.release_year}, {self.genre})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Game):
            return False
        matches = [
            self.title == other.title,
            self.developer == other.developer,
            self.release_year == other.release_year,
            self.genre == other.genre,
            self.game_id == other.game_id
        ]
        return all(matches)

    def __hash__(self) -> int:
        return hash(self.game_id)


def game_type(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if len(args) > 1 and not isinstance(args[1], Game):
            raise TypeError('Game must be of type Game')
        return func(*args, **kwargs)
    return wrapper
