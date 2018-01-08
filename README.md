# Silly Gamble
Fair, simple and open source game to gamble bitcoin. Currently Silly Gamble hosts a single game named Monty Hall, named after the [Monty Hall paradox](https://en.wikipedia.org/wiki/Monty_Hall_problem).

![Silly Gamble](https://github.com/anderson-joyle/silly-gamble/blob/master/montyhall_game.png)

## Deposits
In order to play, player needs to deposit a certain amount to a specific [wallet address](https://www.sillygamble.com/howto/). Once transaction is confirmed, the player can come back to home page and type in his bitcoin wallet address.
> NOTE: Avoid to deposit funds from multiple wallet for now. 

## Instructions and rules
Very simple:
* Four cards are going to be displayed. Choose one.
* Your card will be mark as selected and a random card (which doesn't contain the prize) will be releaved.
* Choose between to keep your original card or change your mind.

And thats it.

## Provable
When a new game starts, game data is generated backend side. This game data contains which card holds the prize, game cards set and salt random values.
A SHA1 is extracted from game data and it is visible durring all game steps. At the end, player has the chance to download this data and compare its SHA1 content with the one from game session. 