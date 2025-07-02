
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
    
    HOWTO_ADD_LINE_BREAKS = "You can add a LineBreak to a measure by adding the following inside the measure tag: " \
    """
    ```
    <LayoutBreak>
       <subtype>line</subtype>
    </LayoutBreak>
    ```
    """

    
    HOWTO_UNDERSTAND_MULTIMEASURE_RESTS = "Multimeasure rests are a contiguous collection of measures that all contain a single rest tag in them. They all start with a measure tag with a `len` attribute." \
                                        "To add a line break to a multimeasure rest: add a LineBreak to the very last measure in the collection, and add a LineBreak to the measure with the rest in it itself"

    LINE_BREAKS_INSTRUCTIONS = "For any measure that has a rehearsal mark tag, add a line break to the measure before it. Remember to add it inside a measure tag " \
    #"Then, add a LineBreak roughly every 4 measures. we would like there to be a roughly equal number of Music Elements between any given set of LineBreaks"

    ALT_LINE_BREAK_INSTRUCTIONS = "We would like to add a LineBreak after roughly every "

    END = "Please only return the newly formatted file and nothing else, in plaintext. the file should start with <?xml version=\"1.0\" encoding=\"UTF-8\"?>"

    GPT_PROMPT = """I have a MuseScore `.mscx` file (uncompressed format). Please insert system breaks to make the score more legible by spacing out the music. Try to insert breaks every 3–4 measures or at natural phrase points. To insert a system break, add the following XML inside the appropriate `<Measure>` tag:

<LayoutBreak>
  <subtype>Line</subtype>
</LayoutBreak>

Do not modify any other musical content. Return the modified `.mscx` file.
"""

    NEW_GPT_PROMPT = """You are modifying a MuseScore `.mscx` file (uncompressed MuseScore format). Your task is to improve the score's readability by inserting system (line) breaks.

Rules:
- Add a system break every 3 to 4 measures, or where musical phrases naturally end.
- Insert the following XML inside the appropriate <Measure> tag to create a system break:

<LayoutBreak>
  <subtype>line</subtype>
</LayoutBreak>

- Do NOT change any other content in the file: do not edit notes, rhythms, dynamics, articulations, or formatting. Do not edit the position of any tags. The part tag.
- Return the modified `.mscx` file with the added system breaks only.

Make the spacing more even and legible, but keep everything else exactly the same.
"""

    def _how_tos(self):
        return self.HOWTO_ADD_LINE_BREAKS + self.HOWTO_UNDERSTAND_MULTIMEASURE_RESTS

    def generate(self):
        return self.INIT + self.END
    
    def alt_generate(self):
        return self.NEW_ALT_INIT + self._how_tos() + self.LINE_BREAKS_INSTRUCTIONS + self.END
    
    def gpt_prompt(self):
        return self.NEW_GPT_PROMPT + self.END