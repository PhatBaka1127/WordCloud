import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from wordcloud import WordCloud
from PIL import Image, ImageTk
import io

class WordCloudUI:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.selected_index = None
        self.wordcloud_image = None
        self.last_wordcloud = None
        self._setup_ui()

    def _setup_ui(self):
        self.root.title("WordCloud")
        self.root.resizable(False, False)
        self._center_window(1200, 600)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        main_frame.columnconfigure(0, weight=1, uniform="group1")
        main_frame.columnconfigure(1, weight=2, uniform="group1")

        # ---- KHUNG TRÁI ----
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        form_frame = tk.LabelFrame(left_frame, text="Nhập dữ liệu", padx=10, pady=10)
        form_frame.pack(fill="x", pady=10)

        tk.Label(form_frame, text="Từ:", width=10, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.entry_word = tk.Entry(form_frame, width=25)
        self.entry_word.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Số lượng:", width=10, anchor="w").grid(row=1, column=0, padx=5, pady=5)
        self.entry_count = tk.Entry(form_frame, width=25)
        self.entry_count.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Thêm / Cập nhật", command=self.add_or_update).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Xóa", command=self.delete_word).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Tạo WordCloud", command=self.generate_wordcloud).grid(row=0, column=2, padx=5)

        list_frame = tk.LabelFrame(left_frame, text="Danh sách từ", padx=5, pady=5)
        list_frame.pack(fill="both", expand=True, pady=10)
        self.listbox = tk.Listbox(list_frame, width=40, height=20)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # ---- KHUNG PHẢI ----
        right_frame = tk.LabelFrame(main_frame, text="WordCloud Preview", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.image_label = tk.Label(
            right_frame,
            bg="#f4f4f4",
            width=80,
            height=30,
            relief="sunken",
            text="(WordCloud sẽ hiển thị ở đây)"
        )
        self.image_label.pack(fill="both", expand=True)

        # ➕ Nút Xuất file ảnh
        ttk.Button(right_frame, text="💾 Xuất file ảnh (.png)", command=self.save_wordcloud).pack(pady=10)

    def _center_window(self, width, height):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

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

    def generate_wordcloud(self):
        words = {w: c for w, c in self.data_manager.get_all()}
        if not words:
            messagebox.showwarning("Trống", "Không có từ nào để tạo WordCloud!")
            return

        wc = WordCloud(width=900, height=500, background_color="white", colormap="plasma")
        wc.generate_from_frequencies(words)
        self.last_wordcloud = wc  # lưu lại để export sau

        img_buf = io.BytesIO()
        wc.to_image().save(img_buf, format="PNG")
        img_buf.seek(0)
        image = Image.open(img_buf)
        image = image.resize((700, 450))
        self.wordcloud_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.wordcloud_image, text="")

    def save_wordcloud(self):
        if self.last_wordcloud is None:
            messagebox.showinfo("Chưa có ảnh", "Hãy tạo WordCloud trước khi lưu!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Lưu WordCloud thành ảnh"
        )
        if not file_path:
            return

        self.last_wordcloud.to_file(file_path)
        messagebox.showinfo("Thành công", f"Đã lưu file ảnh:\n{file_path}")
