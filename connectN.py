# Design and implement a multi-round console-based game called Connect N.
# The goal for players is to align their respective markers in N consecutive positions in any direction on a board.

from enum import Enum

'''
This is the start of the HW.
If there is any conflict between the doc string and the HW document,
please follow the instruction in the HW document.
Good Luck and have fun !
'''

class Notation(Enum):
    """Enumeration for representing different types of notations in the game.

    Attributes:
        EMPTY (int): Represents an empty cell on the board.
        PLAYER1 (int): Represents a cell occupied by Player 1.
        PLAYER2 (int): Represents a cell occupied by Player 2.
    """

    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

class Player:
    """Represents each player in the game, keeping track of their details and performance.

    Attributes:
        __playerName (str): The name of the player.
        __playerNotation (Notation): The notation (symbol) used by the player on the board.
        __curScore (int): The current score of the player.

    Args:
        playerName (str): The name of the player.
        playerNotation (Notation): The notation (symbol) used by the player.
        curScore (int): The initial score of the player.
    """

    def __init__(self, playerName: str, playerNotation: Notation, curScore: int) -> None:
        self.__playerName = playerName
        self.__playerNotation = playerNotation
        self.__curScore = curScore


    def display(self):
        """Return the display string for the player."""
        return print(f"Player: {self.__playerName}, Notation: {self.__playerNotation.name}, Score: {self.__curScore}")

    def addScoreByOne(self) -> None:
        """Increments the player's score by one."""
        self.__curScore += 1

    def getScore(self) -> int:
        """Returns the current score of the player."""
        return self.__curScore

    def getName(self) -> str:
        """Returns the name of the player."""
        return self.__playerName

    def getNotation(self) -> Notation:
        """Returns the notation used by the player."""
        return self.__playerNotation

class Board:
    """Handle the game board operations and check for winning conditions.

    Attributes:
        __rowNum (int): Number of rows in the board.
        __colNum (int): Number of columns in the board.
        __grid (list): 2D list representing the game board.

    Args:
        rowNum (int): Number of rows in the board.
        colNum (int): Number of columns in the board.
    """

    def __init__(self, rowNum: int, colNum: int) -> None:
        """Initialize the board with empty notations."""
        self.__rowNum = rowNum
        self.__colNum = colNum
        self.__grid = [[Notation.EMPTY for _ in range(self.__colNum)] for _ in range(self.__rowNum)]

    def initGrid(self) -> None:
        """Initializes the game board with empty cells."""
        self.__grid = [[Notation.EMPTY for _ in range(self.__colNum)] for _ in range(self.__rowNum)]

    def getColNum(self) -> int:
        """Returns the number of columns in the board."""
        return self.__colNum

    def placeMark(self, colNum: int, mark: Notation) -> bool:
        """Attempt to place a player's mark in a column, returning success status.

        Args:
            colNum (int): The column number where the mark is to be placed.
            mark (Notation): The mark to be placed on the board.

        Returns:
            bool: True if the mark was successfully placed, False otherwise.
        """
        if colNum < 0 or colNum >= self.__colNum: # It should be within the range of the board's columns and not a negative integer.
            print("Error: Invalid column number.")
            return False
        elif self.__grid[0][colNum] != Notation.EMPTY: # Check if the top cell of the specified column is already occupied.
            print("Error: Column is full.")
            return False
        elif mark == Notation.EMPTY: # Validate if the mark provided is Notation.EMPTY.
            print("Error: Invalid marker.")
            return False
        else: # Iterate through the cells of the specified column from bottom to top and place the mark in the first empty cell found.
            for i in range(self.__rowNum - 1, -1, -1):
                if self.__grid[i][colNum] == Notation.EMPTY:
                    self.__grid[i][colNum] = mark
                    return True

    def checkFull(self) -> bool:
        """Checks if the board is completely filled.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for row in range(self.__rowNum):
            for col in range(self.__colNum):
                if self.__grid[row][col] == Notation.EMPTY:
                    return False
        return True

    def display(self) -> None:
        """Displays the current state of the board."""
        boardStr = '' # Initialize an empty string to store the board representation.
        for i in range(self.__rowNum): # Loop through each row in the board.
            for j in range(self.__colNum):
                if self.__grid[i][j] == Notation.EMPTY: # For each cell in the row: append 'O' if the cell contains Notation.EMPTY.
                    boardStr += 'O '
                elif self.__grid[i][j] == Notation.PLAYER1: # Append 'R' if the cell contains Notation.PLAYER1.
                    boardStr += 'R '
                elif self.__grid[i][j] == Notation.PLAYER2: # Append 'Y' if the cell contains Notation.PLAYER2.
                    boardStr += 'Y '
            boardStr += '\n' # After processing each row, append a newline character to boardStr.
        print("Current Board is:\n" + boardStr) # Print the current board.

    # Private methods for internal use
    def __checkWinHorizontal(self, target: int) -> Notation | None:
        """Check and return winner Notation based on horizontal alignment.
        'target' represents the number of markers needed to become a winner
        If there is a winner return the winner Notation, otherwise return None."""
        for row in range(self.__rowNum): # Loop through each row in the board.
            count = 0 # Initialize the counter to keep track of the number of consecutive marks.
            lastNotation = Notation.EMPTY # Initialize a variable to store the last notation encountered.
            for col in range(self.__colNum): # Loop through each column in the board.
                cell = self.__grid[row][col] # Get the notation of the current cell.
                if cell == lastNotation and cell != Notation.EMPTY: # If the current cell's notation is the same as the last notation and not empty, increment the counter by 1.
                    count += 1
                    if count == target: # If the counter reaches the target number of consecutive marks, return the notation of the winning player.
                        return lastNotation
                else: # If the current cell's notation is different from the last notation or is empty, reset the counter to 1 and update the last notation to current cell's notation.
                    count = 1
                    lastNotation = cell

    def __checkWinVertical(self, target: int) -> Notation | None:
        """Check and return winner Notation based on vertical alignment."""
        for col in range(self.__colNum): # Loop through each column in the board.
            count = 0 # Initialize the counter to keep track of the number of consecutive marks.
            lastNotation = Notation.EMPTY # Initialize a variable to store the last notation encountered.
            for row in range(self.__rowNum): # Loop through each row in the board.
                cell = self.__grid[row][col] # Get the notation of the current cell.
                if cell == lastNotation and cell != Notation.EMPTY: # If the current cell's notation is the same as the last notation and not empty, increment the counter by 1.
                    count += 1
                    if count == target: # If the counter reaches the target number of consecutive marks, return the notation of the winning player.
                        return lastNotation
                else: # If the current cell's notation is different from the last notation or is empty, reset the counter to 1 and update the last notation to current cell's notation.
                    count = 1
                    lastNotation = cell

    def __checkWinOneDiag(self, target: int) -> Notation | None:
        """Check and return winner Notation based on one diagonal alignment."""
        for i in range(self.__rowNum - target + 1): # Loop through the rows in the board.
            count = 0 # Initialize the counter to keep track of the number of consecutive marks.
            lastNotation = Notation.EMPTY # Initialize a variable to store the last notation encountered.
            for j in range(target): # Loop through the target number of cells in the diagonal direction.
                cell = self.__grid[i + j][j]
                if cell == lastNotation and cell != Notation.EMPTY: # If the current cell's notation is the same as the last notation and not empty, increment the counter by 1.
                    count += 1
                    if count == target: # If the counter reaches the target number of consecutive marks, return the notation of the winning player.
                        return lastNotation
                else: # If the current cell's notation is different from the last notation or is empty, reset the counter to 1 and update the last notation to current cell's notation.
                    count = 1
                    lastNotation = cell

    def __checkWinAntiOneDiag(self, target: int) -> Notation | None:
        """Check and return winner Notation based on anti-diagonal alignment."""
        for i in range(self.__rowNum - target + 1): # Loop through the rows in the board.
            count = 0 # Initialize the counter to keep track of the number of consecutive marks.
            lastNotation = Notation.EMPTY # Initialize a variable to store the last notation encountered.
            for j in range(target): # Loop through the target number of cells in the anti-diagonal direction.
                cell = self.__grid[i + j][j]
                if cell == lastNotation and cell != Notation.EMPTY: # If the current cell's notation is the same as the last notation and not empty, increment the counter by 1.
                    count += 1
                    if count == target: # If the counter reaches the target number of consecutive marks, return the notation of the winning player.
                        return lastNotation
                else: # If the current cell's notation is different from the last notation or is empty, reset the counter to 1 and update the last notation to current cell's notation.
                    count = 1
                    lastNotation = cell

    def __checkWinDiagonal(self, target: int) -> Notation | None:
        """ Check and return winner Notation based on diagonal alignments."""
        result = self.__checkWinOneDiag(target)
        if result:
            return result
        result = self.__checkWinAntiOneDiag(target)
        if result:
            return result
        return None

    def checkWin(self, target: int) -> Notation | None:
        """Check for any winning condition on the board and return the winner's Notation or None.
        The checkWin function should call the other checker functions and return the winner. Return None if there is not.

        Args:
            target (int): The number of consecutive marks needed for a win.

        Returns:
            Notation or None: The notation of the winning player, or None if there is no winner.
        """
        if self.__checkWinHorizontal(target):
            return self.__checkWinHorizontal(target)
        elif self.__checkWinVertical(target):
            return self.__checkWinVertical(target)
        elif self.__checkWinDiagonal(target):
            return self.__checkWinDiagonal(target)
        else:
            return None

class Game:
    """Manage the game's logic, including player turns, rounds, and overall game progression.
    Notice: PLAYER1 always goes first.

    Args:
        rowNum (int): Number of rows in the game board.
        colNum (int): Number of columns in the game board.
        connectN (int): Number of consecutive marks needed for a win.
        targetScore (int): The score a player needs to reach to win the game.
        playerName1 (str): Name of the first player.
        playerName2 (str): Name of the second player.
    """

    def __init__(self, rowNum: int, colNum: int, connectN: int, targetScore: int, playerName1: str, playerName2: str) -> None:
        """Initialize the game."""
        self.__board = Board(rowNum, colNum)  # Initialize a Board instance with (rowNum, colNum) and set it to the __board attribute.
        self.__connectN = connectN  # Set the number of consecutive marks needed for a win.
        self.__targetScore = targetScore  # Set the target score to win the game.
        player1 = Player(playerName1, Notation.PLAYER1, 0)  # Initialize the first player instance with Notation.PLAYER1 and playerName1.
        player2 = Player(playerName2, Notation.PLAYER2, 0)  # Initialize the second player instance with Notation.PLAYER2 and playerName2.
        self.__playerList = [player1, player2]  # Store the instances in __playerList attribute.
        self.__curPlayer = player1  # Set the __curPlayer to the first player instance reference.


    def __playBoard(self, curPlayer: Player) -> None:
        """Handle a player's turn to play on the board.

        Args:
            curPlayer (Player): The current player who is making the move.
        """
        isPlaced = False # Initialize isPlaced to False.
        while not isPlaced: # Iterate until a valid move is made.
            try: # Prompt the current player to enter a column number to place their mark.
                colNum = input(f"{curPlayer.getName()}, enter the column number to place your mark: ")
                if not colNum.isdigit() or colNum.startswith('00'): # Check if the input is a valid integer and does not start with '0'.
                    print("Invalid input. Please enter a valid column number.")
                else:
                    colNum = int(colNum)
                    if colNum < 0 or colNum >= self.__board.getColNum(): # Check if the column number is within the valid range.
                        print("Invalid column number. Please try again.")
                    else: # If the column number is valid, attempt to place the mark on the board.
                        if self.__board.placeMark(colNum, curPlayer.getNotation()):
                            isPlaced = True
                        else:
                            print("Column is full or invalid marker. Please try again.")
            except ValueError: # Handle the exception if the input is not a valid integer.
                print("Invalid input. Please enter a valid column number.")

    def __changeTurn(self) -> None:
        """Switch the active player by switching the __curPlayer attribute."""
        if self.__curPlayer == self.__playerList[0]:
            self.__curPlayer = self.__playerList[1]
        else:
            self.__curPlayer = self.__playerList[0]

    def playRound(self) -> None:
        """Handle a full round of game play."""
        curWinnerNotation = None  # Initialize curWinnerNotation to None.
        self.__board.initGrid()  # Initialize the game board.
        self.__curPlayer = self.__playerList[0]  # Set the current player to the first player in the player list.
        print("Starting a new round...")  # Display a message indicating the start of a new round.

        while True:
            self.__curPlayer.display()  # Display the current player's details.
            self.__board.display()  # Display the current state of the board.
            self.__playBoard(self.__curPlayer)  # Let the current player play their turn.
            curWinnerNotation = self.__board.checkWin(self.__connectN)  # Check if there is a winner.

            if curWinnerNotation:
                print(f"{self.__curPlayer.getName()} wins this round!")  # Announce the winner by printing their name.
                self.__curPlayer.addScoreByOne()  # Increase the winner's score by 1.
                self.__board.display()  # Display the final state of the board.
                break

            if self.__board.checkFull():
                print("The board is full. No winner for this round.")  # Announce that the board is full and there is no winner.
                break

            self.__changeTurn()  # Switch to the other player.

    def play(self) -> None:
        """Manage the entire game until a player reaches the target score or quits."""
        while True:
            self.playRound()
            if self.__playerList[0].getScore() >= self.__targetScore or self.__playerList[1].getScore() >= self.__targetScore:
                print("Game Over")
                print(self.__playerList[0].display())
                print(self.__playerList[1].display())
                break

"""
############################## Homework ConnectN ##############################

% Student Name: Julia Campbell

% Student Unique Name: juliacam

% Lab Section 00X: 102

% I worked with the following classmates:

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def main():
    """Main function to start the game."""
    game = Game(4, 4, 3, 2, 'P1', 'P2')
    game.play()

if __name__ == "__main__":
    main()
