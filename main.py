import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import random
from database import Database
from session import Session


class Window:
    def __init__(self, master):
        # Master settings
        self.master = master
        self.master.title("Saper")

        self.get_window_size()

        self.master.geometry(f"{self.width}x{self.height}+{self.center_width}+{self.center_height}")
        self.master.resizable(False, False)
        self.master.bind("<Escape>", self.confirm_exit)

        # Font settings
        self.font_family = "Arial"
        self.font_family_sec = "Bauhaus 93"
        if 1920 >= self.width > 1600 and 1080 >= self.height > 900:
            self.main_font = ctk.CTkFont(family=self.font_family, size=36)
            self.smaller_font = ctk.CTkFont(family=self.font_family, size=32)
            self.bigger_font = ctk.CTkFont(family=self.font_family_sec, size=256)
        elif 1600 >= self.width > 1280 and 900 >= self.height > 720:
            self.main_font = ctk.CTkFont(family=self.font_family, size=32)
            self.smaller_font = ctk.CTkFont(family=self.font_family, size=28)
            self.bigger_font = ctk.CTkFont(family=self.font_family_sec, size=224)
        elif 1280 >= self.width > 960 and 720 >= self.height > 540:
            self.main_font = ctk.CTkFont(family=self.font_family, size=28)
            self.smaller_font = ctk.CTkFont(family=self.font_family, size=24)
            self.bigger_font = ctk.CTkFont(family=self.font_family_sec, size=208)
        else:
            self.main_font = ctk.CTkFont(family=self.font_family, size=24)
            self.smaller_font = ctk.CTkFont(family=self.font_family, size=20)
            self.bigger_font = ctk.CTkFont(family=self.font_family_sec, size=196)

        # DB and Session
        self.db = Database()
        self.db.initialize_database()
        self.session = Session()

        # Game settings
        self.disabled_buttons = set()
        self.relwidth = 0.35
        self.relheight = 0.075

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Login menu
        self.login_menu()

    def get_window_size(self):
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        if self.screen_width > 1920:
            self.width = 1920
        else:
            self.width = self.screen_width

        if self.screen_height > 1080:
            self.height = 1080
        else:
            self.height = self.screen_height

        self.center_width = (self.screen_width - self.width) // 2
        self.center_height = (self.screen_height - self.height) // 2

        self.ratio = self.width / self.height

    def set_font(self, frame):
        for widget in frame.winfo_children():
            widget.configure(font=self.main_font)

    def confirm_exit(self, event=None):
        if messagebox.askyesno("Wyjście", "Czy na pewno chcesz wyjść z gry?"):
            self.master.destroy()

    def change_frame(self, old, new_func):
        old.destroy()
        new_func()

    def login_menu(self):
        # Login Frame
        self.login_menu_frame = ctk.CTkFrame(self.main_frame)
        self.login_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Login Widgets
        register_label = ctk.CTkLabel(master=self.login_menu_frame, text="Nie masz konta?")
        register_button = ctk.CTkButton(master=self.login_menu_frame, text="Stwórz konto", corner_radius=20,
                                        command=lambda: self.change_frame(self.login_menu_frame,
                                                                          self.register_menu))
        login_label = ctk.CTkLabel(master=self.login_menu_frame, text="Login")
        self.login_entry = ctk.CTkEntry(master=self.login_menu_frame, corner_radius=20)
        password_label = ctk.CTkLabel(master=self.login_menu_frame, text="Hasło")
        self.password_entry = ctk.CTkEntry(master=self.login_menu_frame, show="*", corner_radius=20)
        submit_button = ctk.CTkButton(master=self.login_menu_frame, text="Zaloguj się",
                                      command=self.login_submit, corner_radius=20)

        # Configure Widgets
        self.set_font(frame=self.login_menu_frame)
        register_label.configure(font=self.smaller_font)

        # Login Widgets Placing
        login_label.place(relx=0.5, rely=3 / 16, anchor="center")
        self.login_entry.place(relx=0.5, rely=4 / 16, relwidth=self.relwidth, relheight=self.relheight,
                               anchor="center")
        password_label.place(relx=0.5, rely=6 / 16, anchor="center")
        self.password_entry.place(relx=0.5, rely=7 / 16, relwidth=self.relwidth, relheight=self.relheight,
                                  anchor="center")
        submit_button.place(relx=0.5, rely=9 / 16, relwidth=self.relwidth, relheight=self.relheight,
                            anchor="center")
        register_label.place(relx=0.5, rely=12 / 16, anchor="center")
        register_button.place(relx=0.5, rely=13 / 16, relwidth=self.relwidth, relheight=self.relheight,
                              anchor="center")

    def register_menu(self):
        # Login Frame
        self.login_menu_frame = ctk.CTkFrame(self.main_frame)
        self.login_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Login Widgets
        login_ask_label = ctk.CTkLabel(master=self.login_menu_frame, text="Masz już konto?")
        login_button = ctk.CTkButton(master=self.login_menu_frame, text="Zaloguj się",
                                     command=lambda: self.change_frame(self.login_menu_frame,
                                                                       self.login_menu))
        login_label = ctk.CTkLabel(master=self.login_menu_frame, text="Login")
        self.login_entry = ctk.CTkEntry(master=self.login_menu_frame, corner_radius=20)
        password_label = ctk.CTkLabel(master=self.login_menu_frame, text="Hasło")
        self.password_entry = ctk.CTkEntry(master=self.login_menu_frame, show="*", corner_radius=20)
        submit_button = ctk.CTkButton(master=self.login_menu_frame, text="Zarejestruj się",
                                      command=self.create_user, corner_radius=20)

        # Configure Widgets
        self.set_font(frame=self.login_menu_frame)

        # Login Widgets Placing
        login_label.place(relx=0.5, rely=0.25, anchor="center")
        self.login_entry.place(relx=0.5, rely=0.32, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        password_label.place(relx=0.5, rely=0.4, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.47, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        submit_button.place(relx=0.5, rely=0.6, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        login_ask_label.place(relx=0.5, rely=0.8, anchor="center")
        login_button.place(relx=0.5, rely=0.9, relwidth=self.relwidth, relheight=self.relheight, anchor="center")

    def create_user(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        user_exist = self.db.check_user(username=username, password=password)

        if user_exist:
            print("Taki użytkownik już istnieje")
        else:
            user = self.db.create_user(username=username, password=password)
            self.login_user(user=user)

    def login_user(self, user):
        self.session.login(user)
        print(f"Zalogowano jako: {self.session.user_username}")
        self.change_frame(old=self.login_menu_frame, new_func=self.main_menu)

    def login_submit(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        user_exist = self.db.check_user(username=username, password=password)

        if user_exist:
            self.login_user(user=user_exist)
        else:
            print("nie istnieje")

    def level_selection(self):
        # Level Frame
        self.level_frame = ctk.CTkFrame(self.main_frame)
        self.level_frame.pack(fill=tk.BOTH, expand=True)

        # Level Widgets
        amateur_button = ctk.CTkButton(self.level_frame, text="Amator", corner_radius=20,
                                       command=lambda: self.start_game(9, 9, 10))
        medium_button = ctk.CTkButton(self.level_frame, text="Średni", corner_radius=20,
                                      command=lambda: self.start_game(16, 16, 40))
        expert_button = ctk.CTkButton(self.level_frame, text="Ekspert", corner_radius=20,
                                      command=lambda: self.start_game(30, 16, 99))

        # Configure Widgets
        self.set_font(frame=self.level_frame)

        # Level Widgets Placing
        amateur_button.place(relx=0.5, rely=0.3, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        medium_button.place(relx=0.5, rely=0.5, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        expert_button.place(relx=0.5, rely=0.7, relwidth=self.relwidth, relheight=self.relheight, anchor="center")

    def start_game(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.change_frame(old=self.level_frame, new_func=self.new_game)

    def main_menu(self):
        # Main Menu Frame
        self.main_menu_frame = ctk.CTkFrame(self.main_frame)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Main Menu Widgets
        title_label = ctk.CTkLabel(self.main_menu_frame, text="Saper")
        new_game_button = ctk.CTkButton(self.main_menu_frame, text="Nowa gra", corner_radius=20,
                                        command=lambda: self.change_frame(old=self.main_menu_frame,
                                                                          new_func=self.level_selection))
        scoreboard_button = ctk.CTkButton(self.main_menu_frame, text="Sala chwały", corner_radius=20)
        exit_button = ctk.CTkButton(self.main_menu_frame, text="Wyjście", corner_radius=20,
                                    command=self.confirm_exit)
        login_label = ctk.CTkLabel(self.main_menu_frame, text=self.session.user_username)

        # Configure Widgets
        self.set_font(frame=self.main_menu_frame)
        title_label.configure(font=self.bigger_font)

        # Main Menu Widgets Placing
        login_label.place(relx=0.99, rely=0.01, anchor="ne")
        title_label.place(relx=0.5, rely=0.25, anchor="center")
        new_game_button.place(relx=0.5, rely=0.55, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        scoreboard_button.place(relx=0.5, rely=0.7, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        exit_button.place(relx=0.5, rely=0.85, relwidth=self.relwidth, relheight=self.relheight, anchor="center")

    def new_game(self):
        # Main Game Frame
        self.main_game_frame = ctk.CTkFrame(self.main_frame)
        self.main_game_frame.pack(fill=tk.BOTH, expand=True)

        # Main Game Widgets
        self.time_label = ctk.CTkLabel(master=self.main_game_frame,
                                       text="00:00")

        # Main Game Widgets Placing
        self.time_label.place(relx=0.5, rely=0.075, relheight=0.1, anchor="center")

        # Functions
        self.start_time = time.time()
        self.update_time()

        # Board Frame
        self.board_frame = ctk.CTkFrame(self.main_game_frame, fg_color="#e0e0e0")
        self.board_frame.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.4, anchor="center")

        # Functions
        self.generate_board()

    def generate_board(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.flags = set()

        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] == 0:
                self.board[row][col] = -1
                mines_placed += 1

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1:
                    self.board[row][col] = sum(1 for r in range(row - 1, row + 2)
                                               for c in range(col - 1, col + 2)
                                               if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == -1)

        self.buttons = [[None] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            self.board_frame.grid_rowconfigure(i, weight=1)
            for j in range(self.cols):
                self.board_frame.grid_columnconfigure(j, weight=1)
                button = ctk.CTkButton(self.board_frame)
                button.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                button.bind("<Button-1>", lambda event, row=i, col=j: self.click_tile(row, col))
                button.bind("<Button-3>", lambda event, row=i, col=j: self.mark_flag(row, col, event))
                if self.board[i][j] == -1:
                    button.configure(text="*")
                else:
                    button.configure(text="")
                self.buttons[i][j] = button

    def click_tile(self, row, col):
        if self.board[row][col] == -1:
            messagebox.showinfo("Game Over", "You clicked on a mine! Game Over.")
            self.change_frame(old=self.main_game_frame, new_func=self.main_menu)
        else:
            self.reveal_empty(row, col)

    def reveal_empty(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols and (row, col) not in self.disabled_buttons:
            self.disabled_buttons.add((row, col))
            self.buttons[row][col].configure(text=str(self.board[row][col]))
            if self.board[row][col] == 0:
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        self.reveal_empty(r, c)

    def mark_flag(self, row, col, event):
        if (row, col) in self.flags:
            self.flags.remove((row, col))
            if self.board[row][col] == -1:
                self.buttons[row][col].configure(text="*")
            else:
                self.buttons[row][col].configure(text=str(self.board[row][col]))
        else:
            self.flags.add((row, col))
            self.buttons[row][col].configure(text="F")

    def update_time(self):
        current_time = int(time.time() - self.start_time)
        minutes = current_time // 60
        seconds = current_time % 60

        time_str = "{:02d}:{:02d}".format(minutes, seconds)

        self.time_label.configure(text=time_str)
        self.time_label.after(1000, self.update_time)


def main():
    root = ctk.CTk()
    game_window = Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
