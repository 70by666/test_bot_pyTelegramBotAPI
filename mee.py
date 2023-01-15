import os
import shutil


def delete1():
    v_list = os.listdir("C:/Users/70by666/Desktop/4/bot_1/data/")
    for i in v_list:
        dir_path = f"C:/Users/70by666/Desktop/4/bot_1/data/{i}"
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Ошибка: %s : %s" % (dir_path, e.strerror))
