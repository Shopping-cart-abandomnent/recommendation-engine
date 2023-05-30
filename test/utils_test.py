from src.utils import get_image_path


def test_get_public_url():
    products_id = 448831026
    public_urls = get_image_path(products_id)
    assert public_urls == "https://storage.googleapis.com/bucket_hm/articles_image/044/0448831026.jpg"
