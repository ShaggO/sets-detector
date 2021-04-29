from sets_types import Card, Color, Shape, Filling, Count, CardSet
from typing import List, Tuple, Union
from itertools import chain, combinations
    

class Table:
    def __init__(self, cards: List[List[Card]]):
        self.cards = cards
    
    def get_sets(self) -> List[CardSet]:
        cards = chain.from_iterable(self.cards)
        combs = combinations(cards, 3)
        sets = []
        for comb in combs:
            try:
                sets.append(CardSet(*comb))
            except ValueError:
                pass
        return sets

    def print(self, highlight: Union[List[Card], CardSet]):
        out = []
        for row in self.cards:
            row_p = []
            for card in row:
                card_p = card.print(card in highlight)
                if not row_p:
                    row_p = card_p
                    continue
                row_p = list(map(lambda x: ''.join(x), zip(row_p, card_p)))
            out.append('\n'.join(row_p))
        print('\n'.join(out))                


def detect_table(data: List[List[str]]) -> Table:
    table = []
    for x in data:
        row = []
        for y in x:
            row.append(Card.from_string(y))
        table.append(row)
    return Table(table)
        

def main(data: List[List[str]]) -> None:
    table = detect_table(data)
    sets = table.get_sets()
    print(f"Number of sets: {len(sets)}")
    
    for i, x in enumerate(sets):
        print(f'Set {i+1}:')
        table.print(highlight=x)


if __name__ == '__main__':
    print('Starting sets checker')
    data = [
        ['gde3','goe3','pwe1','roe1','pof2'],
        ['pde3','rdf1','roe3','gdf1','poe1'],
        ['pod2','gwd3','gwf2','rwf3','rwe2'],
    ]
    main(data)