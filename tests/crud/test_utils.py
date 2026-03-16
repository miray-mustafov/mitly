from src.app.crud.utils import ShortUrlIdGenerator


def test_generate_short_url_id_following_the_base62_encoding():
    test_cases = (  # (input, expected)
        (0, "0"),
        (1, "1"),
        (10, "a"),
        (61, "Z"),
        (62, "10"),
        (123, "1Z"),
        (98_267_983_555, "1JgmryH")
    )
    for num, expected in test_cases:
        assert ShortUrlIdGenerator.generate_short_url_id(num) == expected
