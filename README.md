# musescore-part-formatter-poc
POC for programmatically

debating options -- whether its better to do this programmatically somehow? or just send it to an LLM? no idea yet, will experiment

Things it needs to do:
- Add the text in a consistent spot according to data in database (Number, Show Title) -- programmatically?
- Add double bar lines at rehearsal marks -- AI
- Drum Parts should add the text for long and broken up slashes -- AI
- Add Line Breaks (LLM?) -- AI
- 

DONE SO FAR:
- Adding line breaks kinda

TODOS:
- Refactor code bc its shit rn


Line break steps:
- First Pass: Rehearsal Marks
  - Goal: Add a line break before every rehearsal mark