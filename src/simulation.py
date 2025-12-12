from random import randint, choice, seed
from src.games_db import GAMES_DATABASE
from src.game_store import GameStore
from src.game import Game

EVENTS_DATABASE = [
    "add",
    "remove",
    "buy",
    "stats",
    "search",
    "return"
]

SEARCH_TYPES = [
    "genre",
    "year",
    "developer"
]


def random_game() -> Game:
    return choice(GAMES_DATABASE)


def random_price() -> int:
    return randint(500, 3500)


def random_balance() -> int:
    return randint(1000, 7000)


def random_event() -> str:
    return choice(EVENTS_DATABASE)


def simulate(start_games_amount: int, steps: int, random_seed: int | None = None) -> None:
    if random_seed is not None:
        seed(random_seed)

    store: GameStore = GameStore()
    print("🔃Preparing to simulate...\n")

    for _ in range(start_games_amount):
        store.add_game(random_game(), random_price())

    print("\n🔃Starting simulation...")

    for i in range(steps):
        print(f"\n📋Step: {i + 1}/{steps}")
        event: str = random_event()

        match event:
            case "add":
                store.add_game(random_game(), random_price())
            case "remove":
                store.remove_game(random_game())
            case "buy":
                store.buy_game(random_game(), random_balance())
            case "stats":
                store.get_stats()
            case "search":
                search_type: str = choice(SEARCH_TYPES)
                game_for_search: Game = random_game()

                match search_type:
                    case "genre":
                        store.search_by_genre(game_for_search.genre)
                    case "year":
                        store.search_by_release_year(game_for_search.release_year)
                    case "developer":
                        store.search_by_developer(game_for_search.developer)
            case "return":
                days: int = randint(1, 60)
                store.return_game(random_game(), random_price(), days)

    print("\n✅Simulation complete\n")
    store.get_stats()
