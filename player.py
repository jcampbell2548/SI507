from media import Media, Track, Movie
from linked_list import LinkedList
import json
class Player:
    """
    A media player class that manages a playlist of media.

    This class utilizes a doubly linked list (LinkedList) to store and manage media in a playlist.
    It provides methods for adding, removing, playing, and navigating through media.

    Attributes
    ----------
    playlist : LinkedList
        A doubly linked list that stores the media in the playlist.
    currentMediaNode : Node or None
        The current media being played, represented as a node in the linked list.
    """

    def __init__(self) -> None:
        """
        Initializes the Player with an empty playlist and None as currentMediaNode.
        """
        self.playlist = LinkedList()
        self.currentMediaNode = None

    def addMedia(self, media) -> None:
        """
        Adds a media to the end of the playlist.
        Set the currentMediaNode to the first node in the playlist,
        if currentMediaNode is None.

        Parameters
        ----------
        media : Media | Track | Movie
            The media to add to the playlist.
        """
        self.playlist.append(media)  # Add the media to the end of the playlist
        if self.currentMediaNode is None:  # Check if currentMediaNode is None
            self.currentMediaNode = self.playlist.dummyHead.next  # Set currentMediaNode to the first node in the playlist

    def removeMedia(self, index) -> bool:
        """
        Removes a media from the playlist based on its index.
        You can assume the only invalid input is invalid index.
        Set the currentMediaNode to its next, if currentMediaNode is removed,
        and remeber using _isNodeUnbound(self.currentMediaNode) to check if a link is broken.

        Parameters
        ----------
        index : int
            The index of the media to remove.

        Returns
        -------
        bool
            True if the media was successfully removed, False otherwise.
        """
        if index < 0 or index >= self.playlist.size:    # Check if the index is invalid
            return False
        self.playlist.deleteAtIndex(index) # Remove the media from the playlist
        if self.playlist._isNodeUnbound(self.currentMediaNode):  # Check if the currentMediaNode link is broken
            self.currentMediaNode = self.currentMediaNode.next  # Set the currentMediaNode to its next
        return True

    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        self.currentMediaNode = self.currentMediaNode.next  # Move currentMediaNode to the next media
        return self.currentMediaNode != self.playlist.dummyHead and self.currentMediaNode != self.playlist.dummyTail  # Return True if currentMediaNode is not the dummyNode

    def prev(self) -> bool:
        """
        Moves currentMediaNode to the previous media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the previous media, False otherwise.
        """
        self.currentMediaNode = self.currentMediaNode.prev  # Move currentMediaNode to the previous media
        return self.currentMediaNode != self.playlist.dummyHead and self.currentMediaNode != self.playlist.dummyTail  # Return True if currentMediaNode is not the dummyNode

    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media.

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        if self.playlist.size > 0:
            self.currentMediaNode = self.playlist.dummyHead.next  # Set the current media to the first media in the playlist
            return True

    def play(self) -> None:
        """
        Plays the current media in the playlist.
        Call the play method of the media instance.
        Remember currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None,
        print "The current media is empty.".
        """
        if self.currentMediaNode is None or self.currentMediaNode.data is None:  # Check if the current media is empty
            print("The current media is empty.")
        else:
            self.currentMediaNode.data.play()  # Call the play method of the media instance

    def playForward(self) -> None:
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.
        Remember each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.".
        """
        if self.playlist.size == 0: # Check if the playlist is empty.
            print("Playlist is empty.")
        else:
            current = self.playlist.dummyHead.next  # Start from the first media in the playlist
            while current != self.playlist.dummyTail:  # Iterate through the playlist
                current.data.play()  # Play the current media.
                current = current.next  # Move to the next media.

    def playBackward(self) -> None:
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.
        Remember each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.".
        """
        if self.playlist.size == 0: # Check if the playlist is empty
            print("Playlist is empty.")
        else:
            current = self.playlist.dummyTail.prev  # Start from the last media in the playlist
            while current != self.playlist.dummyHead:   # Iterate through the playlist
                current.data.play()    # Play the current media
                current = current.prev  # Move to the previous media

    def loadFromJson(self, fileName) -> None:
        """
        Loads media from a JSON file and adds them to the playlist.
        The order should be the same as the provided json file.
        You could assume the filename is always valid
        Notice, for each given json object,
        you should create instance of the correct instance type, (movie,track,media).
        You need to observe the provided json and figure how to do it.
        You could assume if a json object is not track or movie,
        it has to be a media.
        Pay attention the name of the key in each json object.
        Set the currentMediaNode to the first media in the playlist,
        if there is at least one media in the playlist.
        Remeber to use the dictionary get method.

        Parameters
        ----------
        filename : str
            The name of the JSON file to load media from.
        """
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)  # Load the JSON file
        for item in data:  # Iterate through the JSON file
            if item.get("kind") == "song":  # Check if the JSON object is a Track
                track = Track(item.get("trackName"), item.get("artistName"), item.get("releaseDate"), item.get("trackViewUrl"), item.get("collectionName"), item.get("primaryGenreName"), item.get("trackTimeMillis"))
                self.addMedia(track)  # Add the Track object to the playlist
            elif item.get("kind") == "feature-movie":  # Check if the JSON object is a Movie
                movie = Movie(item.get("trackName"), item.get("artistName"), item.get("releaseDate"), item.get("trackViewUrl"), item.get("contentAdvisoryRating"), item.get("trackTimeMillis"))
                self.addMedia(movie)  # Add the Movie object to the playlist
            else:  # The JSON object must be a Media
                media = Media(item.get("trackName"), item.get("artistName"), item.get("releaseDate"), item.get("trackViewUrl"))
                self.addMedia(media)  # Add the Media object to the playlist
        if self.playlist.size > 0:
            self.currentMediaNode = self.playlist.dummyHead.next
