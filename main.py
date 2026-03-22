import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

class TimeTableApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Time Table")
        self.geometry("1200x600")

        # メインフレーム
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_grid()

    def create_grid(self):
        # 左上空白
        ctk.CTkLabel(self.grid_frame, text="").grid(row=0, column=0)

        # 時間（横）
        for hour in range(24):
            label = ctk.CTkLabel(self.grid_frame, text=str(hour))
            label.grid(row=0, column=hour + 1, padx=2, pady=2)

        # 曜日（縦） + マス
        self.cells = {}

        for r, day in enumerate(DAYS):
            # 曜日ラベル
            ctk.CTkLabel(self.grid_frame, text=day).grid(row=r + 1, column=0)

            for c in range(24):
                frame = ctk.CTkFrame(self.grid_frame, width=40, height=30)
                frame.grid(row=r + 1, column=c + 1, padx=1, pady=1)
                frame.grid_propagate(False)

                # クリックで仮カード追加
                frame.bind("<Button-1>", lambda e, d=day, h=c: self.add_card(d, h))

                self.cells[(day, c)] = frame

    def add_card(self, day, hour):
        frame = self.cells[(day, hour)]

        # 既存を消す（簡易）
        for widget in frame.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(frame, text="Task", fg_color="green", corner_radius=5)
        label.pack(fill="both", expand=True, padx=2, pady=2)


if __name__ == "__main__":
    app = TimeTableApp()
    app.mainloop()