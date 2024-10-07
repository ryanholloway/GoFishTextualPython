import cards
import random  

class GoFishGame:
    def __init__(self):
        self.deck=cards.buildDeck()
        self.player = []
        self.computer = []
        self.player_pairs=[]
        self.computer_pairs=[]

    def setup(self):
        for _ in range(7):
            self.player.append(self.deck.pop())
            self.computer.append(self.deck.pop())
        self.identify_computer_pairs()
        self.identify_player_pairs()

    def identify_player_pairs(self):
        self.player.sort()
        self.player, pairs=cards.identify_remove_pairs(self.player)
        self.player_pairs.extend(pairs)

    def identify_computer_pairs(self):
        self.computer, pairs=cards.identify_remove_pairs(self.computer)
        self.computer_pairs.extend(pairs)

    def show_player_hand(self):
        self.player.sort()
        print("\nPlayers hand:")
        for n,card in enumerate(self.player):
            print(f"\tSelect {n} for {card}")

    
    def player_turn(self):
        choice = input("\nPlease select the number for the card you want from the above list: ")
        selection=self.player[int(choice)]
        value=selection[:selection.find(" ")]
        
        found_it=False
        for n,card in enumerate(self.computer):
            if card.startswith(value):
                found_it=n
                break
        
        if isinstance(found_it,bool):
            print("Go Fish!\n")
            self.player.append(self.deck.pop())
            print(f"You drew a {self.player[-1]}")
            if len(self.deck)==0:
                pass #temp
        else:
            print(f"Here is your card from the computer: {self.computer[n]}\n")
            self.player.append(self.computer.pop(n))


    def computer_turn(self):
        card=random.choice(self.computer)
        value=card[:card.find(" ")]
        
        choice = input(f"\nFrom the computer: Do you have a {value}? (y/n) ")
        
        if choice.lower() in ["y", "yes"]:
            #find first card in player hand that starts with "value"
            for n, card in enumerate(self.player):
                if card.startswith(value):            
                    break
            #remove from player hand and add to computer hand
            self.computer.append(self.player.pop(n))
        else:
            self.computer.append(self.deck.pop())
            if len(self.deck)==0:
                pass
        
    def get_winner(self):
        if len(self.player_pairs) > len(self.computer_pairs):
            return "You win!"
        elif len(self.player_pairs) < len(self.computer_pairs):
            return "Computer wins!"
        else:
            return "It's a draw!"
        

    def is_game_over(self):
        if not self.player or not self.computer or not self.deck:
            return True
        return False