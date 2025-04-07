# Building an electronic cash register and the software to run it
# Given an amount of money and a list of coin types, we want to find the smallest number of coins that will make up that amount of money
# Write a function called 'change(amount, coins)'
# Where the 'amount' is a non-negative integer indicating the amount of change to be made
# And 'coins' is a list of integers indicating the coin types available
# The function should return a non-negative integer indicating the minimum number of coins required to make up the given 'amount'
# If there is no possible solution, return 'math.inf'

# Define a function called 'change' and use dynamic programming (tabulation method)
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

    # Create a table to store the minimum coins needed for each amount
    dp = [math.inf] * (amount + 1)
    dp[0] = 0 # Base case: 0 coins are needed to make amount 0

    # Iterate through each coin
    for coin in coins:
        # Update the dp table for each amount that can be reached by the current coin
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    # Return the result for the given amount
    return dp[amount] if dp[amount] != math.inf else math.inf

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

    # Create a table to store the minimum coins needed for each amount
    dp = [math.inf] * (amount + 1)
    dp[0] = 0 # Base case: 0 coins are needed to make amount 0

    # Create a table to store the coins used for each amount
    coin_used = [None] * (amount + 1)

    # Iterate through each coin
    for coin in coins:
        # Update the dp table for each amount that can be reached by the current coin
        for x in range(coin, amount + 1):
            if dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
                coin_used[x] = coin

    # If the amount cannot be formed, return [math.inf, []]
    if dp[amount] == math.inf:
        return [math.inf, []]

    # Backtrack to find the coins used
    result_coins = []
    current_amount = amount
    while current_amount > 0:
        result_coins.append(coin_used[current_amount])
        current_amount -= coin_used[current_amount]

    # Return the minimum number of coins and the list of coins used
    return [dp[amount], result_coins]

if __name__ == "__main__":
    change()
    giveChange()
