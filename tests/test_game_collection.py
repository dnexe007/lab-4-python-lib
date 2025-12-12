from src.game import Game
from src.game_collection import GameCollection
from src.games_db import GAMES_DATABASE


def test_empty_collection() -> None:
    collection = GameCollection()
    assert len(collection) == 0
    assert repr(collection) == "GameCollection([])"


def test_collection_with_initial_games() -> None:
    initial_games = [GAMES_DATABASE[0], GAMES_DATABASE[1]]
    collection = GameCollection(initial_games)
    assert len(collection) == 2
    assert GAMES_DATABASE[0] in collection
    assert GAMES_DATABASE[1] in collection


def test_add_game() -> None:
    collection = GameCollection()
    game = GAMES_DATABASE[0]

    collection.add_game(game)
    assert len(collection) == 1
    assert game in collection


def test_add_multiple_games() -> None:
    collection = GameCollection()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[1]

    collection.add_game(game1)
    collection.add_game(game2)

    assert len(collection) == 2
    assert game1 in collection
    assert game2 in collection


def test_remove_game() -> None:
    collection = GameCollection()
    game = GAMES_DATABASE[0]

    collection.add_game(game)
    assert len(collection) == 1

    collection.remove_game(game)
    assert len(collection) == 0
    assert game not in collection


def test_remove_nonexistent_game() -> None:
    collection = GameCollection()
    game_in = GAMES_DATABASE[0]
    game_not_in = GAMES_DATABASE[1]

    collection.add_game(game_in)

    try:
        collection.remove_game(game_not_in)
        assert False
    except ValueError as e:
        assert str(e) == "Game is not in collection"


def test_index() -> None:
    collection = GameCollection()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[1]

    collection.add_game(game1)
    collection.add_game(game2)

    assert collection.index(game1) == 0
    assert collection.index(game2) == 1


def test_getitem() -> None:
    collection = GameCollection()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[1]

    collection.add_game(game1)
    collection.add_game(game2)

    assert collection[0] == game1
    assert collection[1] == game2


def test_iteration() -> None:
    collection = GameCollection()
    games = [GAMES_DATABASE[0], GAMES_DATABASE[1], GAMES_DATABASE[2]]

    for game in games:
        collection.add_game(game)

    iterated = list(collection)
    assert len(iterated) == 3
    assert iterated == games


def test_clear() -> None:
    collection = GameCollection()
    games = [GAMES_DATABASE[0], GAMES_DATABASE[1]]

    for game in games:
        collection.add_game(game)

    assert len(collection) == 2
    collection.clear()
    assert len(collection) == 0


def test_game_type_decorator_wrong_type() -> None:
    collection = GameCollection()

    try:
        collection.add_game("not a game")
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"

    try:
        collection.remove_game("not a game")
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"

    try:
        collection.index("not a game")
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"

    try:
        "not a game" in collection
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"


def test_contains_with_wrong_type() -> None:
    collection = GameCollection()
    collection.add_game(GAMES_DATABASE[0])

    try:
        "string" in collection
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"


def test_repr_content() -> None:
    collection = GameCollection()
    game = GAMES_DATABASE[0]

    collection.add_game(game)

    repr_str = repr(collection)
    assert "GameCollection" in repr_str
    assert game.title in repr_str
    assert game.developer in repr_str
    assert str(game.release_year) in repr_str
    assert game.genre in repr_str


def test_duplicate_games() -> None:
    collection = GameCollection()
    game = GAMES_DATABASE[0]

    collection.add_game(game)
    collection.add_game(game)

    assert len(collection) == 2
    assert game in collection


def test_initial_empty_collection() -> None:
    collection = GameCollection()
    assert len(collection) == 0
    assert repr(collection) == "GameCollection([])"


def test_game_type_decorator_with_none() -> None:
    collection = GameCollection()

    try:
        collection.add_game(None)
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"


def test_collection_as_iterable() -> None:
    collection = GameCollection()
    games = [GAMES_DATABASE[0], GAMES_DATABASE[1], GAMES_DATABASE[2]]

    for game in games:
        collection.add_game(game)

    count = 0
    for game in collection:
        assert isinstance(game, Game)
        count += 1

    assert count == 3
