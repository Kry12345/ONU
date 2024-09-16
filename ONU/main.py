#  Card code information:
#  There are two characters that represent each card:
#    * The first character represents the color of the card (excluding unused wild cards) and they are represented as:
#        *  "R" = Red
#        *  "Y" = Yellow
#        *  "G" = Green
#        *  "B" = Blue
#    * The second character represents the number of the card or an used wild card (excluding unused wild cards) and they are represented as:
#        *  "0" = Zero
#        *  "1" = One
#        *  "2" = Two
#        *  "3" = Three
#        *  "4" = Four
#        *  "5" = Five
#        *  "6" = Six
#        *  "7" = Seven
#        *  "8" = Eight
#        *  "9" = Nine
#        *  " " = Used Wild Card
#    *  Unused wild cards are represented as "WC"
#  This way of coding cards allows identifying them to be efficient
#The program is a shorter python version of the well-known game "UNO". A user can play against a bot. The game will end when either the user or bot's hand is empty. 
import random
import time

cards = [] # The list that contains all the cards the deck should have
deck = [] # The list that is updated throughout the game to be the deck
hands = [[], []] # The list that stores the players hands
global middleCard # The variable that will store the middle card throughout the game
middleCard = ""

# Generates the cards in the "cards" list in an efficient way rather than typing every value one by one
colors = ["R", "G", "Y", "B"]
for i in range (4):
  for j in range(10):
    cards.append(colors[i] + str(j))
  cards.append("WC")

# Asks for the players name
playerName = str(input("Hello, welcome to \033[1m\033[4mONU!\033[0m \nPlease type in your name: ")) 


def translateCard(card):
  if (card == "WC"): 
    return "\033[91mW\033[92mi\033[93ml\033[94md \033[91mC\033[92ma\033[93mr\033[94md\033[0m"
  translatedCard = ""
  colorNames = ["\033[91mRed", "\033[92mGreen", "\033[93mYellow", "\033[94mBlue"]
  numberNames = ["Zero\033[0m", "One\033[0m", "Two\033[0m", "Three\033[0m", "Four\033[0m", "Five\033[0m", "Six\033[0m", "Seven\033[0m", "Eight\033[0m", "Nine\033[0m"]
  for i in range(4):
    if (card[0:1] == colors[i]):
      translatedCard += colorNames[i] + " "
  if (card[1:2] == " "):
    translatedCard += "Wild Card\033[0m"
    return translatedCard
  for i in range(10):
    if (card[1:2] == str(i)):
      translatedCard += numberNames[i]
      return translatedCard
  return "nil"

# Draws the first card of the game, and prevents it from being a wild card to prevent awkwardness
def drawFirstCard():
  while True:
    randIndex = random.randint(0, len(deck) - 1)
    if (deck[randIndex] != "WC"):
      return deck.pop(randIndex)

# Checks if the card in the parameter is either a wild card, a card with the same color as the middle card, or a card with the same number as the middle card, and returns true if so since it can be placed. Otherwise, it will return false
def canBePlaced(card):
  if(card == "WC" or card[0:1] == middleCard[0:1] or card[1:2] == middleCard[1:2]):
    return True
  return False


def chooseWildCardColor(hand):
  count = [0, 0, 0, 0]
  colorValues = ["R", "G", "Y", "B"]
  for card in hand:
    if (card[0:1] == "R"):
      count[0] += 1
    elif (card[0:1] == "G"):
      count[1] += 1
    elif (card[0:1] == "Y"):
      count[2] += 1
    elif ((card[0:1] == "B")):
      count[3] += 1  
  max = count[0]
  i = 1
  for num in count:
    if (num > max):
      max = num
  i = 0
  while (i < len(count)):
    if (count[i] != max):
      count.pop(i)
      colorValues.pop(i)
      i -= 1
    i += 1
  if (len(count) == 1):
    return colorValues[0]
  else:
    return colorValues[random.randint(0, len(colorValues) - 1)]

#Controls the game and asks the user whether they want to play again at the end of one
def createGame():
  global middleCard
  global deck
  deck = cards.copy()
  playersTurn = ["P", "B"]
  random.shuffle(playersTurn)
  for i in range(7):
    for j in range(2):
      hands[j].append(deck.pop(random.randint(0, len(deck) - 1)))
  middleCard = drawFirstCard()
  turn = 0
  while True:
    if(playersTurn[turn % 2] == "P"):
      playerMove()
    else:
      botMove()
    turn += 1
    if (len(hands[0]) == 0 or len(hands[1]) == 0): # checks whether someone does not have any more cards in their hand in order to declare the winner and end the game
      if (len(hands[0]) == 0):
        for _ in range(5):
          print("\033[1m\033[93mCongratulations, you won!\033[0m\n")
          time.sleep(0.1)
      elif (len(hands[1]) == 0):
        print("Onu Master has no more cards in his deck...")
        for _ in range(3):
         print("\033[1mBot wins!\033[0m\n")
      response = input("Would you like to play again? (Type \'Y\' if yes or \'N\' for no): ") 
      if (response == "Y"):
        hands[0].clear()
        hands[1].clear()
        createGame() # restarts the game if the player wants to play the game again
      else:
        print("\033[1mHave a nice day!!!!\033[0m")
        return

# Tries to convert the parameter into an int and returns true if so. Otherwise, the parameter is left untouched and the function returns false
def isDigit(num):
  try:
    num = int(num)
    return True
  except ValueError:
    return False

#This procedure is for the player's turn.
def playerMove(): 
  global middleCard
  print("\033[36m\033[1m\n" + playerName + ", It's your turn!")
  print("Make your move! (☞ ͡° ͜ʖ ͡°)☞\033[0m") #Cute face
  time.sleep(1)
  print("\033[91m\nOnu Masters number of cards: " + '\033[4m'+ str(len(hands[1])) + '\033[0m')
  time.sleep(0.2)
  print("Middle Card: " + '\033[4m\033[1m' + translateCard(middleCard) + '\033[0m' + "\n")
  time.sleep(0.2)
  for i in range(len(hands[0])): #This loop outputs the user's current cards.
    num = i + 1
    print(str(num) + ")" + translateCard(hands[0][i]) + "\n") 
    time.sleep(0.1)
  while True: #Makes sure that the user inputs a valid integer.
    print("Type the \033[1m\033[95mNUMBER\033[0m of the card you want to play")
    index = input("or type \'\033[1m\033[95mD\033[0m\' to draw a card: ")
    if (isDigit(index) and int(index) <= len(hands[0]) and int(index) > 0 and canBePlaced(hands[0][int(index) - 1])): #Makes sure the card can be played.
      middleCard = hands[0][int(index) - 1] #Sets the played card as the middle card.
      deck.append(hands[0].pop(int(index)- 1)) #Removes card from hand and goes back to deck.
      print("You placed a....", end = "")
      time.sleep(1)
      print(translateCard(middleCard) + "!!\n")
      time.sleep(2)
      if len(hands[0]) == 1: #When user has one card left, it says "ONU!"
        print("\033[1m\033[96m!!!", playerName, " says: ONU!!!\033[0m\n")
        time.sleep(2)
      if middleCard == "WC":  
        while True:
          color = input("Choose a color! (Type \'R\' for red, \'G\' for green, \'Y\' for yellow, and \'B\' for blue): ")
          if (color == "R" or color == "G" or color == "Y" or color == "B"):
            middleCard = color + " "
            break
          else: #until valid input given
            print("Invalid Input")
            time.sleep(0.1)
      break #Ends procedure and goes to botMove()
    elif (index == "D"): #When 'D' is inputted, a random card is added to user's hand.
      print("You drew a Card\n")
      hands[0].append(deck.pop(random.randint(0, len(deck) - 1)))
      time.sleep(2)
      break #Ends procedure and goes to botMove().
    else:
      print("Invalid input") #If the user inputs an invalid input, it will ask for an input again. 
      time.sleep(0.1)

#code for bots turn
def botMove():
  global middleCard
  playableCards = []
  random.shuffle(hands[1])
  for i in range(len(hands[1])):
    if (canBePlaced(hands[1][i])):
      playableCards.append(i)
  print("It's \033[91mOnu Masters'\033[0m turn!")
  time.sleep(1)
  print("He is making his move right now...\n┏(-_-)┛\n")
  time.sleep(2)
  if (len(playableCards) != 0):
    randIndex = playableCards[random.randint(0, len(playableCards) - 1)]
    if (hands[1][randIndex] == "WC"):
      deck.append(hands[1].pop(randIndex))
      colorNames = ["\033[91mRed\033[0m", "\033[92mGreen\033[0m", "\033[93mYellow\033[0m", "\033[94mBlue\033[0m"]
      colorName = ""
      wildCardColor = chooseWildCardColor(hands[1])
      if (wildCardColor == "R"):
        colorName = colorNames[0]
      elif (wildCardColor == "G"):
        colorName = colorNames[1]
      elif (wildCardColor == "Y"):
        colorName = colorNames[2]
      else:
        colorName = colorNames[3]
      num = random.randint(0, 3)
      middleCard = wildCardColor + " "
      print("Onu Master placed a \033[91mW\033[92mi\033[93ml\033[94md \033[91mC\033[92ma\033[93mr\033[94md\033[0m and set the color to " + colorName + "!")
      time.sleep(3)
    else:
      print("Onu Master placed...", end = "")
      time.sleep(1)
      print(translateCard(hands[1][randIndex]) + "!!\n")
      middleCard = hands[1].pop(randIndex)
      deck.append(middleCard)
      if len(hands[1]) == 1:
        print("\033[1mOnu Master says: ONU!\033[0m")
      time.sleep(2)
  else:
    print("Onu Master draws a card...")
    hands[1].append(deck.pop(random.randint(0, len(deck) - 1))) # takes a card away from the deck and adds it to the bots hand if they have no playable cards
    time.sleep(3)

createGame() # runs the procedure to start a game