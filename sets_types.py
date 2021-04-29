from __future__ import annotations
from enum import Enum
from typing import NewType, Tuple


COLORTERM = '\x1b[0m'


class Color(str, Enum):
    GREEN = 'g'
    PURPLE = 'p'
    RED = 'r'
    
    @property
    def print(self) -> str:
        seq = '\x1b['
        if self.value == self.GREEN:
            seq += '32'
        elif self.value == self.PURPLE:
            seq += '35'
        elif self.value == self.RED:
            seq += '31'
        return f'{seq}m{{}}{COLORTERM}'


class Shape(str, Enum):
    DIAMOND = 'd',
    OVAL = 'o'
    WIGGLE = 'w'
    
    @property
    def print(self) -> str:
        if self.value == self.DIAMOND:
            return '<{}>'
        elif self.value == self.OVAL:
            return '({})'
        elif self.value == self.WIGGLE:
            return '≈{}≈'


class Filling(str, Enum):
    EMPTY = 'e'
    DASHED = 'd'
    FILLED = 'f'
    
    @property
    def print(self) -> str:
        if self.value == self.EMPTY:
            return ' '
        elif self.value == self.DASHED:
            return '/'
        elif self.value == self.FILLED:
            return '■'


class Count(str, Enum):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    
    @property
    def print(self) -> Tuple[str, str, str]:
        ret = [' '*3]*3
        value = int(self.value)
        if value >= 1:
            ret[1] = '{}'
        if value >= 2:
            ret[0] = '{}'
        if value == 3:
            ret[2] = '{}'
        return tuple(ret)
            

CardPrint = NewType("CardPrint", Tuple[str,str,str,str,str])


class Card:
    def __init__(self, color: Color, shape: Shape, fill: Filling, count: Count):
        self.color = color
        self.shape = shape
        self.fill = fill
        self.count = count
    
    def compare(self, card: Card) -> Tuple[bool, bool, bool, bool]:
        return (
            self.color == card.color,
            self.shape == card.shape,
            self.fill == card.fill,
            self.count == card.count,
        )
    
    def __str__(self):
        return f'Card({self.color}, {self.shape}, {self.fill}, {self.count})'
    
    def __repr__(self):
        return self.__str__()
    
    def print(self, highlight: bool = False) -> CardPrint:
        markers = list(self.count.print)
        for i, marker in enumerate(markers):
            if marker:
                markers[i] = marker.format(self.color.print.format(self.shape.print.format(self.fill.print)))
                
        edge_color = '37'
        if highlight:
            edge_color = '33;5'
        edge_color = f'\x1b[{edge_color}m'
        
        return (
            '{ec}+-----+{ct}'.format(ec=edge_color, ct=COLORTERM),
            '{ec}| {}{ec} |{ct}'.format(markers[0], ec=edge_color, ct=COLORTERM),
            '{ec}| {}{ec} |{ct}'.format(markers[1], ec=edge_color, ct=COLORTERM),
            '{ec}| {}{ec} |{ct}'.format(markers[2], ec=edge_color, ct=COLORTERM),
            '{ec}+-----+{ct}'.format(ec=edge_color, ct=COLORTERM),
        )
    
    @classmethod
    def from_string(cls, item: str) -> Card:
        assert len(item) == 4, "String must consist of 4 characters (color, shape, filling, count)"
        return cls(Color(item[0]), Shape(item[1]), Filling(item[2]), Count(item[3]))


class CardSet:
    def __init__(self, card0: Card, card1: Card, card2: Card):
        self.cards = (card0, card1, card2)
        if not self.is_set():
            raise ValueError('Not a valid set')
        
    def is_set(self):
        for attr in ('color', 'shape', 'fill', 'count'):
            cmp01 = getattr(self.cards[0], attr) == getattr(self.cards[1], attr)
            cmp02 = getattr(self.cards[0], attr) == getattr(self.cards[2], attr)
            if cmp01 and cmp02:
                # Same
                continue
            if cmp01 != cmp02:
                # 0 is equal to one and different from another
                return False
            cmp12 = getattr(self.cards[1], attr) == getattr(self.cards[2], attr)
            if cmp12:
                # 1 and 2 are equal, but 0 is different
                return False
        return True
    
    def __contains__(self, item: Card):
        return item in self.cards

    def __str__(self):
        out = 'CardSet('
        out += ', '.join([x.__str__() for x in self.cards])
        out += ')'
        return out
    
    def __repr__(self):
        return self.__str__()
            


if __name__ == '__main__':
    card = Card(Color('r'),Shape('w'),Filling('d'),Count('3'))
    print('\n'.join(card.print()))