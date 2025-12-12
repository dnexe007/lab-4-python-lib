from typing import Any, Callable


class Game:
    """Represents a video game with metadata.

    Attributes:
        title: Name of the game.
        developer: Game's developer/publisher.
        release_year: Year the game was released.
        genre: Game's primary genre.
        game_id: Unique identifier for the game.
    """

    def __init__(self, title: str, developer: str, release_year: int, genre: str, game_id: str) -> None:
        """Initialize a Game instance.

        Args:
            title: Name of the game.
            developer: Game's developer/publisher.
            release_year: Year the game was released.
            genre: Game's primary genre.
            game_id: Unique identifier for the game.
        """
        self.title = title
        self.developer = developer
        self.release_year = release_year
        self.genre = genre
        self.game_id = game_id

    def __repr__(self) -> str:
        """Return string representation of the game."""
        return f"{self.title} ({self.developer}, {self.release_year}, {self.genre})"

    def __eq__(self, other: Any) -> bool:
        """Check equality based on all game attributes.

        Args:
            other: Object to compare with.

        Returns:
            True if all attributes match, False otherwise.
        """
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
        """Return hash based on game_id for use in collections.

        Returns:
            Hash value of game_id.
        """
        return hash(self.game_id)


def game_type(func: Callable) -> Callable:
    """Decorator to ensure second argument is a Game instance."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper function that validates argument type.

        Args:
            *args: Positional arguments passed to decorated function.
            **kwargs: Keyword arguments passed to decorated function.

        Returns:
            Result of decorated function.

        Raises:
            TypeError: If second argument is not a Game instance.
        """
        if len(args) > 1 and not isinstance(args[1], Game):
            raise TypeError('Game must be of type Game')
        return func(*args, **kwargs)

    return wrapper
