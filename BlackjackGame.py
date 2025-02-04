import tkinter as tk
from tkinter import ttk
import random

class BlackJack(tk.Tk):
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

        self.dealerShown = ttk.Label(main_frame, text="Dealer Card: ")
        self.dealerShown.pack(pady=10)

        self.playerShown = ttk.Label(main_frame, text="Player Cards: ")
        self.playerShown.pack(pady=2)

        self.totalShown = ttk.Label(main_frame, text="Total: ")
        self.totalShown.pack(pady=2)

        self.win = ttk.Label(main_frame, text="You Win!")
        self.lose = ttk.Label(main_frame, text="You Lose!")
        self.push = ttk.Label(main_frame, text="Push!")

        self.hit_button = ttk.Button(main_frame, text="Hit", command=self.hit)
        self.stand_button = ttk.Button(main_frame, text="Stand", command=self.stand)

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
        self.bet_button.pack_forget()
        self.bet_entry.pack_forget()
        self.dealCards()

    def dealCards(self):
        self.cards = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}
        self.dealerCards = [random.choice(list(self.cards.keys()))] 
        self.playerCards = [random.choice(list(self.cards.keys())), random.choice(list(self.cards.keys()))]
        self.hitCount = 0
        self.calcTotal()

        self.dealerShown.config(text=f"Dealer Card: {self.dealerCards[0]}")
        self.playerShown.config(text=f"Player Cards: {self.playerCards[0]} {self.playerCards[1]}")
        self.totalShown.config(text=f"Total: {self.playerTotal}")

        self.hit_button.pack(pady=2)
        self.stand_button.pack(pady=2)

        self.win.pack_forget()
        self.lose.pack_forget()
        self.push.pack_forget()

        if self.playerTotal == 21:
            self.stand()
    
    def calcTotal(self):
        self.playerTotal = sum([int(self.cards[card]) for card in self.playerCards])
        self.dealerTotal = sum([int(self.cards[card]) for card in self.dealerCards])
        if self.playerTotal > 21 and "A" in self.playerCards:
            self.playerTotal -= 10
            self.playerCards.remove("A")
            self.totalShown.config(text=f"Total: {self.playerTotal}")

    def hit(self):
        self.hitCount += 1
        self.playerCards.append(random.choice(list(self.cards.keys())))
        self.playerShown.config(text=f"Player Cards: {' '.join(self.playerCards)}")
        self.calcTotal()
        self.totalShown.config(text=f"Total: {self.playerTotal}")
        if self.playerTotal > 21:
            self.playerLose()
        elif self.playerTotal == 21:
            self.stand()
        
    def stand(self):
        self.calcTotal()
        while self.dealerTotal < 17:
            self.dealerCards.append(random.choice(list(self.cards.keys())))
            self.calcTotal()
        self.dealerShown.config(text=f"Dealer Cards: {' '.join(self.dealerCards)} ({self.dealerTotal})")
        if self.dealerTotal > 21:
            self.playerWin()
        elif self.dealerTotal > self.playerTotal:
            self.playerLose()
        elif self.dealerTotal == self.playerTotal:
            self.playerPush()
        else:
            self.playerWin()
        self.resetGame()
    
    def resetGame(self):
        self.hit_button.pack_forget()
        self.stand_button.pack_forget()
        self.balance_label.config(text=f"Balance: {self.balance}")
        self.balance_label.pack(pady=10)
        self.bet_button.pack(pady=2)
        self.bet_entry.pack(pady=2)
    
    def playerWin(self):
        self.win.pack(pady=2)
        self.balance += 2 * self.bet
        self.resetGame()
    
    def playerLose(self):
        self.lose.pack(pady=2)
        self.resetGame()

    def playerPush(self):
        self.push.pack(pady=2)
        self.balance += self.bet
        self.resetGame()

def main():
    game = BlackJack()
    game.mainloop()

if __name__ == "__main__":
    main()
