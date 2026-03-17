import xml.etree.ElementTree as ET

from musescore_part_formatter.canonical.models import Score, Part, Measure

from logging import getLogger

LOGGER = getLogger(__name__)


def convert_staff_to_canonical_part(staff: ET.Element) -> Part:
    """We only want to process one "staff" at a time for processing. Eventually support taking in full obj's"""

    processed_measures = []
    measure_num = 0

    mm_rest_len = 0

    for i in range(len(staff)):
        elem = staff[i]
        if elem.tag != "Measure":
            continue

        voice = elem.find("voice")
        if voice is None:
            LOGGER.warning("Encountered a measure with no voice -- skipping")
            continue

        measure_num += 1

        if mm_rest_len > 0:
            mm_rest_len -= 1
            if mm_rest_len == 0 and voice.find("BarLine") is not None:
                processed_measures[-1].double_bar_position = "r"

            continue

        is_rehearsal_mark = voice.find("RehearsalMark") is not None
        is_mm_rest = (elem.attrib.get("len") is not None) or (elem.find("multiMeasureRest") is not None)
        has_notes = False if is_mm_rest else True
        has_barline = voice.find("BarLine") is not None
        
        # Handle BarLine placement - if this measure is an MM rest with a BarLine,
        # the BarLine should apply to the previous measure, not the MM rest itself
        if is_mm_rest and has_barline:
            double_bar_position = None  # MM rest itself doesn't get the bar position
            mm_rest_is_double_bar = True  # Flag to apply bar to previous measure
        else:
            if has_barline:
                double_bar_position = "r"
            elif processed_measures and processed_measures[-1].double_bar_position == "r":
                double_bar_position = "l"
            else:
                double_bar_position = None
            mm_rest_is_double_bar = False

        if is_mm_rest:
            assert mm_rest_len == 0, "Somehow this file had overlapping MM rests"

            # For a MM Rest of len 4, musescore stores 5 measures
            # 1. bar of full rest
            # 2. Bar that contains mm rest info
            # 3-5. fill bars of rest. 

            #So, we need to remove the first bar of rest, and skip 1 less

            prev = processed_measures.pop() 
            
            # If the MM rest has a BarLine, it applies to the measure we just popped
            if mm_rest_is_double_bar:
                prev.double_bar_position = "r"
                processed_measures.append(prev)  # Re-add the popped measure with updated bar position
                double_bar_position = "l"  # MM rest itself gets "l"
            else:
                # Check if the new last measure (which remains) has 'r' from a BarLine
                if processed_measures and processed_measures[-1].double_bar_position == "r":
                    # MM rest that follows a measure with 'r' should have 'l'
                    double_bar_position = "l"
                    # Don't modify the previous measure
                elif processed_measures:
                    # Only modify if the previous measure doesn't have 'r'
                    processed_measures[-1].double_bar_position = 'l' if prev.double_bar_position == 'l' else None
                # else: keep the earlier double_bar_position value (None for rest-only cases)
                
            mm_rest_len = int(elem.find("multiMeasureRest").text)
            measure_num -= 1

        processed_measures.append(
            Measure(
                number=measure_num,
                is_rehearsal_mark=is_rehearsal_mark,
                double_bar_position="l" if mm_rest_is_double_bar else double_bar_position,
                is_mm_rest_start=is_mm_rest,
                mm_rest_len=(mm_rest_len) if mm_rest_len > 0 else None,
                has_notes=has_notes
            )
        )

        if is_mm_rest:
            # Since we have to skip the first measure, shorten the MM rest len
            mm_rest_len -= 1



    return Part(name="idfk", measures=processed_measures)




def convert_mscz_to_canonical(file_path: str) -> Score:

    # load in score
    # read title props
    # read meta props
    #convert staves to canonical
    #return finished score object