import os
import json
import shutil
from core.logger import logger 

# Пути
DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, ".history")
UNDO_FILE = os.path.join(DATA_DIR, ".undo.json")
TRASH_DIR = os.path.join(DATA_DIR, ".trash")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TRASH_DIR, exist_ok=True)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        pass

if not os.path.exists(UNDO_FILE):
    with open(UNDO_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# История
def add_command(cmd: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(cmd.strip() + "\n")

def show_history(n: int = 15):
    if not os.path.exists(HISTORY_FILE):
        print("История пуста.")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    recent = lines[-n:]
    for i, line in enumerate(recent, start=len(lines) - len(recent) + 1):
        print(f"{i:3}: {line.strip()}")

# Undo
def register_undo_action(action: str, src: str, dst: str = None):
    record = {"action": action, "src": src, "dst": dst}
    with open(UNDO_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

def undo_last():
    if not os.path.exists(UNDO_FILE):
        print("Нет действий для отмены.")
        return
    try:
        with open(UNDO_FILE, "r", encoding="utf-8") as f:
            rec = json.load(f)
        action = rec.get("action")
        src = rec.get("src")
        dst = rec.get("dst")
        if not action:
            print("Файл undo повреждён.")
            return

        success = False
        msg = ""

        if action == "rm":
            if dst and os.path.exists(dst):
                restore_to = src
                if os.path.exists(restore_to):
                    restore_to += "_restored"
                shutil.move(dst, restore_to)
                msg = f"Файл восстановлен: {restore_to}"
                success = True
            else:
                msg = "Файл не найден в корзине."

        elif action == "mv":
            if dst and os.path.exists(dst):
                shutil.move(dst, src)
                msg = f"Отменено перемещение: {dst} → {src}"
                success = True
            else:
                msg = "Целевой файл не существует — нечего отменять."

        elif action == "cp":
            if dst and os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
                msg = f"Копия удалена: {dst}"
                success = True
            else:
                msg = "Копия уже удалена."

        else:
            msg = f"Отмена не поддерживается для: {action}"

        if os.path.exists(UNDO_FILE):
            os.remove(UNDO_FILE)

        if success:
            print(msg)
            logger.info(f"undo {action} OK → {msg}")
        else:
            print(f"Ошибка undo: {msg}")
            logger.error(f"undo FAILED: {msg}")

    except Exception as e:
        print(f"Критическая ошибка при undo: {e}")
        logger.error(f"undo EXCEPTION: {e}")
        if os.path.exists(UNDO_FILE):
            os.remove(UNDO_FILE)


