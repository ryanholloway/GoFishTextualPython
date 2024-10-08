from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static,Label
from gofish import GoFishGame
import random

class GameStatus(Static):
    def update_status(self, message: str):
        self.update(message)

class GoFishApp(App):
    
    CSS = """
    
    #cardContainer {
        layout: grid;
        grid-size: 6;
        align-horizontal: center; 
        align-vertical: middle;  
        padding: 2;
    }
    Button {
        width: 10;
        height: 5;
        margin: 1;
        content-align: center middle;
    }
    #selectionButtons{
        layout: grid;
        grid-size: 2;
        align-horizontal: center; 
        align-vertical: middle;  
    }       
    """
   

    def compose(self) -> ComposeResult:
        yield Header("Go Fish")
        self.computerText=GameStatus("")
        yield self.computerText
        self.status = GameStatus("Welcome to Go Fish! Press Start to begin.")
        yield self.status
        
        yield Container(
            Button("Start Game", id="start", variant="primary"),
            Button("Quit Game", id="quit", variant="error"),
            id="mainButtons"
        )
        yield Container(
            Button("",id="cardA"),
            Button("",id="cardB"),
            Button("",id="cardC"),
            Button("",id="cardD"),
            Button("",id="cardE"),
            Button("",id="cardF"),
            Button("",id="cardG"),
            Button("",id="cardH"),
            Button("",id="cardI"),
            Button("",id="cardJ"),
            Button("",id="cardK"),
            Button("",id="cardL"),
            Button("",id="cardM"),
            id="cardContainer"
        )
        yield Container(
            Button("Yes", id="yes"),
            Button("No", id="no"),
            id="selectionButtons"
            
        )
        self.amountOfPairs=GameStatus("Amount of Pairs: 0")
        yield self.amountOfPairs
        #self.comptPairs=GameStatus("Computer Pairs: 0")
        #yield self.comptPairs
        yield Footer()
        
    def on_mount(self):
        self.hideCards()
        self.hideSelection()
        

    def hideStart(self):
       button= self.query_one("#mainButtons Button#start")
       button.display=False
    
    def showStart(self):
       button= self.query_one("#mainButtons Button#start")
       button.display=True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "start":
            self.start_game()
            event.button.label = "Restart Game"
        elif button_id == "quit":
            self.exit()
        elif button_id.startswith("card"):
            self.select_card(button_id)
        elif button_id == "yes":
            self.computer_response(True)
        elif button_id == "no":
            self.computer_response(False)
    
    def hideCards(self):
        card_buttons = self.query("Container#cardContainer Button")
        for button in card_buttons:
            button.display=False

    def showCards(self):
        card_buttons = self.query("Container#cardContainer Button")
        for button in card_buttons:
            button.display=True

    def setupButtons(self):
        player_cards = self.game.player
        card_buttons = self.query("Container#cardContainer Button")
        for i, card in enumerate(player_cards):
            card_buttons[i].display = True
            card_buttons[i].label = str(card)

        for i in range(len(player_cards), len(card_buttons)):
            card_buttons[i].display = False
            
    def select_card(self, button_id: str):
        card_index = ord(button_id[-1]) - ord('A')  # Get the index from the button ID (cardA -> 0)
        selected_card = self.game.player[card_index]
        value = selected_card[:selected_card.find(" ")]

        found_it = False
        computer_cards = self.game.computer  # Assuming this holds the computer's cards

        for n, card in enumerate(computer_cards):
            if card.startswith(value):
                found_it = n
                break

        if isinstance(found_it, bool):
            status="Go Fish!\n"
            self.game.player.append(self.game.deck.pop())  # Assuming you have a deck in your game
            status+=(f"You drew a {self.game.player[-1]}")
            self.computerText.update_status(status)
            if len(self.game.deck) == 0:
                self.checkWin()
        else:
            self.computerText.update_status(f"Here is your card from the computer: {computer_cards[n]}\n")
            self.game.player.append(computer_cards.pop(n))
        
        self.game.identify_player_pairs()
        self.setupButtons()
        self.amountOfPairs.update_status(f"Amount of Pairs: {self.getPairs()}")
        self.checkWin()
        self.computer_turn()

    def getPairs(self):
        return int(len(self.game.player_pairs)/2)


    def computer_turn(self):
        if not self.game.computer:
            self.status.update_status("The computer has no cards left!")
            return
        
        global cardComputerWants,compvalue
        cardComputerWants=random.choice(self.game.computer)
        
        compvalue = cardComputerWants[:cardComputerWants.find(" ")]
        self.status.update_status(f"Computer asks: Do you have a {compvalue}?")
        self.game.identify_computer_pairs()
        self.setCardsInactive()
        self.showSelection()
        #self.comptPairs.update_status(f"Computer Pairs: {int(len(self.game.computer_pairs)/2)}")
        self.checkWin()
    
    def setCardsInactive(self):
        card_buttons = self.query("Container#cardContainer Button")
        for button in card_buttons:
            button.disabled=True

    def setCardsActive(self):
        card_buttons = self.query("Container#cardContainer Button")
        for button in card_buttons:
            button.disabled=False
        
    
    def hideSelection(self):
        buttons = self.query("Container#selectionButtons Button")
        for button in buttons:
            button.display=False
    
    def showSelection(self):
        buttons = self.query("Container#selectionButtons Button")
        for button in buttons:
            button.display=True

    def computer_response(self, has_card: bool):
        if has_card:
            for n, card in enumerate(self.game.player):
                if card.startswith(compvalue):            
                    self.game.computer.append(self.game.player.pop(n))  # Move card from player to computer
                    self.status.update_status(f"Computer got your {card}.")
                    break
        else:
            if self.game.deck:
                self.game.computer.append(self.game.deck.pop()) 
                self.status.update_status("Go Fish! The computer drew a card.")
            else:
                self.status.update_status("The deck is empty. No more cards to draw.")
                self.checkWin()

        self.setupButtons()
        self.setCardsActive()
        self.hideSelection()
        self.computerText.update_status("")
        self.game.identify_computer_pairs()
        self.checkWin()

    def start_game(self):
        self.game = GoFishGame()
        self.game.setup()  # Set up the game
        self.status.update_status("Game Started! Ask Computer for a card.")
        self.hideSelection()
        self.showCards()
        self.setupButtons()
        self.hideStart()

    def checkWin(self):
        if self.game.is_game_over():
            self.status.update_status(self.game.get_winner())
            self.hideCards()
            self.hideSelection()
            self.showStart()


if __name__ == "__main__":
    app = GoFishApp()
    app.run()
