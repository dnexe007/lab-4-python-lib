from src.game_dict import DictByID, DictByDeveloper, DictByReleaseYear, DictByGenre
from src.game_collection import GameCollection
from src.games_db import GAMES_DATABASE


def test_dict_by_id_basic_operations() -> None:
    game_dict = DictByID()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert len(game_dict) == 1
    assert game.game_id in game_dict
    assert game in game_dict[game.game_id]

    game_dict.remove_game(game)
    assert len(game_dict) == 0
    assert game.game_id not in game_dict


def test_dict_by_developer_basic_operations() -> None:
    game_dict = DictByDeveloper()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert len(game_dict) == 1
    assert game.developer in game_dict
    assert game in game_dict[game.developer]

    game_dict.remove_game(game)
    assert len(game_dict) == 0
    assert game.developer not in game_dict


def test_dict_by_release_year_basic_operations() -> None:
    game_dict = DictByReleaseYear()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert len(game_dict) == 1
    assert game.release_year in game_dict
    assert game in game_dict[game.release_year]

    game_dict.remove_game(game)
    assert len(game_dict) == 0
    assert game.release_year not in game_dict


def test_dict_by_genre_basic_operations() -> None:
    game_dict = DictByGenre()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert len(game_dict) == 1
    assert game.genre in game_dict
    assert game in game_dict[game.genre]

    game_dict.remove_game(game)
    assert len(game_dict) == 0
    assert game.genre not in game_dict


def test_multiple_games_same_key() -> None:
    game_dict = DictByDeveloper()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[1]

    game_dict.add_game(game1)
    game_dict.add_game(game2)

    assert len(game_dict) == 1
    assert game1.developer in game_dict
    assert len(game_dict[game1.developer]) == 2

    game_dict.remove_game(game1)
    assert len(game_dict) == 1
    assert game2 in game_dict[game2.developer]


def test_empty_collection_removal() -> None:
    game_dict = DictByDeveloper()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    game_dict.remove_game(game)

    assert len(game_dict) == 0
    assert game.developer not in game_dict


def test_search_method() -> None:
    game_dict = DictByDeveloper()
    game = GAMES_DATABASE[0]

    result = game_dict.search(game.developer)
    assert len(result) == 0

    game_dict.add_game(game)
    result = game_dict.search(game.developer)
    assert len(result) == 1
    assert game in result


def test_search_nonexistent_key() -> None:
    game_dict = DictByDeveloper()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    result = game_dict.search("Nonexistent Developer")
    assert isinstance(result, GameCollection)
    assert len(result) == 0


def test_remove_nonexistent_game() -> None:
    game_dict = DictByDeveloper()
    game_in = GAMES_DATABASE[0]
    game_not_in = GAMES_DATABASE[1]

    game_dict.add_game(game_in)

    try:
        game_dict.remove_game(game_not_in)
        assert False
    except ValueError as e:
        assert str(e) == "Game is not in dict"


def test_dict_iteration() -> None:
    game_dict = DictByDeveloper()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[3]

    game_dict.add_game(game1)
    game_dict.add_game(game2)

    keys = list(game_dict)
    assert len(keys) == 2
    assert game1.developer in keys
    assert game2.developer in keys


def test_repr_string() -> None:
    game_dict = DictByDeveloper()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    repr_str = repr(game_dict)

    assert "DictByDeveloper" in repr_str
    assert game.developer in repr_str


def test_game_type_decorator() -> None:
    game_dict = DictByDeveloper()

    try:
        game_dict.add_game("not a game")
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"

    try:
        game_dict.remove_game("not a game")
        assert False
    except TypeError as e:
        assert str(e) == "Game must be of type Game"


def test_dict_by_id_specific() -> None:
    game_dict = DictByID()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert game_dict._get_key(game) == game.game_id
    assert game.game_id in game_dict


def test_dict_by_release_year_specific() -> None:
    game_dict = DictByReleaseYear()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert game_dict._get_key(game) == game.release_year
    assert game.release_year in game_dict


def test_dict_by_developer_specific() -> None:
    game_dict = DictByDeveloper()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert game_dict._get_key(game) == game.developer
    assert game.developer in game_dict


def test_dict_by_genre_specific() -> None:
    game_dict = DictByGenre()
    game = GAMES_DATABASE[0]

    game_dict.add_game(game)
    assert game_dict._get_key(game) == game.genre
    assert game.genre in game_dict


def test_multiple_dict_types_with_same_game() -> None:
    game = GAMES_DATABASE[0]

    dict_by_id = DictByID()
    dict_by_dev = DictByDeveloper()
    dict_by_year = DictByReleaseYear()
    dict_by_genre = DictByGenre()

    dict_by_id.add_game(game)
    dict_by_dev.add_game(game)
    dict_by_year.add_game(game)
    dict_by_genre.add_game(game)

    assert game.game_id in dict_by_id
    assert game.developer in dict_by_dev
    assert game.release_year in dict_by_year
    assert game.genre in dict_by_genre


def test_dict_getitem_key_error() -> None:
    game_dict = DictByDeveloper()

    try:
        _ = game_dict["Nonexistent"]
        assert False
    except KeyError:
        assert True


def test_dict_contains_wrong_type() -> None:
    game_dict = DictByDeveloper()

    # __contains__ не использует декоратор game_type напрямую,
    # но проверяем, что он работает с правильными типами
    game = GAMES_DATABASE[0]
    game_dict.add_game(game)

    # Должен работать со строками для ключей
    assert game.developer in game_dict
    assert "Nonexistent" not in game_dict


def test_dict_clear_empty_collection() -> None:
    game_dict = DictByDeveloper()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[1]

    game_dict.add_game(game1)
    game_dict.add_game(game2)

    game_dict.remove_game(game1)
    assert len(game_dict) == 1

    game_dict.remove_game(game2)
    assert len(game_dict) == 0
    assert game1.developer not in game_dict
