from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Generic
from typing import Iterator
from typing import TypeVar

from src.game import Game
from src.game import game_type
from src.game_collection import GameCollection

K = TypeVar("K", str, int)


class GameDict(ABC, Generic[K]):
    """Abstract base class for dictionary-like collections of games.

    Organizes games by a key (either string or integer) into GameCollection instances.
    """

    def __init__(self) -> None:
        """Initialize an empty game dictionary."""
        self.dct: Dict[K, GameCollection] = {}

    def __getitem__(self, key: K) -> GameCollection:
        """Return game collection associated with the key.

        Args:
            key: Key to look up in dictionary.

        Returns:
            GameCollection for the specified key.
        """
        return self.dct[key]

    def __contains__(self, key: K) -> bool:
        """Check if key exists in dictionary.

        Args:
            key: Key to check for existence.

        Returns:
            True if key exists, False otherwise.
        """
        return key in self.dct

    def __len__(self) -> int:
        """Return number of keys in dictionary.

        Returns:
            Count of distinct keys in dictionary.
        """
        return len(self.dct)

    def __iter__(self) -> Iterator[K]:
        """Return iterator over dictionary keys.

        Returns:
            Iterator for keys in dictionary.
        """
        return iter(self.dct)

    def __repr__(self) -> str:
        """Return string representation of the dictionary.

        Returns:
            String representation showing class name and contents.
        """
        return f"{self.__class__.__name__}: {self.dct}"

    @game_type
    def add_game(self, game: Game) -> None:
        """Add a game to the dictionary using derived key.

        Args:
            game: Game object to add.
        """
        key = self._get_key(game)
        if key not in self.dct:
            self.dct[key] = GameCollection()
        self.dct[key].add_game(game)

    @game_type
    def remove_game(self, game: Game) -> None:
        """Remove a game from the dictionary.

        Args:
            game: Game object to remove.

        Raises:
            ValueError: If game is not found in dictionary.
        """
        key = self._get_key(game)
        if key not in self.dct or game not in self.dct[key]:
            raise ValueError("Game is not in dict")

        self.dct[key].remove_game(game)
        if len(self.dct[key]) == 0:
            del self.dct[key]

    def search(self, key: K) -> GameCollection:
        """Search for games by key.

        Args:
            key: Key to search for.

        Returns:
            GameCollection for the key, empty if key not found.
        """
        return self.dct.get(key, GameCollection())

    @abstractmethod
    def _get_key(self, game: Game) -> K:
        """Abstract method to extract key from a game.

        Args:
            game: Game object to extract key from.

        Returns:
            Key value (string or integer) for the game.

        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")


class DictByID(GameDict[str]):
    """Dictionary that organizes games by their unique ID."""

    def _get_key(self, game: Game) -> str:
        """Extract game ID as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's unique identifier.
        """
        return game.game_id


class DictByReleaseYear(GameDict[int]):
    """Dictionary that organizes games by release year."""

    def _get_key(self, game: Game) -> int:
        """Extract release year as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's release year.
        """
        return game.release_year


class DictByDeveloper(GameDict[str]):
    """Dictionary that organizes games by developer."""

    def _get_key(self, game: Game) -> str:
        """Extract developer as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's developer name.
        """
        return game.developer


class DictByGenre(GameDict[str]):
    """Dictionary that organizes games by genre."""

    def _get_key(self, game: Game) -> str:
        """Extract genre as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's genre.
        """
        return game.genre
