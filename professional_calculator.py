import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Calculator")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0a0a")
        
        # Set style
        self.setup_styles()
        
        # Variables
        self.display_var = tk.StringVar(value="0")
        self.history = []
        self.current_operation = None
        self.first_number = None
        self.memory = 0
        
        # Create UI
        self.create_widgets()
        
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background="#0a0a0a")
        style.configure('TLabel', background="#0a0a0a", foreground="#e040fb")
        
        style.configure('TLabelframe', background="#0a0a0a", bordercolor="#8e24aa")
        style.configure('TLabelframe.Label', background="#0a0a0a", foreground="#e040fb", font=("Arial", 11, "bold"))
        
        # Treeview styles
        style.configure('Treeview', 
                        background="#050505",
                        foreground="#ffeb3b",
                        rowheight=25,
                        fieldbackground="#050505",
                        bordercolor="#8e24aa")
        style.map('Treeview', background=[('selected', '#8e24aa')], foreground=[('selected', '#000000')])
        
        style.configure('Treeview.Heading', 
                        background="#111111", 
                        foreground="#e040fb", 
                        font=("Arial", 10, "bold"))
        style.map('Treeview.Heading', background=[('active', '#222222')])
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="✨ Professional Calculator ✨", 
                               font=("Arial", 20, "bold"), foreground="#e040fb")
        title_label.pack(pady=10)
        
        # Display frame
        display_frame = ttk.LabelFrame(main_frame, text="Display", padding=10)
        display_frame.pack(fill=tk.X, pady=10)
        
        # Display - wrap in canvas for lightning border
        self.disp_border = tk.Canvas(display_frame, bg="#0a0a0a", bd=0, highlightthickness=0)
        self.disp_border.pack(fill=tk.X, padx=5, pady=5)
        
        # Display
        display_entry = tk.Entry(self.disp_border, textvariable=self.display_var, 
                                font=("Arial", 28, "bold"), justify="right", 
                                bg="#000000", fg="#ffeb3b", bd=0, 
                                readonlybackground="#000000")
        display_entry.pack(fill=tk.X, padx=3, pady=3)
        display_entry.config(state='readonly')
        
        self.light_pos = 0
        self.animate_lightning()
        
        # Footer
        footer_label = tk.Label(main_frame, text="crafted by laxmi🌻💖", font=("Arial", 12, "italic"), bg="#0a0a0a", fg="#e040fb")
        footer_label.pack(side=tk.BOTTOM, pady=10)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Split into left (buttons) and right (history)
        left_frame = ttk.Frame(buttons_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        right_frame = ttk.Frame(buttons_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Calculator buttons
        self.create_calculator_buttons(left_frame)
        
        # History display
        self.create_history_display(right_frame)
        
    def animate_lightning(self):
        """Animate yellowish lightning moving around the display box"""
        if not hasattr(self, 'disp_border'):
            return
            
        w = self.disp_border.winfo_width()
        h = self.disp_border.winfo_height()
        
        if w > 10 and h > 10:
            perimeter = 2*w + 2*h
            
            # Update position (speed = 2 pixels per frame for slower movement)
            self.light_pos = (self.light_pos + 2) % perimeter
            
            # Clear previous drawings
            self.disp_border.delete("lightning")
            
            # Draw the static purple border
            self.disp_border.create_rectangle(1, 1, w-1, h-1, outline="#8e24aa", width=2, tags="lightning")
            
            # Helper to get x, y from perimeter position
            def get_coords(pos):
                pos = pos % perimeter
                if pos < w:
                    return pos, 0
                elif pos < w + h:
                    return w, pos - w
                elif pos < 2*w + h:
                    return w - (pos - (w + h)), h
                else:
                    return 0, h - (pos - (2*w + h))
                    
            # Create a moving yellowish light with a tail
            for i in range(8):
                # Tail position lags behind the leading point
                pos = (self.light_pos - i*8) % perimeter
                cx, cy = get_coords(pos)
                
                # Size decreases along the tail
                size = 18 - i*2
                
                # Colors fade from white-yellow to deep yellow
                colors = ["#ffffff", "#ffffcc", "#ffff66", "#ffff00", "#cccc00", "#999900", "#666600", "#333300"]
                color = colors[i]
                
                self.disp_border.create_oval(cx-size, cy-size, cx+size, cy+size, 
                                            fill=color, outline="", tags="lightning")
        
        # Schedule next frame
        self.root.after(30, self.animate_lightning)

    def create_calculator_buttons(self, parent):
        """Create calculator buttons"""
        button_layout = [
            ['MC', 'MR', 'M+', 'M-'],
            ['C', 'CE', '←', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '√'],
            ['π', 'e', '^', '%'],
            ['sin', 'cos', 'tan', 'log'],
            ['1/x', 'x²', 'x³', '|x|'],
        ]
        
        buttons_grid = ttk.Frame(parent)
        buttons_grid.pack(fill=tk.BOTH, expand=True)
        
        for row_idx, row in enumerate(button_layout):
            for col_idx, btn_text in enumerate(row):
                # Wrapper frame for purple lighting (neon border) effect
                border_frame = tk.Frame(buttons_grid, bg="#8e24aa", bd=0)
                border_frame.grid(row=row_idx, column=col_idx, padx=4, pady=4, sticky="nsew")
                
                btn = tk.Button(border_frame, text=btn_text, font=("Arial", 13, "bold"),
                              command=lambda x=btn_text: self.on_button_click(x),
                              bg="#000000", fg="#ffeb3b", bd=0, relief=tk.FLAT,
                              activebackground="#e040fb", activeforeground="#000000",
                              cursor="hand2")
                btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Configure grid weights
        for i in range(len(button_layout)):
            buttons_grid.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_grid.grid_columnconfigure(i, weight=1)
    
    def create_history_display(self, parent):
        """Create history display table"""
        history_label = ttk.Label(parent, text="⚡ Calculation History", font=("Arial", 14, "bold"), foreground="#e040fb")
        history_label.pack(pady=5)
        
        # Treeview for history
        columns = ('Operation', 'Result', 'Time')
        self.history_tree = ttk.Treeview(parent, columns=columns, height=15, show='headings')
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Define column headings and widths
        self.history_tree.column('Operation', width=120, anchor=tk.W)
        self.history_tree.column('Result', width=100, anchor=tk.E)
        self.history_tree.column('Time', width=80, anchor=tk.CENTER)
        
        self.history_tree.heading('Operation', text='Operation')
        self.history_tree.heading('Result', text='Result')
        self.history_tree.heading('Time', text='Time')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.configure(yscroll=scrollbar.set)
        
        # Alternating row colors
        self.history_tree.tag_configure('oddrow', background='#0a0a0a', foreground='#ffeb3b')
        self.history_tree.tag_configure('evenrow', background='#1a1a1a', foreground='#ffeb3b')
        
        # Clear history button with neon effect
        clear_frame = tk.Frame(parent, bg="#8e24aa", bd=0)
        clear_frame.pack(fill=tk.X, padx=5, pady=10)
        
        clear_btn = tk.Button(clear_frame, text="Clear History", font=("Arial", 11, "bold"),
                            bg="#000000", fg="#e040fb", command=self.clear_history,
                            activebackground="#e040fb", activeforeground="#000000",
                            cursor="hand2", relief=tk.FLAT, bd=0)
        clear_btn.pack(fill=tk.X, padx=2, pady=2)
    
    def on_button_click(self, btn_text):
        """Handle button clicks"""
        current = self.display_var.get()
        
        # Number buttons
        if btn_text in '0123456789':
            if current == "0":
                self.display_var.set(btn_text)
            else:
                self.display_var.set(current + btn_text)
        
        # Decimal point
        elif btn_text == '.':
            if '.' not in current:
                self.display_var.set(current + '.')
        
        # Basic operations
        elif btn_text in ['+', '-', '*', '/']:
            if current and current != "-":
                self.first_number = float(current)
                self.current_operation = btn_text
                self.display_var.set("0")
        
        # Equals
        elif btn_text == '=':
            self.calculate_result()
        
        # Clear all
        elif btn_text == 'C':
            self.display_var.set("0")
            self.first_number = None
            self.current_operation = None
        
        # Clear entry
        elif btn_text == 'CE':
            self.display_var.set("0")
        
        # Backspace
        elif btn_text == '←':
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
        
        # Square root
        elif btn_text == '√':
            try:
                num = float(current)
                result = math.sqrt(num)
                self.add_to_history(f"√{num}", result)
                self.display_var.set(str(result))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Power
        elif btn_text == '^':
            if current and current != "-":
                self.first_number = float(current)
                self.current_operation = '^'
                self.display_var.set("0")
        
        # Percentage
        elif btn_text == '%':
            try:
                num = float(current)
                result = num / 100
                self.add_to_history(f"{num}%", result)
                self.display_var.set(str(result))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Pi
        elif btn_text == 'π':
            self.display_var.set(str(math.pi))
        
        # Euler's number
        elif btn_text == 'e':
            self.display_var.set(str(math.e))
        
        # Trigonometric functions
        elif btn_text == 'sin':
            try:
                num = float(current)
                result = math.sin(math.radians(num))
                self.add_to_history(f"sin({num}°)", result)
                self.display_var.set(str(round(result, 10)))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        elif btn_text == 'cos':
            try:
                num = float(current)
                result = math.cos(math.radians(num))
                self.add_to_history(f"cos({num}°)", result)
                self.display_var.set(str(round(result, 10)))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        elif btn_text == 'tan':
            try:
                num = float(current)
                result = math.tan(math.radians(num))
                self.add_to_history(f"tan({num}°)", result)
                self.display_var.set(str(round(result, 10)))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Logarithm
        elif btn_text == 'log':
            try:
                num = float(current)
                if num > 0:
                    result = math.log10(num)
                    self.add_to_history(f"log({num})", result)
                    self.display_var.set(str(result))
                else:
                    messagebox.showerror("Error", "Log of non-positive number")
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Reciprocal
        elif btn_text == '1/x':
            try:
                num = float(current)
                if num != 0:
                    result = 1 / num
                    self.add_to_history(f"1/{num}", result)
                    self.display_var.set(str(result))
                else:
                    messagebox.showerror("Error", "Division by zero")
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Square
        elif btn_text == 'x²':
            try:
                num = float(current)
                result = num ** 2
                self.add_to_history(f"{num}²", result)
                self.display_var.set(str(result))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Cube
        elif btn_text == 'x³':
            try:
                num = float(current)
                result = num ** 3
                self.add_to_history(f"{num}³", result)
                self.display_var.set(str(result))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Absolute value
        elif btn_text == '|x|':
            try:
                num = float(current)
                result = abs(num)
                self.add_to_history(f"|{num}|", result)
                self.display_var.set(str(result))
            except:
                messagebox.showerror("Error", "Invalid operation")
        
        # Memory operations
        elif btn_text == 'MC':  # Memory Clear
            self.memory = 0
        
        elif btn_text == 'MR':  # Memory Recall
            self.display_var.set(str(self.memory))
        
        elif btn_text == 'M+':  # Memory Add
            try:
                self.memory += float(current)
            except:
                pass
        
        elif btn_text == 'M-':  # Memory Subtract
            try:
                self.memory -= float(current)
            except:
                pass
    
    def calculate_result(self):
        """Calculate result of operation"""
        try:
            second_number = float(self.display_var.get())
            
            if self.current_operation == '+':
                result = self.first_number + second_number
                operation = f"{self.first_number} + {second_number}"
            elif self.current_operation == '-':
                result = self.first_number - second_number
                operation = f"{self.first_number} - {second_number}"
            elif self.current_operation == '*':
                result = self.first_number * second_number
                operation = f"{self.first_number} × {second_number}"
            elif self.current_operation == '/':
                if second_number == 0:
                    messagebox.showerror("Error", "Division by zero")
                    return
                result = self.first_number / second_number
                operation = f"{self.first_number} ÷ {second_number}"
            elif self.current_operation == '^':
                result = self.first_number ** second_number
                operation = f"{self.first_number}^{second_number}"
            else:
                return
            
            result = round(result, 10)
            self.add_to_history(operation, result)
            self.display_var.set(str(result))
            self.first_number = None
            self.current_operation = None
        
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def add_to_history(self, operation, result):
        """Add calculation to history"""
        time_str = datetime.now().strftime("%H:%M:%S")
        self.history.append((operation, result, time_str))
        
        # Add to treeview
        tag = 'evenrow' if len(self.history) % 2 == 0 else 'oddrow'
        self.history_tree.insert('', tk.END, values=(operation, f"{result:.6g}", time_str), tags=(tag,))
        
        # Scroll to bottom
        self.history_tree.see(self.history_tree.get_children()[-1])
    
    def clear_history(self):
        """Clear history"""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            self.history.clear()
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)


class CalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = CalculatorGUI(self.root)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
