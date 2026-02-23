from musescore_part_formatter.canonical.models import Part
from musescore_part_formatter.format.config import FormattingConfig, Defaults

def add_line_breaks(part: Part, config: FormattingConfig) -> Part:
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
            i = 0
            prev_measure = measure
            continue

        if measure.is_rehearsal_mark is True:
            prev_measure.add_line_break = True
            i = 0
            prev_measure = measure
            continue

        if measure.double_bar_position == "l":
            prev_measure.add_line_break = True
            i = 0
            prev_measure = measure
            continue

        if i == nmpl:
            measure.add_line_break = True
            prev_measure = measure
            i = 0
            continue


        prev_measure = measure

        # assert False, "Should never reach this point ..."

    return part
        



def balance_line_breaks(part: Part, config: FormattingConfig):
    """
    add_line_breaks sometimes adds too many line breaks. IN the first step we add a bunch, pehaps overly too many. 
    IN this step, we go through and balance out the lines so that there isnt any funny business

    case - rehearsal mark every 8 bars, but nmpl is set to 6. this would look funny, so in balancing we want to end up with 4 / 4 instead of 6 / 2
    
    :param part: Description
    :type part: Part
    :param config: Description
    :type config: FormattingConfig
    """
    pass