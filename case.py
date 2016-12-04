"""Case instances represent a pair (stdin, expected stdout).

"""


class Case:
    """Implementation of a test case, which is a pair (stdin, expected stdout).

    A scoring function can, with a unit and a case, provides a score.
    See test_case.py for API usage examples.

    """
    def __init__(self, input:str or callable, expected:str or callable):
        self.callable_input = callable(input)
        self.callable_output = callable(expected)
        self._input = input
        self._expected = expected

    def __iter__(self):
        if self.callable_input:
            stdin = self._input()
            expected = (self._expected(stdin) if self.callable_output
                        else self._expected.format(stdin=stdin))
            return iter((stdin, expected))
        else:
            return iter((self._input, self._expected))
