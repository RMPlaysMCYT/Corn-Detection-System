import tkinter as tk
from tkinter import ttk


THEME_BG = "#2b2b2b"
THEME_FG = "#e8e8e8"
THEME_ACCENT = "#4a9eff"
THEME_ACCENT_FG = "#ffffff"
THEME_FIELD_BG = "#3c3c3c"
THEME_FONT = ("Segoe UI", 10)


def apply_theme(root):
    """Apply the project theme as defaults; per-widget options override these."""
    root.configure(bg=THEME_BG)
    root.option_add("*background", THEME_BG)
    root.option_add("*foreground", THEME_FG)
    root.option_add("*font", THEME_FONT)
    root.option_add("*Entry.background", THEME_FIELD_BG)
    root.option_add("*Text.background", THEME_FIELD_BG)
    root.option_add("*Listbox.background", THEME_FIELD_BG)
    root.option_add("*Button.background", THEME_ACCENT)
    root.option_add("*Button.foreground", THEME_ACCENT_FG)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(".", background=THEME_BG, foreground=THEME_FG, fieldbackground=THEME_FIELD_BG, font=THEME_FONT)


class Main:
    def __init__(self, root):
        self.root = root
        root.title("Main")
        root.geometry("400x300")
        root.update_idletasks()
        root.geometry(
            f"+{(root.winfo_screenwidth() - 400) // 2}"
            f"+{(root.winfo_screenheight() - 300) // 2}"
        )
        apply_theme(root)

        self.frame1 = tk.Frame(root, relief="groove", bd=2)
        self.frame1.place(x=0, y=0, width=400, height=300)

        self.label1 = tk.Label(root, text="Corn Detetcion System")
        self.label1.place(x=10, y=10, width=150, height=30)

        self.label2 = tk.Label(root, text="", bg="#c27070")
        self.label2.place(x=10, y=50, width=380, height=230)

        self.label3 = tk.Label(root, text="Status")
        self.label3.place(x=20, y=60, width=180, height=30)

        self.label4 = tk.Label(root, text="NaN")
        self.label4.place(x=200, y=60, width=180, height=30)

        self.label5 = tk.Label(root, text="No. of Seeds Detected")
        self.label5.place(x=20, y=90, width=180, height=30)

        self.label6 = tk.Label(root, text="NaN")
        self.label6.place(x=200, y=90, width=180, height=30)

        self.label7 = tk.Label(root, text="No. of Healthy Seeds")
        self.label7.place(x=20, y=120, width=180, height=30)

        self.label8 = tk.Label(root, text="NaN")
        self.label8.place(x=200, y=120, width=180, height=30)

        self.label9 = tk.Label(root, text="No. of Unealthy Seeds")
        self.label9.place(x=20, y=150, width=180, height=30)

        self.label10 = tk.Label(root, text="NaN")
        self.label10.place(x=200, y=150, width=180, height=30)

        self.button1 = tk.Button(root, text="START SORTING", command=self.on_button1, fg="#2b2727", bg="#748daa", font=("Helvetica", 10, "bold"))
        self.button1.place(x=30, y=210, width=340, height=60)

    def open_sorting_state(self):
        return SortingState(self.root)

    def on_button1(self):
        self.open_sorting_state()


class SortingState:
    def __init__(self, master):
        root = tk.Toplevel(master)
        self.root = root
        root.title("Sorting State")
        root.geometry("400x300")
        apply_theme(root)

        self.frame1 = tk.Frame(root, relief="groove", bd=2)
        self.frame1.place(x=0, y=0, width=400, height=300)

        self.label1 = tk.Label(self.frame1, text="", bg="#463f3f")
        self.label1.place(x=10, y=50, width=380, height=230)

        self.label4 = tk.Label(self.frame1, text="No. of Seeds Detected")
        self.label4.place(x=20, y=110, width=180, height=30)

        self.label5 = tk.Label(self.frame1, text="Status")
        self.label5.place(x=20, y=76, width=180, height=30)

        self.label6 = tk.Label(self.frame1, text="No. of Healthy Seeds")
        self.label6.place(x=20, y=135, width=180, height=30)

        self.label7 = tk.Label(self.frame1, text="No. of Unealthy Seeds")
        self.label7.place(x=26, y=165, width=180, height=30)

        self.label8 = tk.Label(self.frame1, text="Sorting")
        self.label8.place(x=200, y=76, width=180, height=30)

        self.label9 = tk.Label(self.frame1, text="NaN")
        self.label9.place(x=200, y=106, width=180, height=30)

        self.label10 = tk.Label(self.frame1, text="NaN")
        self.label10.place(x=200, y=136, width=180, height=30)

        self.label11 = tk.Label(self.frame1, text="NaN")
        self.label11.place(x=200, y=160, width=180, height=30)

        self.label12 = tk.Label(self.frame1, text="Corn Detetcion System")
        self.label12.place(x=10, y=10, width=150, height=30)

        self.button1 = tk.Button(self.frame1, text="START SORTING", command=self.on_button1, fg="#2b2727", bg="#748daa", font=("Helvetica", 10, "bold"), state="disabled")
        self.button1.place(x=26, y=210, width=340, height=60)

    def on_button1(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
