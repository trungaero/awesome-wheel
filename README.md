# awesome-wheel
Web game for english club


# Input
Provide a list of ```<word>;<definition>``` in the file *list_of_words.txt*. Put one word per line

# Reveal modes
Three modes of revealing hidden letters:
- Reveal by specific letter (case-insensitive) e.g: 'A', 'a'. Note: just one letter is accepted at a time
- Reveal by position which refers to the literal index from left to right e.g: 1, 2, 3 
- Reveal randomly, player has to specify the number of letters. Letters will be revealed randomly among the remaining hidden ones. Note that the complete word can be revealed using this mode and specifying the total number of remaining letters.

# Reset timer
Each time an attempt is made, the timer will be reset. To reset the timer intentionally, hit *Reset* button
