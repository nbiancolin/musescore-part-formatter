# musescore-part-formatter-poc
POC for programmatically

debating options -- whether its better to do this programmatically somehow? or just send it to an LLM? no idea yet, will experiment


Currently Does:
- Adds line breaks at rehearsal marks

In progress
- If a slur goes across a barline (and there is a multimeasure rest after it), add the linebreak to the measure itself instead of the one before
- If there is the scenario: (MM Repeat) <Rehearsal Mark>[LineBreak] (MM Repeat)<Rehearsal Mark>[LineBreak] -- there should only be one line break
  - In words: If there is a lineBreak added to a MultiMeasureRest, and then another line break added to a multimeasure rest, remove the initial one, only keep the second one

- For regular stuff, every 4 - 6 bars of music, add a line break. When a rehearsal mark / Line Break is encounterd, reset the count (ie, leave it on a new line) TODO: Not certain about this


==OLD==

Things it needs to do:
- Add the text in a consistent spot according to data in database (Number, Show Title)
- Add double bar lines at rehearsal marks
- Drum Parts should add the text for long and broken up slashes
- Add Line Breaks (LLM?)
- For adding styles, can literally just "replace" the existing file
- 
- 
