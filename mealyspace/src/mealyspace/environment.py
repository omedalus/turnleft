from random import getrandbits


class Environment:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.is_victory_path_east = bool(getrandbits(1))
        self.is_active = True
        self.was_success: bool | None = None

    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def available_moves(self) -> tuple[str, ...]:
        if not self.is_active:
            return ()

        return ("N", "E", "S", "W")

    def sensors(self) -> tuple[int, int, int, int]:
        return (
            int(self.is_traversible(self.x, self.y + 1)),
            int(self.is_traversible(self.x + 1, self.y)),
            int(self.is_traversible(self.x, self.y - 1)),
            int(self.is_traversible(self.x - 1, self.y)),
        )

    def is_traversible(self, x: int, y: int) -> bool:
        if x == 0:
            return -1 <= y <= 1

        if y == 1:
            return -2 <= x <= 2

        if y == -1 and x in {-1, 1}:
            return self.is_victory_path_east == (x == 1)

        return False

    def is_end_of_maze(self, x: int, y: int) -> bool:
        return y == 1 and x in {-2, 2}

    def end_round(self, success: bool) -> None:
        self.was_success = success
        self.is_active = False

    def handle_maze_end(self, x: int, y: int) -> None:
        if self.is_victory_path_east and x == 2 and y == 1:
            self.end_round(True)
            return

        if not self.is_victory_path_east and x == -2 and y == 1:
            self.end_round(True)
            return

        self.end_round(False)

    def move(self, direction: str) -> None:
        if not self.is_active:
            raise ValueError("Round is not active. Begin or reset to continue.")

        next_x = self.x
        next_y = self.y

        if direction == "N":
            next_y += 1
        elif direction == "E":
            next_x += 1
        elif direction == "S":
            next_y -= 1
        elif direction == "W":
            next_x -= 1
        else:
            raise ValueError(f"Unknown direction: {direction}")

        if not self.is_traversible(next_x, next_y):
            self.end_round(False)
            return

        self.x = next_x
        self.y = next_y

        if self.is_end_of_maze(next_x, next_y):
            self.handle_maze_end(next_x, next_y)
