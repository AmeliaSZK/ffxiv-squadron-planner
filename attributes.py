from dataclasses import dataclass

@dataclass(order=True, frozen=True)
class Attributes:
    """
    Immutable object to group attributes, and do operations on them.

    phy = Physical
    men = Mental
    tac = Tactical

    Supports additions, subtractions, and equality,
    by operating on each attribute separately:
        >>> a1 = Attributes(10, 20, 30)
        >>> a2 = Attributes(10, 20, 30)
        >>> print(a1 == a2)
        True
        >>> a3 = a1 + a2
        >>> print(a3)
        ( 20 /  40 /  60)
        >>> a4 = a3 - Attributes(10, 10, 10)
        >>> print(a4)
        ( 10 /  30 /  50)
        >>> a3.phy = 40
        Traceback (most recent call last):
            ...
        dataclasses.FrozenInstanceError: cannot assign to field 'phy'
    
    To sum a list, use `start=Attributes()` in the call to sum():
        >>> as_list = [a1, a2, a3, a4]
        >>> print(*as_list, sep='\n')
        ( 10 /  20 /  30)
        ( 10 /  20 /  30)
        ( 20 /  40 /  60)
        ( 10 /  30 /  50)
        >>> sum_of_list = sum(as_list, start=Attributes())
        >>> print(sum_of_list)
        ( 50 / 110 / 170)
    
    Attributes are printed as `(phy / men / tac)`
    So `( 50 / 110 / 170)` means:
        Physical =  50
        Mental   = 110
        Tactical = 170
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
        """Verifies that all three attributes meet the specified requirements.
        
        Each attribute must be greater than or equal to the corresponding
        attribute in the specificed requirements.
        """
        return (    self.phy >= requirements.phy
                and self.men >= requirements.men
                and self.tac >= requirements.tac)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

