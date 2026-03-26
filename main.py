import sys
import threading

from PySide6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt, Signal, QObject

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# ===== データ =====
def create_grid():
    return [
        [{"event": "~~~~", "type": -1} for _ in range(24)]
        for _ in range(7)
    ]

grid = create_grid()

# ===== Qt用シグナル =====
class Bridge(QObject):
    update_signal = Signal()

bridge = Bridge()

# ===== GUI =====
class GridWindow(QTableWidget):
    def __init__(self):
        super().__init__(7, 24)

        self.setWindowTitle("生活管理シート")
        self.setHorizontalHeaderLabels([str(h) for h in range(24)])
        self.setVerticalHeaderLabels(DAYS)

        # マスサイズ調整
        for col in range(24):
            self.setColumnWidth(col, 50)

        for row in range(7):
            self.setRowHeight(row, 40)

        self.horizontalHeader().setFixedHeight(20)
        self.verticalHeader().setFixedWidth(50)

        self.refresh()

        # シグナル接続
        bridge.update_signal.connect(self.refresh)

    def refresh(self):
        for d in range(7):
            for h in range(24):
                val = grid[d][h]["event"]

                text = "" if val == "~~~~" else val[:4]

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(d, h, item)

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

    # GUI更新
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

    window = GridWindow()
    window.resize(1260, 310)
    window.show()

    # コンソールを別スレッドで動かす
    thread = threading.Thread(target=console_loop, daemon=True)
    thread.start()

    sys.exit(app.exec())