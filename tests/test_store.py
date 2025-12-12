from src.game_store import GameStore
from src.games_db import GAMES_DATABASE


def test_empty_store() -> None:
    """Test initialization and basic properties of empty store."""
    store = GameStore()
    assert len(store) == 0
    assert repr(store) == "Game store: 0 unique games (0 total copies)"
    assert not store.search_by_genre("FPS")
    assert not store.search_by_developer("Valve")


def test_add_and_remove_game() -> None:
    """Test basic game addition and removal operations."""
    store = GameStore()
    game = GAMES_DATABASE[0]

    store.add_game(game, 299)
    assert len(store) == 1
    assert game in store

    result = store.remove_game(game)
    assert result
    assert len(store) == 0
    assert game not in store


def test_add_duplicate_games() -> None:
    """Test adding multiple copies of same game updates price."""
    store = GameStore()
    game1 = GAMES_DATABASE[0]
    game2 = GAMES_DATABASE[0]

    store.add_game(game1, 1999)
    store.add_game(game2, 2499)

    assert len(store) == 2
    assert len(store.by_id) == 1
    assert store.prices[game1] == 2499


def test_buy_game_success_and_failure() -> None:
    """Test game purchase with sufficient and insufficient funds."""
    store = GameStore()
    game = GAMES_DATABASE[0]

    store.add_game(game, 2299)

    result = store.buy_game(game, 3000)
    assert result
    assert len(store) == 0
    assert store.profit == 2299
    assert store.sold_games == 1

    store.add_game(game, 2299)
    result = store.buy_game(game, 2000)
    assert not result
    assert len(store) == 1
    assert store.sold_games == 1


def test_return_game() -> None:
    """Test successful game return within 14-day period."""
    store = GameStore()
    game = GAMES_DATABASE[1]

    store.add_game(game, 499)
    store.profit = 1000

    result = store.return_game(game, 499, 2)
    assert result
    assert store.profit == 501
    assert store.return_games == 1
    assert len(store) == 1


def test_search_functions() -> None:
    """Test search functionality by developer, genre, and year."""
    store = GameStore()

    games = [GAMES_DATABASE[0], GAMES_DATABASE[5], GAMES_DATABASE[6]]

    for game in games:
        store.add_game(game, 999)

    assert store.search_by_developer("Remedy Entertainment")
    assert not store.search_by_developer("Ubisoft")

    assert store.search_by_genre("Action")
    assert not store.search_by_genre("MMORPG")

    assert store.search_by_release_year(2019)
    assert not store.search_by_release_year(1999)


def test_statistics() -> None:
    """Test store statistics reflect correct inventory counts."""
    store = GameStore()

    games = [GAMES_DATABASE[0], GAMES_DATABASE[4], GAMES_DATABASE[8]]

    for game in games:
        store.add_game(game, 999)

    assert len(store) == 3
    assert len(store.by_id) == 3
    assert len(store.by_developer) == 3
    assert len(store.by_genre) == 3
    assert len(store.by_release_year) == 2


def test_iterator() -> None:
    """Test iteration over store inventory."""
    store = GameStore()

    games = [GAMES_DATABASE[0], GAMES_DATABASE[1]]

    for game in games:
        store.add_game(game, 999)

    iterated_games = list(store)
    assert len(iterated_games) == 2
    assert all(game in games for game in iterated_games)


def test_complete_scenario() -> None:
    """Test complete purchase and return scenario."""
    store = GameStore()
    game = GAMES_DATABASE[2]

    store.add_game(game, 1000)
    assert len(store) == 1
    assert store.profit == 0
    assert store.sold_games == 0
    assert store.return_games == 0

    store.buy_game(game, 1500)
    assert len(store) == 0
    assert store.profit == 1000
    assert store.sold_games == 1
    assert store.return_games == 0

    store.return_game(game, 800, 1)
    assert store.profit == 200
    assert store.sold_games == 1
    assert store.return_games == 1


def test_edge_cases() -> None:
    """Test edge cases with non-existent items."""
    store = GameStore()

    game_from_db = GAMES_DATABASE[0]
    assert not store.search_by_developer("NoDev")
    assert not store.search_by_release_year(9999)

    result = store.buy_game(game_from_db, 1000)
    assert not result

    result = store.remove_game(game_from_db)
    assert not result


def test_return_game_failure() -> None:
    """Test failed return due to exceeding 14-day period."""
    store = GameStore()
    game = GAMES_DATABASE[3]

    store.add_game(game, 1000)
    store.profit = 500

    result = store.return_game(game, 1000, 15)
    assert not result
    assert store.profit == 500
    assert store.return_games == 0


def test_print_search_method() -> None:
    """Test static search result display method."""
    from src.game_collection import GameCollection

    games = GameCollection()
    games.add_game(GAMES_DATABASE[0])
    games.add_game(GAMES_DATABASE[1])

    result = GameStore.print_search(games, "test", "value")
    assert isinstance(result, bool)
    assert result

    empty_games = GameCollection()
    result = GameStore.print_search(empty_games, "test", "value")
    assert not result


def test_game_database_content() -> None:
    """Verify game database contains expected data."""
    assert len(GAMES_DATABASE) > 0

    game = GAMES_DATABASE[0]
    assert game.title == "Control"
    assert game.developer == "Remedy Entertainment"
    assert game.release_year == 2019
    assert game.genre == "Action"
    assert game.game_id == "CTL_RMD"


def test_multiple_genres_search() -> None:
    """Test searching games across multiple genres."""
    store = GameStore()

    games = [GAMES_DATABASE[0], GAMES_DATABASE[5], GAMES_DATABASE[9]]

    for game in games:
        store.add_game(game, 999)

    assert store.search_by_genre("Action")
    assert store.search_by_genre("FPS")
    assert store.search_by_genre("Survival Horror")
    assert not store.search_by_genre("Racing")


def test_multiple_developers_search() -> None:
    """Test searching games from multiple developers."""
    store = GameStore()

    games = [GAMES_DATABASE[0], GAMES_DATABASE[3], GAMES_DATABASE[5]]

    for game in games:
        store.add_game(game, 999)

    assert store.search_by_developer("Remedy Entertainment")
    assert store.search_by_developer("Naughty Dog")
    assert store.search_by_developer("Valve")
    assert not store.search_by_developer("Bethesda")


def test_multiple_years_search() -> None:
    """Test searching games from multiple release years."""
    store = GameStore()

    games = [GAMES_DATABASE[0], GAMES_DATABASE[1], GAMES_DATABASE[2]]

    for game in games:
        store.add_game(game, 999)

    assert store.search_by_release_year(2019)
    assert store.search_by_release_year(2016)
    assert store.search_by_release_year(2023)
    assert not store.search_by_release_year(2020)


def test_racing_games_from_database() -> None:
    """Test searching for racing genre games in database."""
    store = GameStore()

    for game in GAMES_DATABASE:
        if game.genre == "Racing":
            store.add_game(game, 1999)

    assert store.search_by_genre("Racing")
    assert store.search_by_developer("Electronic Arts") or store.search_by_developer("Codemasters")
