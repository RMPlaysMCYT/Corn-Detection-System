import tkinter as tk
from tkinter import ttk
import threading
import time


from hardware import Camera, Servo
from model import CornClassifier, MockClassifier
from sorter import Sorter

import os

USE_MOCK_MODEL = True


THEME_BG = "#2b2b2b"
THEME_FG = "#e8e8e8"
THEME_ACCENT = "#4a9eff"
THEME_ACCENT_FG = "#ffffff"
THEME_FIELD_BG = "#3c3c3c"
THEME_FONT = ("Segoe UI", 10)

def apply_theme(root):
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

    
class CornSorterApp:
    def __init__(self, root):
        self.root = root
        root.title("Corn Detection System")
        root.geometry("400x300")
        root.update_idletasks()
        root.geometry(
            f"+{(root.winfo_screenwidth() - 400) // 2}"
            f"+{(root.winfo_screenheight() - 300) // 2}"
        )
        apply_theme(root)

        # Container for pages
        self.container = tk.Frame(root, bg=THEME_BG)
        self.container.place(x=0, y=0, width=400, height=300)

        
        # Model path – adjust to your actual .tflite file
        BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "OUTPUT_CapstoneProject_corn_seed_quality_detection_128x128_v0_0_1-stream.tflite")
        MODEL_PATH = os.path.normpath(MODEL_PATH)  # cleans up the ".." into a proper path
        if USE_MOCK_MODEL:
            self.classifier = MockClassifier(healthy_bias=0.7)
        else:
            self.classifier = CornClassifier(MODEL_PATH)
            print("Model loaded.")
            
        self.camera = Camera(camera_id=0)
        self.servo = Servo(pin=18)

        
        self.sorter = None

        
        self.show_main_page()

    # ---------- Page Management ----------
    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_page(self):
        self._clear_container()
        self.main_frame = tk.Frame(self.container, relief="groove", bd=2, bg=THEME_BG)
        self.main_frame.place(x=0, y=0, width=400, height=300)

        tk.Label(self.main_frame, text="Corn Detection System", bg=THEME_BG) \
            .place(x=10, y=10, width=150, height=30)

        tk.Label(self.main_frame, text="", bg="#c27070") \
            .place(x=10, y=50, width=380, height=230)

        tk.Label(self.main_frame, text="Status", bg=THEME_BG) \
            .place(x=20, y=60, width=180, height=30)
        self.main_status = tk.Label(self.main_frame, text="Ready", bg=THEME_BG)
        self.main_status.place(x=200, y=60, width=180, height=30)

        tk.Label(self.main_frame, text="No. of Seeds Detected", bg=THEME_BG) \
            .place(x=20, y=90, width=180, height=30)
        self.main_seeds = tk.Label(self.main_frame, text="0", bg=THEME_BG)
        self.main_seeds.place(x=200, y=90, width=180, height=30)

        tk.Label(self.main_frame, text="No. of Healthy Seeds", bg=THEME_BG) \
            .place(x=20, y=120, width=180, height=30)
        self.main_healthy = tk.Label(self.main_frame, text="0", bg=THEME_BG)
        self.main_healthy.place(x=200, y=120, width=180, height=30)

        tk.Label(self.main_frame, text="No. of Unhealthy Seeds", bg=THEME_BG) \
            .place(x=20, y=150, width=180, height=30)
        self.main_unhealthy = tk.Label(self.main_frame, text="0", bg=THEME_BG)
        self.main_unhealthy.place(x=200, y=150, width=180, height=30)

        tk.Button(
            self.main_frame,
            text="START SORTING",
            command=self.start_sorting,
            fg="#2b2727",
            bg="#748daa",
            font=("Helvetica", 10, "bold")
        ).place(x=30, y=210, width=340, height=60)

    def show_sorting_page(self):
        self._clear_container()
        self.sort_frame = tk.Frame(self.container, relief="groove", bd=2, bg=THEME_BG)
        self.sort_frame.place(x=0, y=0, width=400, height=300)

        tk.Label(self.sort_frame, text="", bg="#463f3f") \
            .place(x=10, y=50, width=380, height=230)

        tk.Label(self.sort_frame, text="Corn Detection System", bg=THEME_BG) \
            .place(x=10, y=10, width=150, height=30)

        tk.Label(self.sort_frame, text="Status", bg=THEME_BG) \
            .place(x=20, y=76, width=180, height=30)
        self.sort_status = tk.Label(self.sort_frame, text="Sorting...", bg=THEME_BG)
        self.sort_status.place(x=200, y=76, width=180, height=30)

        tk.Label(self.sort_frame, text="No. of Seeds Detected", bg=THEME_BG) \
            .place(x=20, y=110, width=180, height=30)
        self.sort_seeds = tk.Label(self.sort_frame, text="0", bg=THEME_BG)
        self.sort_seeds.place(x=200, y=110, width=180, height=30)

        tk.Label(self.sort_frame, text="No. of Healthy Seeds", bg=THEME_BG) \
            .place(x=20, y=135, width=180, height=30)
        self.sort_healthy = tk.Label(self.sort_frame, text="0", bg=THEME_BG)
        self.sort_healthy.place(x=200, y=135, width=180, height=30)

        tk.Label(self.sort_frame, text="No. of Unhealthy Seeds", bg=THEME_BG) \
            .place(x=26, y=165, width=180, height=30)
        self.sort_unhealthy = tk.Label(self.sort_frame, text="0", bg=THEME_BG)
        self.sort_unhealthy.place(x=200, y=165, width=180, height=30)

        # Disabled start button (visual)
        tk.Button(
            self.sort_frame,
            text="START SORTING",
            state="disabled",
            fg="#2b2727",
            bg="#748daa",
            font=("Helvetica", 10, "bold")
        ).place(x=26, y=210, width=340, height=60)

    def show_complete_page(self, total, healthy, unhealthy):
        self._clear_container()
        self.complete_frame = tk.Frame(self.container, relief="groove", bd=2, bg=THEME_BG)
        self.complete_frame.place(x=0, y=0, width=400, height=300)

        tk.Label(self.complete_frame, text="SORTING COMPLETE!", bg=THEME_BG,
                 font=("Helvetica", 14, "bold"), fg="#4aef4a") \
            .place(x=60, y=20, width=280, height=40)

        tk.Label(self.complete_frame, text="Total Seeds Processed", bg=THEME_BG) \
            .place(x=20, y=80, width=180, height=30)
        tk.Label(self.complete_frame, text=str(total), bg=THEME_BG) \
            .place(x=200, y=80, width=180, height=30)

        tk.Label(self.complete_frame, text="Healthy Seeds", bg=THEME_BG) \
            .place(x=20, y=120, width=180, height=30)
        tk.Label(self.complete_frame, text=str(healthy), bg=THEME_BG) \
            .place(x=200, y=120, width=180, height=30)

        tk.Label(self.complete_frame, text="Unhealthy Seeds", bg=THEME_BG) \
            .place(x=20, y=160, width=180, height=30)
        tk.Label(self.complete_frame, text=str(unhealthy), bg=THEME_BG) \
            .place(x=200, y=160, width=180, height=30)

        tk.Button(
            self.complete_frame,
            text="← BACK TO MAIN",
            command=self.reset_and_return,
            fg="#2b2727",
            bg="#748daa",
            font=("Helvetica", 10, "bold")
        ).place(x=60, y=220, width=280, height=50)

    # ---------- Sorting Control ----------
    def start_sorting(self):
        """Called when user clicks START SORTING."""
        # Reset counters in UI
        self.main_seeds.config(text="0")
        self.main_healthy.config(text="0")
        self.main_unhealthy.config(text="0")
        
        # Switch to sorting page
        self.show_sorting_page()

        # Create the sorter with callbacks
        self.sorter = Sorter(
            camera=self.camera,
            servo=self.servo,
            classifier=self.classifier,
            hopper_empty_callback=self.on_sorting_done,
            update_callback=self.update_sorting_ui
        )
        self.sorter.start()

    def update_sorting_ui(self, processed, healthy, unhealthy):
        """Called from the sorter thread – schedules UI update on main thread."""
        self.root.after(0, self._update_labels, processed, healthy, unhealthy)

    def _update_labels(self, processed, healthy, unhealthy):
        """Actually update the sorting page labels."""
        try:
            self.sort_seeds.config(text=str(processed))
            self.sort_healthy.config(text=str(healthy))
            self.sort_unhealthy.config(text=str(unhealthy))
        except Exception:
            pass

    def on_sorting_done(self, total, healthy, unhealthy):
        """Called when sorting finishes – switch to complete page."""
        self.root.after(0, self.show_complete_page, total, healthy, unhealthy)

    def reset_and_return(self):
        """Return to main page and release resources if needed."""
        if self.sorter:
            self.sorter.stop()
            self.sorter = None
        self.show_main_page()

    # ---------- Cleanup ----------
    def on_closing(self):
        """Release hardware when window is closed."""
        if self.sorter:
            self.sorter.stop()
        self.camera.release()
        self.servo.detach()
        self.root.destroy()

# -------------------- Run the App --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CornSorterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
