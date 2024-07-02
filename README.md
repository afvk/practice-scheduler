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

## Todo

- [ ] 




Problems:
- Fully random, no prioritization
    - Options:
        - Do time-based
        - Do spaced repetition

For spaced repetition, what is a card?
Options:
- Template, e.g. "Improvise over {{standard}} in {{key}} at {{tempo}}."
    - Problem: certain standards or keys might be much more difficult than others
- Instance, e.g. "Improvise over Nardis in Gb at 120bpm." 
    - Problem: not clear what to do when template is extended, e.g. to "Improvide over Nardis in Gb at 120bpm with continuous eight note lines."

Generalize across instruments.
Change format to YAML.
Restructure repo. 

What problems does this solve?
- Only practicing what you know well already. 
- Watching some Jens Larsen video with a useful exercise, doing it for 20 minutes, then never coming back to it. 
- Not having a structured way of maintaining your repertoire. 

Make it CLI runnable:
- "music-practice add standard Autumn Leaves"
- "music-practice"


Verify inputs, e.g. make sure that all variables mentioned in exercises actually exist. 

Add modes, i.e. purely random, spaced repetition, etc.

Add tempo variable, make position variable optional. In general, split into exercise-specific and general variables. 


