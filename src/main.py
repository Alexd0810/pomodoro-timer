import time
import tkinter as tk
from threading import Thread
from plyer import notification

# Pomodoro Timer Settings
WORK_MIN = 25  # Work time in minutes
SHORT_BREAK_MIN = 5  # Short break in minutes
LONG_BREAK_MIN = 15  # Long break after 4 cycles

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")
        
        self.timer_label = tk.Label(root, text="Pomodoro Timer", font=("Arial", 14))
        self.timer_label.pack(pady=10)
        
        self.time_display = tk.Label(root, text="00:00", font=("Arial", 24))
        self.time_display.pack()
        
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack()
        
        self.running = False
        self.cycles = 0

    def start_timer(self):
        if not self.running:
            self.running = True
            Thread(target=self.run_pomodoro, daemon=True).start()
    
    def run_pomodoro(self):
        while self.running:
            for duration, phase in [(WORK_MIN, "Work"), (SHORT_BREAK_MIN, "Break")]:
                if self.cycles % 4 == 0 and self.cycles > 0:
                    duration, phase = LONG_BREAK_MIN, "Long Break"
                
                self.update_timer(duration * 60, phase)
                if not self.running:
                    break
                self.cycles += 1
    
    def update_timer(self, seconds, phase):
        self.timer_label.config(text=f"{phase} Time")
        while seconds > 0 and self.running:
            mins, secs = divmod(seconds, 60)
            self.time_display.config(text=f"{mins:02}:{secs:02}")
            self.root.update()
            time.sleep(1)
            seconds -= 1
        
        if self.running:
            self.show_notification(phase)
    
    def show_notification(self, phase):
        notification.notify(
            title="Pomodoro Timer",
            message=f"{phase} session is over!",
            timeout=5
        )
    
    def reset_timer(self):
        self.running = False
        self.cycles = 0
        self.timer_label.config(text="Pomodoro Timer")
        self.time_display.config(text="00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
