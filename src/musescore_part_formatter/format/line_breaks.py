from musescore_part_formatter.canonical.models import Part
from musescore_part_formatter.format.config import FormattingConfig, Defaults

from logging import getLogger

LOGGER = getLogger(__name__)


def add_line_breaks(part: Part, config: FormattingConfig) -> Part:
    """
    Exported function to add and balance line breaks
    """

    part = _add_line_breaks(part, config)
    part = _balance_line_breaks(part, config)

    return part


def _add_line_breaks(part: Part, config: FormattingConfig) -> Part:
    """
    Applying Line Breaks:

    Want one at every rehearsal mark and double bar line
    And then, one at each

    :param part: Description
    :type part: Part
    """

    nmpl = config.get("num_measures_per_line", Defaults.NUM_MEASURES_PER_LINE)

    i = 0
    prev_measure = None
    for measure in part.measures:
        i += 1

        if measure.add_line_break is True:
            LOGGER.warning("Encountered a measure with a line break in a clean part!")
            i = 0
            prev_measure = measure
            continue

        if measure.is_rehearsal_mark is True:
            prev_measure.add_line_break = True
            i = 1
            prev_measure = measure
            continue

        if measure.double_bar_position == "r":
            measure.add_line_break = True
            i = 0
            prev_measure = measure
            continue

        if measure.double_bar_position == "l":
            if prev_measure.add_line_break is False:
                LOGGER.warning("Encountered a barline without a line break!")

        if i == nmpl:
            measure.add_line_break = True
            prev_measure = measure
            i = 0
            continue

        prev_measure = measure

        # assert False, "Should never reach this point ..."

    return part


def balance_line_breaks(part: Part, config: FormattingConfig) -> Part:
    """
    add_line_breaks sometimes adds too many line breaks. IN the first step we add a bunch, pehaps overly too many.
    IN this step, we go through and balance out the lines so that there isnt any funny business

    case - rehearsal mark every 8 bars, but nmpl is set to 6. this would look funny, so in balancing we want to end up with 4 / 4 instead of 6 / 2

    :param part: Description
    :type part: Part
    :param config: Description
    :type config: FormattingConfig
    """
    measures = part.measures


    """
    Balancing Rules:

    AT MOST nmpl measures per line
    AT MIN 3 measures per line (unless nmpl is set to 2 for some reason) [MVP skip]

    Rehearsal marks and bar lines do not always have to start on a new line.

    if a line has less than MIN measures per line:
    
    (simple):
    - Remove the line break before it, and balance those two lines


    (advanced):
    - remove the line break after and before it, and balance those three
    """

    # If first line is nmpl, then balance according to that (ie. if we have a double bar every 8 measures and nmpl is 6, we don't always need)


    if config.balance_mm_rest_line_breaks is True:
        part = _balance_mm_rest_line_breaks(part)

    # Last measure should not have a line break
    if measures[-1].add_line_break is True:
        LOGGER.info(f"Removing line break from last measure of part {part.name}")
        measures[-1].add_line_break = False

    return part


def _balance_mm_rest_line_breaks(part: Part) -> Part:
    """
    Scenario: MM rest -> Rehearsal mark -> MM Rest -> Rehearsal mark. 

    We do not need two line breaks here.
    We can have up to two mm rests per line break
    """


    flag = False
    prev_measure_idx = None

    for i, measure in enumerate(part.measures):
        if measure.is_mm_rest_start is True:
            if flag is False:
                flag = True
                prev_measure_idx = i
                continue
            else:
                #flag is True
                part.measures[prev_measure_idx].add_line_break = False
                prev_measure_idx = None
                flag = False
                continue
        else:
            flag = False
            prev_measure_idx = None
