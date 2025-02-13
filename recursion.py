# Building an electronic cash register and the software to run it
# Given an amount of money and a list of coin types, we want to find the smallest number of coins that will make up that amount of money
# Write a function called 'change(amount, coins)'
# Where the 'amount' is a non-negative integer indicating the amount of change to be made
# And 'coins' is a list of integers indicating the coin types available
# The function should return a non-negative integer indicating the minimum number of coins required to make up the given 'amount'
# If there is no possible solution, return 'math.inf'

# Define a recursive function called 'change'
def change(amount: int, coins: list) -> int:
    '''determines the minimum number of coins needed to make up a given amount

    Parameters:
    -----------
    amount: int
        the amount of money to make up

    coins: list
        the coin types available

    Returns:
    --------
    int
        the minimum number of coins needed to make up the given amount
    '''
    # Import the math module
    import math

    # Base case: if the amount is 0, return 0
    if amount == 0:
        return 0

    # Initialize the minimum number of coins to infinity
    min_coins = math.inf

    # Iterate through the coin types
    for coin in coins:
        # If the coin value is less than or equal to the amount
        if coin <= amount:
            # Recursively call the function with the reduced amount
            # and add 1 to the result to account for the current coin
            num_coins = change(amount - coin, coins) + 1
            # Update the minimum number of coins if the current result is smaller
            min_coins = min(min_coins, num_coins)

    # Return the minimum number of coins
    return min_coins

# Define a new function called 'giveChange'
# It will take the same arguments as 'change' but will return a list
# Where the first member is the minimum number of coins as an integer
# And the second member is a list of the coins in that optimal solution

def giveChange(amount: int, coins: list) -> list:
    '''determines the minimum number of coins needed to make up a given amount and the list of said coins

    Parameters:
    -----------
    amount: int
        the amount of money to make up

    coins: list
        the coin types available

    Returns:
    --------
    list
        the minimum number of coins needed to make up the given amount
        and the list of coins used to make up the amount
    '''
    # Import the math module
    import math

    # Base case: if the amount is 0, return 0
    if amount == 0:
        return [0, []]

    # Initialize the minimum number of coins to infinity
    min_coins = math.inf
    # Initialize the list of coins to an empty list
    coin_list = []

    # Iterate through the coin types
    for coin in coins:
        # If the coin value is less than or equal to the amount
        if coin <= amount:
            # Recursively call the function with the reduced amount
            # and add 1 to the result to account for the current coin
            num_coins, coins_used = giveChange(amount - coin, coins)
            num_coins += 1
            # Update the minimum number of coins if the current result is smaller
            if num_coins < min_coins:
                min_coins = num_coins
                coin_list = coins_used + [coin]

    # Return the minimum number of coins and the list of coins used
    return [min_coins, coin_list]

if __name__ == "__main__":
    change()
    giveChange()

