
from deepdiff import DeepDiff


def assert_eq_json(expected, actual):
    ddiff_result = DeepDiff(expected, actual,
                            ignore_order=True,
                            significant_digits=10)

    if len(ddiff_result) != 0:
        raise AssertionException("Expected results do not match actual \
            results. Differences are: " + str(ddiff_result))

def eq_json(expected, actual):
    ddiff_result = DeepDiff(expected, actual,
                            ignore_order=True,
                            significant_digits=10)

    if len(ddiff_result) == 0:
        return True
    else:
        print(f'* Asser eq JSON diff: {ddiff_result}')
        return False


class AssertionException(Exception):
    def __init__(self, message):
        message = "\n\t\t" + message
        Exception.__init__(self, message)
        self.message = message