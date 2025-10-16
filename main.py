# main.py
import tkinter as tk
from data_manager import WordDataManager
from ui import WordCloudUI

def main():
    root = tk.Tk()
    data_manager = WordDataManager()
    app = WordCloudUI(root, data_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
