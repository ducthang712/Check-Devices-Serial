import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from datetime import datetime
from openpyxl import load_workbook
import pandas as pd
import serial.tools.list_ports
import serial
import time
import os


def START_COMMAND():
    device = device_var.get()
    com_port = com_var.get()
    baudrate = baudrate_var.get()
    path = path_var.get()
    # Triển khai câu lệnh với các lựa chọn trên
    print(f"Device: {device}, COM Port: {com_port}, Baudrate: {baudrate}")
    # Open PORT thành công
    if check_com_ports(com_port) == True:
        device_check(com_port, baudrate)
        update_leds('green')
    # Open PORT không thành công
    else:
        messagebox.showinfo("ERROR", "Check again your settings!")
        status_label.config(text="waiting for connection...", fg="black")
        update_leds('red')
    # Kiểm tra xem path có hợp lệ không
    if not path or not os.path.isdir(path):
        messagebox.showerror("Error", "Path không hợp lệ hoặc chưa được chọn.")
        return
    else:
        messagebox.showinfo("SUCCESS!", "READY TO SAVE")

def device_confirm(device):
    global path_txt
    if device == 'banana':
        path_txt = 'devices_config//banana_config.txt'
    elif device == 'orange':
        path_txt = 'devices_config//orange_config.txt'
    elif device == 'apple':
        path_txt = 'devices_config//apple_config.txt'
    data['name'] = device


def device_process(path_txt):
    try:
        with open(path_txt, 'r') as file:
            # Read the file line by line
            commands = file.readlines()

        # Process demand in file
        for command in commands:
            command = command.strip()  # Remove any leading/trailing whitespace
            if command:  # Check if the line is not empty
                print(command)
            else:
                continue
    except FileNotFoundError:
        print(f"Error: The file {path_txt} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_com_ports(com_port):
    try:
        ser = serial.Serial(f'{com_port}')  # ser = serial.Serial(comport)
        ser.close()
        return True
    except (serial.SerialException, ValueError):
        return False

def device_check(com_port, baudrate):
    global ser
    ser = None
    ser = serial.Serial(f'{com_port}', baudrate, timeout=1)
    ser.write(b"hello")
    start_time = time.time()
    response = None
    while time.time() - start_time < 1.5:  # 5 = time delay
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            print(f"{response}\n")
            break
        time.sleep(0.1)
    # Xử lý dữ liệu trả về từ ESP32
    if response == "world":
        status_label.config(text="ESP is ready", fg="green")
        top_text.insert(tk.END, "----------DEVICE IS READY-----------\n")

    elif response is None:
        status_label.config(text="CANNOT CONNECT. TRY AGAIN...", fg="red")
    else:
        status_label.config(text="WRONG SYNTAX...", fg="red")

def create_excel_file(filename):
    df = pd.DataFrame(
        columns=['UpdateTime', 'SerialNumber', 'Name', 'Type', 'DeviceID', 'UUID', 'Secret', 'AppKey', 'DevUI',
                 'Description'])
    df.to_excel(filename, index=False)

    global data
    data = {
        'time': [''],
        'seri': [''],
        'name': [''],
        'type': [''],
        'deid': [''],
        'uuid': [''],
        'secr': [''],
        'keys': [''],
        'deui': [''],
        'stat': ['']
    }

# Lấy đường dẫn từ người dùng hoặc sử dụng đường dẫn đã lưu
def check_file_path(new_path):
    config_file = 'path_config.txt'

    # Kiểm tra nếu đã có đường dẫn lưu trong file config
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            saved_path = file.readline().strip()
        # new_path = input(f"Nhập đường dẫn lưu trữ file Excel (hoặc nhấn Enter để sử dụng '{saved_path}'): ").strip()

        if new_path == '':
            tk.messagebox.showerror("Error", "Path invalid or cannot found.")
            return None

        if new_path == saved_path and os.path.exists(saved_path):
            return saved_path

        # Nếu đường dẫn mới khác, cập nhật file config
        with open(config_file, 'w') as file:
            file.write(new_path)
            create_excel_file("device_info.xlsx")
        return new_path

def append_to_excel(filename):
    data['time'] = current_time()
    df = pd.DataFrame(data)
    # Mở file Excel và thêm dữ liệu mới vào
    with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

def browse_file():
    global path_xlsx
    filename = filedialog.askdirectory()
    path_var.set(filename)
    user_input = None
    while user_input is None:
        user_input = simpledialog.askstring("Input", "Nhập tên file: ")
        if user_input is not None:
            path_xlsx = f'{user_input}.xlsx'
            create_excel_file(path_xlsx)
            break
        else:
            messagebox.showerror("BAT BUOC Nhap ten file. Try again")
            break

def update_leds(value):
    if value == 'green':
        green_led_label.config(bg='green')
        red_led_label.config(bg='grey')
    elif value == 'red':
        green_led_label.config(bg='grey')
        red_led_label.config(bg='red')
    elif value == 'off':
        green_led_label.config(bg='grey')
        red_led_label.config(bg='grey')

# Sự kiện khi nhấn Enter với TextBox
def text_update(event):
    device_confirm(f"{device_var.get()}")
    top_text_data = top_text.get("1.0", tk.END).strip().splitlines()[-1]

    #print top text data
    top_text.insert(tk.END, f"\n{current_time()} {top_text_data}")
    response = data_response(f"{top_text_data.lower()}")
    if response == "accepted":
        bottom_text.insert(tk.END, f" DEVICE ACCEPTED...\n")
        process_data_response_1()


    append_to_excel(path_xlsx)


def data_response(send_text):
    ser.write(send_text.encode())
    bottom_text.insert(tk.END, f"{current_time()} '{send_text.rstrip()}' >>>> ")
    start_time = time.time()
    response = None

    while time.time() - start_time < 1.2:
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            break
        time.sleep(0.1)

    # Kiểm tra và in ra dữ liệu trả về
    if response == "???":
        bottom_text.insert(tk.END, " ERROR\n")
        return False

    elif response is None:
        bottom_text.insert(tk.END, " NO RESPONSE\n")
        return False

    else:
        return response


def process_data_response_1():
    try:
        with open(path_txt, 'r') as file:
            # Read the file line by line
            commands = file.readlines()

        # Process demand in file
        for command in commands:
            process_base_on_config_file(command)
    except FileNotFoundError:
        # bottom_text.insert(tk.END, f"{current_time()} The file {path_txt} was not found.\n")
        print(f"Error: The file {path_txt} was not found.")
    except Exception as e:
        # bottom_text.insert(tk.END, f"{current_time()} An error occured: {e}\n")
        print(f"An error occurred: {e}")

def process_base_on_config_file(command):
    response = data_response(f"{command}")

    if response is False:
        data[f"{command}"] = "FAILED"
    if response is not False:
        # data process
        title = response[0:4]
        content = response[5:]

        # Sort the response data
        data[f"{title}"] = content
        # Print bottom text
        bottom_text.insert(tk.END, " PASS\n")



def process_data_response(response):
    parts = response.split('||')
    for part in parts:
        bottom_text.insert(tk.END, f"{current_time()} {part}\n")
        # data process
        title = part[0:4]
        content = part[5:]

        #Sort the response data
        data[f"{title}"] = content


# Thời gian thực
def current_time():
    _current_time = datetime.now().strftime('[%Y-%m-%d,%H:%M:%S]')
    return _current_time


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Device Configuration")
root.geometry("1300x800")

# Chia cửa sổ thành hai phần
left_frame = tk.LabelFrame(root, text="DataLogs", width=900, height=800)
right_frame = tk.LabelFrame(root, text="Device Settings", width=400, height=800)
left_frame.grid(row=0, column=0, sticky='nsew')
right_frame.grid(row=0, column=1, sticky='nsew')

root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=1)

# Tạo các biến để lưu trữ lựa chọn
device_var = tk.StringVar()
com_var = tk.StringVar()
baudrate_var = tk.StringVar()
path_var = tk.StringVar()

# Chia khung bên trái thành hai phần trên và dưới
top_left_frame = ttk.LabelFrame(left_frame, text="Sending Keys", width=900, height=400)
bottom_left_frame = ttk.LabelFrame(left_frame, text="Device Logs", width=900, height=400)

top_left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
bottom_left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_rowconfigure(0, weight=1)

# Tạo Text widget để nhập liệu trong phần trên và dưới của khung trái
top_text = tk.Text(top_left_frame, wrap='word', height=19)
top_text.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

bottom_text = tk.Text(bottom_left_frame, wrap='word', height=19)
bottom_text.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

top_left_frame.grid_rowconfigure(0, weight=1)
top_left_frame.grid_columnconfigure(0, weight=1)

bottom_left_frame.grid_rowconfigure(0, weight=1)
bottom_left_frame.grid_columnconfigure(0, weight=1)

# Thêm sự kiện để phát hiện khi nhấn Enter trong ô "Thông tin trên"
top_text.bind("<Return>", text_update)

# Chia khung bên phải thành hai phần trên và dưới, với phần trên nhỏ hơn phần dưới
top_right_frame = ttk.LabelFrame(right_frame, text="Settings", width=400, height=150)
bottom_right_frame = ttk.LabelFrame(right_frame, text="Status", width=400, height=250)

top_right_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
bottom_right_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=3)

# Tạo nhãn hiển thị trạng thái kết nối trong phần trên của khung phải
status_label = tk.Label(bottom_right_frame, text="wait for connection...", foreground="black", font=("Arial", 14))
status_label.grid(row=3, column=1, padx=5, pady=5)

# Tạo khung cho các cài đặt trong phần trên của khung phải
settings_frame = ttk.LabelFrame(top_right_frame, text="Configuration")
settings_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Thiết kế các nhãn và combo box trong khung cài đặt
ttk.Label(settings_frame, text="Chọn Device:", anchor='e').grid(row=0, column=0, sticky='e')
device_var.set("banana")
device_combo = ttk.Combobox(settings_frame, textvariable=device_var, values=["banana", "orange", "apple"])
device_combo.grid(row=0, column=1, columnspan=2, sticky='w')

ttk.Label(settings_frame, text="Chọn cổng COM:", anchor='e').grid(row=1, column=0, sticky='e')
com_var.set("COM7")
com_combo = ttk.Combobox(settings_frame, textvariable=com_var, values=[f"COM{i}" for i in range(1, 16)])
com_combo.grid(row=1, column=1, columnspan=2, sticky='w')

ttk.Label(settings_frame, text="Chọn Baudrate:", anchor='e').grid(row=2, column=0, sticky='e')
baudrate_var.set("115200")
baudrate_combo = ttk.Combobox(settings_frame, textvariable=baudrate_var,
                              values=["9600", "19200", "38400", "57600", "115200"])
baudrate_combo.grid(row=2, column=1, columnspan=2, sticky='w')

ttk.Label(settings_frame, text="Chọn Path File:", anchor='e').grid(row=3, column=0, sticky='e')
path_entry = ttk.Entry(settings_frame, textvariable=path_var, width=25)
path_entry.grid(row=3, column=1, sticky='w')
ttk.Button(settings_frame, text="...", command=browse_file).grid(row=3, column=2, sticky='w')

# Tạo nút Start,Save,AutoSave trong phần trên của khung phải
ttk.Button(top_right_frame, text="                  START                 ", command=START_COMMAND).grid(row=5,
                                                                                                         column=0,
                                                                                                         columnspan=4,
                                                                                                         pady=10)

# Tạo đèn LED xanh và đỏ trong phần dưới của khung phải
led_frame = ttk.LabelFrame(bottom_right_frame, text="Device Status")
led_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

green_led_label = tk.Label(led_frame, text="Connect", bg='gray', width=20)
green_led_label.grid(row=0, column=0, padx=5, pady=5)

red_led_label = tk.Label(led_frame, text="Disconnect", bg='red', width=20)
red_led_label.grid(row=0, column=1, padx=5, pady=5)

# Đặt căn lề bên phải cho tất cả các widget trong khung cài đặt
for child in settings_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
