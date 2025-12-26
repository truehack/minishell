import os
import shutil
import zipfile
import tarfile


def handle(cmd, args, logger):
    try:
        # ZIP 
        if cmd == "zip":
            if len(args) < 2:
                print("Использование: zip <папка> <архив.zip>")
                return

            folder, archive = args[0], args[1]

            if not os.path.exists(folder):
                print("Папка не найдена")
                logger.error(f"zip ERROR: folder not found {folder}")
                return

            archive_name = archive.replace(".zip", "")
            shutil.make_archive(archive_name, "zip", folder)

            print(f"ZIP архив {archive} создан")
            logger.info(f"zip {folder} {archive} OK")

        elif cmd == "unzip":
            if len(args) < 1:
                print("Использование: unzip <архив.zip>")
                return

            archive = args[0]

            if not os.path.exists(archive):
                print("Архив не найден")
                logger.error(f"unzip ERROR: archive not found {archive}")
                return

            with zipfile.ZipFile(archive, "r") as zf:
                zf.extractall()

            print(f"Архив {archive} распакован")
            logger.info(f"unzip {archive} OK")

        # TAR
        elif cmd == "tar":
            if len(args) < 2:
                print("Использование: tar <папка> <архив.tar.gz>")
                return

            folder, archive = args[0], args[1]

            if not os.path.exists(folder):
                print("Папка не найдена")
                logger.error(f"tar ERROR: folder not found {folder}")
                return

            with tarfile.open(archive, "w:gz") as tarf:
                tarf.add(folder, arcname=os.path.basename(folder))

            print(f"TAR архив {archive} создан")
            logger.info(f"tar {folder} {archive} OK")

        elif cmd == "untar":
            if len(args) < 1:
                print("Использование: untar <архив.tar.gz>")
                return

            archive = args[0]

            if not os.path.exists(archive):
                print("Архив не найден")
                logger.error(f"untar ERROR: archive not found {archive}")
                return

            with tarfile.open(archive, "r:gz") as tarf:
                tarf.extractall()

            print(f"Архив {archive} распакован")
            logger.info(f"untar {archive} OK")

        else:
            print("Неизвестная архивная команда")
            logger.error(f"archive unknown command: {cmd}")

    except Exception as e:
        print("Ошибка:", e)
        logger.error(f"{cmd} {' '.join(args)} ERROR: {e}")
