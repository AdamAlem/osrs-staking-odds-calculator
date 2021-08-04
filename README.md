# osrs-staking-odds-calculator
Simple Markov chain based calculator that gives fair staking odds for different stats and melee set-ups in OSRS

# How to use

Create both players by typing p1=Player(), p2=Player(). Once these objects are created, you can use built-in functions to change the weapon, armour, stats or bonuses for each player.

Calculate the odds of a death match by using the function Calc(p1, p2, food=[0,0]). Where food=[0,0] is the amount of food each player has in cumulative hp.
