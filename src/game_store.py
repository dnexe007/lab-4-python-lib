from typing import Iterator

from src.game import Game
from src.game import game_type
from src.game_collection import GameCollection
from src.game_dict import DictByDeveloper
from src.game_dict import DictByGenre
from src.game_dict import DictByID
from src.game_dict import DictByReleaseYear


class GameStore:
    """Store for managing game inventory, sales, and statistics.

    Tracks games through multiple indexing strategies and handles transactions.
    """

    def __init__(self) -> None:
        """Initialize game store with empty collections and statistics."""
        self._all_copies: GameCollection = GameCollection()
        self._by_id: DictByID = DictByID()
        self._by_developer: DictByDeveloper = DictByDeveloper()
        self._by_release_year: DictByReleaseYear = DictByReleaseYear()
        self._by_genre: DictByGenre = DictByGenre()
        self._prices: dict[Game, int] = {}
        self._profit: int = 0
        self._sold_games = 0
        self._return_games = 0

    def __len__(self) -> int:
        """Return total number of game copies in store.

        Returns:
            Count of all game copies in inventory.
        """
        return len(self._all_copies)

    def __contains__(self, game: Game) -> bool:
        """Check if specific game copy exists in store.

        Args:
            game: Game object to check for.

        Returns:
            True if game exists in store, False otherwise.
        """
        return game in self._all_copies

    def __iter__(self) -> Iterator[Game]:
        """Return iterator over all game copies in store.

        Returns:
            Iterator for all Game objects in inventory.
        """
        return iter(self._all_copies)

    def __repr__(self) -> str:
        """Return summary of store inventory.

        Returns:
            String with unique game count and total copies count.
        """
        unique_games = len(self._by_id)
        total_copies = len(self._all_copies)
        return f"Game store: {unique_games} unique games ({total_copies} total copies)"

    def add_game(self, game: Game, price: int) -> None:
        """Add a game copy to store inventory with specified price.

        Args:
            game: Game object to add.
            price: Price in rubles for the game.
        """
        self._all_copies.add_game(game)
        self._by_id.add_game(game)
        self._by_developer.add_game(game)
        self._by_release_year.add_game(game)
        self._by_genre.add_game(game)
        self._prices[game] = price
        print(f'📦"{game.title}" added. New price: {price} rub')

    @game_type
    def remove_game(self, game: Game, print_log: bool = True) -> bool:
        """Remove a game copy from store inventory.

        Args:
            game: Game object to remove.
            print_log: Whether to print removal messages.

        Returns:
            True if removal successful, False if game not found.
        """
        if game.game_id not in self._by_id:
            print(f'❌"{game.title}" remove failed:')
            print("\t⚠️game is not in store")
            return False
        self._by_id.remove_game(game)
        self._all_copies.remove_game(game)
        self._by_developer.remove_game(game)
        self._by_release_year.remove_game(game)
        self._by_genre.remove_game(game)
        if print_log:
            print(f'🚫copy of "{game.title}" removed from sale.')
        if game.game_id not in self._by_id:
            del self._prices[game]
            print(f'⛔️"{game.title}" is out of stock.')
        return True

    @game_type
    def return_game(self, game: Game, price: int, days_passed: int) -> bool:
        """Process game return from a client.

        Args:
            game: Game object being returned.
            price: Price to refund in rubles.
            days_passed: Days since purchase for return eligibility.

        Returns:
            True if return successful, False if return period expired.
        """
        if days_passed > 14:
            print(f'❌"{game.title}" return failed:')
            print("\t⚠️two weeks passed")
            return False
        print(f'↩️"{game.title}" returned by client. Price: {price} rub')
        self._profit -= price
        self._return_games += 1
        return True

    @game_type
    def buy_game(self, game: Game, client_balance: int) -> bool:
        """Process game purchase by a client.

        Args:
            game: Game object to purchase.
            client_balance: Client's available balance in rubles.

        Returns:
            True if purchase successful, False if failed.
        """
        if game.game_id not in self._by_id:
            print(f'❌"{game.title}" sell failed:')
            print("\t⚠️Game is not in store")
            return False

        price = self._prices[game]
        if client_balance < price:
            print(f'❌"{game.title}" sell failed:')
            print(f"\t⚠️Not enough money ({client_balance} rub of {price} rub)")
            return False

        print(f'✅"{game.title}" sold for {price} rub')
        self.remove_game(game, False)
        self._profit += price
        self._sold_games += 1
        return True

    def get_stats(self) -> None:
        """Display comprehensive store statistics."""
        print(
            "📊Statistics:\n"
            + f"\t🎮Number of games: {len(self._all_copies)}\n"
            + f"\t🆔Unique games: {len(self._by_id)}\n"
            + f"\t‍💻Unique developers: {len(self._by_developer)}\n"
            + f"\t📅Unique release years: {len(self._by_release_year)}\n"
            + f"\t🎭Unique genres: {len(self._by_genre)}\n"
            + f"\t💰Profit: {self._profit} rub\n"
            + f"\t✅Sold games: {self._sold_games}\n"
            + f"\t↩️Returned games: {self._return_games}"
        )

    def search_by_genre(self, genre: str) -> bool:
        """Search for games by genre.

        Args:
            genre: Genre to search for.

        Returns:
            True if games found, False otherwise.
        """
        result = GameCollection()
        if genre in self._by_genre:
            result = self._by_genre[genre]
        self.print_search(result, "genre", genre)
        return len(result) != 0

    def search_by_release_year(self, release_year: int) -> bool:
        """Search for games by release year.

        Args:
            release_year: Year to search for.

        Returns:
            True if games found, False otherwise.
        """
        result = GameCollection()
        if release_year in self._by_release_year:
            result = self._by_release_year[release_year]
        self.print_search(result, "release year", release_year)
        return len(result) != 0

    def search_by_developer(self, developer: str) -> bool:
        """Search for games by developer.

        Args:
            developer: Developer name to search for.

        Returns:
            True if games found, False otherwise.
        """
        result = GameCollection()
        if developer in self._by_developer:
            result = self._by_developer[developer]
        self.print_search(result, "developer", developer)
        return len(result) != 0

    @staticmethod
    def print_search(found_games: GameCollection, search_type: str, value: str | int) -> bool:
        """Display search results in formatted output.

        Args:
            found_games: Collection of found games.
            search_type: Type of search performed.
            value: Search parameter value.

        Returns:
            True if games found, False otherwise.
        """
        result = set(found_games)
        print(f"🔍Search result ({search_type} - {value}):")
        if result:
            for game in result:
                print(f"\t🎮{game}")
            return True
        else:
            print("\t🎮No games found")
            return False
