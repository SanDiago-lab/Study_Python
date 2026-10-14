import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import json
import csv
from pathlib import Path

JSON_FILE = Path(__file__).parent / "collection.json"

DOWNLOADS_DIR = Path.home() / "Downloads"
UNTAPPED_JSON_FILE = DOWNLOADS_DIR / "untapped_collection.json"


def save_collection():
    # 現在時刻を取得
    sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # CLを取得
    cl = cl_entry.get()

    # 現在のcollection.jsonを読み込む
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            collection_data = json.load(file)
    except FileNotFoundError:
        collection_data = {}

    # CLと同期日時だけ更新
    collection_data["collection_level"] = cl
    collection_data["last_sync"] = sync_time

    # JSONファイルに保存
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(
            collection_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    # 画面を更新
    sync_label.config(text=f"最終同期: {sync_time}")
    status_label.config(
        text=f"CL: {cl} / "
             f"カード数: {len(collection_data.get('cards', []))}枚"
    )


def load_collection():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            collection_data = json.load(file)

        cl = collection_data.get(
            "collection_level",
            ""
        )

        sync_time = collection_data.get(
            "last_sync",
            "--"
        )

        cards = collection_data.get(
            "cards",
            []
        )

        # CLを入力欄に表示
        cl_entry.delete(0, tk.END)
        cl_entry.insert(0, cl)

        # 同期日時を表示
        sync_label.config(
            text=f"最終同期: {sync_time}"
        )

        # CLとカード数を表示
        status_label.config(
            text=f"CL: {cl or '--'} / "
                 f"カード数: {len(cards)}枚"
        )

        # =========================
        # 最新同期の新規カードを表示
        # =========================

        sync_history = collection_data.get(
            "sync_history",
            []
        )

        if sync_history:
            latest_sync = sync_history[-1]

            added_cards = latest_sync.get(
                "added_cards",
                []
            )

            display_new_cards(added_cards)

    except FileNotFoundError:
        # collection.jsonがまだ存在しない場合
        pass

    except json.JSONDecodeError:
        status_label.config(
            text="collection.jsonの形式が不正です"
        )


def display_new_cards(added_cards):
    """
    新規取得カードをGUIに表示する
    """

    # 表示欄を一度クリア
    new_cards_text.delete("1.0", tk.END)

    if not added_cards:
        new_cards_text.insert(
            tk.END,
            "前回同期で新しく獲得したカードはありません。"
        )
        return

    # タイトル
    new_cards_text.insert(
        tk.END,
        f"★ 新しく獲得したカード（{len(added_cards)}枚）\n\n"
    )

    # カード名を1行ずつ表示
    for card_name in added_cards:
        new_cards_text.insert(
            tk.END,
            f"★ {card_name}\n"
        )


def import_untapped():
    # Untapped JSONの場所
    file_path = UNTAPPED_JSON_FILE

    # JSONが存在するか確認
    if not file_path.exists():
        status_label.config(
            text="Untapped JSONがDownloadsにありません"
        )
        return

    try:
        # Untapped JSONを読み込む
        with open(file_path, "r", encoding="utf-8") as file:
            untapped_data = json.load(file)

        cards = untapped_data.get("cards", [])

        # 現在のcollection.jsonを読み込む
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                collection_data = json.load(file)
        except FileNotFoundError:
            collection_data = {}

        # =========================
        # 前回のカード情報を取得
        # =========================

        old_cards = collection_data.get(
            "cards",
            []
        )

        # 前回のカード名だけをセットにする
        old_names = {
            card.get("name")
            for card in old_cards
            if card.get("name")
        }

        # 今回のカード名
        new_names = {
            card.get("name")
            for card in cards
            if card.get("name")
        }

        # 新しく追加されたカード
        added_cards = sorted(
            new_names - old_names
        )

        # カード数
        old_count = len(old_cards)
        new_count = len(cards)

        # 増加枚数
        difference = new_count - old_count

        # =========================
        # 同期日時
        # =========================

        sync_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # =========================
        # カード情報を更新
        # =========================

        collection_data["cards"] = cards

        # 同期日時を更新
        collection_data["last_sync"] = sync_time

        # =========================
        # 同期履歴
        # =========================

        sync_history = collection_data.get(
            "sync_history",
            []
        )

        sync_record = {
            "sync_time": sync_time,
            "collection_level": collection_data.get(
                "collection_level",
                "--"
            ),
            "card_count": new_count,
            "added": difference,
            "added_cards": added_cards
        }

        sync_history.append(sync_record)

        collection_data["sync_history"] = sync_history

        # =========================
        # collection.jsonに保存
        # =========================

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(
                collection_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        # =========================
        # 画面を更新
        # =========================

        sync_label.config(
            text=f"最終同期: {sync_time}"
        )

        status_label.config(
            text=f"CL: {collection_data.get('collection_level', '--')} / "
                 f"カード数: {new_count}枚 / "
                 f"+{difference}枚"
        )

        # 新規カードを表示
        display_new_cards(added_cards)

    except json.JSONDecodeError:
        status_label.config(
            text="Untapped JSONの形式が不正です"
        )


def export_csv():
    try:
        # collection.jsonを読み込む
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            collection_data = json.load(file)

        cards = collection_data.get("cards", [])

        if not cards:
            status_label.config(text="カード情報がありません。")
            return

        # CLと同期日時を取得
        collection_level = collection_data.get(
            "collection_level",
            "--"
        )

        last_sync = collection_data.get(
            "last_sync",
            "--"
        )

        # 保存先を選択
        file_path = filedialog.asksaveasfilename(
            title="CSVを保存",
            defaultextension=".csv",
            initialfile=f"marvel_snap_collection_CL{collection_level}.csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        # キャンセルされた場合
        if not file_path:
            return

        # CSVに書き込む
        with open(
            file_path,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            writer = csv.writer(file)

            # メタデータ
            writer.writerow([
                f"# Collection Level: {collection_level}"
            ])

            writer.writerow([
                f"# Last Sync: {last_sync}"
            ])

            # 空行
            writer.writerow([])

            # ヘッダー
            writer.writerow([
                "名前",
                "コスト",
                "パワー"
            ])

            # カード情報
            for card in cards:
                writer.writerow([
                    card.get("name", ""),
                    card.get("cost", ""),
                    card.get("power", "")
                ])

        status_label.config(
            text=f"CSV出力完了: {len(cards)}枚 / CL: {collection_level}"
        )

    except FileNotFoundError:
        status_label.config(
            text="collection.jsonが見つかりません"
        )

    except json.JSONDecodeError:
        status_label.config(
            text="collection.jsonの形式が不正です"
        )


# =========================
# ウィンドウ
# =========================

window = tk.Tk()
window.title("Marvel Snap Collection Manager")
window.geometry("450x500")


# =========================
# タイトル
# =========================

title_label = ttk.Label(
    window,
    text="Marvel Snap Collection Manager",
    font=("Helvetica", 18)
)
title_label.pack(pady=(30, 25))


# =========================
# CL
# =========================

cl_frame = ttk.Frame(window)
cl_frame.pack(pady=10)

cl_label = ttk.Label(
    cl_frame,
    text="Collection Level:"
)
cl_label.pack(side="left", padx=5)

cl_entry = ttk.Entry(
    cl_frame,
    width=10
)
cl_entry.pack(side="left", padx=5)


# =========================
# 同期日時
# =========================

sync_label = ttk.Label(
    window,
    text="最終同期: --"
)
sync_label.pack(pady=15)


# =========================
# 状態
# =========================

status_label = ttk.Label(
    window,
    text="CL: --"
)
status_label.pack(pady=5)


# =========================
# 新規カード表示
# =========================

new_cards_label = ttk.Label(
    window,
    text="前回同期で新しく獲得したカード"
)
new_cards_label.pack(pady=(15, 5))

new_cards_text = tk.Text(
    window,
    height=8,
    width=45
)
new_cards_text.pack(pady=5)

new_cards_text.config(
    state="normal"
)


# =========================
# 同期ボタン
# =========================

sync_button = ttk.Button(
    window,
    text="同期状態を保存",
    command=save_collection
)
sync_button.pack(pady=10)


import_button = ttk.Button(
    window,
    text="Untappedから同期",
    command=import_untapped
)
import_button.pack(pady=5)


export_button = ttk.Button(
    window,
    text="CSVを書き出す",
    command=export_csv
)
export_button.pack(pady=5)


# =========================
# 保存済みデータを読み込む
# =========================

load_collection()


# =========================
# アプリ起動
# =========================

window.mainloop()