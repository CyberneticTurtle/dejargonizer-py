## De-Jargonizer

This de-jargonizer is based on the original [Jargon
Project](https://github.com/NoamAndRoy/JargonProject). This library provides
three functions:

 1. `get_jargon_percent()` which returns the percentage of jargon words in the input text;
 2. `get_jargon_words()` which returns a list of jargon words and the number of occurrences of the word in the input text; and
 3. `get_jargon_score()` which calculates the jargon score of the input text. The jargon score is calculated by the following formula:
    ```
    jargon_score = 100 * (1 - num_of_uncommon_words / total_words - num_of_rare_words / total_words)
    ```

### Credits
Original Jargon Project: https://scienceandpublic.com/, https://github.com/NoamAndRoy/JargonProject <br />
cmwxyz: https://github.com/cmwxyz/word-rarity
