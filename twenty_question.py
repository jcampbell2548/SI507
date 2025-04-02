class TwentyQuestions:
    def __init__(self):
        """
        Initialize the TwentyQuestions class with predefined small and medium trees.
        Sets the current tree to the small tree by default.
        """
        self.smallTree = (
            "Is it bigger than a breadbox?",
            ("an elephant", None, None),
            ("a mouse", None, None),
        )
        self.mediumTree = (
            "Is it bigger than a breadbox?",
            ("Is it gray?", ("an elephant", None, None), ("a tiger", None, None)),
            ("a mouse", None, None),
        )
        self.currentTree = self.smallTree  # Default tree

    def inputChecker(self, userIn: str) -> bool:
        """
        aka(yes(userIn))
        Check if the user's input is an affirmative response.

        Parameters
        ----------
        userIn : str
            The input string from the user.

        Returns
        -------
        bool
            True if the input is an affirmative response ('y', 'yes', 'yup', 'sure'), else False.
        """
        affirmative_responses = ["y", "yes", "yup", "sure"]
        return userIn.strip().lower() in affirmative_responses

    def checkIfLeaf(self, curNode) -> bool:
        """
        Determine if the given node is a leaf node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the node is a leaf (both children are None), else False.
        """
        return curNode[1] is None and curNode[2] is None

    def simplePlay(self, curNode) -> bool:
        """
        Conduct a single playthrough of the game using the current node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the player successfully guesses the item, else False.
        """
        # If the tree is a leaf, make a guess
        if self.checkIfLeaf(curNode):
            user_input = input(f"Is it {curNode[0]}? (yes/no): ").strip().lower()
            if self.inputChecker(user_input):
                return True
            else:
                return False
        else:
            # Ask the question in the current tree
            user_input = input(curNode[0] + " (yes/no): ").strip().lower()
            if self.inputChecker(user_input):
                # Recur on the "yes" subtree
                return self.simplePlay(curNode[1])
            else:
                # Recur on the "no" subtree
                return self.simplePlay(curNode[2])

    def createNode(self, userQuestion: str, userAnswer: str, isCorrectForQues: bool, curNode: tuple) -> tuple:
        """
        Create a new node in the decision tree.

        Parameters
        ----------
        userQuestion : str
            The question to differentiate the new answer from the current node.
        userAnswer : str
            The answer provided by the user.
        isCorrectForQues : bool
            True if the userAnswer is the correct response to the userQuestion.
        curNode : tuple
            The current node in the decision tree at which the game has arrived.
            This node typically represents the point in the game
            where the player's guess was incorrect,
            and a new question-answer pair needs to be
            added to refine the tree.

        Returns
        -------
        tuple
            The new node created with the user's question and answer
            and curNode
        """
        if isCorrectForQues:
            # If the user's answer is the correct response to the question,
            # the "yes" branch should point to the new answer, and the "no" branch should point to the current node.
            return (userQuestion, (userAnswer, None, None), curNode)
        else:
            # If the user's answer is not the correct response to the question,
            # the "no" branch should point to the new answer, and the "yes" branch should point to the current node.
            return (userQuestion, curNode, (userAnswer, None, None))

    def playLeaf(self, curNode) -> tuple:
        """
        Handle gameplay when a leaf node is reached in the decision tree. This method is called when
        the game's traversal reaches a leaf node, indicating a guess at the player's thought.
        If the guess is incorrect, the method will
        1. prompts the player for the correct answer
        2. prompts the player for a distinguishing question
        3. ask user what is the answer for the new input item to this distinguishing question(refer the io result of play in the homework doc)
           notice the node should follow (tree question, (node for answer yes), (node for answer no))
        4. creating a new node in the tree for future gameplay. It should call self.createNode(...)

        Parameters
        ----------
        curNode : tuple
            The current leaf node in the decision tree. A leaf node is represented as a tuple with the guessed 
            object as the first element and two `None` elements, signifying that it has no further branches.

        Returns
        -------
        tuple
            The updated node based on user input. If the player's response indicates that the initial guess was 
            incorrect, this method returns a new node that includes the correct answer and a new question 
            differentiating it from the guessed object. If the guess was correct, it simply returns the unchanged 
            `curNode`.

        Notes
        -----
        The method interacts with the player to refine the decision tree. It's a crucial part of the learning 
        aspect of the game, enabling the tree to expand with more nuanced questions and answers based on 
        player feedback.
        """
        while True:
            user_input = input(f"Is it {curNode[0]}? (yes/no): ").strip().lower()
            if self.inputChecker(user_input):
                return curNode  # Return the unchanged node if the guess is correct
            elif user_input in ["n", "no"]:
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")

        correct_answer = input("What were you thinking of? ").strip()
        distinguishing_question = input(f"Give me a question to distinguish {correct_answer} from {curNode[0]}: ").strip()
        while True:
            answer_for_new_item = input(f"What is the answer for {correct_answer} to the question '{distinguishing_question}'? (yes/no): ").strip().lower()
            if self.inputChecker(answer_for_new_item):
                is_correct_for_question = True
                break
            elif answer_for_new_item in ["n", "no"]:
                is_correct_for_question = False
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")

        new_node = self.createNode(distinguishing_question, correct_answer, is_correct_for_question, curNode)
        return new_node

    def play(self, curNode) -> tuple:
        """
        Conduct gameplay starting from the given node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        tuple
            The updated tree after playing from the given node.
        """
        if self.checkIfLeaf(curNode):
            return self.playLeaf(curNode)
        else:
            while True:
                user_input = input(curNode[0] + " (yes/no): ").strip().lower()
                if self.inputChecker(user_input):
                    updated_yes_subtree = self.play(curNode[1])
                    return (curNode[0], updated_yes_subtree, curNode[2])
                elif user_input in ["n", "no"]:
                    updated_no_subtree = self.play(curNode[2])
                    return (curNode[0], curNode[1], updated_no_subtree)
                else:
                    print("Invalid input. Please answer 'yes' or 'no'.")

    def playRound(self) -> None:
        """
        Execute a single round of the game, starting from the current state of the currentTree attribute. This method
        calls the 'play' method to navigate through the tree. It then updates the 'currentTree'
        attribute with the potentially modified tree resulting from this round of gameplay.


        Returns
        -----
        None
        """
        # Call the play method starting from the current tree
        self.currentTree = self.play(self.currentTree)


    def saveTree(self, node, treeFile) -> None:
        """
        Recursively save the decision tree to a file.

        Parameters
        ----------
        node : tuple
            The current node in the decision tree.
        treeFile : _io.TextIOWrapper
            The file object where the tree is to be saved.
        """
        if node is None:
            return

        # Check if the node is a leaf
        if self.checkIfLeaf(node):
            # Write the leaf node to the file
            treeFile.write("Leaf\n")
            treeFile.write(f"{node[0]}\n")
        else:
            # Write the internal node (question) to the file
            treeFile.write("Internal node\n")
            treeFile.write(f"{node[0]}\n")
            # Recursively save the "yes" subtree
            self.saveTree(node[1], treeFile)
            # Recursively save the "no" subtree
            self.saveTree(node[2], treeFile)

    def saveGame(self, treeFileName) -> None:
        """
        Save the current state of the game's decision tree to a specified file. This method opens the file
        with the given filename and writes the structure of the current decision tree to it. The tree is saved
        in a txt format.

        The method uses the 'saveTree' function to perform the recursive traversal and writing of the tree
        structure. Each node of the tree is written to the file with its type ('Leaf' or 'Internal node')
        followed by its content (question or object name).

        Important: the format of the txt file should be exactly the same as the ones in our doc to pass the autograder.

        Parameters
        ----------
        treeFileName : str
            The name of the file where the current state of the decision tree will be saved. The file will be
            created or overwritten if it already exists.

        """
        try:
            # Open the file in write mode
            with open(treeFileName, "w") as treeFile:
                # Use the saveTree method to write the tree structure to the file
                self.saveTree(self.currentTree, treeFile)
            print(f"Game saved successfully to {treeFileName}.")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")


    def loadTree(self, treeFile) -> tuple:
        """
        Recursively read a binary decision tree from a file and reconstruct it.

        Parameters
        ----------
        treeFile : _io.TextIOWrapper
            An open file object to read the tree from.

        Returns
        -------
        tuple
            The reconstructed binary tree.
        """
        pass

    def loadGame(self, treeFileName) -> None:
        """
        Load the game state from a specified file and update the current decision tree. This method opens the 
        file with the given filename and reconstructs the decision tree based on its contents. 

        The method employs the 'loadTree' function to perform recursive reading of the tree structure from the 
        file. Each node's type ('Leaf' or 'Internal node') and content (question or object name) are read and 
        used to reconstruct the tree in memory. This restored tree becomes the new 'self.currentTree' of the game.

        Parameters
        ----------
        treeFileName : str
            The name of the file from which the game state will be loaded. The file should exist and contain a 
            previously saved decision tree.

        """
        pass


    def printTree(self):
        self._printTree(tree = self.currentTree)

    def _printTree(self, tree, prefix = '', bend = '', answer = ''):
        """Recursively print a 20 Questions tree in a human-friendly form.
        TREE is the tree (or subtree) to be printed.
        PREFIX holds characters to be prepended to each printed line.
        BEND is a character string used to print the "corner" of a tree branch.
        ANSWER is a string giving "Yes" or "No" for the current branch."""
        text, left, right = tree
        if left is None  and  right is None:
            print(f'{prefix}{bend}{answer}It is {text}')
        else:
            print(f'{prefix}{bend}{answer}{text}')
            if bend == '+-':
                prefix = prefix + '| '
            elif bend == '`-':
                prefix = prefix + '  '
            self._printTree(left, prefix, '+-', "Yes: ")
            self._printTree(right, prefix, '`-', "No:  ")
"""
############################## Homework 20questions ##############################

% Student Name: Julia Campbell

% Student Unique Name: juliacam

% Lab Section 00X: 102

% I worked with the following classmates:

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def validateFileName(file_name: str) -> bool:
    """
    Validate the given file name.

    Parameters
    ----------
    file_name : str
        The file name to validate.

    Returns
    -------
    bool
        True if the file name is valid, False otherwise.
    """
    # Add validation logic here (e.g., check for invalid characters, length, etc.)
    return bool(file_name.strip())


def main():
    """
    Main function to run the 20 Questions game.

    Print a welcome message, and start playing the game with the smallTree.
    Ask the user if they'd like to play again when finished.
    Play again if yes, otherwise end the game.
    When the game is over, ask the user if they would like to save the file.
    If so, ask for a file name.
    """
    print("Welcome to 20 Questions!")
    game = TwentyQuestions()
    game.currentTree = game.smallTree  # Start with the smallTree

    while True:
        game.playRound()
        while True:
            play_again = input("Would you like to play again? (yes/no): ").strip().lower()
            if game.inputChecker(play_again):
                break
            elif play_again in ["n", "no"]:
                play_again = False
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")
        if not play_again:
            break

    while True:
        save_tree = input("Would you like to save this tree for later? (yes/no): ").strip().lower()
        if game.inputChecker(save_tree):
            while True:
                file_name = input("Please enter a file name: ").strip()
                if validateFileName(file_name):
                    game.saveGame(file_name)
                    print("Thank you! The file has been saved.")
                    break
                else:
                    print("Invalid file name. Please try again.")
            break
        elif save_tree in ["n", "no"]:
            break
        else:
            print("Invalid input. Please answer 'yes' or 'no'.")

    print("Bye!")


if __name__ == '__main__':
    main()
