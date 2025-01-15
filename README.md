# Practical Information
The app can be found here: [Míreadóir](https://mireadoir.ie)

I hacked it in a little over a day, added a bunch of stuff as needed over a month or so when I had time, and then had a lot of refactoring to do. I'm still working on tidying up main.py. Fixing the sorting and normalising sped it up substantially. 

### TODO:
- the file interleaves functions and other code, making it hard to understand the structure -> moving all non-function code to a if __name__ == "__main__": block at the bottom.
- extract the long literals in get_text into constants (or maybe a helper module). Typically a lot of this html formatting work would be done via templates (e.g. jinja)

### I have a research license with Foras Na Gaeilge. Please contact them if you would like permission to use data from Teangleann. 

## Project Description and Some Future Work
Míreadóir enables users to search Irish words by substring. 
In its current state, it has been used as:
- a crude rhyming dictionary
- to check certain spelling conventions
- to put in parts of a word that a learner remebers hearing to find the full word they were unfamiliar with
  
Future iterations are planned to enable rhyming matches by dialect. For instance, in the Ulster dialect, words ending with ú or adh would rhyme. 
I am currently looking into the SpaCy comunity plug-in for syllable segmentation as well. 

Current work is aimed at segmenting words into their "morphemes" (see below) so that it can enable users to look up words by root meanings. 
I am exploring both machine learning and rule based approaches towards this goal. 

"Morphemes" are the smallest parts of words that contain meaning on their own. There is inflectional and derivational morphology. 
Inflectional morphology has to do with changes to words that affect the grammar. 

Examples: 
- adding s to cat to make it the plural "cats"
- initial mutations in Irish like leniting a regular verb to make it past tense: tóg -> thóg

This project is more concerned with derivational morphology which has to do with separating words into their roots.

Examples:
- feargach ("angry") -> fearg ("anger") + -ach ("connected to" or "having")
- rófhada ("too far") -> ró ("too much") + fada ("long" or "far")

Benefits of this could include aiding "sense-by-sense" translation not just from Irish to English or vice versus, but also for interlingual translation (between the dialects). 
There is a fair amount of evidence that morpheme segmentation or sub-word tokenisation that captures morphological features can aid in NLP tasks for "Morphologically rich" 
languages such as Irish, Russian, Hungarian, etc... 

