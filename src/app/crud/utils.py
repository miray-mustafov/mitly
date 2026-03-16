class ShortUrlIdGenerator:
    ENCODING_SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @classmethod
    def _encode_base62(cls, num: int) -> str:  # O(log62(n))
        if num == 0:
            return cls.ENCODING_SYMBOLS[0]

        base = len(cls.ENCODING_SYMBOLS)  # 62
        result = []
        while num > 0:
            num, remainder = divmod(num, base)
            result.append(cls.ENCODING_SYMBOLS[remainder])

        return "".join(reversed(result))

    @classmethod
    def generate_short_url_id(cls, cur_id: int) -> str:
        return cls._encode_base62(cur_id)
