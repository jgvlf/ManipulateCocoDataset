import os.path

FROM_JSON_FILE: str = "instances_train2017.json"
TO_JSON_FILE: str = "instances_val2017.json"
FROM_IMG_FOLDER: str = "train2017"
TO_IMG_FOLDER: str = "val2017"


def move_images(choose_object: list[dict]):
    from_image_folder: str = os.path.abspath(f"./datasets_images/{FROM_IMG_FOLDER}")
    to_image_folder: str = os.path.abspath(f"./datasets_images/{TO_IMG_FOLDER}")
    for obj in choose_object:
        if os.path.exists(f"{from_image_folder}/{obj["file_name"]}"):
            os.replace(f"{from_image_folder}/{obj["file_name"]}", f"{to_image_folder}/{obj["file_name"]}")


def change_object(ff: str, tf: str, choose_object: list[dict], indexes: list[int]):
    import json

    with open(ff, 'r+') as ff:
        from_file = json.load(ff)
        from_img_list: list[dict] = from_file["images"]
        from_ann_list: list[dict] = from_file["annotations"]
        for i in indexes:
            del from_img_list[i]
            del from_ann_list[i]
            ff.seek(0)
        json.dump(from_file, ff, indent=3)
        ff.truncate()
        ff.close()
    with open(tf, 'r+') as tf:
        to_file = json.load(tf)
        to_file_img_list: list[dict] = to_file["images"]
        to_file_ann_list: list[dict] = to_file["annotations"]
        for obj in choose_object:
            to_file_img_list.append(obj["object_img"])
            to_file_ann_list.append(obj["object_bbox"])
            tf.seek(0)
        json.dump(to_file, tf, indent=3)
        tf.truncate()


def get_files(json_file: dict, indexes: list[int]) -> list[dict]:
    import os
    import datetime

    now: datetime = datetime.datetime.now()
    date = now.strftime("(%d-%m-%Y)_(%H-%M-%S)")
    img_data: list[dict] = list()
    if not os.path.exists("./choose_files/"):
        os.makedirs("./choose_files/")
    for i in indexes:
        with open(f"./choose_files/files-{date}", "a") as f:
            f.write(f"{str(json_file["images"][i])}\n")
        img_data.append({"object_img": json_file["images"][i],
                         "file_name": json_file["images"][i]["file_name"], "object_bbox": json_file["annotations"][i]})
    return img_data


def generate_rand_numbers(qtd: int, size: int) -> list[int]:
    from random import randint
    generated_nums: list[int] = list()
    final_nums: list[int] = list()
    while len(final_nums) < qtd:
        rand_num: int = randint(0, size-1)
        generated_nums.append(rand_num)
        final_nums.append(rand_num) if generated_nums.count(rand_num) == 1 else None
    return final_nums


def load_json(file: str) -> dict:
    import json
    with open(file) as f:
        data: dict = json.load(f)
    return data


def main() -> None:
    ff: str = f"from_file/{FROM_JSON_FILE}"
    tf: str = f"to_file/{TO_JSON_FILE}"
    train_json: dict = load_json(ff)
    indexes: list[int] = generate_rand_numbers(5, len(train_json["images"]))
    data_object: list[dict] = get_files(train_json, indexes)
    change_object(ff, tf, get_files(train_json, indexes), indexes)
    move_images(data_object)


if __name__ == '__main__':
    main()
