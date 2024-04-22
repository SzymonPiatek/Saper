import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import random
import database


class Session:
    def __init__(self):
        self.logged_in = False
        self.user = None
        self.user_username = None

    def login(self, username):
        self.user = username
        self.user_username = self.user[1]
        self.logged_in = True

    def logout(self):
        self.user = None
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in

    def get_username(self):
        return self.user_username


class Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Saper")
        self.master.geometry("1024x720+0+0")
        self.master.bind("<Escape>", self.confirm_exit)

        database.main()
        self.session = Session()


        self.ratio = 1024 / 720

        self.disabled_buttons = set()

        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)


        self.login_menu()

    def confirm_exit(self, event=None):
        if messagebox.askyesno("Wyjście", "Czy na pewno chcesz wyjść z gry?"):
            self.master.destroy()

    def change_frame(self, old, new_func):
        old.destroy()
        new_func()

    def login_menu(self):
        self.login_menu_frame = ctk.CTkFrame(self.main_frame)
        self.login_menu_frame.pack(fill=tk.BOTH, expand=True)

        register_button = ctk.CTkButton(master=self.login_menu_frame,
                                        text="Stwórz konto",
                                        command=lambda: self.change_frame(self.login_menu_frame,
                                                                          self.register_menu))

        login_label = ctk.CTkLabel(master=self.login_menu_frame,
                                   text="Login")
        self.login_entry = ctk.CTkEntry(master=self.login_menu_frame)

        password_label = ctk.CTkLabel(master=self.login_menu_frame,
                                      text="Hasło")
        self.password_entry = ctk.CTkEntry(master=self.login_menu_frame,
                                           show="*")

        submit_button = ctk.CTkButton(master=self.login_menu_frame,
                                      text="Zaloguj się",
                                      command=self.login_submit)

        login_label.place(relx=0.5, rely=0.35, relwidth=0.25, anchor="center")
        self.login_entry.place(relx=0.5, rely=0.4, relwidth=0.25, anchor="center")
        password_label.place(relx=0.5, rely=0.5, relwidth=0.25, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.55, relwidth=0.25, anchor="center")
        submit_button.place(relx=0.5, rely=0.7, relwidth=0.2, anchor="center")
        register_button.place(relx=0.5, rely=0.9, relwidth=0.2, anchor="center")

    def register_menu(self):
        self.login_menu_frame = ctk.CTkFrame(self.main_frame)
        self.login_menu_frame.pack(fill=tk.BOTH, expand=True)

        login_button = ctk.CTkButton(master=self.login_menu_frame,
                                     text="Zaloguj się",
                                     command=lambda: self.change_frame(self.login_menu_frame,
                                                                       self.login_menu))

        login_label = ctk.CTkLabel(master=self.login_menu_frame,
                                   text="Login")
        self.login_entry = ctk.CTkEntry(master=self.login_menu_frame)

        password_label = ctk.CTkLabel(master=self.login_menu_frame,
                                      text="Hasło")
        self.password_entry = ctk.CTkEntry(master=self.login_menu_frame,
                                           show="*")

        submit_button = ctk.CTkButton(master=self.login_menu_frame,
                                      text="Stwórz konto",
                                      command=self.create_user)

        login_label.place(relx=0.5, rely=0.35, relwidth=0.25, anchor="center")
        self.login_entry.place(relx=0.5, rely=0.4, relwidth=0.25, anchor="center")
        password_label.place(relx=0.5, rely=0.5, relwidth=0.25, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.55, relwidth=0.25, anchor="center")
        submit_button.place(relx=0.5, rely=0.7, relwidth=0.2, anchor="center")
        login_button.place(relx=0.5, rely=0.9, relwidth=0.2, anchor="center")

    def create_user(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        user_exist = database.check_user(username=username, password=password)

        if user_exist:
            print("Taki użytkownik już istnieje")
        else:
            user = database.create_user(username=username, password=password)
            self.login_user(user=user)

    def login_user(self, user):
        self.session.login(user)
        print(f"Zalogowano jako: {self.session.get_username()}")

    def login_submit(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        user_exist = database.check_user(username=username, password=password)

        if user_exist:
            self.login_user(user=user_exist)
        else:
            print("nie istnieje")

    def main_menu(self):
        self.main_menu_frame = ctk.CTkFrame(self.main_frame)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ctk.CTkLabel(self.main_menu_frame,
                                   text="Saper",
                                   corner_radius=20)
        new_game_button = ctk.CTkButton(self.main_menu_frame,
                                        text="Nowa gra",
                                        corner_radius=20,
                                        command=lambda: self.change_frame(self.main_menu_frame, self.new_game))
        scoreboard_button = ctk.CTkButton(self.main_menu_frame,
                                          text="Sala chwały",
                                          corner_radius=20)
        exit_button = ctk.CTkButton(self.main_menu_frame,
                                    text="Wyjście",
                                    corner_radius=20,
                                    command=self.confirm_exit)

        title_label.place(relx=0.5, rely=0.25, relwidth=1, relheight=0.5, anchor="center")
        new_game_button.place(relx=0.5, rely=0.55, relwidth=0.5, relheight=0.12, anchor="center")
        scoreboard_button.place(relx=0.5, rely=0.7, relwidth=0.5, relheight=0.12, anchor="center")
        exit_button.place(relx=0.5, rely=0.85, relwidth=0.5, relheight=0.12, anchor="center")

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
        self.board_frame.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.4 * self.ratio, anchor="center")

        self.rows = 10
        self.cols = 10
        self.mines = 10
        self.generate_board()

    def generate_board(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]

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
