import os
import time
import json
import requests
import youtube_dl
from langdetect import detect


def get_wall_posts(name):
    global a

    if not detect(name) == "ru":
        group_name = name
        url = f"https://api.vk.com/method/wall.get?domain={group_name}"
               "&count=100&access_token={vk_api}&v=5.131"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        src = response.json()
        # проверка на повторы
        if os.path.exists(f"{group_name}"):
            print(f"{group_name} такая существует, начинаем обрабатывать посты")
        else:
            os.mkdir(group_name)
        if os.path.exists(
                "data/cats") or os.path.exists("data/video") or os.path.exists("data/memi"):
            print("папки существуют")
        else:
            os.mkdir("data/cats")
            os.mkdir("data/video")
            os.mkdir("data/memi")
        # сохраняем данные в json
        with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file_:
            json.dump(src, file_, indent=5, ensure_ascii=False)
        # собираем ид новых постов
        # fresh_posts_id = []
        posts = src["response"]["items"]
        # проверка на повторные посты, потом доделаю
        '''
        for i in posts:
            i = i["id"]
            fresh_posts_id.append(i)
            '''
        try:
            if not os.path.exists(
                    f"{group_name}/exists_posts_{group_name}.txt"):
                with open(f"{group_name}/exists_posts_{group_name}.txt", "w") as file_:
                    pass
            # извлекаем данные из списка
            for i in posts:
                post_id = i["id"]
                print(f"пост {post_id}")
                try:
                    # проверка на наличие attachments в посте
                    if "attachments" in i:
                        i = i["attachments"]
                        # забираем картинки
                        if i[0]["type"] == "photo":
                            if len(i) == 1:
                                url_img = i[0]["photo"]["sizes"][-1]["url"]
                                a = "data/memi/"
                                download(url_img)
                                print(f"{post_id} загружен через функцию 1")
                            else:
                                for i_ in i:
                                    url_img_2 = i_["photo"]["sizes"][-1]["url"]
                                    a = "data/cats/"
                                    download(url_img_2)
                                    print(
                                        f"{post_id} загружен через функцию 2")
                        # забираем видео и создание ссылки для видео
                        elif i[0]["type"] == "video":
                            if len(i) == 1:
                                print(f"{post_id} video")
                                vak = i[0]["video"]["access_key"]
                                vpi = i[0]["video"]["id"]
                                voi = i[0]["video"]["owner_id"]
                                time.sleep(3)
                                get_url_video = f"https://api.vk.com/method/video.get?videos="
                                                 "{voi}_{vpi}_{vak}&access_token={vk_api}&v=5.131 "
                                response = requests.get(get_url_video)
                                res = response.json()
                                url_video = res["response"]["items"][0]["player"]
                                a = "data/video/"
                                download(url_video)
                                print(f"{post_id} загружен через функцию 4")
                            else:
                                print(f"{post_id} video")
                                vak = i["video"]["access_key"]
                                vpi = i["video"]["id"]
                                voi = i["video"]["owner_id"]
                                time.sleep(3)
                                get_url_video = f"https://api.vk.com/method/video.get?videos={voi}_{vpi}_{vak}\
                                &access_token={vk_api}&v=5.131 "
                                response = requests.get(get_url_video)
                                res = response.json()
                                url_video = res["response"]["items"][0]["player"]
                                a = "data/video/"
                                download(url_video)
                                print(f"{post_id} загружен через функцию 4")
                        else:
                            print(
                                f"пост {post_id} не попал под нужные условия, скачен не был")
                except Exception:
                    print(f"ошибка с постом {post_id}")
            return "загрузка завершена"
            # else:
            #    return "добавились новые элементы к существующим пабликам"
        except Exception:
            return "кто сюда пишет команду?"
            '''
            #with open(f"{group_name}/exists_posts_{group_name}.txt", "a+") as file_:
            #    r = file_.read()
            #    for i in fresh_posts_id:
            #        for y in r:
            #            if i != y:
            #                file_.write(str(i) + "\n")
            '''
        # удаление папки
        '''
        dir_path = f"C:/Users/70by666/Desktop/4/bot_1/{group_name}"
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Ошибка: %s : %s" % (dir_path, e.strerror))
        '''
    else:
        return "кто блять пишет такое на русском"


def download(url):
    if a == "video/":
        try:
            name = a + url.split("/")[-1].split("&")[1].split("=")[1] + ".mp4"
            ydl_op = {"outtmpl": name}
            with youtube_dl.YoutubeDL(ydl_op) as ydl:
                video_info = ydl.extract_info(url, download=False)
                video_duration = video_info["duration"]
                if video_duration > 60:
                    print("видео больше 1 минуты")
                else:
                    print(f"длина {video_duration}")
                    ydl.download([url])
        except Exception:
            (print("не удалось скачать"))
    else:
        name = a + url.split("/")[-1].split("?")[-2]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
        response = requests.get(url, headers, stream=True)
        with open("C:/Users/70by666/Desktop/4/bot_1/" + name, "wb") as r:
            for v in response.iter_content(1024 * 1024):
                r.write(v)
