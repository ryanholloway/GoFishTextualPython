import cards
import random
deck=cards.buildDeck()

player = []
computer = []
player_pairs=[]
computer_pairs=[]

for _ in range(7):
    player.append(deck.pop())
    computer.append(deck.pop())



player, pairs=cards.identify_remove_pairs(player)
player_pairs.extend(pairs)
computer, pairs=cards.identify_remove_pairs(computer)
computer_pairs.extend(pairs)

def show_player_hand():
    player.sort()
    print("\nPlayers hand:")
    for n,card in enumerate(player):
        print(f"\tSelect {n} for {card}")

while True:

    
    
    show_player_hand()
    # Players Turn
    choice = input("\nPlease select the number for the card you want from the above list: ")
    selection=player[int(choice)]
    value=selection[:selection.find(" ")]
    
    found_it=False
    for n,card in enumerate(computer):
        if card.startswith(value):
            found_it=n
            break
    
    if isinstance(found_it,bool):
        print("Go Fish!\n")
        player.append(deck.pop())
        print(f"You drew a {player[-1]}")
        if len(deck)==0:
            break
    else:
        print(f"Here is your card from the computer: {computer[n]}\n")
        player.append(computer.pop(n))
    
    player, pairs=cards.identify_remove_pairs(player)
    player_pairs.extend(pairs)
    
    show_player_hand()
    #Is the game over
    if len(player)==0:
        print("Game over. You ran out of cards")
        if len(computer_pairs)>len(player_pairs):
            print("Computer won, more pairs")
        elif len(computer_pairs)<len(player_pairs):
            print("You won, you had more pairs!")
        else:
            print("It was a draw!")
        break
    
        
    
    #Computers Turn 
    card=random.choice(computer)
    value=card[:card.find(" ")]
    
    choice = input(f"\nFrom the computer: Do you have a {value}? (y/n) ")
    
    if choice.lower() in ["y", "yes"]:
        #find first card in player hand that starts with "value"
        for n, card in enumerate(player):
            if card.startswith(value):            
                break
        #remove from player hand and add to computer hand
        computer.append(player.pop(n))
    else:
        computer.append(deck.pop())
        if len(deck)==0:
            break
        
    
    computer, pairs=cards.identify_remove_pairs(computer)
    computer_pairs.extend(pairs)
    
    #Is the game over
    
    if len(computer)==0:
        print("Computer ran out of cards\n")
        if len(computer_pairs)>len(player_pairs):
            print("Computer won, more pairs")
        elif len(computer_pairs)<len(player_pairs):
            print("You won, you had more pairs!")
        else:
            print("It was a draw!")
        break


if len(deck)==0:
    print("Game over")
    if len(computer_pairs)>len(player_pairs):
        print("Computer won, more pairs")
    elif len(computer_pairs)<len(player_pairs):
        print("You won, you had more pairs!")
    else:
        print("It was a draw!")