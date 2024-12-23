import os
import requests
import random
from minio import Minio
from minio.error import S3Error
from io import BytesIO

minio_client = Minio(
    os.environ['MINIO_ENDPOINT'],
    access_key=os.environ['MINIO_ACCESS_KEY'],
    secret_key=os.environ['MINIO_SECRET_KEY'],
    secure=False
)


def create_bucket(bucket_name):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)


# Получение случайного изображения котика из The Cat API
def get_random_cat_image():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        cat_image_url = response.json()[0]['url']
        return cat_image_url
    else:
        print("Ошибка при получении изображения котика")
        return None


# Загрузка изображения котика в MinIO
def upload_cat_image(bucket_name, cat_image_url):
    cat_image_data = requests.get(cat_image_url).content
    cat_image_name = f"cat_{random.randint(1, 10000)}.jpg"
    cat_image_file = BytesIO(cat_image_data)
    res = True
    try:
        cat_image_file.seek(0)
        minio_client.put_object(bucket_name, cat_image_name, cat_image_file, len(cat_image_data))
        print(f"Загружена картинка {cat_image_name} в MinIO.")
    except S3Error as err:
        print(f"Ошибка при загрузке изображения: {err}")
        res = False
    finally:
        cat_image_file.close()
    return res


def mass_uploading(bucket_name):
    uploading = True
    while uploading:
        cat_image_url = get_random_cat_image()
        if cat_image_url:
            uploading = upload_cat_image(bucket_name, cat_image_url)


def main():
    bucket_cats = "cats"
    bucket_extra = "extra"

    create_bucket("cats")
    create_bucket("extra")

    mass_uploading(bucket_cats)
    print("Превышен размер бакета cats")

    mass_uploading(bucket_extra)
    print("Превышен общий размер хранилища")


if __name__ == "__main__":
    main()
