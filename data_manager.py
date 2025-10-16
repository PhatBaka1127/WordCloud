# data_manager.py

class WordDataManager:
    def __init__(self):
        self.words = []

    def add(self, word, count):
        """Thêm hoặc cập nhật từ."""
        for i, (w, _) in enumerate(self.words):
            if w == word:
                self.words[i] = (word, count)
                return
        self.words.append((word, count))

    def update(self, index, word, count):
        """Cập nhật theo vị trí."""
        if 0 <= index < len(self.words):
            self.words[index] = (word, count)

    def delete(self, index):
        """Xóa theo vị trí."""
        if 0 <= index < len(self.words):
            del self.words[index]

    def get_all(self):
        """Trả về danh sách từ."""
        return self.words
