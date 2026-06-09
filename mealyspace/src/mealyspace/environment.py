class Environment:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def available_moves(self) -> tuple[str, str, str, str]:
        return "N", "E", "S", "W"

    def move(self, direction: str) -> None:
        if direction == "N":
            self.y += 1
            return
        if direction == "E":
            self.x += 1
            return
        if direction == "S":
            self.y -= 1
            return
        if direction == "W":
            self.x -= 1
            return

        raise ValueError(f"Unknown direction: {direction}")
