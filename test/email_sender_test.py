from src.email_sender import generate_template


def test_generate_template():
    user = {"firstname": "Paul", "lastname": "Laroche"}
    products = [
        {"name": "Chaussette Superman", "url": "http://this_is_product1_url.com"},
        {"name": "T-Shirt", "url": "http://this_is_product2_url.com"}
    ]
    path = "test/template/email_template.html"
    templated_body = generate_template(path, user, products)
    assert "<h1>Bonjour Paul Laroche,</h1>" in templated_body
    assert "<span>Chaussette Superman</span>" in templated_body
    assert '<img src="http://this_is_product1_url.com" />' in templated_body





