

from typing import Any


class Cycle:
    # integer to string table
    stoi = {type_: idx for idx, type_ in enumerate(["日拋", "月拋"])}

    def __init__(self, cycle: str):
        self.cycle_str = cycle
    
    # type: integer
    @property
    def cycle_str(self):
        return self._cycle_str
    
    @cycle_str.setter
    def cycle_str(self, cycle: str):
        assert cycle in self.stoi.keys(), f"cycle should be {' or '.join(self.stoi.keys())}, but '{cycle}' was given"
        self._cycle_str = cycle
    
    def __str__(self):
        return self._cycle_str
    
    def __int__(self):
        return self.stoi[self.cycle_str]

class ContactLense:

    def __init__(self, name, cycle: str, water_content: str, diameter: str, price: int):
        self._name = name
        self._cycle: Cycle = Cycle(cycle)
        self.water_content: int = water_content
        self.diameter: float = diameter
        self.price: int = price
    
    def info(self):
        return {
            "name": self.name,
            "cycle": (str(self.cycle), int(self.cycle)),
            "water_content": self.water_content,
            "diameter": self.diameter,
            "price": self.price
        }

    @property
    def name(self):
        return self._name
    
    @property
    def cycle(self):
        return self._cycle

    @property
    def water_content(self):
        return self._water_content

    @property
    def diameter(self):
        return self._diameter

    @property
    def price(self):
        return self._price
    
    @cycle.setter
    def cycle(self, cycle: str):
        self._cycle.cycle_str = cycle
    
    @water_content.setter
    def water_content(self, water_content: str):
        self._water_content = int(water_content[3:-1])

    @diameter.setter
    def diameter(self, diameter: str):
        self._diameter = float(diameter[2:-2])

    @price.setter
    def price(self, price: int):
        assert price > 0, "price can not be negative"
        self._price = price


def _test():
    a = ContactLense("日拋", "含水量38%", "直徑14.1mm", 399)

    print(a.info())

if __name__ == "__main__":
    _test()