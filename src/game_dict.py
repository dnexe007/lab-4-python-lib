from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Iterator

from src.game import Game
from src.game import game_type
from src.game_collection import GameCollection



class GameDict(ABC):
    """Abstract base class for dictionary-like collections of games.

    Organizes games by a key (either string or integer) into GameCollection instances.
    """

    def __init__(self) -> None:
        """Initialize an empty game dictionary."""
        self._dct: Dict[int | str , GameCollection] = {}

    def __getitem__(self, key: int | str) -> GameCollection:
        """Return game collection associated with the key.

        Args:
            key: Key to look up in dictionary.

        Returns:
            GameCollection for the specified key.
        """
        return self._dct[key]

    def __contains__(self, key: int | str) -> bool:
        """Check if key exists in dictionary.

        Args:
            key: Key to check for existence.

        Returns:
            True if key exists, False otherwise.
        """
        return key in self._dct

    def __len__(self) -> int:
        """Return number of keys in dictionary.

        Returns:
            Count of distinct keys in dictionary.
        """
        return len(self._dct)

    def __iter__(self) -> Iterator[int | str]:
        """Return iterator over dictionary keys.

        Returns:
            Iterator for keys in dictionary.
        """
        return iter(self._dct)

    def __repr__(self) -> str:
        """Return string representation of the dictionary.

        Returns:
            String representation showing class name and contents.
        """
        return f"{self.__class__.__name__}: {self._dct}"

    @game_type
    def add_game(self, game: Game) -> None:
        """Add a game to the dictionary using derived key.

        Args:
            game: Game object to add.
        """
        key = self._get_key(game)
        if key not in self._dct:
            self._dct[key] = GameCollection()
        self._dct[key].add_game(game)

    @game_type
    def remove_game(self, game: Game) -> None:
        """Remove a game from the dictionary.

        Args:
            game: Game object to remove.

        Raises:
            ValueError: If game is not found in dictionary.
        """
        key = self._get_key(game)
        if key not in self._dct or game not in self._dct[key]:
            raise ValueError("Game is not in dict")

        self._dct[key].remove_game(game)
        if len(self._dct[key]) == 0:
            del self._dct[key]

    def search(self, key: int | str) -> GameCollection:
        """Search for games by key.

        Args:
            key: Key to search for.

        Returns:
            GameCollection for the key, empty if key not found.
        """
        return self._dct.get(key, GameCollection())

    @abstractmethod
    def _get_key(self, game: Game) -> int | str:
        """Abstract method to extract key from a game.

        Args:
            game: Game object to extract key from.

        Returns:
            Key value (string or integer) for the game.

        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")


class DictByID(GameDict):
    """Dictionary that organizes games by their unique ID."""

    def _get_key(self, game: Game) -> str:
        """Extract game ID as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's unique identifier.
        """
        return game.game_id


class DictByReleaseYear(GameDict):
    """Dictionary that organizes games by release year."""

    def _get_key(self, game: Game) -> int:
        """Extract release year as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's release year.
        """
        return game.release_year


class DictByDeveloper(GameDict):
    """Dictionary that organizes games by developer."""

    def _get_key(self, game: Game) -> str:
        """Extract developer as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's developer name.
        """
        return game.developer


class DictByGenre(GameDict):
    """Dictionary that organizes games by genre."""

    def _get_key(self, game: Game) -> str:
        """Extract genre as dictionary key.

        Args:
            game: Game object to extract key from.

        Returns:
            Game's genre.
        """
        return game.genre
