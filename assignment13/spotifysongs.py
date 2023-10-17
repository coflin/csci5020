#!/usr/bin/python

"""
Assignment 13: Created a playlist (list) of spotify songs and populate next and
previous songs. Uses the concept of a doubly linked list. Prints the playlist forward
and backward.
"""

def main():
    class Playlist:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.previous = None

    songs = [Playlist("Harleys in Hawaii"), Playlist("Wolves"), Playlist("Last Christmas"), Playlist("Bilionera"), Playlist("Under The Influence")]

    for i in range(len(songs) - 1):
        songs[i].next = songs[i + 1]

    for i in range(1, len(songs)):
        songs[i].previous = songs[i - 1]

    print("Print the list forward:")
    current = songs[0]
    while current is not None:
        print(current.value)
        current = current.next

    print("\nPrint the list backward:")
    current = songs[-1]
    while current is not None:
        print(current.value)
        current = current.previous

if __name__=="__main__":
    main()
