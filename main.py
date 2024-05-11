import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import random
from database import Database
from session import Session
from objects import *


class Window:
    def __init__(self, master):
        # Master settings
        self.master = master
        self.master.title("Saper")

        self.get_window_size()
        self.fullscreen_mode = True
        if self.fullscreen_mode:
            self.master.attributes("-fullscreen", True)
        else:
            self.master.geometry(f"{self.width}x{self.height}+{self.center_width}+{self.center_height}")
        self.master.resizable(False, False)
        self.master.bind("<Escape>", self.confirm_exit)

        # Tester mode
        self.is_testing = True

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

        # Colors
        self.tile_color = "#2c6cab"
        self.tile_flagged_color = "#2cab5b"
        self.tile_mine_color = "#b80000"
        self.tile_revealed_color = "#6d7073"

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Login menu
        self.login_menu()

    def get_window_size(self):
        self.screen_width = self.master.winfo_screenwidth() - 100
        self.screen_height = self.master.winfo_screenheight() - 100

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
            messagebox.showinfo("Informacja", "Taki użytkownik już istnieje")
        else:
            user = self.db.create_user(username=username, password=password)
            messagebox.showinfo("Informacja", "Stworzono użytkownika")
            self.login_user(user=user)

    def login_user(self, user):
        self.session.login(user)
        messagebox.showinfo("Informacja", f"Zalogowano jako: {self.session.user_username}")
        self.change_frame(old=self.login_menu_frame, new_func=self.main_menu)

    def login_submit(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        user_exist = self.db.check_user(username=username, password=password)

        if self.is_testing:
            user_exist = self.db.check_user(username="admin", password="admin")

        if user_exist:
            self.login_user(user=user_exist)
        else:
            messagebox.showinfo("Informacja", "Nie istnieje")

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

    def level_selection(self):
        # Level Frame
        self.level_frame = ctk.CTkFrame(self.main_frame)
        self.level_frame.pack(fill=tk.BOTH, expand=True)

        # Level Widgets
        amateur_button = ctk.CTkButton(self.level_frame, text="Amator", corner_radius=20,
                                       command=lambda: self.start_game(0))
        medium_button = ctk.CTkButton(self.level_frame, text="Średni", corner_radius=20,
                                      command=lambda: self.start_game(1))
        expert_button = ctk.CTkButton(self.level_frame, text="Ekspert", corner_radius=20,
                                      command=lambda: self.start_game(2))
        back_button = ctk.CTkButton(self.level_frame, text="Powrót do menu", corner_radius=20,
                                    command=lambda: self.change_frame(old=self.level_frame,
                                                                      new_func=self.main_menu))

        # Configure Widgets
        self.set_font(frame=self.level_frame)

        # Level Widgets Placing
        amateur_button.place(relx=0.5, rely=0.2, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        medium_button.place(relx=0.5, rely=0.4, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        expert_button.place(relx=0.5, rely=0.6, relwidth=self.relwidth, relheight=self.relheight, anchor="center")
        back_button.place(relx=0.5, rely=0.9, relwidth=self.relwidth, relheight=self.relheight, anchor="center")

    def start_game(self, difficulty):
        self.difficulty = difficulty

        if self.difficulty == 0:
            self.rows = 9
            self.cols = 9
            self.mines = 10
        elif self.difficulty == 1:
            self.rows = 16
            self.cols = 16
            self.mines = 40
        elif self.difficulty == 2:
            self.mines = 99
            if self.width > self.height:
                self.rows = 16
                self.cols = 30
            elif self.width > self.height:
                self.rows = 30
                self.cols = 16
            elif self.width == self.height:
                self.rows = 20
                self.cols = 24

        self.change_frame(old=self.level_frame, new_func=self.new_game)

    def new_game(self):
        if hasattr(self, "main_game_frame"):
            self.main_game_frame.destroy()

        # Main Game Frame
        self.main_game_frame = ctk.CTkFrame(self.main_frame)
        self.main_game_frame.pack(fill=tk.BOTH, expand=True)

        # Main Game Widgets
        self.time_label = ctk.CTkLabel(master=self.main_game_frame,
                                       text="00:00")
        self.count_mines_label = ctk.CTkLabel(master=self.main_game_frame,
                                              text=self.mines)
        back_button = ctk.CTkButton(self.main_game_frame, text="Powrót do menu", corner_radius=20,
                                    command=lambda: self.change_frame(old=self.main_game_frame,
                                                                      new_func=self.main_menu))

        # Configure Widgets
        self.set_font(frame=self.main_game_frame)

        # Main Game Widgets Placing
        self.time_label.place(relx=0.6, rely=0.05, relheight=0.1, anchor="center")
        self.count_mines_label.place(relx=0.4, rely=0.05, relheight=0.1, anchor="center")
        back_button.place(relx=0.5, rely=0.9, relwidth=self.relwidth, relheight=self.relheight, anchor="center")

        # Board Frame
        self.board_frame = ctk.CTkFrame(self.main_game_frame, fg_color="#e0e0e0")
        self.board_frame.place(relx=0.5, rely=0.45, relwidth=(0.7 / self.ratio) / (self.rows/self.cols),
                               relheight=0.7, anchor="center")

        # Functions
        self.generate_board()
        self.start_time = time.time()
        self.update_time()

    def generate_board(self):
        self.board = Board(rows=self.rows,
                           cols=self.cols,
                           mines=self.mines)

        self.board.generate_board()

        self.buttons = []

        for row in range(0, self.board.rows):
            self.board_frame.grid_rowconfigure(row, weight=1)
            for col in range(0, self.board.cols):
                self.board_frame.grid_columnconfigure(col, weight=1)

                button = ctk.CTkButton(self.board_frame, text=" ", fg_color=self.tile_color)
                button.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

                if self.is_testing:
                    cell = self.board.get_cell_by_axis(x=row, y=col)
                    button.configure(text=cell.value)

                button.bind("<Button-1>", lambda event, row=row, col=col, button=button: self.click_tile(row, col, button))
                button.bind("<Button-3>", lambda event, row=row, col=col, button=button: self.mark_flag(row, col, button))

    def click_tile(self, row, col, button):
        if button.cget('state') == 'disabled':
            return

        cell = self.board.get_cell_by_axis(x=row, y=col)

        if cell.value == -1:
            button.configure(fg_color=self.tile_mine_color)
            messagebox.showinfo("Game Over", "Trafiłeś na minę. Przegrałeś!")
            self.change_frame(old=self.main_game_frame, new_func=self.main_menu)
        else:
            self.board.check_value(cell)
            button.configure(fg_color=self.tile_revealed_color)
            if self.board.tiles_revealed == self.board.tiles - 1 - self.board.mines:
                self.player_win()
            self.reveal_empty(cell)
            button.configure(text=self.board.check_value(tile=cell), state='disabled')

    def reveal_empty(self, cell):
        self.board.check_value(tile=cell)
        self.board.check_tiles_revealed(tile=cell)

    def mark_flag(self, row, col, button):
        cell = self.board.get_cell_by_axis(x=row, y=col)

        if not cell.is_revealed:
            if not cell.is_flagged:
                button.configure(fg_color=self.tile_flagged_color)
                cell.is_flagged = True
                self.board.flags += 1
                if cell.value == -1:
                    self.board.mines_revealed += 1
                button.configure(state='disabled')
            else:
                button.configure(fg_color=self.tile_color, state='normal')
                cell.is_flagged = False
                self.board.flags -= 1
                if cell.value == -1:
                    self.board.mines_revealed -= 1

            if self.board.flags == self.board.mines_revealed and self.board.mines == self.board.mines_revealed:
                self.player_win()

    def player_win(self):
        self.db.insert_score(user_id=self.session.user_id,
                             difficulty_level=self.difficulty,
                             score=self.get_time())
        messagebox.showinfo("You won", "Wygrałeś!")
        self.change_frame(old=self.main_game_frame, new_func=self.main_menu)

    def get_time(self):
        return int(time.time() - self.start_time)

    def update_time(self):
        current_time = int(time.time() - self.start_time)

        time_str = "{:02d}".format(current_time)

        self.time_label.configure(text=time_str)
        self.time_label.after(1000, self.update_time)


def main():
    root = ctk.CTk()
    game_window = Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
