
class Prompts:

    INIT = "This file is a Musescore music score file. It is a large XML file containing a single 'Staff' tag, and a collection of 'measure' tags. " \
        "Each measure tag respresents a measure. Sometimes, these measure tags have a subtag labeled 'multiMeasureRest'. " \
        "The numerical value in this tag is how many measures in after this one are considered one 'block'." \
        "For measures that are not directly after a 'multuMeasureRest' tag, they count as one block."
    
    ALT_INIT = "This file is a Musescore music score file. It is a large XML file containing a single 'Staff' tag, and a collection of 'measure' tags. " \
        "Each Measure tag represents a measure in the score. These Measure tags contain one 'voice' tag, and inside this voice tag, there are many different types of sub elements. We will refer to these as 'Music Elements'" \
        "When formatting the score, we wish to add LineBreaks to make the score readable."
    
    NEW_ALT_INIT = "This file is a Musescore music score file. It is a large XML file containing a single 'Staff' tag, and a collection of 'measure' tags. " \
        "Each Measure tag represents a measure in the score. These Measure tags contain one 'voice' tag, and inside this voice tag, there are many different types of sub elements. We will refer to these as 'Music Elements'" \
        "When formatting the score, we wish to add LineBreaks to make the score readable."
    
    HOWTO_ADD_LINE_BREAKS = "You can add a LineBreak to a measure by adding the following inside the measure tag: <LayoutBreak><subtype>line</subtype></LayoutBreak>."
    
    LINE_BREAKS_INSTRUCTIONS = "For any measure that has a rehearsal mark tag, add a line break to the measure before it. Remember to add it inside a measure tag " \
    "Then, add a LineBreak roughly every 4 measures. we would like there to be a roughly equal number of Music Elements between any given set of LineBreaks"

    END = "Please only return the newly formatted XML file and nothing else, in plaintext. the file should start with <?xml version=\"1.0\" encoding=\"UTF-8\"?>"

    def _how_tos(self):
        return self.HOWTO_ADD_LINE_BREAKS

    def generate(self):
        return self.INIT + self.END
    
    def alt_generate(self):
        return self.NEW_ALT_INIT + self._how_tos() + self.LINE_BREAKS_INSTRUCTIONS + self.END