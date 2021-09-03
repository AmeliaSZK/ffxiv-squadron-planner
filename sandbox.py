# A file to experiment with stuff in the Python language


# phy = Physical
# men = Mental
# tac = Tactical
class Stats:
    def __init__(self, phy: int=0, men: int=0, tac: int=0) -> None:
        self.phy = phy
        self.men = men
        self.tac = tac
    
    def __repr__(self) -> str:
        return f'Stats({self.phy}, {self.men}, {self.tac})'
    def __str__(self) -> str:
        return f'({self.phy:3} / {self.men:3} / {self.tac:3})'

s1 = Stats(10, 30, 40)

print("print = ")
print(s1)
print("repr = ")
print(repr(s1))



