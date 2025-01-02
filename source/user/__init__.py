import random, names
from fake_useragent import UserAgent
from .birthday import Birthday

class Identity:
    def __init__(self, gender: int = random.choice([1, 2])) -> None:
        self.useragent = UserAgent(os='Windows').chrome
        self.gender = str(gender) if gender else str(random.choice([1, 2]))
        self.firstname, self.lastname = tuple(names.get_full_name(gender='female' if self.gender == '1' else 'male').split(' '))
        self.birthday = Birthday()

if __name__ == "__main__":
    x = Identity()
    print(x.gender)
    print(x.useragent)
