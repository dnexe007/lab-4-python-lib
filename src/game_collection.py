from typing import Iterator
from src.game import game_type, Game


class GameCollection:
    """Collection for managing Game objects.

    Provides list-like interface with type validation for Game operations.
    """

    def __init__(self, lst: list[Game] | None = None) -> None:
        """Initialize collection with optional list of games.

        Args:
            lst: Optional initial list of Game objects.
        """
        self.games: list[Game] = lst if lst is not None else []

    def __getitem__(self, index: int) -> Game:
        """Return game at the specified index.

        Args:
            index: Position in collection.

        Returns:
            Game object at specified index.
        """
        return self.games[index]

    def __len__(self) -> int:
        """Return number of games in collection.

        Returns:
            Count of games in collection.
        """
        return len(self.games)

    def __iter__(self) -> Iterator[Game]:
        """Return iterator over games in collection.

        Returns:
            Iterator for Game objects in collection.
        """
        return iter(self.games)

    def __repr__(self) -> str:
        """Return string representation of the collection.

        Returns:
            String representation of GameCollection.
        """
        return f"GameCollection({self.games})"

    def clear(self) -> None:
        """Remove all games from the collection."""
        self.games.clear()

    @game_type
    def __contains__(self, game: Game) -> bool:
        """Check if game exists in collection.

        Args:
            game: Game object to search for.

        Returns:
            True if game found, False otherwise.
        """
        return game in self.games

    @game_type
    def add_game(self, game: Game) -> None:
        """Add a game to the collection.

        Args:
            game: Game object to add.
        """
        self.games.append(game)

    @game_type
    def remove_game(self, game: Game) -> None:
        """Remove a game from the collection.

        Args:
            game: Game object to remove.

        Raises:
            ValueError: If game is not in collection.
        """
        if game not in self.games:
            raise ValueError("Game is not in collection")
        self.games.remove(game)

    @game_type
    def index(self, game: Game) -> int:
        """Return index of game in collection.

        Args:
            game: Game object to find.

        Returns:
            Index position of game in collection.
        """
        return self.games.index(game)
