from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.protected_name = "_" + name

    def __get__(self, obj, type_obj=None):
        value = getattr(obj, self.protected_name)
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.protected_name] = value
        self.validate(value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif not self.min_value <= value <= self.max_value:
            raise ValueError(f"Quantity should not be less than {self.min_value} "
                             f"and greater than {self.max_value}.")

class OneOf(Validator):
    def __init__(self, options) -> None:
        self.options = options

    def validate(self, value):
        if value not in self.options:
            self.options = tuple(self.options)
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    buns = Number(2, 3)
    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(
            self,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            buns: int,
            sauce: str
    ) -> None:
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce




 # TypeError: Quantity should be integer.
#
burger = BurgerRecipe(2, 1, 1, 1, 3, 'mayo')
#  # ValueError: Quantity should not be less than 2 and greater than 3.
#
# burger = BurgerRecipe(buns=2, cheese=1, tomatoes=1, cutlets=1, eggs=1, sauce="mustard")
# ValueError: Expected mustard to be one of ('ketchup', 'mayo', 'burger').

# burger = BurgerRecipe(buns=2, cheese=1, tomatoes=1, cutlets=1, eggs=1, sauce="ketchup")
# # burger will be created