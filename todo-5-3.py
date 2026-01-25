import tkinter as tk
import customtkinter as ctk
import json
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Configuration
THEMES = {
    "Skyrim": {"img": "skyrim.png"},
    "8-Bit Wizard": {"img": "wizard.png"},
    "Cyberpunk 64": {"img": "cyberpunk.png"},
    "Infinity Blade": {"img": "knight.png"}
}


class QuestLogApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # UI Scaling for Ubuntu High-DPI
        ctk.set_widget_scaling(1.4)
        ctk.set_appearance_mode("dark")

        self.title("Hero's Quest Log")
        self.geometry("1100x800")

        # XP and Leveling State
        self.game_data = {
            "tasklist": [],
            "donelist": [],
            "xp": 0,
            "level": 1
        }
        self.current_theme_img = None

        # 1. BACKGROUND LABEL (Lowest Layer)
        # We use a label placed with .place to ensure it covers the window
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 2. UI CONTAINER (Transparent Layer on top)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<Configure>", self.on_resize)
        self.show_home_screen()

    def on_resize(self, event):
        if self.current_theme_img:
            self.draw_background(event.width, event.height)

    def draw_background(self, width, height):
        try:
            # Get absolute path to ensure Ubuntu/Pycharm finds the file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, self.current_theme_img)

            if os.path.exists(img_path):
                img = Image.open(img_path).resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image_tk = ImageTk.PhotoImage(img)
                self.bg_label.configure(image=self.bg_image_tk)
                self.bg_label.lower()  # Force background to stay behind UI
        except Exception as e:
            print(f"BG Error: {e}")

    # --- LEVELING LOGIC ---
    def add_xp(self, amount):
        self.game_data["xp"] += amount
        while self.game_data["xp"] >= 100:
            self.game_data["xp"] -= 100
            self.game_data["level"] += 1
            messagebox.showinfo("LEVEL UP!", f"Congratulations! You reached Level {self.game_data['level']}!")

    # --- SCREENS ---
    def show_home_screen(self):
        for widget in self.container.winfo_children(): widget.destroy()
        self.current_theme_img = None
        self.bg_label.configure(image="")  # Reset BG

        menu_card = ctk.CTkFrame(self.container, fg_color="#1a1a1a", corner_radius=15, border_width=2)
        menu_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.6)

        ctk.CTkLabel(menu_card, text="QUEST LOG", font=("Courier", 40, "bold")).pack(pady=30)
        ctk.CTkButton(menu_card, text="LOAD SAVED PROGRESS", command=self.load_file).pack(pady=10)

        self.theme_var = ctk.StringVar(value="Skyrim")
        ctk.CTkOptionMenu(menu_card, values=list(THEMES.keys()), variable=self.theme_var).pack(pady=10)

        ctk.CTkButton(menu_card, text="START ADVENTURE", fg_color="#2ecc71", command=self.start_app).pack(pady=30)

    def start_app(self):
        self.current_theme_img = THEMES[self.theme_var.get()]["img"]
        self.draw_background(self.winfo_width(), self.winfo_height())
        self.show_main_interface()

    def show_main_interface(self):
        for widget in self.container.winfo_children(): widget.destroy()

        # TOP BAR with LEVEL and XP
        nav_bar = ctk.CTkFrame(self.container, fg_color="#111111", corner_radius=0)
        nav_bar.pack(side="top", fill="x")

        ctk.CTkButton(nav_bar, text="Main Menu", width=80, command=self.show_home_screen).pack(side="left", padx=20,
                                                                                               pady=10)

        # XP Bar Label
        xp_text = f"LVL: {self.game_data['level']} | XP: {self.game_data['xp']}/100"
        self.stats_label = ctk.CTkLabel(nav_bar, text=xp_text, font=("Courier", 18, "bold"), text_color="#f1c40f")
        self.stats_label.pack(side="left", padx=40)

        ctk.CTkButton(nav_bar, text="Save Progress", width=120, fg_color="#333333", command=self.export_file).pack(
            side="right", padx=20, pady=10)

        # TABS
        self.tabview = ctk.CTkTabview(self.container, fg_color="#1a1a1a")
        self.tabview.pack(fill="both", expand=True, padx=50, pady=(10, 20))
        self.tabview.add("Active Quests")
        self.tabview.add("Completed")

        # INPUT
        entry_frame = ctk.CTkFrame(self.container, fg_color="#111111")
        entry_frame.pack(side="bottom", fill="x", padx=50, pady=20)
        self.entry = ctk.CTkEntry(entry_frame, placeholder_text="New objective...")
        self.entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        ctk.CTkButton(entry_frame, text="ADD QUEST", width=100, command=self.add_task).pack(side="right", padx=10)

        self.refresh_lists()

    def refresh_lists(self):
        # FIX: Check if tabview actually exists before trying to refresh
        if not hasattr(self, 'tabview'):
            return

        for tab in ["Active Quests", "Completed"]:
            for widget in self.tabview.tab(tab).winfo_children(): widget.destroy()

        for task in self.game_data["tasklist"]:
            f = ctk.CTkFrame(self.tabview.tab("Active Quests"), fg_color="#2b2b2b")
            f.pack(fill="x", pady=4, padx=10)
            ctk.CTkLabel(f, text=f"⚔️ {task}").pack(side="left", padx=15)
            ctk.CTkButton(f, text="Done (+10XP)", width=100, fg_color="#2ecc71",
                          command=lambda t=task: self.confirm_completion(t)).pack(side="right", padx=10)

        for task in self.game_data["donelist"]:
            ctk.CTkLabel(self.tabview.tab("Completed"), text=f"✔️ {task}", text_color="gray").pack(fill="x", pady=2,
                                                                                                   padx=20, anchor="w")

    def add_task(self):
        if t := self.entry.get():
            self.game_data["tasklist"].append(t)
            self.entry.delete(0, 'end')
            self.refresh_lists()

    def confirm_completion(self, task):
        if messagebox.askyesno("Quest", f"Complete '{task}'?"):
            self.game_data["tasklist"].remove(task)
            self.game_data["donelist"].append(task)
            self.add_xp(10)
            self.stats_label.configure(text=f"LVL: {self.game_data['level']} | XP: {self.game_data['xp']}/100")
            self.refresh_lists()

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            with open(path, 'r') as f:
                self.game_data = json.load(f)
            # Ensure keys exist if loading an old save without XP
            self.game_data.setdefault("xp", 0)
            self.game_data.setdefault("level", 1)

            # Check if we are on the main interface before refreshing UI
            if hasattr(self, 'tabview'):
                self.refresh_lists()
            messagebox.showinfo("Success", "Questlog Loaded! Press 'Start Adventure' to see them.")

    def export_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            with open(path, 'w') as f: json.dump(self.game_data, f, indent=4)
            messagebox.showinfo("Success", "Progress Saved!")


if __name__ == "__main__":
    app = QuestLogApp()
    app.mainloop()
