## De-Jargonizer

This de-jargonizer is based on the original [Jargon
Project](https://github.com/NoamAndRoy/JargonProject). This library provides
two functions `get_jargon_words()` which returns a list of jargon words and the
number of occurrences of the word in the input text; and `get_jargon_score()`
which calculates the jargon score of the input text. The jargon score is
calculated by the following formula:

```
jargon_score = 100 * (1 - num_of_uncommon_words / total_words - num_of_rare_words / total_words)
```

