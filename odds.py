import itertools

# Sai Paladugu 101224375
# William Zhu 101231064

# Topic #1: Analysis of Baccarat with a shoe size of 2

# here is the deck mentioned in the explanation
deck = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# the bottom is the frequency of each card
# the index value of each element is equal to its face value
# 32 cards worth 0 points
#   [2 decks * 4 suits * 4 cards(10, J, Q, K)] = 32
# 8 cards with 6 points
#   [2 decks * 4 suits * 1 card(6)] = 8
deckFrequency = [32, 8, 8, 8, 8, 8, 8, 8, 8, 8]

# the bottom populates the list with replaceble permutations of length 6
uniqueHands = list(itertools.product(deck, repeat=6))

# this helper function calculates the total of two cards
def add(cardOne, cardTwo):
  return (cardOne + cardTwo) % 10

def outcome(hand): # the following function determines who wins the hand
  # c1, c2, c3 belong to the player
  # c4, c5, c6 belong to the banker
  # c3 and c6 are considered the "third" card
  [c1,c2,c3,c4,c5,c6] = hand
  playerSum = add(c1, c2)
  bankerSum = add(c4, c5)

  # game rules to add third card to calculation or not
  if playerSum == 6 or playerSum == 7: 
    if bankerSum <= 5:
      bankerSum = add(bankerSum, c6)
  elif playerSum <= 5 and bankerSum < 8:
    playerSum = add(playerSum, c3) 
    if bankerSum <= 2:
      bankerSum = add(bankerSum, c6)
    elif bankerSum == 3 and c3 in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
      bankerSum = add(bankerSum, c6)
    elif bankerSum == 4 and c3 in [2, 3, 4, 5, 6, 7]:
      bankerSum = add(bankerSum, c6)
    elif bankerSum == 5 and c3 in [4, 5, 6, 7]:
      bankerSum = add(bankerSum, c6)
    elif bankerSum == 6 and c3 in [6, 7]:
      bankerSum = add(bankerSum, c6)

  if playerSum > bankerSum:
    return 'player'
  elif bankerSum > playerSum:
    return 'banker'
  return 'tie'

def repCount(hand): # this function counts the total representations of a hand
    # make a fresh list each iteration to safely manipulate
    copyFreq = deckFrequency.copy()
    
    # if each face value in our hand is different
    # the odds of pulling each are independent
    # in which case we simply multiply all the values, for example:
    # (0, 2, 3, 6, 8, 9)
    # total representations = 32 * 8 * 8 * 8 * 8 * 8
    # however if we have recurring face values, we must work around
    # (0, 0, 0, 2, 2, 2)
    # total representations = 32 * 31 * 30 * 8 * 7 * 6
    
    # the following is our method to calcuate the above mentioned
    # our frequency chart looks like: [32, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    # where the index is equal to the face value for some frequency
    count = 1
    for c in hand:
        count *= copyFreq[c]
        copyFreq[c] -= 1
    return count

# here we simply call our previous functions to fetch the data
def calculate():
    counts = { 'player':0, 'banker':0, 'tie':0 }
    for hand in uniqueHands: # for each possible unique hand
      result = outcome(hand) # determine result
      count = repCount(hand) # determine equivalent hands
      counts[result] += count # add to resepective parties tally
    return counts

def printOdds():
    counts = calculate() # get our data
    total = counts['player'] + counts['banker'] + counts['tie']
    print('Player wins:', counts['player'] / total, ' percent of games')
    print('Banker wins:', counts['banker'] / total, 'percent of games')
    print('They tie:   ', counts['tie'] / total, 'percent of games')

printOdds()