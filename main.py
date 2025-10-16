import tkinter as tk
from tkinter import filedialog

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Chọn file Excel",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if file_path:
        label_file.config(text=f"File đã chọn:\n{file_path}")
    else:
        label_file.config(text="Chưa chọn file nào")

# Hàm căn giữa cửa sổ
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry(f"{width}x{height}+{x}+{y}")

# --- Cửa sổ chính ---
root = tk.Tk()
root.title("Import file Excel")

# Kích thước mong muốn và căn giữa
window_width = 450
window_height = 200
center_window(root, window_width, window_height)

# Tiêu đề
tk.Label(root, text="Chọn file Excel để xử lý", font=("Arial", 14)).pack(pady=10)

# Nút chọn file
btn_choose = tk.Button(root, text="📂 Chọn file Excel", command=choose_file, font=("Arial", 12))
btn_choose.pack(pady=10)

# Nhãn hiển thị đường dẫn file
label_file = tk.Label(root, text="Chưa chọn file nào", fg="gray", wraplength=400)
label_file.pack(pady=10)

root.mainloop()
