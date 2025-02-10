"""
############################## Homework TicTacTo ##############################

% Student Name: Julia Campbell

% Student Unique Name: juliacam

% Lab Section 00X: 102

% I worked with the following classmates:

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""


# CONSTANTS
PLAYER_NAMES = ["Nobody", "X", "O"]


# FUNCTIONS
def player_name(player_id) -> str:
    '''return the name of a player with a specified ID

    Looks up the name in the PLAYER_NAMES global list

    Parameters
    ----------
    player_id: int
        player's id, which is an index into PLAYER_NAMES

    Returns
    -------
    string
        the player's name

    '''
    return PLAYER_NAMES[player_id]


def display_board(board) -> None:
    '''display the current state of the board

    board layout:
    1 | 2 | 3
    4 | 5 | 6
    7 | 8 | 9

    Numbers are replaced by players' names once they move.
    Iterate through the board and choose the right thing
    to display for each cell.

    Parameters
    ----------
    board: list
        the playing board

    Returns
    -------
    None
    '''

    board_to_show = "" # string that will display the board, starts empty
    for i in range(len(board)):
        if board[i] == 0: # 0 means unoccupied
            # displayed numbers are one greater than the board index
            board_to_show += str(i + 1) # display cell number
        else:
            board_to_show += player_name(board[i]) # display player's mark
        if (i + 1) % 3 == 0: # every 3 cells, start a new row
            board_to_show += "\n"
        else:
            board_to_show += " | " # within a row, divide the cells
    print()
    print(board_to_show)


def make_move(player, board) -> None:
    '''allows a player to make a move in the game

    displays who's move it is (X or O)
    prompts the user to enter a number 1-9
    validates input, repeats until valid input is entered
    checks move is valid (space is unoccupied) is entered
    updates/modifies the board in place when a valid move is entered

    Parameters
    ----------
    player: int
        the id of the player to move (1 = X, 2 = O)

    board: list
        the board upon which to move
        the board is modified in place when a valid move is entered
    '''
    # Display who's move it is
    print(f"Player {player_name(player)}'s move.")

    # Prompt the user to enter a number 1-9
    while True:
        try:
            move = int(input("Enter a number from 1-9: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number from 1-9: ")

    # Validate input and repeat until valid input is entered
    while move < 1 or move > 9 or board[move - 1] != 0:
        if move < 1 or move > 9:
            move = int(input("Invalid input. Please enter a number from 1-9: "))
        elif board[move - 1] != 0:
            move = int(input("Invalid input. Please enter a number corresponding to an empty space: "))

    # Update the board in place when a valid move is entered
    board[move - 1] = player

    # Display the updated board
  #  display_board(board)


def check_win_horizontal(board) -> int:
    # TODO: write docstring
    '''checks the board for a horizontal win

    if the top, middle, or bottom row are all the same player, then that player wins

    Parameters
    -----------
    board: list
        the board to check

    Returns
    -----------
    int
    '''
    if (board[0] != 0 and 
        board[0] == board[1] and 
        board[0] == board[2]):
        return board[0]
    if (board[3] != 0 and
        board[3] == board[4] and 
        board[3] == board[5]):
        return board[3]
    if (board[6] != 0 and
        board[6] == board[7] and 
        board[6] == board[8]):
        return board[6]
    return 0


def check_win_vertical(board) -> int :
    # TODO: write docstring
    '''checks the board for a vertical win

    if the left, middle, or right column are all the same player, then that player wins

    Parameters
    -----------
    board: list
        the board to check

    Returns
    -----------
    int
        the player ID of the winner. 0 means no winner found.
    '''
    # TODO: implement function
    if (board[0] != 0 and 
        board[0] == board[3] and 
        board[0] == board[6]):
        return board[0]
    if (board[1] != 0 and
        board[1] == board[4] and 
        board[1] == board[7]):
        return board[1]
    if (board[2] != 0 and
        board[2] == board[5] and 
        board[2] == board[8]):
        return board[2]
    return 0


def check_win_diagonal(board)-> int :
    # TODO: write docstring
    '''checks the board for a diagonal win

    if there are 3 boxes diagonally of all the same player, then that player wins

    Parameters
    -----------
    board: list
        the board to check

    Returns
    -----------
    int
        the player ID of the winner. 0 means no winner found.
    '''
    # TODO: implement function
    if (board[0] != 0 and 
        board[0] == board[4] and 
        board[0] == board[8]):
        return board[0]
    if (board[2] != 0 and
        board[2] == board[4] and 
        board[2] == board[6]):
        return board[2]
    return 0


def check_win(board) -> int:
    '''checks a board to see if there's a winner

    delegates to functions that check horizontally, vertically, and
    diagonally to see if there is a winner. Returns the first winner
    found in the case of multiple winners.

    Parameters
    ----------
    board: list
        the board to check

    Returns
    -------
    int
        the player ID of the winner. 0 means no winner found.
    '''

    winner = check_win_horizontal(board)
    if (winner != 0):
        return winner

    winner = check_win_vertical(board)
    if (winner != 0):
        return winner

    return check_win_diagonal(board)


def next_player(current_player) -> int:
    '''determines who goes next

    given the current player ID, returns the player who should 
    go next

    Parameters
    ----------
    current_player: int
        the id of the player who's turn it is now

    Returns
    -------
    int
        the id of the player to go next
    '''
    # Alternate between player 1 (X) and player 2 (O)
    if current_player == 1:
        return 2
    else:
        return 1

# MAIN PROGRAM (INDENT LEVEL 0)

# GLOBAL VARIABLES
# PLease only add the code to print the winner
# Do not delete anything here
# Or the autograder might CRASH
def main() -> int:
    board = [0, 0, 0,   # top row:    indices 0, 1, 2
             0, 0, 0,   # middle row: indices 3, 4, 5
             0, 0, 0]   # bottom row: indices 6, 7, 8

    player = 1          # X goes first
    moves_left = 9      # number of moves so far
    winner = 0          # "Nobody" is winning to start

    while(moves_left > 0 and winner == 0):
        display_board(board)
        make_move(player, board)
        winner = check_win(board)
        player = next_player(player)
        moves_left -= 1

    display_board(board) # Displays the winning board

    if winner !=0:
        print("Congratulations! Player", player_name(winner), "wins!")
    else:
        print("It's a tie!")

    return winner


# TODO: write code to display the correct winner.
# NOTE: where you implement this (in the while loop or outside it) is up to you to decide,
# but your program should behave like the sample output
# NOTE: You may also find it helpful to display the board one final time to make sure
# you are correctly identifying the winner, but you will not be graded on that.

if __name__ == "__main__":
    main()
    print("Game over, thanks for playing!")

