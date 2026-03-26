import sys
import threading

from PySide6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QColor

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# ===== データ =====
def create_grid():
    return [
        [{"event": "~~~~", "type": "none"} for _ in range(24)]
        for _ in range(7)
    ]

grid = create_grid()

# ===== 色 =====
TYPE_COLORS = {
    "sleep": QColor("#a78bfa"),
    "work": QColor("#60a5fa"),
    "eat": QColor("#34d399"),
    "none": QColor("#ffffff")
}

# ===== Qt用シグナル =====
class Bridge(QObject):
    update_signal = Signal()

bridge = Bridge()

# ===== GUI（テーブル） =====
class GridWindow(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(7, 24, parent)

        self.setHorizontalHeaderLabels([str(h) for h in range(24)])
        self.setVerticalHeaderLabels(DAYS)

        # サイズ調整
        for col in range(24):
            self.setColumnWidth(col, 50)
        for row in range(7):
            self.setRowHeight(row, 40)

        self.horizontalHeader().setFixedHeight(20)
        self.verticalHeader().setFixedWidth(50)

        self.setEditTriggers(QTableWidget.NoEditTriggers)

        self.refresh()

        # シグナル
        bridge.update_signal.connect(self.refresh)
        self.cellClicked.connect(self.handle_click)

    def refresh(self):
        for d in range(7):
            for h in range(24):
                val = grid[d][h]["event"]
                t = grid[d][h]["type"]

                text = "" if val == "~~~~" else val[:4]

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)

                # 色
                item.setBackground(TYPE_COLORS.get(t, QColor("#ffffff")))

                self.setItem(d, h, item)

    def handle_click(self, row, col):
        parent = self.parent()

        if parent.current_type is None:
            print("タイプ選択してね")
            return

        grid[row][col]["event"] = parent.current_type
        grid[row][col]["type"] = parent.current_type

        self.refresh()

# ===== メインUI =====
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("生活管理シート")
        self.current_type = None

        layout = QVBoxLayout()

        # テーブル
        self.table = GridWindow(self)
        layout.addWidget(self.table)

        # ボタン
        btn_layout = QHBoxLayout()

        for name in ["sleep", "work", "eat"]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, n=name: self.select_type(n))
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def select_type(self, type_):
        self.current_type = type_
        print(f"選択中: {type_}")

# ===== ロジック =====
def add_event(day_str, start, end, name, type_):
    if day_str not in DAYS:
        print("曜日が不正です")
        return

    day_index = DAYS.index(day_str)

    try:
        start = int(start)
        end = int(end)
    except:
        print("時間は整数で入力してね")
        return

    if not (0 <= start < 24 and 0 < end <= 24 and start < end):
        print("時間の範囲がおかしい")
        return

    for h in range(start, end):
        grid[day_index][h]["event"] = name
        grid[day_index][h]["type"] = type_

    print(f"{day_str} {start}-{end} に '{name}' ({type_}) を追加")

    bridge.update_signal.emit()

# ===== コンソール入力 =====
def console_loop():
    print("コマンド入力: add Mon 9 12 work study")

    while True:
        cmd = input(">>> ").strip()

        if cmd == "exit":
            break

        elif cmd.startswith("add"):
            parts = cmd.split()

            if len(parts) < 6:
                print("形式: add Mon 9 12 work study")
                continue

            _, day, start, end, name, type_ = parts[:6]
            add_event(day, start, end, name, type_)

# ===== 実行 =====
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(1260, 450)
    window.show()

    # コンソール入力（別スレッド）
    thread = threading.Thread(target=console_loop, daemon=True)
    thread.start()

    sys.exit(app.exec())