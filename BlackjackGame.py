import tkinter as tk
from tkinter import ttk
import random

class Blackjack(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BlackJack Game")
        self.geometry("400x300")
        self.minsize(300, 200)

        self.balance = 100
        self.bet = 0

        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        self.dealerShown_label = ttk.Label(main_frame, text="Dealer Card: ")
        self.dealerShown_label.pack(pady=10)

        self.playerShown_label = ttk.Label(main_frame, text="Player Cards: ")
        self.playerShown_label.pack(pady=2)

        self.totalShown_label = ttk.Label(main_frame, text="Total: ")
        self.totalShown_label.pack(pady=2)

        self.win_label = ttk.Label(main_frame, text="You Win!")
        self.lose_label = ttk.Label(main_frame, text="You Lose!")
        self.push_label = ttk.Label(main_frame, text="Push!")

        self.hit_button = ttk.Button(main_frame, text="Hit", command=self.hit)
        self.stand_button = ttk.Button(main_frame, text="Stand", command=self.stand)
        self.double_button = ttk.Button(main_frame, text="Double", command=self.double)

        self.balance_label = ttk.Label(main_frame, text=f"Balance: {self.balance}")
        self.balance_label.pack(pady=10)

        self.bet_entry = ttk.Entry(main_frame)
        self.bet_entry.pack(pady=2)

        self.bet_button = ttk.Button(main_frame, text="Bet and Play", command=self.betAmount)
        self.bet_button.pack(pady=2)

    def betAmount(self):
        self.bet = int(self.bet_entry.get())
        if self.bet > self.balance:
            self.bet = self.balance
        self.balance -= self.bet
        self.balance_label.config(text=f"Balance: {self.balance}")

        self.win_label.pack_forget()
        self.lose_label.pack_forget()
        self.push_label.pack_forget()
        self.bet_button.pack_forget()
        self.bet_entry.pack_forget()

        self.dealCards()

    def dealCards(self):
        self.cards = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}
        self.dealerCards = [random.choice(list(self.cards.keys())), random.choice(list(self.cards.keys()))] 
        self.playerCards = [random.choice(list(self.cards.keys())), random.choice(list(self.cards.keys()))]
        self.playerTotal = sum([int(self.cards[card]) for card in self.playerCards])
        self.dealerTotal = sum([int(self.cards[card]) for card in self.dealerCards])

        self.checkedPlayerAces = 0
        self.checkedDealerAces = 0
        self.playerAceHandler()
        self.dealerAceHandler()

        self.dealerShown_label.config(text=f"Dealer Card: {self.dealerCards[0]}")
        self.playerShown_label.config(text=f"Player Cards: {self.playerCards[0]} {self.playerCards[1]}")
        self.totalShown_label.config(text=f"Total: {self.playerTotal}")

        self.hit_button.pack(pady=2)
        self.stand_button.pack(pady=2)
        self.double_button.pack(pady=2)

        if self.playerTotal == 21 and self.dealerTotal != 21:
            self.playerWin()
        elif self.dealerTotal == 21 and self.playerTotal != 21:
            self.playerLose()

    def hit(self):
        cardDrawn = random.choice(list(self.cards.keys()))
        self.playerCards.append(cardDrawn)
        self.playerTotal += self.cards[cardDrawn]
        self.playerAceHandler()
        self.playerShown_label.config(text=f"Player Cards: {' '.join(self.playerCards)}")
        self.totalShown_label.config(text=f"Total: {self.playerTotal}")
        if self.playerTotal > 21:
            self.playerLose()
        elif self.playerTotal == 21:
            self.stand()
        self.double_button.pack_forget()
        
    def stand(self):
        while self.dealerTotal < 17:
            cardDrawn = random.choice(list(self.cards.keys()))
            self.dealerCards.append(cardDrawn)
            self.dealerTotal += self.cards[cardDrawn]
            self.dealerAceHandler()
        if self.dealerTotal > 21:
            self.playerWin()
        elif self.dealerTotal > self.playerTotal:
            self.playerLose()
        elif self.dealerTotal == self.playerTotal:
            self.playerPush()
        else:
            self.playerWin()
        
    def double(self):
        self.balance -= self.bet
        self.bet *= 2
        self.hit()
        self.stand()
    
    def playerAceHandler(self):
        if self.playerTotal > 21 and self.checkedPlayerAces < self.playerCards.count("A"):
            self.playerTotal -= 10
            self.checkedPlayerAces += 1
            self.totalShown_label.config(text=f"Total: {self.playerTotal}")
    
    def dealerAceHandler(self):
        if self.dealerTotal > 21 and self.checkedDealerAces < self.dealerCards.count("A"):
            self.dealerTotal -= 10
            self.checkedDealerAces += 1
            self.totalShown_label.config(text=f"Total: {self.dealerTotal}")

    def resetGame(self):
        self.dealerShown_label.config(text=f"Dealer Cards: {' '.join(self.dealerCards)} ({self.dealerTotal})")
        self.hit_button.pack_forget()
        self.stand_button.pack_forget()
        self.double_button.pack_forget()
        self.balance_label.config(text=f"Balance: {self.balance}")
        self.balance_label.pack(pady=10)
        self.bet_entry.pack(pady=2)
        self.bet_button.pack(pady=2)
    
    def playerWin(self):
        if self.playerTotal == 21 and len(self.playerCards) == 2:
            self.balance += int(2.5 * self.bet)
        else:
            self.balance += 2 * self.bet
        self.win_label.pack(pady=2)
        self.resetGame()
    
    def playerLose(self):
        self.lose_label.pack(pady=2)
        self.resetGame()

    def playerPush(self):
        self.balance += self.bet
        self.push_label.pack(pady=2)
        self.resetGame()

def main():
    game = Blackjack()
    game.mainloop()

if __name__ == "__main__":
    main()
