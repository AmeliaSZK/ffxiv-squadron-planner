# A file to experiment with stuff in the Python language


class Stats:
    """
    phy = Physical
    men = Mental
    tac = Tactical

    Supports additions, subtractions, and equality,
    by operating on each stat separately.
        s1 = Stats(10, 20, 30)
        s2 = Stats(10, 20, 30)
        print(s1 == s2)     # True
        s3 = s1 + s2
        print(s3)           # ( 20 /  40 /  60)
        s4 = s3 + Stats(10, 10, 10)
        print(s4)           # ( 30 /  50 /  70)

    To sum a list, use `start=Stats()` in the call to sum():
        listed = [s1, s2, s3, s4]
        summed = sum(listed, start=Stats())
        print(summed)       # ( 70 / 130 / 190)
    
    Stats are printed as `(phy / men / tac)`
    So `( 70 / 130 / 190)` means:
        Physical =  70
        Mental   = 130
        Tactical = 190
    """

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

s1 = Stats(10, 20, 30)
s2 = Stats(10, 20, 30)
print(s1 == s2)     # True
s3 = s1 + s2
print(s3)           # Stats(20, 40, 60)
s4 = s3 + Stats(10, 10, 10)
print(s4)           # Stats(30, 50, 70)

listed = [s1, s2, s3, s4]
print(listed)
summed = sum(listed, start=Stats())
print(summed)

