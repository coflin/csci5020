"""
Dungeons and Dragons uses a 20 sided dice to play
the game. Code an app that will simulate this die
being rolled. Indicate a critical roll if a 1 or 20 is
resulted. Update the dice roller app. Change the message to
be “Critical failure” only if a 1 is rolled, and “Critical
success” if a 20 is rolled.
"""

#!/usr/bin/python

from random import randint

roll = randint(1, 20)  # great so this works!
if roll == 1:
    print(f"Critical Failure!")
elif roll == 20:
    print(f"Critical success!")
else:
    print(f"you rolled {roll}")
