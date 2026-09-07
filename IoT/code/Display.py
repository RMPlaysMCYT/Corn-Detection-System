import tkinter as tk
from tkinter import ttk

# --- Theme constants (unchanged) ---
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
    style.configure(".", background=THEME_BG, foreground=THEME_FG,
                    fieldbackground=THEME_FIELD_BG, font=THEME_FONT)

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

        # Container frame that will hold all “pages”
        self.container = tk.Frame(root, bg=THEME_BG)
        self.container.place(x=0, y=0, width=400, height=300)

        # Start with the main page
        self.show_main_page()

    def show_main_page(self):
        """Clear the container and build the main (initial) page."""
        self._clear_container()
        # Create all widgets of the main page as children of self.container
        self.main_frame = tk.Frame(self.container, relief="groove", bd=2, bg=THEME_BG)
        self.main_frame.place(x=0, y=0, width=400, height=300)

        self.label1 = tk.Label(self.main_frame, text="Corn Detetcion System", bg=THEME_BG)
        self.label1.place(x=10, y=10, width=150, height=30)

        self.label2 = tk.Label(self.main_frame, text="", bg="#c27070")
        self.label2.place(x=10, y=50, width=380, height=230)

        self.label3 = tk.Label(self.main_frame, text="Status", bg=THEME_BG)
        self.label3.place(x=20, y=60, width=180, height=30)

        self.label4 = tk.Label(self.main_frame, text="NaN", bg=THEME_BG)
        self.label4.place(x=200, y=60, width=180, height=30)

        self.label5 = tk.Label(self.main_frame, text="No. of Seeds Detected", bg=THEME_BG)
        self.label5.place(x=20, y=90, width=180, height=30)

        self.label6 = tk.Label(self.main_frame, text="NaN", bg=THEME_BG)
        self.label6.place(x=200, y=90, width=180, height=30)

        self.label7 = tk.Label(self.main_frame, text="No. of Healthy Seeds", bg=THEME_BG)
        self.label7.place(x=20, y=120, width=180, height=30)

        self.label8 = tk.Label(self.main_frame, text="NaN", bg=THEME_BG)
        self.label8.place(x=200, y=120, width=180, height=30)

        self.label9 = tk.Label(self.main_frame, text="No. of Unealthy Seeds", bg=THEME_BG)
        self.label9.place(x=20, y=150, width=180, height=30)

        self.label10 = tk.Label(self.main_frame, text="NaN", bg=THEME_BG)
        self.label10.place(x=200, y=150, width=180, height=30)

        self.button1 = tk.Button(
            self.main_frame,
            text="START SORTING",
            command=self.show_sorting_page,   # now calls the new page
            fg="#2b2727",
            bg="#748daa",
            font=("Helvetica", 10, "bold")
        )
        self.button1.place(x=30, y=210, width=340, height=60)

    def show_sorting_page(self):
        """Clear the container and build the sorting page."""
        self._clear_container()
        # Build sorting page widgets as children of self.container
        self.sorting_frame = tk.Frame(self.container, relief="groove", bd=2, bg=THEME_BG)
        self.sorting_frame.place(x=0, y=0, width=400, height=300)

        # Background placeholder (like label1 in original SortingState)
        self.sort_bg = tk.Label(self.sorting_frame, text="", bg="#463f3f")
        self.sort_bg.place(x=10, y=50, width=380, height=230)

        self.sort_label_title = tk.Label(self.sorting_frame, text="Corn Detetcion System", bg=THEME_BG)
        self.sort_label_title.place(x=10, y=10, width=150, height=30)

        self.sort_label_status = tk.Label(self.sorting_frame, text="Status", bg=THEME_BG)
        self.sort_label_status.place(x=20, y=76, width=180, height=30)

        self.sort_label_status_val = tk.Label(self.sorting_frame, text="Sorting", bg=THEME_BG)
        self.sort_label_status_val.place(x=200, y=76, width=180, height=30)

        self.sort_label_seeds = tk.Label(self.sorting_frame, text="No. of Seeds Detected", bg=THEME_BG)
        self.sort_label_seeds.place(x=20, y=110, width=180, height=30)

        self.sort_label_seeds_val = tk.Label(self.sorting_frame, text="NaN", bg=THEME_BG)
        self.sort_label_seeds_val.place(x=200, y=110, width=180, height=30)

        self.sort_label_healthy = tk.Label(self.sorting_frame, text="No. of Healthy Seeds", bg=THEME_BG)
        self.sort_label_healthy.place(x=20, y=135, width=180, height=30)

        self.sort_label_healthy_val = tk.Label(self.sorting_frame, text="NaN", bg=THEME_BG)
        self.sort_label_healthy_val.place(x=200, y=135, width=180, height=30)

        self.sort_label_unhealthy = tk.Label(self.sorting_frame, text="No. of Unealthy Seeds", bg=THEME_BG)
        self.sort_label_unhealthy.place(x=20, y=165, width=180, height=30)

        self.sort_label_unhealthy_val = tk.Label(self.sorting_frame, text="NaN", bg=THEME_BG)
        self.sort_label_unhealthy_val.place(x=200, y=165, width=180, height=30)

        # “START SORTING” button – still disabled as per original
        self.sort_button = tk.Button(
            self.sorting_frame,
            text="START SORTING",
            command=self.do_sort,    # placeholder for actual sorting
            fg="#2b2727",
            bg="#748daa",
            font=("Helvetica", 10, "bold"),
            state="disabled"
        )
        self.sort_button.place(x=26, y=210, width=340, height=60)


    def do_sort(self):
        """Placeholder for the actual sorting logic."""
        pass

    def _clear_container(self):
        """Remove all child widgets from the container."""
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()