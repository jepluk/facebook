import random

class Birthday:
    def __init__(self) -> None:
        self.day = str(random.randint(1, 28))
        self.month = str(random.randint(1, 12))
        self.year = str(random.randint(2000, 2010))
