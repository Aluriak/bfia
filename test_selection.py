
import pytest
import selection
from unit import Unit
from selection import DEFAULT_PROB_FUNCTION



def test_selection_pooling_with_too_little_data():
    "How does the selection handle when there is not enough element to yield ?"
    units = {Unit('+'): 1, Unit('+'): 1}

    # should not allow to select more units than present in the population
    with pytest.raises(ValueError):
        found = tuple(selection.poolling(units, selection_size=3))

    # this may hang, if pooling fails to see that what we ask are impossible
    found = tuple(selection.poolling(units, selection_size=2, unique=True))
    print(found)
    assert found


def test_default_prob_function():
    func = DEFAULT_PROB_FUNCTION
    MIN, MAX = 7000, 9900
    g = lambda x: func(x, MIN, MAX)
    assert g(MIN) > 0., "even the minimal score must have a chance to stand"
    assert g(MAX) < 1., "even the maximal score must have a chance to be discarded"
    assert g(MIN-1) <= 0., "invalid score yield invalid prop"
    assert g(MAX+1) >= 1., "invalid score yield invalid prop"
    assert 0. < g((MIN + MAX) / 2) < 1.


@pytest.fixture
def scores():
    return [8108, 8000, 7944, 7903, 7847, 7795, 7683, 7526, 7503, 7449, 7441, 7429, 7388, 7386, 7376, 7314, 7299, 7296, 7294, 7290, 7229, 7228, 7227, 7226, 7223, 7219, 7218, 7217, 7216, 7214, 7147, 7146, 7145, 7144, 7143, 7142, 7141, 7139, 7075, 7074, 7073, 7070, 7069, 7068, 7067, 7066, 7065, 7001, 7000, 6998, 6997, 6996, 6995, 6994, 6993, 6992, 6991, 6919, 6918, 6917, 6840, 6839, 6838, 6837, 6685, -509128, -509681, -509693, -509827, -509837]


def test_default_prob_function_with_real_data(scores):
    func = DEFAULT_PROB_FUNCTION
    maxi, mini = scores[0], scores[-1]
    probs = [func(s, mini, maxi) for s in scores]
    # from pprint import pprint
    # pprint(tuple(zip(scores, probs)))
    # assert False
    assert max(probs) == probs[0]
    assert min(probs) == probs[-1]
    assert sorted(probs, reverse=True) == probs



def test_default_prob_function_with_real_data_with_ranks(scores):
    func = DEFAULT_PROB_FUNCTION
    ranks = [rank for rank, s in enumerate(scores, start=1)]
    # from pprint import pprint
    # pprint(tuple(zip(scores, ranks)))
    # assert False

    maxi, mini = 1, len(scores) - 1
    probs = [func(s, mini, maxi) for s in scores]
    assert min(probs) == probs[0]
    assert max(probs) == probs[-1]
    assert sorted(probs, reverse=False) == probs

