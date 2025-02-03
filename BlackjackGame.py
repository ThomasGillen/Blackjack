import tkinter as tk
from tkinter import ttk
import random

class BlackJack(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BlackJack Game")
        self.geometry("400x300")
        self.minsize(300, 200)

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

        self.play_button = ttk.Button(main_frame, text="Play", command=self.dealCards)
        self.play_button.pack(pady=5)

        self.hit_button = ttk.Button(main_frame, text="Hit", command=self.hit)
        self.stand_button = ttk.Button(main_frame, text="Stand", command=self.stand)

    def dealCards(self):
        self.cards = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}
        self.dealerCards = [random.choice(list(self.cards.keys()))] 
        self.playerCards = [random.choice(list(self.cards.keys())), random.choice(list(self.cards.keys()))]
        self.hitCount = 0
        self.calcTotal()

        self.dealerShown.config(text=f"Dealer Card: {self.dealerCards[0]}")
        self.playerShown.config(text=f"Player Cards: {self.playerCards[0]} {self.playerCards[1]}")
        self.totalShown.config(text=f"Total: {self.playerTotal}")

        self.play_button.pack_forget()
        self.hit_button.pack(pady=2)
        self.stand_button.pack(pady=2)

        self.win.pack_forget()
        self.lose.pack_forget()
    
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
            self.lose.pack(pady=2)
            self.resetGame()
        elif self.playerTotal == 21:
            self.stand()
        
    def stand(self):
        self.calcTotal()
        while self.dealerTotal < 17:
            self.dealerCards.append(random.choice(list(self.cards.keys())))
            self.calcTotal()
        self.dealerShown.config(text=f"Dealer Cards: {' '.join(self.dealerCards)} ({self.dealerTotal})")
        if self.dealerTotal > 21:
            self.win.pack(pady=2)
        elif self.dealerTotal > self.playerTotal:
            self.lose.pack(pady=2)
        elif self.dealerTotal == self.playerTotal:
            self.push.pack(pady=2)
        else:
            self.win.pack(pady=2)
        self.resetGame()
    
    def resetGame(self):
        self.hit_button.pack_forget()
        self.stand_button.pack_forget()
        self.play_button.pack(pady=5)

def main():
    game = BlackJack()
    game.mainloop()

if __name__ == "__main__":
    main()
