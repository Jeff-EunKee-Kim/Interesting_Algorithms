'''
Online Ad Auctions

'''

import numpy as np

budgets = np.genfromtxt("budgets.csv", dtype=int)
budgetsTotal = np.genfromtxt("budgets.csv", dtype=int)
keywords = np.genfromtxt("keywords.csv", dtype=int)
values = np.genfromtxt("values.csv", delimiter=',', dtype=int)


bidderSpent = np.zeros(5)


def calcBal(bidder):
    return 1 - pow(bidderSpent[bidder] / budgetsTotal[bidder], 0.01)


def balancedAlg(budgets, keywords, values):
    balancedRevenue = 0
    round = 0
    while round < len(keywords):
        keyword = keywords[round]
        bidWinner = -1
        balancePrice = 0
        for i in range(len(budgets)):
            if budgets[i] >= values[i][keyword]:
                if balancePrice < values[i][keyword]*calcBal(i):
                    balancePrice = values[i][keyword]*calcBal(i)
                    bidPrice = values[i][keyword]
                    bidWinner = i
        if bidWinner != -1:
            budgets[bidWinner] -= bidPrice
            bidderSpent[bidWinner] += bidPrice
            balancedRevenue += bidPrice
        round += 1
    print(balancedRevenue)


# greedyAlg(budgets, keywords, values)
balancedAlg(budgets, keywords, values)
