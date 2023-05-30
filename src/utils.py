def get_image_path(article_id):
    bucket_name = 'bucket_hm'
    base_folder = 'articles_image'
    article_id_str = str(article_id)
    folder_path = article_id_str[:3]
    image_filename = article_id_str + '.jpg'
    image_path = f'{base_folder}/{folder_path}/{image_filename}'
    image_public_url = f"https://storage.googleapis.com/{bucket_name}/{image_path}"
    return image_public_url
