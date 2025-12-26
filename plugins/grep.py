import os
import re


def handle(args, logger):
    if len(args) < 2:
        print("Использование: grep <шаблон> <путь> [-r] [-i]")
        return

    pattern = args[0]
    path = args[1]

    recursive = "-r" in args
    ignore_case = "-i" in args
    flags = re.IGNORECASE if ignore_case else 0

    if not os.path.exists(path):
        print("Указанный путь не найден")
        logger.error(f"grep ERROR: path not found {path}")
        return

    def search_in_file(file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    if re.search(pattern, line, flags):
                        print(f"{file_path}:{line_num}: {line.strip()}")
        except Exception:
            pass

    try:
        if os.path.isfile(path):
            search_in_file(path)

        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    search_in_file(full_path)

                if not recursive:
                    break

        logger.info(f"grep {pattern} {path} OK")

    except Exception as e:
        print("Ошибка:", e)
        logger.error(f"grep {pattern} {path} ERROR: {e}")
