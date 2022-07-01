
import crossing
from unit import Unit


def test_crossby_chromosomes():
    parents = Unit('+'*80), Unit('-'*80)
    assert crossing.crossby_chromosomes(parents) == ('+'*8 + '-'*8)*5

def test_crossby_token():
    parents = Unit('++++>++'), Unit('+--+--+')
    assert crossing.crossby_token(parents) == '++++ -- ++ --'.replace(' ', '')

def test_crossby_consensus():
    parents = Unit('++++'), Unit('+-+-'), Unit('+++-')
    assert crossing.crossby_consensus(parents) == '+++-'

def test_crossby_random_draw():
    parents = Unit('+++-'), Unit('+-++')
    founds = set.intersection({crossing.crossby_random_draw(parents) for _ in range(10)})
    assert founds <= {'+++-', '++++', '+-+-', '+-++'}

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
