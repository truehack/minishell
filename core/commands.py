import os
import shutil
from datetime import datetime
from core.logger import logger
from plugins.history import register_undo_action, undo_last, add_command, show_history


def safe_path(path, base_dir):
    full = os.path.abspath(os.path.join(base_dir, path))
    if not full.startswith(os.path.abspath(base_dir)):
        return None
    return full

def parse_args(args, valid_options):
    options, paths = [], []
    for arg in args:
        if arg in valid_options:
            options.append(arg)
        else:
            paths.append(arg)
    return options, paths

class ShellCommands:
    def init(self):
        self.logger = logger
        self.current_dir = os.getcwd()
        self.trash_dir = os.path.join("data", ".trash")
        os.makedirs(self.trash_dir, exist_ok=True)

    # ls
    def ls(self, args):
        options, paths = parse_args(args, ["-l"])
        detailed = "-l" in options
        path = paths[0] if paths else "."
        target = safe_path(path, self.current_dir)
        if not target or not os.path.exists(target):
            print("Нет такого файла или каталога")
            return
        try:
            for entry in os.listdir(target):
                full = os.path.join(target, entry)
                if detailed:
                    stat = os.stat(full)
                    size = stat.st_size
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    mode = oct(stat.st_mode)[-3:]
                    print(f"{entry:30} {size:8} {mtime} {mode}")
                else:
                    print(entry)
            self.logger.info(f"ls {args} OK")
        except Exception as e:
            print("Ошибка:", e)
            self.logger.error(f"ls ERROR: {e}")

    # cd
    def cd(self, args):
        path = args[0] if args else os.path.expanduser("~")
        target = safe_path(path, self.current_dir)
        if not target or not os.path.isdir(target):
            print("Неверный каталог")
            return
        try:
            os.chdir(target)
            self.current_dir = target
            self.logger.info(f"cd {path} OK")
        except Exception as e:
            print("Ошибка:", e)
            self.logger.error(f"cd ERROR: {e}")

    # cat 
    def cat(self, args):
        if not args:
            print("Укажите файл")
            return
        target = safe_path(args[0], self.current_dir)
        if not target or not os.path.isfile(target):
            print("Файл не найден")
            return
        try:
            with open(target, "r", encoding="utf-8") as f:
                print(f.read())
            self.logger.info(f"cat {args[0]} OK")
        except Exception as e:
            print("Ошибка:", e)
            self.logger.error(f"cat ERROR: {e}")

    # cp
    def cp(self, args):
        options, paths = parse_args(args, ["-r"])
        recursive = "-r" in options
        if len(paths) < 2:
            print("Использование: cp [-r] src dst")
            return
        src = safe_path(paths[0], self.current_dir)
        dst = safe_path(paths[1], self.current_dir)
        if not src or not os.path.exists(src):
            print("Источник не найден")
            return
        try:
            if os.path.isdir(src) and recursive:
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            register_for_undo("cp", src, dst)
            self.logger.info(f"cp {src} -> {dst} OK")
        except Exception as e:
            print("Ошибка:", e)
            self.logger.error(f"cp ERROR: {e}")

    #mv 
    def mv(self, args):
        if len(args) < 2:
            print("Использование: mv src dst")
            return
        src = safe_path(args[0], self.current_dir)
        dst = safe_path(args[1], self.current_dir)
        if not src or not os.path.exists(src):
            print("Источник не найден")
            return
        try:
            shutil.move(src, dst)
            register_for_undo("mv", src, dst)
            self.logger.info(f"mv {src} -> {dst} OK")
        except Exception as e:
            print("Ошибка:", e)
            self.logger.error(f"mv ERROR: {e}")

    #  rm 
    def rm(self, args):
        options, paths = parse_args(args, ["-r"])
        recursive = "-r" in options
        if not paths:
            print("Использование: rm [-r] файл")
            return
        target = safe_path(paths[0], self.current_dir)
        if not target or not os.path.exists(target):
            print("Файл или каталог не найден")
            return
        backup = os.path.join(self.trash_dir, os.path.basename(target))
        try:
            if os.path.isdir(target) and recursive:
                shutil.copytree(target, backup, dirs_exist_ok=True)
                shutil.rmtree(target)
            else:
                shutil.copy2(target, backup)
                os.remove(target)
            register_for_undo("rm", target, backup)
            print("Удалено (перемещено в .trash)")
            self.logger.info(f"rm {target} OK")
        except Exception as e:
            print("Ошибка:", e)
            self.logger.error(f"rm ERROR: {e}")
