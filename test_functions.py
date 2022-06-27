
import mutator
import scoring
import crossing
import stepping
import creation
import selection
import reproduction

from unit import Unit
from case import Case



def test_mutator_functions():
    unit = Unit('+-><--[-<')
    for func in mutator.default_functions():
        assert func(unit) is None


def test_scoring_functions():
    unit = Unit('+-><--[-<')
    test = 'input', 'output'
    for func in scoring.default_functions():
        assert isinstance(func(unit, test), scoring.RunResult)


def test_crossing_functions():
    parents = Unit('+'*80), Unit('-'*80)
    for func in crossing.default_functions():
        print(func)
        assert func(parents)


def test_creation_functions():
    for func in creation.default_functions():
        func(10)


def test_selection_functions():
    scored_pop = {Unit('>>>>>+'): scoring.RunResult(10, 'a', 'b'), Unit('++++'): scoring.RunResult(-82, 'a', 'b')}
    for func in selection.default_functions():
        func(scored_pop)


def test_reproduction_functions():
    scored_parent = {Unit('>>>>>+'): scoring.RunResult(10, 'a', 'b'), Unit('++++'): scoring.RunResult(-82, 'a', 'b')}
    crossing_func = next(iter(crossing.default_functions()))
    for func in reproduction.default_functions():
        func(scored_parent, 2, crossing_func)


def test_stepping_functions():
    pop = [Unit('>>>>>+'), Unit('>>>>>+'), Unit('>>>>>+'), Unit('++++')]
    functions = (next(iter(mod.default_functions())) for mod in (scoring, selection, reproduction, crossing, mutator))
    for func in stepping.default_functions():
        func(pop, Case('a', 'b'), len(pop), *functions)
