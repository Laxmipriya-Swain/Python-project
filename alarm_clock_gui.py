import json
import os
import random
import threading
import time
import winsound
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class AlarmClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Alarm Clock")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#121212')
        self.data_file = 'alarm_clock_data.json'
        self.alarms = []
        self.active_alarm = None
        self.sound_thread = None
        self.load_alarms()
        self.create_ui()
        self.update_clock()
        self.check_alarm_loop()

    def load_alarms(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    self.alarms = json.load(f)
                except json.JSONDecodeError:
                    self.alarms = []
        else:
            self.alarms = []

    def save_alarms(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.alarms, f, indent=2)

    def create_ui(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TFrame', background='#121212')
        style.configure('TLabel', background='#121212', foreground='#ffffff')
        style.configure('TButton', font=('Segoe UI', 10), padding=8)
        style.configure('Treeview', background='#1e1e1e', foreground='#ffffff', fieldbackground='#1e1e1e', rowheight=28)
        style.configure('Treeview.Heading', background='#333333', foreground='#ffffff')

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Top edge neon light (purple scanning effect)
        self.glow_canvas = tk.Canvas(main_frame, height=2, bg='#121212', highlightthickness=0)
        self.glow_canvas.pack(fill=tk.X, pady=(0, 15))
        
        self.glow_pieces = []
        # Create a gradient effect for the purple neon light
        colors = ['#121212', '#1a0526', '#2b0642', '#410866', '#5b0a91', '#7a0cc2', '#9f14fa', '#c973ff']
        for i, color in enumerate(colors):
            piece = self.glow_canvas.create_rectangle(i*40 - 400, 0, (i+1)*40 - 400, 2, fill=color, outline='')
            self.glow_pieces.append(piece)

        header = ttk.Label(main_frame, text='Desktop Alarm Clock', font=('Segoe UI', 24, 'bold'))
        header.pack(pady=(0, 15))

        clock_frame = ttk.Frame(main_frame)
        clock_frame.pack(fill=tk.X, pady=(0, 12))

        self.time_label = ttk.Label(clock_frame, text='', font=('Segoe UI', 36, 'bold'))
        self.time_label.pack(side=tk.LEFT, padx=(0, 20))

        self.date_label = ttk.Label(clock_frame, text='', font=('Segoe UI', 14))
        self.date_label.pack(anchor=tk.NW)

        alarm_frame = ttk.LabelFrame(main_frame, text='Create an Alarm', padding=15)
        alarm_frame.pack(fill=tk.X, pady=(0, 15))

        row1 = ttk.Frame(alarm_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Label(row1, text='Alarm Time (HH:MM):', width=20).pack(side=tk.LEFT, padx=(0, 10))
        self.time_entry = ttk.Entry(row1, width=12, font=('Segoe UI', 12))
        self.time_entry.pack(side=tk.LEFT)
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))

        ttk.Label(row1, text='Label:', width=10).pack(side=tk.LEFT, padx=(25, 10))
        self.label_entry = ttk.Entry(row1, width=18, font=('Segoe UI', 12))
        self.label_entry.pack(side=tk.LEFT)
        self.label_entry.insert(0, 'Wake Up')

        row2 = ttk.Frame(alarm_frame)
        row2.pack(fill=tk.X, pady=5)

        ttk.Label(row2, text='Tone:', width=20).pack(side=tk.LEFT, padx=(0, 10))
        self.tone_var = tk.StringVar(value='High Beep')
        tone_dropdown = ttk.Combobox(row2, textvariable=self.tone_var, state='readonly', width=16)
        tone_dropdown['values'] = ('High Beep', 'Low Beep', 'Medium Beep', 'Alert')
        tone_dropdown.pack(side=tk.LEFT)

        ttk.Label(row2, text='Repeat:', width=10).pack(side=tk.LEFT, padx=(25, 10))
        self.repeat_var = tk.StringVar(value='Once')
        repeat_dropdown = ttk.Combobox(row2, textvariable=self.repeat_var, state='readonly', width=16)
        repeat_dropdown['values'] = ('Once', 'Daily')
        repeat_dropdown.pack(side=tk.LEFT)

        btn_frame = ttk.Frame(alarm_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        add_btn = tk.Button(btn_frame, text='Add Alarm', bg='#0078d4', fg='white', command=self.add_alarm, cursor='hand2')
        add_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = tk.Button(btn_frame, text='Clear Fields', bg='#4b4b4b', fg='white', command=self.clear_fields, cursor='hand2')
        clear_btn.pack(side=tk.LEFT)

        list_frame = ttk.LabelFrame(main_frame, text='Alarms', padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('time', 'label', 'tone', 'repeat', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('time', text='Time')
        self.tree.heading('label', text='Label')
        self.tree.heading('tone', text='Tone')
        self.tree.heading('repeat', text='Repeat')
        self.tree.heading('status', text='Status')
        self.tree.column('time', width=100, anchor=tk.CENTER)
        self.tree.column('label', width=240, anchor=tk.W)
        self.tree.column('tone', width=120, anchor=tk.CENTER)
        self.tree.column('repeat', width=100, anchor=tk.CENTER)
        self.tree.column('status', width=120, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        toggle_btn = tk.Button(action_frame, text='Toggle Enable/Disable', bg='#2d7d2d', fg='white', command=self.toggle_alarm, cursor='hand2')
        toggle_btn.pack(side=tk.LEFT, padx=(0, 10))

        delete_btn = tk.Button(action_frame, text='Delete Alarm', bg='#d32f2f', fg='white', command=self.delete_alarm, cursor='hand2')
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))

        dismiss_btn = tk.Button(action_frame, text='Dismiss Active Alarm', bg='#f0a500', fg='white', command=self.dismiss_alarm, cursor='hand2')
        dismiss_btn.pack(side=tk.LEFT)

        self.notification_label = ttk.Label(main_frame, text='', font=('Segoe UI', 12, 'bold'))
        self.notification_label.pack(pady=(10, 0))

        # Ball animation setup
        self.ball_visible = False
        self.ball_radius = 10
        self.ball_grow = True
        self.ball_canvas = tk.Canvas(self.root, width=100, height=100, bg='#121212', highlightthickness=0)
        
        # Create circles for the glowing ball effect
        self.ball_glow3 = self.ball_canvas.create_oval(0, 0, 0, 0, fill='#410866', outline='')
        self.ball_glow2 = self.ball_canvas.create_oval(0, 0, 0, 0, fill='#7a0cc2', outline='')
        self.ball_glow1 = self.ball_canvas.create_oval(0, 0, 0, 0, fill='#c973ff', outline='')
        self.ball_core = self.ball_canvas.create_oval(0, 0, 0, 0, fill='#ffffff', outline='')

        self.refresh_alarm_list()
        self.animate_glow()
        self.animate_ball()

    def format_alarm(self, alarm):
        return (
            alarm['time'],
            alarm['label'],
            alarm['tone'],
            alarm['repeat'],
            'Enabled' if alarm['enabled'] else 'Disabled'
        )

    def refresh_alarm_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for alarm in self.alarms:
            self.tree.insert('', tk.END, iid=alarm['id'], values=self.format_alarm(alarm))

    def clear_fields(self):
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))
        self.label_entry.delete(0, tk.END)
        self.label_entry.insert(0, 'Wake Up')
        self.tone_var.set('High Beep')
        self.repeat_var.set('Once')

    def add_alarm(self):
        alarm_time = self.time_entry.get().strip()
        label = self.label_entry.get().strip() or 'Alarm'
        tone = self.tone_var.get()
        repeat = self.repeat_var.get()

        if not self.validate_time(alarm_time):
            messagebox.showerror('Invalid Time', 'Please enter a valid time in HH:MM format.')
            return

        alarm_id = max((alarm['id'] for alarm in self.alarms), default=0) + 1
        new_alarm = {
            'id': alarm_id,
            'time': alarm_time,
            'label': label,
            'tone': tone,
            'enabled': True,
            'repeat': repeat,
            'created': datetime.now().isoformat()
        }

        self.alarms.append(new_alarm)
        self.save_alarms()
        self.refresh_alarm_list()
        self.notification_label.config(text=f'Alarm added for {alarm_time} ✔', foreground='#00ff7f')

    def validate_time(self, alarm_time):
        try:
            datetime.strptime(alarm_time, '%H:%M')
            return True
        except ValueError:
            return False

    def delete_alarm(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Select Alarm', 'Please select an alarm to delete.')
            return
        alarm_id = int(selected[0])
        self.alarms = [alarm for alarm in self.alarms if alarm['id'] != alarm_id]
        self.save_alarms()
        self.refresh_alarm_list()
        self.notification_label.config(text='Alarm deleted ✔', foreground='#ff6b6b')

    def toggle_alarm(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Select Alarm', 'Please select an alarm to toggle.')
            return
        alarm_id = int(selected[0])
        for alarm in self.alarms:
            if alarm['id'] == alarm_id:
                alarm['enabled'] = not alarm['enabled']
                status = 'enabled' if alarm['enabled'] else 'disabled'
                self.notification_label.config(text=f'Alarm {status} ✔', foreground='#ffd166')
                break
        self.save_alarms()
        self.refresh_alarm_list()

    def dismiss_alarm(self):
        if not self.active_alarm:
            messagebox.showinfo('No Active Alarm', 'There is no active alarm to dismiss.')
            return
        self.active_alarm = None
        self.notification_label.config(text='Alarm dismissed ✔', foreground='#ffd166')
        self.stop_sound()

    def play_sound(self, tone):
        frequency = 1000
        if tone == 'Low Beep':
            frequency = 600
        elif tone == 'Medium Beep':
            frequency = 850
        elif tone == 'Alert':
            frequency = 1400

        duration = 500
        for _ in range(10):
            if not self.active_alarm:
                break
            winsound.Beep(frequency, duration)
            time.sleep(0.2)

    def stop_sound(self):
        self.active_alarm = None

    def show_alarm(self, alarm):
        self.active_alarm = alarm['id']
        self.notification_label.config(text=f"ALARM: {alarm['label']} at {alarm['time']}", foreground='#ff4444')
        if self.sound_thread and self.sound_thread.is_alive():
            self.active_alarm = alarm['id']
            return
        self.sound_thread = threading.Thread(target=self.play_sound, args=(alarm['tone'],), daemon=True)
        self.sound_thread.start()

    def check_alarm_loop(self):
        current_time = datetime.now().strftime('%H:%M')
        for alarm in self.alarms:
            if alarm['enabled'] and alarm['time'] == current_time:
                if self.active_alarm != alarm['id']:
                    self.show_alarm(alarm)
                    if alarm['repeat'] == 'Once':
                        alarm['enabled'] = False
                        self.save_alarms()
                        self.refresh_alarm_list()
        self.root.after(1000, self.check_alarm_loop)

    def animate_glow(self):
        width = self.glow_canvas.winfo_width()
        if width <= 1:
            width = 900
        
        coords = self.glow_canvas.coords(self.glow_pieces[0])
        if coords and coords[0] > width:
            for i, piece in enumerate(self.glow_pieces):
                self.glow_canvas.coords(piece, i*40 - 400, 0, (i+1)*40 - 400, 2)
        else:
            for piece in self.glow_pieces:
                self.glow_canvas.move(piece, 3, 0)
                
        self.root.after(20, self.animate_glow)

    def animate_ball(self):
        if self.active_alarm is not None:
            if not self.ball_visible:
                self.ball_canvas.place(x=20, y=20)
                self.ball_visible = True
                
            if self.ball_grow:
                self.ball_radius += 1.5
                if self.ball_radius >= 40:
                    self.ball_grow = False
            else:
                self.ball_radius -= 1.5
                if self.ball_radius <= 10:
                    self.ball_grow = True
                    
            cx, cy = 50, 50
            jitter = random.uniform(-2, 2)
            
            # Outer glow
            r3 = max(0, self.ball_radius + jitter)
            self.ball_canvas.coords(self.ball_glow3, cx - r3, cy - r3, cx + r3, cy + r3)
            # Middle glow
            r2 = max(0, self.ball_radius * 0.75 + jitter)
            self.ball_canvas.coords(self.ball_glow2, cx - r2, cy - r2, cx + r2, cy + r2)
            # Inner glow
            r1 = max(0, self.ball_radius * 0.5 + jitter)
            self.ball_canvas.coords(self.ball_glow1, cx - r1, cy - r1, cx + r1, cy + r1)
            # Core
            rc = max(0, self.ball_radius * 0.25)
            self.ball_canvas.coords(self.ball_core, cx - rc, cy - rc, cx + rc, cy + rc)
        else:
            if self.ball_visible:
                self.ball_canvas.place_forget()
                self.ball_visible = False
                
        self.root.after(30, self.animate_ball)

    def update_clock(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime('%H:%M:%S'))
        self.date_label.config(text=now.strftime('%A, %B %d, %Y'))
        self.root.after(500, self.update_clock)


if __name__ == '__main__':
    root = tk.Tk()
    app = AlarmClockGUI(root)
    root.mainloop()
