import os
import shutil


def delete1():
    v_list = os.listdir("data/")
    for i in v_list:
        dir_path = f"data/{i}"
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Ошибка: %s : %s" % (dir_path, e.strerror))
