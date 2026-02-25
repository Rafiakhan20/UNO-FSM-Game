

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# CARD LOGIC 
colors = ["Red", "Yellow", "Green", "Blue"]
numbers = list(map(str, range(0, 10)))
special_cards = ["Skip", "Reverse", "Draw Two"]
wild_cards = ["Wild", "Wild Draw Four"]

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def is_playable(self, top):
        return self.color == top.color or self.value == top.value or self.color == "Wild"

    def img(self):
        val = self.value.replace(" ", "")
        if self.color == "Wild":
            return f"{val}.png"
        return f"{self.color}_{val}.png"

#DECK
def create_deck():
    deck = []
    for color in colors:
        deck.append(Card(color, "0"))
        for n in range(1, 10):
            deck.append(Card(color, str(n)))
            deck.append(Card(color, str(n)))
    for color in colors:
        for action in special_cards:
            deck.append(Card(color, action))
            deck.append(Card(color, action))
    for wild in wild_cards:
        for _ in range(4):
            deck.append(Card("Wild", wild))
    random.shuffle(deck)
    return deck

# GAME
class UNOGame:
    def __init__(self, players, cards_per_player):
        self.deck = create_deck()
        self.players = [{"name": name, "hand": [self.deck.pop() for _ in range(cards_per_player)]} for name in players]
        self.current_player = 0
        self.direction = 1
        while True:
            top = self.deck.pop()
            if top.value in numbers:
                self.top_card = top
                break
        self.draw_done = False
     
    def draw_card(self, player_index, count=1):
        for _ in range(count):
            if self.deck:
                self.players[player_index]["hand"].append(self.deck.pop())

    def play_card(self, player_index, card_index):
        card = self.players[player_index]["hand"][card_index]
        if card.is_playable(self.top_card):
            self.top_card = card
            self.players[player_index]["hand"].pop(card_index)
            return card
        return None

    def next_player_index(self):
        return (self.current_player + self.direction) % len(self.players)

# GUI 
root = tk.Tk()
root.title("UNO Card Game")
root.geometry("1000x750")
root.configure(bg="#1a1a1a")

# Background Frame with subtle gradient effect
bg_frame = tk.Frame(root, bg="#1a1a1a")
bg_frame.place(relwidth=1, relheight=1)

# CUSTOM INPUT BOX 
def custom_askstring(title, prompt):
    top = tk.Toplevel(root)
    top.title(title)
    top.configure(bg="white")
    top.geometry("400x180")
    top.resizable(False, False)
    top.update_idletasks()
    x = (top.winfo_screenwidth() // 2) - (400 // 2)
    y = (top.winfo_screenheight() // 2) - (180 // 2)
    top.geometry(f"+{x}+{y}")
    tk.Label(top, text=prompt, bg="white", font=("Helvetica", 14, "bold")).pack(pady=(20,10))
    var = tk.StringVar()
    entry = tk.Entry(top, textvariable=var, font=("Helvetica", 16), width=25, bg="white", bd=2, relief="solid")
    entry.pack(pady=5)
    entry.focus_set()
    result = {"value": None}
    def submit():
        result["value"] = var.get()
        top.destroy()
    def cancel():
        result["value"] = None
        top.destroy()
    btn_frame = tk.Frame(top, bg="white")
    btn_frame.pack(pady=15)
    def on_enter(e): e.widget.config(bg="#FFD700", fg="black")
    def on_leave(e): e.widget.config(bg="white", fg="black")
    ok_btn = tk.Button(btn_frame, text="OK", command=submit, font=("Helvetica", 12, "bold"), bg="white", fg="black", width=10)
    ok_btn.pack(side="left", padx=10)
    ok_btn.bind("<Enter>", on_enter)
    ok_btn.bind("<Leave>", on_leave)
    cancel_btn = tk.Button(btn_frame, text="Cancel", command=cancel, font=("Helvetica", 12, "bold"), bg="white", fg="black", width=10)
    cancel_btn.pack(side="left", padx=10)
    cancel_btn.bind("<Enter>", on_enter)
    cancel_btn.bind("<Leave>", on_leave)
    top.transient(root)
    top.grab_set()
    root.wait_window(top)
    return result["value"]

def custom_askinteger(title, prompt, minval=None, maxval=None):
    while True:
        val = custom_askstring(title, prompt)
        if val is None:
            return None
        try:
            val = int(val)
            if (minval is not None and val < minval) or (maxval is not None and val > maxval):
                raise ValueError
            return val
        except:
            messagebox.showerror("Invalid Input", f"Please enter a number between {minval} and {maxval}")

# USER INPUT
# Minimum 2 players
num_players = custom_askinteger("Players", "Enter number of players (2–5):", 2, 5)
player_names = []
for i in range(num_players):
    name = custom_askstring("Player Name", f"Enter name for Player {i+1}:")
    if not name:
        name = f"Player {i+1}"
    player_names.append(name)

cards_per_player = custom_askinteger("Cards", "Enter number of cards per player:", 1, 20)
game = UNOGame(player_names, cards_per_player)

# WIDGETS 
label_style = {"bg": "#1a1a1a", "fg": "white", "font": ("Helvetica", 16, "bold")}
player_label = tk.Label(root, text=f"{game.players[game.current_player]['name']}'s Turn", **label_style)
player_label.pack(pady=10)

# Top Card Frame
top_frame = tk.Frame(root, bg="#333333", bd=3, relief="ridge")
top_frame.pack(pady=10)
top_label = tk.Label(top_frame, text="Top Card", bg="#333333", fg="#FFD700", font=("Helvetica", 14, "bold"))
top_label.pack(pady=5)
top_img_lbl = tk.Label(top_frame, bg="#333333")
top_img_lbl.pack(pady=5, padx=5)

hand_frame = tk.Frame(root, bg="#1a1a1a")
hand_frame.pack(pady=20)

# LABEL(SHOW ALL MESSAGES)
info = tk.Label(root, text="", bg="#1a1a1a", fg="#FFD700", font=("Helvetica", 14, "bold"),
                wraplength=900, justify="center")
info.pack(pady=10)

other_players_frame = tk.Frame(root, bg="#222222", bd=2, relief="ridge")
other_players_frame.pack(pady=5)
other_players_label = tk.Label(other_players_frame, text="", bg="#222222", fg="white", font=("Helvetica", 12))
other_players_label.pack(padx=10, pady=5)

# FUNCTIONS 
def load_img(name):
    img = Image.open("cards/" + name)
    img = img.resize((90,130))
    return ImageTk.PhotoImage(img)

def update_top():
    img = load_img(game.top_card.img())
    top_img_lbl.config(image=img)
    top_img_lbl.image = img

def refresh_hand():
    for w in hand_frame.winfo_children():
        w.destroy()
    current_hand = game.players[game.current_player]["hand"]
    for i, card in enumerate(current_hand):
        img = load_img(card.img())
        btn = tk.Button(hand_frame, image=img, command=lambda idx=i: play_card(idx),
                        bg="#444444", activebackground="#FFD700", bd=2, relief="raised")
        btn.image = img
        btn.pack(side="left", padx=6)
    update_other_players()

def update_other_players():
    text = "Other Players:\n"
    for i, p in enumerate(game.players):
        if i != game.current_player:
            text += f"{p['name']}: {len(p['hand'])} cards\n"
    other_players_label.config(text=text)

# PLAY CARD FUNCTION WITH UNO CALL
def play_card(index):
    player_index = game.current_player
    player = game.players[player_index]
    card = game.play_card(player_index, index)
    if card:
        info.config(text=f"{player['name']} played {card.value}")
        handle_special_card(card)
        if len(player["hand"]) == 1:
            info.config(text=f"{player['name']} says UNO!")
            messagebox.showinfo("UNO!", f"{player['name']} says UNO!")
        check_winner(player_index)
        game.draw_done = False
        next_turn()
    else:
        info.config(text="Invalid Move")
    update_top()
    refresh_hand()


def draw_card():
    if not game.draw_done:
        game.draw_card(game.current_player)
        info.config(text=f"{game.players[game.current_player]['name']} drew a card. Now play or pass.")
        game.draw_done = True
    else:
        info.config(text="You already drew a card this turn!")
    refresh_hand()

def pass_turn():
    # Sirf tab pass hoga agar card draw ho chuka ho
    if game.draw_done:
        info.config(text=f"{game.players[game.current_player]['name']} passed the turn")
        game.draw_done = False  # Reset for next player
        next_turn()
    else:
        # Agar baghair draw kiye pass dabaya jaye
        info.config(text="You must draw a card before you can pass!")


def next_turn():
    if len(game.players) <= 1:
        if len(game.players) == 1:
            info.config(text=f"{game.players[0]['name']} is the last player remaining. GAME OVER!")
            messagebox.showinfo("Game Over", f"{game.players[0]['name']} is the last player remaining. GAME OVER!")
        draw_btn.config(state="disabled")
        pass_btn.config(state="disabled")
        for w in hand_frame.winfo_children():
            w.destroy()
        return

    # Turn change logic
    game.draw_done = False # Reset flag for the new player
    game.current_player = game.next_player_index()
    player_label.config(text=f"{game.players[game.current_player]['name']}'s Turn")
    refresh_hand()

def handle_special_card(card):
    num_players = len(game.players)
    next_player = game.next_player_index()
    if card.value == "Skip":
        game.current_player = next_player
        info.config(text=f"{game.players[game.current_player]['name']}'s turn skipped!")
    elif card.value == "Reverse":
        game.direction *= -1
        if num_players == 2:
            game.current_player = next_player
        info.config(text="Play direction reversed!")
    elif card.value == "Draw Two":
        game.draw_card(next_player, 2)
        info.config(text=f"{game.players[next_player]['name']} draws 2 cards")
    elif card.value == "Wild Draw Four":
        chosen_color = choose_wild_color()
        card.color = chosen_color
        game.draw_card(next_player, 4)
        info.config(text=f"{game.players[next_player]['name']} draws 4 cards")
        info.config(text=f"Wild color set to {card.color}")
        update_top()
    elif card.value == "Wild":
        chosen_color = choose_wild_color()
        card.color = chosen_color
        info.config(text=f"Wild color set to {card.color}")
        

def choose_wild_color():
    top = tk.Toplevel(root)
    top.title("Choose Wild Color")
    top.configure(bg="white")
    top.geometry("300x250")
    top.resizable(False, False)
    top.update_idletasks()
    x = (top.winfo_screenwidth() // 2) - (300 // 2)
    y = (top.winfo_screenheight() // 2) - (250 // 2)
    top.geometry(f"+{x}+{y}")

    chosen = {"color": None}
    def select(color):
        chosen["color"] = color
        top.destroy()

    for c in colors:
        btn = tk.Button(top, text=c, width=10, font=("Helvetica", 12, "bold"),
                        bg=c.lower(), fg="white", activebackground="#FFD700",
                        command=lambda col=c: select(col))
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(relief="raised", bd=3))
        btn.bind("<Leave>", lambda e, b=btn: b.config(relief="flat", bd=2))

    top.transient(root)
    top.grab_set()
    top.wait_window()
    return chosen["color"]



def check_winner(player_index):
    player = game.players[player_index]
    if len(player["hand"]) == 0:
        winner = player['name']
        info.config(text=f"{winner} WINS THIS ROUND!")
        messagebox.showinfo("Round Over", f"{winner} wins this round!")
        show_winner_animation(winner)

        # Remove the winner from the player list
        game.players.pop(player_index)
        # Adjust current player index if necessary
        if len(game.players) == 0:
            info.config(text="All players finished. GAME OVER!")
            draw_btn.config(state="disabled")
            pass_btn.config(state="disabled")
            for w in hand_frame.winfo_children():
                w.destroy()
        elif game.current_player >= len(game.players):
            game.current_player = 0
        player_label.config(text=f"{game.players[game.current_player]['name']}'s Turn")
        refresh_hand()

# BUTTONS STYLE
def on_enter(e):
    e.widget.config(bg="#FFD700", fg="black", relief="raised", bd=3)

def on_leave(e):
    e.widget.config(bg="#333333", fg="white", relief="flat", bd=2)

btn_style = {"bg":"#333333", "fg":"white", "activebackground":"#FFD700",
             "activeforeground":"#1a1a1a", "font":("Helvetica",12,"bold"), "width":18,
             "relief":"flat", "bd":2, "highlightthickness":0}

draw_btn = tk.Button(root, text="Draw Card", command=draw_card, **btn_style)
draw_btn.pack(pady=5)
draw_btn.bind("<Enter>", on_enter)
draw_btn.bind("<Leave>", on_leave)

pass_btn = tk.Button(root, text="Pass Turn", command=pass_turn, **btn_style)
pass_btn.pack(pady=5)
pass_btn.bind("<Enter>", on_enter)
pass_btn.bind("<Leave>", on_leave)

exit_btn = tk.Button(root, text="Exit", command=root.destroy, **btn_style)
exit_btn.pack(pady=5)
exit_btn.bind("<Enter>", on_enter)
exit_btn.bind("<Leave>", on_leave)


def show_winner_animation(winner_name):
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.configure(bg="black")
    overlay.attributes("-alpha", 0.75)

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    overlay.geometry(f"{sw}x{sh}+0+0")

    # CONFETTI CANVAS
    canvas = tk.Canvas(overlay, bg="black", highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)

    confetti = []
    colors_list = ["red", "yellow", "blue", "green", "white"]

    for _ in range(120):
        x = random.randint(0, sw)
        y = random.randint(-sh, 0)
        size = random.randint(6, 12)
        c = canvas.create_oval(
            x, y, x + size, y + size,
            fill=random.choice(colors_list),
            outline=""
        )
        confetti.append(c)

    def fall_confetti():
        for c in confetti:
            canvas.move(c, 0, random.randint(6, 12))
            if canvas.coords(c)[1] > sh:
                canvas.move(c, 0, -sh)
        overlay.after(50, fall_confetti)

    fall_confetti()

    #WINNER CARD 
    card = tk.Frame(
        overlay,
        bg="#FFD700",
        bd=8,
        relief="ridge"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(
        card,
        text="🏆 WINNER 🏆",
        font=("Helvetica", 18, "bold"),
        bg="#FFD700",
        fg="black"
    )
    title.pack(pady=(15, 5))

    name_lbl = tk.Label(
        card,
        text=winner_name,
        font=("Helvetica", 32, "bold"),
        bg="#FFD700",
        fg="black"
    )
    name_lbl.pack(pady=(0, 20))

    scale = 0.5
    growing = True
    glow = False

    def animate():
        nonlocal scale, growing, glow

        if growing:
            scale += 0.05
            if scale >= 1:
                scale = 1
                growing = False

        card.tk.call("tk", "scaling", scale)

        if not growing:
            glow = not glow
            card.config(bg="#FFF2AA" if glow else "#FFD700")
            title.config(bg=card["bg"])
            name_lbl.config(bg=card["bg"])

        overlay.after(60, animate)

    animate()
    overlay.after(4000, overlay.destroy)


# Start
update_top()
refresh_hand()
root.mainloop()
