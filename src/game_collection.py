from typing import Iterator
from src.game import game_type, Game


class GameCollection:
    def __init__(self, lst: list[Game] | None = None) -> None:
        self.games: list[Game] = lst if lst is not None else []

    def __getitem__(self, index: int) -> Game:
        return self.games[index]

    def __len__(self) -> int:
        return len(self.games)

    def __iter__(self) -> Iterator[Game]:
        return iter(self.games)

    def __repr__(self) -> str:
        return f"GameCollection({self.games})"

    def clear(self)->None:
        self.games.clear()

    @game_type
    def __contains__(self, game: Game) -> bool:
        return game in self.games

    @game_type
    def add_game(self, game: Game) -> None:
        self.games.append(game)

    @game_type
    def remove_game(self, game: Game) -> None:
        if game not in self.games:
            raise ValueError("Game is not in collection")
        self.games.remove(game)

    @game_type
    def index(self, game: Game) -> int:
        return self.games.index(game)
