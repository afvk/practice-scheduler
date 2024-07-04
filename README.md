# Practice scheduler

Getting good at something requires deliberate practice. However, we often get to a certain level where we are comfortable and stop improving. The aim of `practice-scheduler` is to remove the burden of deciding what to practice. 

## How does it work?

- Specify exercises as flexible templates, for example: "Improvise over {song} in {key} at {tempo} bpm." 
- Fill the template by randomly sampling the variables
- Prioritize based on a spaced repetition algorithm, least recently practiced exercise, etc. 

## Example applications

- Practicing an instrument
- Learning a dance
- ...

## What problems does this solve?
- Only practicing stuff you know well already
- Watching some Jens Larsen video with a useful exercise, doing it for 20 minutes, then never coming back to it
- Not having a structured way of maintaining your repertoire

## Todo

- [ ] Change exercises to JSON/YAML?
- [ ] Add prioritization modes, e.g. random, spaced repetition, time-based, etc.
- [ ] Make it a CLI command, e.g. "practice-scheduler practice", "practice-scheduler add exercise ...", etc.
- [ ] Verify inputs, e.g. make sure that all variables mentioned in exercises actually exist. 
- [ ] Add tempo variable, make position variable optional. In general, handle exercise-specific and general variables.
- [ ] Introduce "skill" abstraction, e.g. "jazz-guitar", "jazz-trumpet"

## Thoughts

### For spaced repetition, what is a card?
Options:
- Template, e.g. "Improvise over {standard} in {key} at {tempo}."
    - Problem: certain standards or keys are more difficult than others
        - Potential solution: give scores (e.g. SM2 easiness factor) to templates and variables individually, then do weighted sampling based on scores
- Instance, e.g. "Improvise over Nardis in Gb at 120bpm." 
    - Problems: 
        - not clear what to do when template is extended, e.g. to "Improvise over Nardis in Gb at 120bpm with continuous eight note lines."
        - number of combinations is extremely large
- Somehow combine scores of both the template and its variables. 
