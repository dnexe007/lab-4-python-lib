from typing import Dict, Iterator, TypeVar, Generic
from src.game import game_type, Game
from src.game_collection import GameCollection
from abc import ABC, abstractmethod

K = TypeVar('K', str, int)

class GameDict(ABC, Generic[K]):
    def __init__(self) -> None:
        self.dct: Dict[K, GameCollection] = {}

    def __getitem__(self, key: K) -> GameCollection:
        return self.dct[key]

    def __contains__(self, key: K) -> bool:
        return key in self.dct

    def __len__(self) -> int:
        return len(self.dct)

    def __iter__(self) -> Iterator[K]:
        return iter(self.dct)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.dct}"

    @game_type
    def add_game(self, game: Game) -> None:
        key = self._get_key(game)
        if key not in self.dct:
            self.dct[key] = GameCollection()
        self.dct[key].add_game(game)

    @game_type
    def remove_game(self, game: Game) -> None:
        key = self._get_key(game)
        if key not in self.dct or game not in self.dct[key]:
            raise ValueError("Game is not in dict")

        self.dct[key].remove_game(game)
        if len(self.dct[key]) == 0:
            del self.dct[key]

    def search(self, key: K) -> GameCollection:
        return self.dct.get(key, GameCollection())

    @abstractmethod
    def _get_key(self, game: Game) -> K:
        raise NotImplementedError("Must be implemented by subclass")


class DictByID(GameDict[str]):
    def _get_key(self, game: Game) -> str:
        return game.game_id


class DictByReleaseYear(GameDict[int]):
    def _get_key(self, game: Game) -> int:
        return game.release_year


class DictByDeveloper(GameDict[str]):
    def _get_key(self, game: Game) -> str:
        return game.developer


class DictByGenre(GameDict[str]):
    def _get_key(self, game: Game) -> str:
        return game.genre
