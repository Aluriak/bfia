

import itertools
from collections import Counter

import interpreter
from statistics import Saver
import mutator
import algogen
from unit import Unit


# simulation
POP_SIZE = 400
# printing
MAX_PRINTED_PROPS = 10


def score(unit):
    return algogen.score(unit)


def main(saver:Saver=None):
    specs = range(30, 40), range(3, 20), '<<<>>>++--[],..'
    pop = tuple(Unit.from_spec(*specs) for _ in range(POP_SIZE))
    MUTATORS = mutator.all_mutators()
    for genid in itertools.count(1):
        print('#{}:'.format(genid))
        # pop = {unit: score(unit) for unit in pop}
        scored_pop = algogen.multisolve(pop)  # unit: results
        if saver:
            results = tuple(sorted(tuple(scored_pop.values()), key=lambda r: r.score, reverse=True))
            saver.save((';'.join(str(r.score) for r in results), results[0].score, results[-1].score))
        best_unit = max(pop, key=lambda u: scored_pop[u].score)
        best_result = scored_pop[best_unit]
        print('SCORES:', sorted(tuple(set(round(r.score, 3) for u, r in scored_pop.items())), reverse=True))
        proportions = Counter(r.score for r in scored_pop.values())
        print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
        print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3), '\tOUTPUTS:', '"' + best_result.found + '"', '\t(expect {})'.format(best_result.expected))
        print('SOURCE:', best_unit.source)
        # print('EZKCUI: FIRSTS:', {u: r for u, r in pop.items() if r.score == best.score})
        selected = algogen.select(scored_pop, pattern=(
            (0, 40),  # select the first 10%
            # (45, 50),  # and those in between the 25% and the 40%
            (60, 65),  # and…
            (80, 85),  # and…
        ))
        print('SELECTED: {} of {}'.format(len(selected), len(scored_pop)))
        # NB: the best unit is not necessarily in the final population because,
        #  if many units have the same score, not all could be selected.
        #  then, the best unit that is arbitrarily choosed early
        #  could not appear in the selected, so in the next pop.
        pop = tuple(algogen.pop_from(selected, POP_SIZE, mutators=MUTATORS))
        print()


if __name__ == "__main__":
    main()
    exit()
    with Saver(('scores', 'max_score', 'min_score')) as saver:
        try:
            main(saver)
        except KeyboardInterrupt:
            pass
    saver.commit()
    print('STOPPED')
    files = Saver.data_files()
    print('FILES:', files)
    Saver.plot(max(files))
