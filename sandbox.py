# A file to experiment with stuff in the Python language

from dataclasses import dataclass

@dataclass(order=True, frozen=True)
class Attributes:
    """
    phy = Physical
    men = Mental
    tac = Tactical

    Supports additions, subtractions, and equality,
    by operating on each attribute separately:
        s1 = Attributes(10, 20, 30)
        s2 = Attributes(10, 20, 30)
        print(s1 == s2)     # True
        s3 = s1 + s2
        print(s3)           # ( 20 /  40 /  60)
        s4 = s3 + Attributes(10, 10, 10)
        print(s4)           # ( 30 /  50 /  70)

    To sum a list, use `start=Attributes()` in the call to sum():
        listed = [s1, s2, s3, s4]
        summed = sum(listed, start=Attributes())
        print(summed)       # ( 70 / 130 / 190)
    
    Attributes are printed as `(phy / men / tac)`
    So `( 70 / 130 / 190)` means:
        Physical =  70
        Mental   = 130
        Tactical = 190
    """

    phy: int = 0
    men: int = 0
    tac: int = 0

    def __str__(self) -> str:
        return f'({self.phy:3} / {self.men:3} / {self.tac:3})'

    def __add__(self, other):
        if isinstance(other, Attributes):
            return Attributes(self.phy + other.phy,
                         self.men + other.men,
                         self.tac + other.tac)
        else:
            return NotImplemented
    def __sub__(self, other):
        if isinstance(other, Attributes):
            return Attributes(self.phy - other.phy,
                         self.men - other.men,
                         self.tac - other.tac)
        else:
            return NotImplemented

    def clears(self, requirements: 'Attributes') -> bool:
        """Verifies that all three attributes meet the specified requirements."""
        return (    self.phy >= requirements.phy
                and self.men >= requirements.men
                and self.tac >= requirements.tac)

a1 = Attributes(10, 20, 30)
a2 = Attributes(10, 20, 30)
print(a1 == a2)
a3 = a1 + a2
print(a3)
a4 = a3 + Attributes(10, 10, 10)
print(a4)

listed = [a1, a2, a3, a4]
print(listed)

summed = sum(listed, start=Attributes())
print(summed)

in_set = set(listed)
print(in_set)

sorted_list = sorted(listed)
print(sorted_list)


