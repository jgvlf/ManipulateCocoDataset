import os.path

FROM_JSON_FILE: str = "instances_train2017.json"
TO_JSON_FILE: str = "instances_val2017.json"
FROM_IMG_FOLDER: str = "train2017"
TO_IMG_FOLDER: str = "val2017"


def move_images(choose_object: list[dict]):
    from_image_folder: str = os.path.abspath(f"./COCO/{FROM_IMG_FOLDER}")
    to_image_folder: str = os.path.abspath(f"./COCO/{TO_IMG_FOLDER}")
    for obj in choose_object:
        if os.path.exists(f"{from_image_folder}/{obj["file_name"]}"):
            os.replace(f"{from_image_folder}/{obj["file_name"]}", f"{to_image_folder}/{obj["file_name"]}")


def change_object(ff: str, tf: str, choose_object: list[dict], indexes: list[int]):
    import json

    with open(ff, 'r+') as ff:
        from_file = json.load(ff)
        from_img_list: list[dict] = from_file["images"]
        from_ann_list: list[dict] = from_file["annotations"]
        rewrite_index_img: int = 0
        rewrite_index_ann: int = 0
        for i in indexes:
            del from_img_list[i]
            del from_ann_list[i]
            ff.seek(0)
        for file_img in from_img_list:
            file_img["id"] = rewrite_index_img
            rewrite_index_img += 1
            ff.seek(0)
        for file_ann in from_ann_list:
            file_ann["id"] = rewrite_index_ann
            rewrite_index_ann += 1
            ff.seek(0)
        json.dump(from_file, ff, indent=3)
        ff.truncate()
        ff.close()
    rewrite_index_img = 0
    rewrite_index_ann = 0
    with open(tf, 'r+') as tf:
        to_file = json.load(tf)
        to_file_img_list: list[dict] = to_file["images"]
        to_file_ann_list: list[dict] = to_file["annotations"]
        last_img_id: int = to_file_img_list[len(to_file_img_list) - 1]["id"]
        last_ann_id: int = to_file_ann_list[len(to_file_ann_list) - 1]["id"]
        for file_img in to_file_img_list:
            file_img["id"] = rewrite_index_img
            rewrite_index_img += 1
            tf.seek(0)
        for file_ann in to_file_ann_list:
            file_ann["id"] = rewrite_index_ann
            rewrite_index_ann += 1
            tf.seek(0)
        for obj in choose_object:
            last_img_id += 1
            last_ann_id += 1
            obj["object_img"]["id"] = last_img_id
            obj["object_bbox"]["id"] = last_ann_id
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
    img_id: list[int] = list()
    new_ids: list[int] = list()
    if not os.path.exists("./choose_files/"):
        os.makedirs("./choose_files/")
    for img_list_id in json_file["annotations"]:
        img_id.append(img_list_id["image_id"])
    for i in indexes:
        if img_id.count(i) > 1:
            for ff in json_file["annotations"]:
                if ff["image_id"] == i:
                    new_ids.append(ff["id"])
        break
    for ids in new_ids:
        indexes.append(ids)
        indexes.sort(reverse=True)
    for i in indexes:
        with open(f"./choose_files/files-{date}.txt", "a") as f:
            f.write(f"{str(json_file["images"][i])}\n")
        img_data.append({"object_img": json_file["images"][i],
                         "file_name": json_file["images"][i]["file_name"], "object_bbox": json_file["annotations"][i]})
    return img_data


def generate_rand_numbers(qtd: int, size: int) -> list[int]:
    from random import randint
    import json

    generated_nums: list[int] = list()
    final_nums: list[int] = list()
    while len(final_nums) < qtd:
        rand_num: int = randint(0, size-1)
        generated_nums.append(rand_num)
        final_nums.append(rand_num) if generated_nums.count(rand_num) == 1 else None
    final_nums.sort(reverse=True)
    return final_nums


def load_json(file: str) -> dict:
    import json
    with open(file) as f:
        data: dict = json.load(f)
    return data


def main() -> None:
    ff: str = os.path.abspath(f"./COCO/annotations/{FROM_JSON_FILE}")
    tf: str = os.path.abspath(f"./COCO/annotations/{TO_JSON_FILE}")
    train_json: dict = load_json(ff)
    indexes: list[int] = generate_rand_numbers(540, len(train_json["images"]))
    data_object: list[dict] = get_files(train_json, indexes)
    change_object(ff, tf, data_object, indexes)
    move_images(data_object)


if __name__ == '__main__':
    main()
