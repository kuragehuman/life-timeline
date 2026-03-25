# life_timeline.py

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# ===== 初期化 =====
def create_grid():
    return [
        [
            {"event": "~~~~", "type": -1}
            for _ in range(24)
        ]
        for _ in range(7)
    ]

grid = create_grid()

# ===== 追加処理 =====
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

# ===== 表示 =====
def print_grid():
    # ヘッダー
    header = "     " + "".join([f"{h:>3}" for h in range(24)])
    print(header)
    print("    " + "---" * 24)

    for d, day in enumerate(DAYS):
        row = f"{day:>3} |"
        for h in range(24):
            val = grid[d][h]["event"]

            # 表示短縮（長いと崩れる）
            if val == "~~~~":
                cell = " . "
            else:
                cell = f"{val[:2]:>2} "

            row += cell

        print(row)

# ===== コマンド処理 =====
def run():
    print("コマンドを入力してね")
    print("add Mon 9 12 work study")
    print("print")
    print("exit")

    while True:
        cmd = input(">>> ").strip()

        if cmd == "exit":
            break

        elif cmd == "print":
            print_grid()

        elif cmd.startswith("add"):
            parts = cmd.split()

            if len(parts) < 6:
                print("形式: add Mon 9 12 work study")
                continue

            _, day, start, end, name, type_ = parts[:6]
            add_event(day, start, end, name, type_)

        else:
            print("不明なコマンド")

# ===== 実行 =====
if __name__ == "__main__":
    run()