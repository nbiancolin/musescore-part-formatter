"""
Code to dynamically predict the optimal formatting params for a score

WIP still but Im working on it
"""

from .utils import FormattingParams



def predict_best_num_measures_per_line(time_sig) -> int:
    # TODO: Should this depend on more things?
    match time_sig:
        case "4/4":
            return 6
        case "3/4":
            return 4
        case "12/8":
            return 4
        case _:
            return 8


#NEW ONE use this!!
NUM_INSTS_TO_SPATIUM_MAP = {
    1: 1.75,
    2: 1.75,
    3: 1.75,
    4: 1.70,
    5: 1.65,
    6: 1.65,
    7: 1.60,
    8: 1.55,
    9: 1.65,#jumps back up
    10: 1.65,
    11: 1.60,
}


# NOTE: if landscape, can subtract 0.005 from these (at least)
# NUM_INSTS_STAFF_SPACING_MAP = {
#     1: 0.069,
#     2: 0.069,
#     3: 0.069,
#     4: 0.06,
#     5: 0.055,
#     6: 0.05,
#     7: 0.0425,
#     # TODO: Add more
# }

# NOTE: Musescore stores these values as "spatium"
# where 1sp == 0.069 in


# def _convert_in_to_sp(val: float) -> float:
#     return round(val * (1 / 0.069), 4)


def _predict_staff_spacing(num_staves, page_dimensions=(8.5, 11)) -> float:
    """get value from dict, or approximate it"""
    if num_staves in NUM_INSTS_TO_SPATIUM_MAP.keys():
        return NUM_INSTS_TO_SPATIUM_MAP[num_staves]
    # linearly estimate best guess
    res = (
        (NUM_INSTS_TO_SPATIUM_MAP[11] - NUM_INSTS_TO_SPATIUM_MAP[9])
        / (11 - 9)
        * (num_staves - 9)
        + NUM_INSTS_TO_SPATIUM_MAP[9]
    )
    return round(res, 4)


def predict_params_based_on_score_info(score_info) -> dict[str, str]:
    res = {}
    if num_staves := score_info.get("num_staves"):
        res["staff_spacing"] = str(_predict_staff_spacing(num_staves))

    return res
