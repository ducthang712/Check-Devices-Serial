import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def save_settings():
    com_port = com_var.get()
    baud_rate = baudrate_var.get()
    file_path = path_var.get()
    device = device_var.get()
    
    settings = f"Device: {device}\nCOM Port: {com_port}\nBaudrate: {baud_rate}\nFile Path: {file_path}"
    
    try:
        with open(file_path, 'w') as file:
            file.write(settings)
        messagebox.showinfo("Success", "Settings saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save settings: {e}")

def browse_path():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        path_var.set(file_path)

# Create the main window
root = tk.Tk()
root.title("Settings")
root.geometry("700x300")  # Set the window size to be larger

# Create a frame for the left side
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=20, pady=20)

# Create and place labels and input fields in the left frame
tk.Label(left_frame, text="Select Device:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10, sticky='w')
tk.Label(left_frame, text="Select COM Port:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10, sticky='w')
tk.Label(left_frame, text="Set Baudrate:", font=("Helvetica", 14)).grid(row=2, column=0, pady=10, sticky='w')
tk.Label(left_frame, text="Select Path to Save File:", font=("Helvetica", 14)).grid(row=3, column=0, pady=10, sticky='w')

device_var = tk.StringVar(left_frame)
device_var.set("ESP32")
device_menu = tk.OptionMenu(left_frame, device_var, "ESP32", "ESP8266")
device_menu.config(font=("Helvetica", 12))
device_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

com_var = tk.StringVar(left_frame)
com_var.set("1")
com_menu = tk.OptionMenu(left_frame, com_var, *list(range(1, 11)))
com_menu.config(font=("Helvetica", 12))
com_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')

baudrate_var = tk.StringVar(left_frame)
baudrate_entry = tk.Entry(left_frame, textvariable=baudrate_var, font=("Helvetica", 12))
baudrate_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

path_var = tk.StringVar(left_frame)
path_entry = tk.Entry(left_frame, textvariable=path_var, width=30, font=("Helvetica", 12))
path_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')
browse_button = tk.Button(left_frame, text="Browse...", command=browse_path, font=("Helvetica", 12))
browse_button.grid(row=3, column=2, padx=10, pady=10, sticky='w')

# Create and place the save button in the left frame
save_button = tk.Button(left_frame, text="Save Settings", command=save_settings, font=("Helvetica", 14))
save_button.grid(row=4, column=0, columnspan=3, pady=20, sticky='w')

# Create a frame for the right side (empty frame)
right_frame = tk.Frame(root)
right_frame.pack(side="right", padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()
