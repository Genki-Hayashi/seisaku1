import os
import random
from PIL import Image, ImageTk
import tkinter as tk


class ContinueDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("continue?")
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        self.result = None
        self.grab_set()  # ダイアログが閉じるまで他のウィンドウとの対話を防止する
        self.focus_set()  # ダイアログにフォーカスを設定する
        self.lift()  # ダイアログを最前面に移動する

        label = tk.Label(self, text="続行しますか？", font=("Helvetica", 20, "bold"))
        label.pack(padx=50, pady=10)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        yes_button = tk.Button(button_frame, text="はい", command=self.continue_game_yes, font=("Helvetica", 16, "bold"))
        yes_button.pack(side=tk.LEFT, padx=5)
        no_button = tk.Button(button_frame, text="いいえ", command=self.continue_game_no, font=("Helvetica", 16, "bold"))
        no_button.pack(side=tk.RIGHT, padx=5)

    def continue_game_yes(self):
        self.result = "はい"
        self.destroy()

    def continue_game_no(self):
        self.result = "いいえ"
        self.destroy()


class HighLowGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("High & Low Game")
        self.geometry("1920x1080")
        self.configure(bg='green')
        self.cards = [{'value': str(value), 'image': f'{suit}{value}.png'} for suit in ['club', 'diamond', 'heart', 'spade'] for value in range(1, 14)]
        self.card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        self.computer_card = None
        self.player_card = None

        self.create_widgets()
        self.draw_cards()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=600, height=250, bg='green')
        self.canvas.pack(pady=20, side=tk.LEFT)

        self.player_canvas = tk.Canvas(self, width=600, height=250, bg='green')
        self.player_canvas.pack(pady=20, side=tk.RIGHT)

        button_frame = tk.Frame(self, bg='green')
        button_frame.pack(pady=80)

        self.high_button = tk.Button(button_frame, text="High", command=self.high_guess, bg='white', fg='black', font=("Helvetica", 16, "bold"))
        self.high_button.pack(side=tk.LEFT, padx=30)

        self.low_button = tk.Button(button_frame, text="Low", command=self.low_guess, bg='white', fg='black', font=("Helvetica", 16, "bold"))
        self.low_button.pack(side=tk.RIGHT, padx=50)

        self.result_label = tk.Label(self, text="", bg='green', fg='white', font=("Helvetica", 20, "bold"))
        self.result_label.pack(pady=80)

        self.computer_card_label = tk.Label(self, text="コンピューターのカード: ", bg='green', fg='white', font=("Helvetica", 16, "bold"))
        self.computer_card_label.pack()

        self.player_card_label = tk.Label(self, text="プレイヤーのカード: ", bg='green', fg='white', font=("Helvetica", 16, "bold"))
        self.player_card_label.pack()

        self.draw_cards()

    def draw_cards(self):
        folder_path = "C:/Users/frontier-Python/Desktop/trump"
        if os.path.exists(folder_path):
            self.computer_card = random.choice(self.cards)
            computer_image_path = os.path.join(folder_path, self.computer_card['image'])
            computer_image = Image.open(computer_image_path).resize((200, 250))
            self.computer_photo = ImageTk.PhotoImage(computer_image)
            self.canvas.create_image(350, 0, anchor=tk.NW, image=self.computer_photo)
            self.computer_card_label.config(text="コンピューターのカード: " + self.computer_card['value'])

            self.player_card = None
            self.player_photo = None
            self.player_canvas.delete("all")
            self.player_card_label.config(text="プレイヤーのカード: ")
        else:
            self.result_label.config(text="No image files found in the specified folder.")

    def high_guess(self):
        self.get_new_player_card()
        self.evaluate_guess("high")

    def low_guess(self):
        self.get_new_player_card()
        self.evaluate_guess("low")

    def get_new_player_card(self):
        self.player_card = random.choice(self.cards)
        player_image_path = os.path.join("C:/Users/frontier-Python/Desktop/trump", self.player_card['image'])
        player_image = Image.open(player_image_path).resize((200, 250))
        self.player_photo = ImageTk.PhotoImage(player_image)
        self.player_canvas.create_image(50, 0, anchor=tk.NW, image=self.player_photo)
        self.player_card_label.config(text="プレイヤーのカード: " + self.player_card['value'])

    def evaluate_guess(self, guess):
        if self.computer_card is None or self.player_card is None:
            return

        player_value = int(self.player_card['value'])
        computer_value = int(self.computer_card['value'])

        result = ""

        if guess == "high":
            if player_value > computer_value:
                result = "プレイヤーの勝利！"
            elif player_value < computer_value:
                result = "コンピューターの勝利！"
            else:
                result = "引き分けです！"
        elif guess == "low":
            if player_value < computer_value:
                result = "プレイヤーの勝利！"
            elif player_value > computer_value:
                result = "コンピューターの勝利！"
            else:
                result = "引き分けです！"

        self.result_label.config(text=result)

        continue_dialog = ContinueDialog(self)
        self.wait_window(continue_dialog)

        if continue_dialog.result == "はい":
            self.draw_cards()
            self.result_label.config(text="")
        else:
            self.quit()
    


if __name__ == "__main__":
    app = HighLowGame()
    app.mainloop()
