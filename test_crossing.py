
import crossing
from unit import Unit


def test_crossby_chromosomes():
    parents = Unit('+'*80), Unit('-'*80)
    assert crossing.crossby_chromosomes(parents) == ('+'*8 + '-'*8)*5
def test_crossby_token():
    parents = Unit('++++>++'), Unit('+--+--+')
    assert crossing.crossby_token(parents) == '++++ -- ++ --'.replace(' ', '')
def test_crossby_pivot():
    parents = Unit(']<>.->><-.>>.+>.+<<]+>->]<.><>'), Unit('.>,-<[>-.[<-<]<-.>.>-<,>>-->.<->')
    found = crossing.crossby_pivot(parents)
    print(found)
    assert found

    parents = Unit('+++...,,,..-]'), Unit('+++.[.[.')
    found = crossing.crossby_pivot(parents)
    print(found)
    assert found

    parents = Unit('+++'), Unit('-----')
    found = crossing.crossby_pivot(parents)
    print(found)
    assert found
