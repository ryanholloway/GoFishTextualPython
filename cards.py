import random
from collections import Counter

faces=("Jack", "Queen","King","Ace")
suits=("Clubs","Spades","Hearts","Diamonds")
nums=(2,3,4,5,6,7,8,9,10)

def buildDeck():
    """ Build and return a shuffled deck of 52 cards."""
    deck=[]
    for suit in suits:
        for value in faces+nums:
            deck.append(f"{value} of {suit}")
    random.shuffle(deck)
    return deck


def cardsDict():
    """
    Return a shuffled dictionary of cards with the keys being the card name and the values being the card's value.
    The values are numeric exept for the aces with returns a list of possible values
    """
    cards={}
    for suit in suits:
        for card in faces+nums:
            if card=="Ace":
                value =[1,11]
            elif card in ["Jack", "Queen","King"]:
                value = 10
            else:
                value=card
            cards[f"{card} of {suit}"]=value
    # The next 3 lines are inspired by StackOverFlow:
    #https://stackoverflow.com/questions/61074422/how-to-shuffle-a-python-dictionary
    cards_list= list(cards.items())
    random.shuffle(cards_list)
    return dict(cards_list)


def identify_remove_pairs(hand):
    """
    This Function recieves a list of cards (called "hand"), then processes them to identify any pairs of cards, 
    and if found removes the pairs from the hand and returns two lists: 
    the hand with the pairs removed, and a list of removed cards
    """
    values=[]
    thirds=set()
    for card in hand:
        value=card[:card.find(" ")]
        values.append(value)
    c=Counter(values)
    pairs =[]
    for k,v in c.items(): #k is Key v is Value
        if v in [2,4]:
            pairs.append(k)
        elif v==3:
            pairs.append(k)
            thirds.add(k)
    add_back_in=[]
    for value in thirds:
        for card in hand:
            if card.startswith(value):
                add_back_in.append(card)
                break
    to_remove=[]
    for p in pairs:
        for card in hand:
            if card.startswith(p):
                to_remove.append(card)         
    for card in to_remove:
        hand.remove(card)
    for card in add_back_in:
        hand.append(card)
        to_remove.remove(card)      
    return hand,to_remove