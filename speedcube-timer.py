import tkinter as tk
from tkinter import font, messagebox
import time
import random
import requests
import json

# Flask server URL - change if running on different host/port
SERVER_URL = "lucazeduck.github.io/server.py"

class LoginWindow:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login
        self.root.title("Login")
        self.root.geometry("300x220")
        self.root.configure(bg="#f0f0f0")
        
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Speedcubing Timer", font=('Helvetica', 16),
                 bg="#f0f0f0", fg="#000000").pack(pady=10)
        
        tk.Label(main_frame, text="Username:", font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").pack()
        self.username_entry = tk.Entry(main_frame, font=('Helvetica', 12))
        self.username_entry.pack(pady=5)
        
        tk.Label(main_frame, text="Password:", font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").pack()
        self.password_entry = tk.Entry(main_frame, font=('Helvetica', 12), show="*")
        self.password_entry.pack(pady=5)
        
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Login", command=self.login,
                  bg="#d0d0d0", fg="#000000").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sign Up", command=self.signup,
                  bg="#d0d0d0", fg="#000000").pack(side=tk.LEFT, padx=5)
    
    def try_request(self, func):
        try:
            return func()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", f"Cannot connect to server at {SERVER_URL}. Please start the Flask server first.")
            return None
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        response = self.try_request(lambda: requests.post(
            f"{SERVER_URL}/api/login",
            json={'username': username, 'password': password}
        ))
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.root.destroy()
                self.on_login(
                    data['user_id'],
                    data['username'],
                    data.get('solves', []),
                    data.get('leaderboard', [])
                )
            else:
                messagebox.showerror("Error", data.get('error', 'Login failed'))
        elif response:
            messagebox.showerror("Error", "Invalid username or password")
    
    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        response = self.try_request(lambda: requests.post(
            f"{SERVER_URL}/api/signup",
            json={'username': username, 'password': password}
        ))
        
        if response and response.status_code == 200:
            data = response.json()
            if data.get('success'):
                messagebox.showinfo("Success", "Account created! Please login.")
            else:
                messagebox.showerror("Error", data.get('error', 'Signup failed'))
        else:
            messagebox.showerror("Error", "Signup failed")

class SpeedcubeTimer:
    def __init__(self, root, user_id, username, solves, leaderboard):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.root.title(f"Speedcubing Timer - {username}")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")
        
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.solves = solves or []
        self.leaderboard = leaderboard or []
        
        # Main container
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scramble at the top
        self.scramble_var = tk.StringVar(value=self.generate_scramble())
        scramble_font = font.Font(family='Courier', size=14)
        scramble_label = tk.Label(
            self.main_frame, textvariable=self.scramble_var, font=scramble_font,
            bg="#f0f0f0", fg="#000000"
        )
        scramble_label.pack(pady=10)
        
        # Split into left (timer) and right (leaderboard)
        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Timer
        self.timer_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.timer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Timer display
        self.time_var = tk.StringVar(value="00:00.000")
        timer_font = font.Font(family='Helvetica', size=48)
        timer_label = tk.Label(
            self.timer_frame, textvariable=self.time_var, font=timer_font,
            bg="#f0f0f0", fg="#000000"
        )
        timer_label.pack(pady=10)
        
        # Title
        tk.Label(self.timer_frame, text=f"Welcome, {username}", font=('Helvetica', 16),
                 bg="#f0f0f0", fg="#000000").pack(pady=5)
        
        # Stats
        stats_frame = tk.Frame(self.timer_frame, bg="#f0f0f0")
        stats_frame.pack(pady=5)
        
        self.solve_count_var = tk.StringVar(value=str(len(self.solves)))
        self.average_var = tk.StringVar(value=self.format_time(sum(self.solves) / len(self.solves)) if self.solves else "--:--.---")
        self.best_var = tk.StringVar(value=self.format_time(min(self.solves)) if self.solves else "--:--.---")
        
        tk.Label(stats_frame, text="Solves: ", font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").grid(row=0, column=0)
        tk.Label(stats_frame, textvariable=self.solve_count_var, font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").grid(row=0, column=1)
        
        tk.Label(stats_frame, text="Average: ", font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").grid(row=0, column=2, padx=10)
        tk.Label(stats_frame, textvariable=self.average_var, font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").grid(row=0, column=3)
        
        tk.Label(stats_frame, text="Best: ", font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").grid(row=0, column=4)
        tk.Label(stats_frame, textvariable=self.best_var, font=('Helvetica', 12),
                 bg="#f0f0f0", fg="#000000").grid(row=0, column=5)
        
        # Solves list
        self.solves_frame = tk.Frame(self.timer_frame, bg="#f0f0f0")
        self.solves_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.timer_frame, bg="#f0f0f0")
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Clear All", command=self.clear_all,
                  bg="#d0d0d0", fg="#000000").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Switch User", command=self.switch_user,
                  bg="#d0d0d0", fg="#000000").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh LB", command=self.refresh_leaderboard,
                  bg="#d0d0d0", fg="#000000").pack(side=tk.LEFT, padx=5)
        
        # Right side - Leaderboard
        self.leaderboard_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.leaderboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        lb_title = tk.Label(self.leaderboard_frame, text="Leaderboard (Global)", font=('Helvetica', 16),
                           bg="#f0f0f0", fg="#000000")
        lb_title.pack(pady=5)
        
        self.lb_entries_frame = tk.Frame(self.leaderboard_frame, bg="#f0f0f0")
        self.lb_entries_frame.pack(fill=tk.BOTH, expand=True)
        
        self.update_solves_display()
        self.update_leaderboard_display()
        
        # Instructions
        tk.Label(self.main_frame, text="Press SPACE to start/stop, S for new scramble", 
                 font=('Helvetica', 10), bg="#f0f0f0", fg="#666666").pack(pady=5)
        
        # Key bindings
        root.bind('<space>', self.on_space_press)
        root.bind('<s>', self.on_s_press)
        
        self.update_display()
    
    def try_request(self, func):
        try:
            return func()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", f"Cannot connect to server at {SERVER_URL}")
            return None
    
    def switch_user(self):
        self.root.destroy()
        root = tk.Tk()
        LoginWindow(root, self.start_main_app)
        root.mainloop()
    
    def start_main_app(self, user_id, username, solves, leaderboard):
        root = tk.Tk()
        SpeedcubeTimer(root, user_id, username, solves, leaderboard)
        root.mainloop()
    
    def generate_scramble(self):
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        moves = []
        last_face = None
        for _ in range(20):
            face = random.choice(faces)
            while face == last_face:
                face = random.choice(faces)
            modifier = random.choice(["", "'", "2"])
            moves.append(face + modifier)
            last_face = face
        return " ".join(moves)
    
    def format_time(self, ms):
        total_seconds = int(ms // 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = int(ms % 1000)
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def update_display(self):
        self.time_var.set(self.format_time(self.elapsed_time))
    
    def toggle_timer(self):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        if self.is_running:
            return
        self.start_time = time.time() - (self.elapsed_time / 1000)
        self.is_running = True
        self.update_clock()
    
    def stop_timer(self):
        if not self.is_running:
            return
        self.is_running = False
        if self.elapsed_time > 100:
            self.record_solve(self.elapsed_time)
    
    def update_clock(self):
        if self.is_running:
            self.elapsed_time = (time.time() - self.start_time) * 1000
            self.update_display()
            self.root.after(10, self.update_clock)
    
    def reset_timer(self):
        self.stop_timer()
        self.elapsed_time = 0
        self.update_display()
    
    def record_solve(self, time_ms):
        self.solves.insert(0, time_ms)
        self.update_solves_display()
        self.update_stats()
        self.reset_timer()
        
        # Submit to server
        response = self.try_request(lambda: requests.post(
            f"{SERVER_URL}/api/submit",
            json={'user_id': self.user_id, 'time_ms': time_ms}
        ))
        
        if response and response.status_code == 200:
            if response.json().get('success'):
                # Refresh leaderboard
                self.refresh_leaderboard()
        
        # New scramble
        self.scramble_var.set(self.generate_scramble())
    
    def clear_all(self):
        self.solves = []
        for widget in self.solves_frame.winfo_children():
            widget.destroy()
        self.update_stats()
        
        # Clear on server
        response = self.try_request(lambda: requests.post(
            f"{SERVER_URL}/api/clear",
            json={'user_id': self.user_id}
        ))
    
    def refresh_leaderboard(self):
        response = self.try_request(lambda: requests.get(f"{SERVER_URL}/api/leaderboard"))
        if response and response.status_code == 200:
            self.leaderboard = response.json()
            self.update_leaderboard_display()
    
    def update_solves_display(self):
        for widget in self.solves_frame.winfo_children():
            widget.destroy()
        
        for solve_time in self.solves:
            label = tk.Label(self.solves_frame, text=self.format_time(solve_time),
                           font=('Helvetica', 12), bg="#f0f0f0", fg="#000000")
            label.pack(pady=2, fill=tk.X)
    
    def update_stats(self):
        self.solve_count_var.set(str(len(self.solves)))
        
        if not self.solves:
            self.average_var.set("--:--.---")
            self.best_var.set("--:--.---")
            return
        
        best_time = min(self.solves)
        avg_time = sum(self.solves) / len(self.solves)
        
        self.best_var.set(self.format_time(best_time))
        self.average_var.set(self.format_time(avg_time))
    
    def update_leaderboard_display(self):
        for widget in self.lb_entries_frame.winfo_children():
            widget.destroy()
        
        for i, entry in enumerate(self.leaderboard[:10]):
            frame = tk.Frame(self.lb_entries_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=2)
            
            rank = tk.Label(frame, text=str(i+1), width=3, font=('Helvetica', 12),
                          bg="#f0f0f0", fg="#000000")
            rank.pack(side=tk.LEFT)
            
            name = tk.Label(frame, text=entry.get('name', 'Unknown'), font=('Helvetica', 12),
                          bg="#f0f0f0", fg="#000000")
            name.pack(side=tk.LEFT, padx=10)
            
            time_lb = tk.Label(frame, text=self.format_time(entry.get('time', 0)), 
                             font=('Helvetica', 12), bg="#f0f0f0", fg="#000000")
            time_lb.pack(side=tk.RIGHT)
    
    def on_space_press(self, event):
        self.toggle_timer()
        return 'break'
    
    def on_s_press(self, event):
        self.scramble_var.set(self.generate_scramble())

def start_app():
    root = tk.Tk()
    LoginWindow(root, lambda user_id, username, solves, leaderboard: 
        SpeedcubeTimer(tk.Tk(), user_id, username, solves, leaderboard).root.mainloop())
    root.mainloop()

if __name__ == "__main__":
    start_app()
