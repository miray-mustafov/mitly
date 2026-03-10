import threading


class ShortUrlIdGenerator:
    _ID_LOCK = threading.Lock()
    ID = 98_267_983_555
    ENCODING_SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @classmethod
    def _encode_base62(cls, num: int) -> str:
        if num == 0:
            return cls.ENCODING_SYMBOLS[0]

        base = len(cls.ENCODING_SYMBOLS)
        result = []
        while num > 0:
            num, remainder = divmod(num, base)
            result.append(cls.ENCODING_SYMBOLS[remainder])

        return "".join(reversed(result))

    @classmethod
    def generate_short_url_id(cls) -> str:
        # In the real-world where users create urls concurrently, the same id may be read at the same time.
        with cls._ID_LOCK:  # Thread Safety ✅
            short_id = cls._encode_base62(cls.ID)
            cls.ID += 1
        return short_id
