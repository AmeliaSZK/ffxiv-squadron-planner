# A file to experiment with stuff in the Python language


"""
phy = Physical
men = Mental
tac = Tactical

Comparisons are done by summing all 3 stats:
    s1 = Stats(10, 20, 30)
    s2 = Stats(40, 50, 60)
    s1 < s2 # True: (10 + 20 + 30) < (40 + 50 + 60)
            #                   60 < 150
"""
class Stats:
    def __init__(self, phy: int=0, men: int=0, tac: int=0) -> None:
        self.phy = phy
        self.men = men
        self.tac = tac
    
    def __repr__(self) -> str:
        return f'Stats({self.phy}, {self.men}, {self.tac})'
    def __str__(self) -> str:
        return f'({self.phy:3} / {self.men:3} / {self.tac:3})'
    
    def __eq__(self, other):
        if isinstance(other, Stats):
            return (    self.phy == other.phy
                    and self.men == other.men
                    and self.tac == other.tac)
        else:
            return NotImplemented


    def __add__(self, other):
        if isinstance(other, Stats):
            return Stats(self.phy + other.phy,
                         self.men + other.men,
                         self.tac + other.tac)
        else:
            return NotImplemented
    def __sub__(self, other):
        if isinstance(other, Stats):
            return Stats(self.phy - other.phy,
                         self.men - other.men,
                         self.tac - other.tac)
        else:
            return NotImplemented

s1 = Stats(10, 30, 40)
s2 = Stats(10, 30, 40)


print("print = ")
print(s1)
print("repr = ")
print(repr(s1))

print(f"s1: {s1}")
print(f"s1: {s2}")
print(f"s1 == s2: {s1 == s2}")
print(f"s1  + s2: {s1 + s2}")



