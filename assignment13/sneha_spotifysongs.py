#!/usr/bin/python

"""
Assignment 13: Spotify songs next and previous.
"""

class Nodes:
    def __init__(self,value):
        self.value=value
        self.next=None
        self.previous=None
        
song1 = Nodes("Spirits")
song2 = Nodes("Wolves")
song3 = Nodes("Last Christmas")
song4 = Nodes("Bilionera")
song5 = Nodes("Under The Influence")

for i in range(1,6):
    if exec(f"song{i} != song5"):
        exec(f"song{i}.next = 'song{i+1}'")

"""
song1.next = song2
song2.next = song3
song3.next = song4
song4.next = song5

song5.previous = song4
song4.previous = song3
song3.previous = song2
song2.previous = song1
"""

song = song1

while song!=song5:
    print(song.value)
    song = song.next
print(song5.value)

while song!=song1:
    print(song.value)
    song = song.previous
print(song1.value)

