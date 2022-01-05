# Wordless

Wordless is the #1 app for helping you cheat at Wordle, which is sure to make you popular at parties.

Run Wordless with the following:

```bash
pip install -r requirements.txt
python wordless.py
```

Wordless will prompt you to enter grey, yellow, and green letters and give you a set of words you can guess to continue.

```
Welcome to Wordless! The #1 app in the world for helping you cheat at Wordle.

So far we know:
Missing letters:
[]
Letters that are present but in the wrong positions:
[]
Letters that are present and in the correct positions:
[]
Unknown letters:
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

Current number of candidates: 12972

Maybe try one of these words next:
aeros, soare, arose, aesir, arise, reais, raise, serai, aloes, laser

Input the word you guessed: aeros
Input the colors that correspond to aeros
'b' for a black letter, 'y' for a yellow letter, 'g' for a green letter
Input colors: byybb

So far we know:
Missing letters:
['a', 'o', 's']
Letters that are present but in the wrong positions:
[('e', 1), ('r', 2)]
Letters that are present and in the correct positions:
[]
Unknown letters:
['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y', 'z']

Current number of candidates: 349

Maybe try one of these words next:
uteri, urite, tried, tride, rudie, niter, inter, inert, nitre, trine
```
