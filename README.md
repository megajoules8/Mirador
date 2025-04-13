# Practical Information
The app can be found here: [Míreadóir](https://mireadoir.ie)

I'm still working on tidying up. Fixing the sorting and normalising sped it up substantially. 
There are extensive doc strings if you're interested in how the code works. 

### TODO:

- extract the long literals in get_text into constants (or maybe a helper module). Typically a lot of this html formatting work would be done via templates (e.g. jinja)

- add feedback form

- consider migrating instructions to sidebar 

### I have a research license with Foras Na Gaeilge. Please contact them if you would like permission to use data from Teangleann. 

## Project Description and Some Future Work
Míreadóir enables users to search Irish words by substring. 
In its current state, it has been used as:
- a rhyming dictionary
- to check certain spelling conventions
- to put in parts of a word heard to find the full word users were unfamiliar with
  
Future iterations are planned to actually reccord common rhymes by dialect so users don't have to use regex. 
Rhyme does change substantially by dialect and is interesting to look at in regards to interligual translation of sean-nós songs, for instance. 
As an example, in the Ulster dialect, words ending with ú, odh, or adh usually rhyme. 
It's important to note that Kevin Scannell released a lovely rhyming dictionary (in the form of a PDF) back in December of 2019 but I noticed 
it didn't have rhymes that fit with the dialect I am familiar with so I wanted to make a more flexible digital resource. 

I am currently looking into the SpaCy comunity plug-in for syllable segmentation as well. I beleive he also has a lot of the word done as far as hyphenation goes, but
once again, it would likely need to be replicated by dialect. Anyone interested in collaborating on a project like this with me should feel free to reach out. 
It might make for an interesting citizen science project. In my free time, I've been gathering songs from different regions and analysing rhyming patterns that way. I've learnt a lot about the sounds of Irish through this lense, finding the differences both surprising and delightful. 

Current work is also aimed at segmenting words into their "morphemes" (see below) so that it can enable users to look up words by root meanings. 
I am exploring both machine learning and rule based approaches towards this goal. At the moment, I have over 5,000 words tagged with their know prefix and/or suffix.
Feel free to reach out if you want this data/code. It's very much a work-in-progress. 

"Morphemes" are the smallest parts of words that contain meaning on their own. There is inflectional and derivational morphology. 
Inflectional morphology has to do with changes to words that arrise from grammar. This project isn't really focused on that.
In fact, if you look at the repo for Teanglann, there is an extensive morphological data base (in JSON files) with inflected forms! 

Examples: 
- adding s to cat to make it the plural "cats"
- initial mutations in Irish like leniting a regular verb to make it past tense: tóg -> thóg

This project is more concerned with derivational morphology which has to do with separating words into their roots.

Examples:
- feargach ("angry") -> fearg ("anger") + -ach ("connected to" or "having")
- rófhada ("too far") -> ró ("too much") + fada ("long" or "far")

Benefits of this could include potentially aiding "sense-by-sense" translation not just from Irish to English or vice versus, but also for interlingual translation (between the dialects). It could also be used as a teaching aid to help students learn to break down words and guess at the meaning of words they haven't seen before. 

There is a fair amount of evidence that morpheme segmentation or sub-word tokenisation that captures morphological features can aid in NLP tasks for "morphologically rich" 
languages such as Irish, Russian, Hungarian, etc... 
Similar to how it may help students figure out words, it seems that sub-word tokenisation can help translate "out of dictionary" terms.
(for my sources please see the bibliography of mine and Ellen's paper). 

