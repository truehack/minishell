import os
from core.commands import ShellCommands
from plugins.history import add_command, show_history, undo_last
from plugins import archive, grep

def main():
    shell = ShellCommands()
    shell.init() 

    print("Добро пожаловать в MiniShell! Введите 'help' для списка команд.")

    while True:
        try:
            cmd_line = input(f"{os.path.basename(shell.current_dir)}$ ").strip()
            if not cmd_line:
                continue

            add_command(cmd_line)

            parts = cmd_line.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in ("exit", "quit"):
                print("Выход.")
                break
            elif cmd == "help":
                print("Доступные команды: ls, cd, cat, cp, mv, rm, zip, unzip, tar, untar, grep, history, undo, exit")
            elif cmd == "ls":
                shell.ls(args)
            elif cmd == "cd":
                shell.cd(args)
            elif cmd == "cat":
                shell.cat(args)
            elif cmd == "cp":
                shell.cp(args)
            elif cmd == "mv":
                shell.mv(args)
            elif cmd == "rm":
                shell.rm(args)
            elif cmd in ("zip", "unzip", "tar", "untar"):
                archive.handle(cmd, args, shell.logger)
            elif cmd == "grep":
                grep.handle(args, shell.logger)
            elif cmd == "history":
                show_history()
            elif cmd == "undo":
                undo_last()
            else:
                print(f"Неизвестная команда: {cmd}")
        except KeyboardInterrupt:
            print("\nВыход.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
