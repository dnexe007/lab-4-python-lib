from typing import List
from src.simulation import simulate


def main() -> None:
    print("💥Welcome to the game store simulation!")

    while True:
        print("\n▶️To start simulation, enter:")
        print("\tsm <start games amount> <steps> <seed - optional>")
        print("⏹️To close program, enter: \n\tquit\n")

        user_input: str = input("command: ").strip()
        args: List[str] = user_input.split()

        if not args:
            print("empty command\n")
            continue

        if args[0] == "sm":
            if len(args) not in [3, 4]:
                print("invalid arguments\n")
                continue

            seed: int | None = None
            try:
                start: int = int(args[1])
                steps: int = int(args[2])
            except ValueError:
                print("invalid arguments\n")
                continue

            if len(args) == 4:
                try:
                    seed = int(args[3])
                except ValueError:
                    print("invalid arguments\n")
                    continue

            print("\n")
            simulate(start, steps, seed)

        elif args[0] == "quit":
            break

        else:
            print("unknown command\n")


if __name__ == "__main__":
    main()
