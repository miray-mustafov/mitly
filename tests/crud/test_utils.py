from src.app.crud.utils import ShortUrlIdGenerator


def test_encode_base62():
    # Test cases: (input, expected)
    test_cases = (
        (0, "0"),
        (1, "1"),
        (10, "a"),
        (61, "Z"),
        (62, "10"),
        (123, "1Z"),
        (98_267_983_555, "1JgmryH")
    )
    for num, expected in test_cases:
        assert ShortUrlIdGenerator._encode_base62(num) == expected


def test_generate_short_url_id():
    # Store initial ID
    initial_id = ShortUrlIdGenerator.ID

    # Generate an ID
    id1 = ShortUrlIdGenerator.generate_short_url_id()
    assert id1 == ShortUrlIdGenerator._encode_base62(initial_id)

    # Generate another ID
    id2 = ShortUrlIdGenerator.generate_short_url_id()
    assert id2 == ShortUrlIdGenerator._encode_base62(initial_id + 1)
    assert id1 != id2
