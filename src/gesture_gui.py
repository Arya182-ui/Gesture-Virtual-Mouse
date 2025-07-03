import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import StringVar, DoubleVar, ttk
from threading import Thread
from Gesture_Controller import GestureController 


class GestureControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖐 Gesture Controller")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        self.controller_thread = None

        settings_frame = tb.Frame(root, padding=10)
        settings_frame.pack(side=LEFT, fill=Y)

        tb.Label(settings_frame, text="Gesture Controller", font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        self.hand_var = StringVar(value="Right")
        tb.Label(settings_frame, text="Dominant Hand", font=("Segoe UI", 12)).pack()
        tb.Radiobutton(settings_frame, text="Right", variable=self.hand_var, value="Right", bootstyle="success").pack()
        tb.Radiobutton(settings_frame, text="Left", variable=self.hand_var, value="Left", bootstyle="info").pack()

        self.sensitivity = DoubleVar(value=0.3)
        tb.Label(settings_frame, text="Pinch Sensitivity", font=("Segoe UI", 12)).pack(pady=(15, 5))
        tb.Scale(settings_frame, from_=0.1, to=1.0, length=200, variable=self.sensitivity, bootstyle="primary").pack()

        tb.Button(settings_frame, text="Start Controller", bootstyle="success", width=25,
                  command=self.start_controller).pack(pady=20)

        tb.Button(settings_frame, text="Exit", bootstyle="danger", command=self.root.quit, width=25).pack()


        self.status_label = tb.Label(settings_frame, text="Detected: None", font=("Segoe UI", 10), bootstyle="secondary")
        self.status_label.pack(pady=10)

        help_frame = tb.LabelFrame(root, text="Gesture Reference Guide", padding=10)
        help_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        columns = ("gesture", "action")
        self.table = ttk.Treeview(help_frame, columns=columns, show="headings", height=15)
        self.table.heading("gesture", text="Gesture")
        self.table.heading("action", text="Action")
        self.table.column("gesture", width=150)
        self.table.column("action", width=400)

        self.table.pack(fill=BOTH, expand=True)
        self.populate_gesture_table()

    def populate_gesture_table(self):
        gesture_actions = {
            "FIST": "Click & Drag",
            "V_GEST": "Move Mouse Cursor",
            "MID": "Left Click",
            "INDEX": "Right Click",
            "TWO_FINGER_CLOSED": "Double Click",
            "PINCH_MINOR": "Scroll (Vertical/Horizontal)",
            "PINCH_MAJOR": "Adjust Volume / Brightness",
        }
        for g_name, action in gesture_actions.items():
            self.table.insert("", "end", values=(g_name, action))

    def start_controller(self):
        GestureController.dom_hand = (self.hand_var.get() == "Right")
        GestureController.pinch_threshold = self.sensitivity.get()

        self.gc = GestureController()

        from Gesture_Controller import Controller
        original_handle = Controller.handle_controls

        def handle_with_label_update(gesture, hand_result):
            try:
                gesture_name = gesture.name
            except:
                gesture_name = str(gesture)
            self.status_label.config(text=f"Detected: {gesture_name}")
            original_handle(gesture, hand_result)

        Controller.handle_controls = handle_with_label_update

        self.controller_thread = Thread(target=self.gc.start, daemon=True)
        self.controller_thread.start()

if __name__ == "__main__":
    root = tb.Window(themename="cyborg")  
    app = GestureControlApp(root)
    root.mainloop()
