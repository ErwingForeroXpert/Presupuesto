
from numpy import number
import numpy as np


def validate_empty_or_cero(value):
    try:
        if isinstance(value, (str, int, number)):
            if int(value) == 0 or str(value).strip().__len__ == 0:
                return True
        elif value is None or np.isnan(value) :
            return True

        return False

    except ValueError:
        return True


