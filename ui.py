# ui.py
import tkinter as tk
from tkinter import ttk, messagebox

class WordCloudUI:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.selected_index = None
        self._setup_ui()

    def _setup_ui(self):
        self.root.title("WordCloud Input")
        self.root.resizable(False, False)
        self._center_window(420, 450)

        # ---- Frame nhập liệu ----
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=15)

        # Dòng 1: Label + Entry "Từ"
        tk.Label(input_frame, text="Từ:", width=10, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.entry_word = tk.Entry(input_frame, width=30)
        self.entry_word.grid(row=0, column=1, padx=5, pady=5)

        # Dòng 2: Label + Entry "Số lượng"
        tk.Label(input_frame, text="Số lượng:", width=10, anchor="w").grid(row=1, column=0, padx=5, pady=5)
        self.entry_count = tk.Entry(input_frame, width=30)
        self.entry_count.grid(row=1, column=1, padx=5, pady=5)

        # ---- Nút thao tác ----
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=10)

        ttk.Button(frame_btn, text="Thêm / Cập nhật", command=self.add_or_update).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btn, text="Xóa", command=self.delete_word).grid(row=0, column=1, padx=5)

        # ---- Danh sách từ ----
        self.listbox = tk.Listbox(self.root, width=40, height=15)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def _center_window(self, width, height):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # --- Các hàm logic (giữ nguyên như trước) ---
    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for w, c in self.data_manager.get_all():
            self.listbox.insert(tk.END, f"{w} - {c}")

    def clear_inputs(self):
        self.entry_word.delete(0, tk.END)
        self.entry_count.delete(0, tk.END)

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            self.selected_index = None
            return
        self.selected_index = selection[0]
        word, count = self.data_manager.get_all()[self.selected_index]
        self.entry_word.delete(0, tk.END)
        self.entry_word.insert(0, word)
        self.entry_count.delete(0, tk.END)
        self.entry_count.insert(0, str(count))

    def add_or_update(self):
        word = self.entry_word.get().strip()
        count = self.entry_count.get().strip()

        if not word or not count.isdigit():
            messagebox.showerror("Lỗi", "Vui lòng nhập từ và số lượng hợp lệ!")
            return

        if self.selected_index is not None:
            self.data_manager.update(self.selected_index, word, int(count))
        else:
            self.data_manager.add(word, int(count))

        self.refresh_listbox()
        self.clear_inputs()
        self.selected_index = None

    def delete_word(self):
        if self.selected_index is None:
            messagebox.showwarning("Chưa chọn", "Hãy chọn một mục để xóa!")
            return
        self.data_manager.delete(self.selected_index)
        self.refresh_listbox()
        self.clear_inputs()
        self.selected_index = None
