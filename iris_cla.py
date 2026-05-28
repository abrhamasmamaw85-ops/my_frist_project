import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import time

# Load and train model
iris = load_iris()
X = iris.data
y = iris.target
target_names = iris.target_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Create main window
root = tk.Tk()
root.title("Iris Classifier")
root.geometry("600x650")
root.configure(bg='#1a1a2e')
root.resizable(False, False)

# Main container
main_frame = tk.Frame(root, bg='#16213e')
main_frame.pack(pady=20, padx=20, fill='both', expand=True)

# Title
title_label = tk.Label(main_frame, text="Iris Classifier", 
                       font=("Helvetica", 22, "bold"), 
                       bg='#16213e', fg='#e94560')
title_label.pack(pady=(20, 5))

# Subtitle
sub_label = tk.Label(main_frame, text="Advanced Botanical Morphological Analysis", 
                     font=("Helvetica", 10, "italic"), 
                     bg='#16213e', fg='#a0a0a0')
sub_label.pack(pady=(0, 25))

# Input frame - 2x2 grid layout
input_frame = tk.Frame(main_frame, bg='#16213e')
input_frame.pack(pady=10, padx=30, fill='x')

# Entry variables
sepal_length = tk.DoubleVar(value=5.1)
sepal_width = tk.DoubleVar(value=3.5)
petal_length = tk.DoubleVar(value=1.4)
petal_width = tk.DoubleVar(value=0.2)

# ========== SEPAL SECTION ==========
sepal_frame = tk.LabelFrame(input_frame, text="🌿 SEPAL", 
                            font=("Helvetica", 11, "bold"),
                            bg='#16213e', fg='#e94560',
                            bd=2, relief='ridge')
sepal_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

tk.Label(sepal_frame, text="Length (cm):", font=("Helvetica", 10), 
         bg='#16213e', fg='white').grid(row=0, column=0, padx=15, pady=(15,5), sticky='w')
entry_sl = tk.Entry(sepal_frame, textvariable=sepal_length, font=("Helvetica", 12), 
                    width=12, bg='#0f3460', fg='white', insertbackground='white',
                    justify='center')
entry_sl.grid(row=0, column=1, padx=10, pady=(15,5))

tk.Label(sepal_frame, text="Width (cm):", font=("Helvetica", 10), 
         bg='#16213e', fg='white').grid(row=1, column=0, padx=15, pady=10, sticky='w')
entry_sw = tk.Entry(sepal_frame, textvariable=sepal_width, font=("Helvetica", 12), 
                    width=12, bg='#0f3460', fg='white', insertbackground='white',
                    justify='center')
entry_sw.grid(row=1, column=1, padx=10, pady=10)

# ========== PETAL SECTION ==========
petal_frame = tk.LabelFrame(input_frame, text="🌸 PETAL", 
                            font=("Helvetica", 11, "bold"),
                            bg='#16213e', fg='#e94560',
                            bd=2, relief='ridge')
petal_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

tk.Label(petal_frame, text="Length (cm):", font=("Helvetica", 10), 
         bg='#16213e', fg='white').grid(row=0, column=0, padx=15, pady=(15,5), sticky='w')
entry_pl = tk.Entry(petal_frame, textvariable=petal_length, font=("Helvetica", 12), 
                    width=12, bg='#0f3460', fg='white', insertbackground='white',
                    justify='center')
entry_pl.grid(row=0, column=1, padx=10, pady=(15,5))

tk.Label(petal_frame, text="Width (cm):", font=("Helvetica", 10), 
         bg='#16213e', fg='white').grid(row=1, column=0, padx=15, pady=10, sticky='w')
entry_pw = tk.Entry(petal_frame, textvariable=petal_width, font=("Helvetica", 12), 
                    width=12, bg='#0f3460', fg='white', insertbackground='white',
                    justify='center')
entry_pw.grid(row=1, column=1, padx=10, pady=10)

input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)

# ========== MOVING ANIMATION SECTION ==========
animation_frame = tk.Frame(main_frame, bg='#16213e')
animation_frame.pack(pady=20, padx=40, fill='x')

# Moving text/animation label
moving_label = tk.Label(animation_frame, text="⚪", 
                        font=("Helvetica", 20), 
                        bg='#16213e', fg='#e94560')
moving_label.pack(pady=5)

# Animation status
anim_status = tk.Label(animation_frame, text="", 
                       font=("Helvetica", 9), 
                       bg='#16213e', fg='#a0a0a0')
anim_status.pack()

# Progress bar
progress_bar = ttk.Progressbar(animation_frame, mode='indeterminate', length=400)
progress_bar.pack(pady=10)
progress_bar.pack_forget()

# Animation variables
animation_running = False
animation_step = 0
animation_direction = 1  # 1 = forward, -1 = backward

# Moving animation function (back and forward)
def move_animation():
    global animation_step, animation_direction, animation_running
    
    if not animation_running:
        return
    
    # Moving symbols (back and forth)
    symbols = ["⚪", "🟡", "🟢", "🔵", "🟣", "🔴", "🟠", "🟡", "⚪"]
    positions = ["⬅️", "➡️", "⬅️", "➡️", "⬅️", "➡️", "⬅️", "➡️", "⬅️"]
    
    # Change symbol based on step (creates movement effect)
    moving_label.config(text=f"{symbols[animation_step % len(symbols)]} {positions[animation_step % len(positions)]}")
    
    # Update status text with dots (loading effect)
    dots = ["", ".", "..", "...", "..", "."]
    anim_status.config(text=f"Analyzing features{dots[animation_step % len(dots)]}")
    
    # Move step back and forth
    animation_step += animation_direction
    
    # Reverse direction at boundaries
    if animation_step >= 8:
        animation_direction = -1  # Go backward
    elif animation_step <= 0:
        animation_direction = 1   # Go forward
    
    # Continue animation
    root.after(150, move_animation)

# Start moving animation
def start_animation():
    global animation_running, animation_step, animation_direction
    animation_running = True
    animation_step = 0
    animation_direction = 1
    progress_bar.pack(pady=10)
    progress_bar.start(20)
    move_animation()

# Stop moving animation
def stop_animation():
    global animation_running
    animation_running = False
    progress_bar.stop()
    progress_bar.pack_forget()
    moving_label.config(text="✅", fg='#00ff88')
    anim_status.config(text="Complete!")
    root.after(1500, lambda: moving_label.config(text="⚪", fg='#e94560'))
    root.after(1500, lambda: anim_status.config(text=""))

# Result display frame
result_frame = tk.Frame(main_frame, bg='#0f3460', relief='ridge', bd=2)
result_frame.pack(pady=20, padx=40, fill='x')

result_label = tk.Label(result_frame, text="—", 
                        font=("Helvetica", 16, "bold"), 
                        bg='#0f3460', fg='#e94560')
result_label.pack(pady=20)

confidence_label = tk.Label(result_frame, text="", 
                            font=("Helvetica", 9), 
                            bg='#0f3460', fg='#a0a0a0')
confidence_label.pack(pady=(0, 10))

# Prediction function
def predict_flower():
    try:
        # Start moving animation
        start_animation()
        
        # Update GUI to show animation
        root.update()
        
        # Simulate processing time (so animation is visible)
        root.after(500, lambda: process_prediction())
        
    except Exception as e:
        stop_animation()
        messagebox.showerror("Error", f"Please enter valid numbers!\nError: {str(e)}")

def process_prediction():
    try:
        # Get values
        s_len = sepal_length.get()
        s_wid = sepal_width.get()
        p_len = petal_length.get()
        p_wid = petal_width.get()
        
        # Predict
        input_data = np.array([[s_len, s_wid, p_len, p_wid]])
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        species_names = {
            0: '🌸 Iris Setosa',
            1: '🌼 Iris Versicolor', 
            2: '🌺 Iris Virginica'
        }
        
        confidence = probabilities[prediction] * 100
        
        # Show result
        result_label.config(text=species_names[prediction], fg='#00ff88')
        confidence_label.config(text=f"Confidence: {confidence:.1f}%")
        status_label.config(text=f"✅ Prediction: {species_names[prediction]} ({confidence:.1f}%)")
        
        # Stop animation
        stop_animation()
        
    except Exception as e:
        stop_animation()
        messagebox.showerror("Error", f"Please enter valid numbers!\nError: {str(e)}")
        result_label.config(text="—", fg='#e94560')
        confidence_label.config(text="")
        status_label.config(text="❌ Error: Invalid input")

# Status label
status_label = tk.Label(main_frame, text="✅ Ready - Enter values and click PROCESS", 
                        font=("Helvetica", 9), 
                        bg='#16213e', fg='#a0a0a0')
status_label.pack(pady=10)

# PROCESS BUTTON
process_button = tk.Button(main_frame, 
                           text="🔍 PROCESS", 
                           command=predict_flower,
                           font=("Helvetica", 14, "bold"),
                           bg='#e94560', 
                           fg='white',
                           activebackground='#c73e54',
                           activeforeground='white',
                           bd=0, 
                           padx=40, 
                           pady=12,
                           cursor='hand2')
process_button.pack(pady=15)

# Footer
footer = tk.Label(main_frame, text="© Iris Classification System | Model Accuracy: ~97%", 
                  font=("Helvetica", 8), 
                  bg='#16213e', fg='#555555')
footer.pack(pady=(10, 10))

# Allow Enter key to work
root.bind('<Return>', lambda event: predict_flower())

# Run the application
root.mainloop()
