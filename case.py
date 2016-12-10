"""Case instances represent a pair (stdin, expected stdout).

"""


class Case:
    """Implementation of a test case, which is a pair (stdin, expected stdout).

    A scoring function can, with a unit and a case, provides a score.
    See test_case.py for API usage examples.

    stdin can be either a string or a callable.
    expected can be either a string (could contains the substring "{stdin}"),
    or a callable (stdin value -> expected string).

    """
    def __init__(self, input:str or callable, expected:str or callable):
        self._input = input if callable(input) else str(input)
        self._expected = expected if callable(expected) else str(expected)

    @property
    def callable_input(self):
        return callable(self._input)

    @property
    def callable_output(self):
        return callable(self._expected)

    def __iter__(self):
        if self.callable_input:
            stdin = self._input()
            expected = (self._expected(stdin) if self.callable_output
                        else self._expected.format(stdin=stdin))
            return iter((stdin, expected))
        else:
            return iter((self._input, self._expected))
