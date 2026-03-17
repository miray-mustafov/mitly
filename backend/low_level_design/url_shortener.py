from datetime import datetime, timedelta
import re
import threading


class ShortUrl:
    ID = 987_267_983_555  # starting from a large number to test the encoding algorithm
    _ID_LOCK = threading.Lock()
    EXPIRATION_DAYS = 30
    ORIGINAL_URL_REGEX = r"^https?://[^\s/$.?#].[^\s]*$"
    DOMAIN = 'mit.ly'
    ENCODING_SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, original_url, expiration_days=EXPIRATION_DAYS):
        self._original_url = self._validate_original_url(original_url)
        self._creation_datetime = datetime.now()
        self._expiration_datetime = (
                self.creation_datetime +
                timedelta(days=self._validate_expiration_days(expiration_days))
        )
        # Thread Safety ❌
        # In real-world multi-threaded where users create urls concurrently, same id may be read at the same time.
        # self._base62_id = self._encode_base62(self.ID)
        # ShortUrl.ID += 1

        # Thread Safety ✅
        with ShortUrl._ID_LOCK:
            self._base62_id = self._encode_base62(self.ID)
            ShortUrl.ID += 1

    @property
    def original_url(self):  # make it read only to avoid accidental modification
        return self._original_url

    @property
    def base62_id(self):
        return self._base62_id

    @property
    def creation_datetime(self):
        return self._creation_datetime

    @property
    def expiration_datetime(self):
        return self._expiration_datetime

    @staticmethod
    def _validate_original_url(original_url):
        if not re.match(ShortUrl.ORIGINAL_URL_REGEX, original_url):
            raise ValueError("Invalid URL. Correct format: https://www.example.com")
        return original_url

    @staticmethod
    def _validate_expiration_days(expiration_days):
        if not 1 <= expiration_days <= 365:
            raise ValueError("Expiration days must be in the range 1-365")
        return expiration_days

    @classmethod
    def _encode_base62(cls, num: int) -> str:
        """
        The core algorithm used in URL shorteners like Bitly.
        Converts a base-10 integer into a base62 string. The result is reversed
        to ensure the most significant digits appear first (e.g., if num=123 then 3 would contribute
        the smallest change to value 123 so its base62 representation should be placed last).

        Runtime: O(log62(n))
        Memory: O(log62(n))
        """

        if num == 0:
            return cls.ENCODING_SYMBOLS[0]

        base = len(cls.ENCODING_SYMBOLS)
        result = []
        while num > 0:
            num, remainder = divmod(num, base)
            result.append(cls.ENCODING_SYMBOLS[remainder])

        return "".join(reversed(result))

    def get_short_url(self):
        short_url = f"https://{self.DOMAIN}/{self._base62_id}"
        return short_url

    def __str__(self):
        return f"<ShortURL: {self.get_short_url()}>"

    def __repr__(self):
        return self.__str__()


class UrlShortener:
    def __init__(self, short_url_class):
        self.short_url_class = short_url_class  # composition used so that we can use different short url classes
        self.short_urls = {}

    def get_short_url_obj(self, original_url, expiration_days=None):
        """
        Custom alias skipped because may break the uniqueness that is already guaranteed by the url class
        """
        short_url_obj = self.short_url_class(original_url, expiration_days)
        self.short_urls[short_url_obj.base62_id] = short_url_obj
        return short_url_obj

    def redirect(self, short_url):
        cur_id = short_url.split("/")[-1]
        if cur_id not in self.short_urls:
            return "No such short URL"
        return self.short_urls[cur_id].original_url


# url1 = ShortUrl("https://www.google.com", 35)
# url2 = ShortUrl("https://www.google.com", 35)
# url3 = ShortUrl("https://www.google.com", 35)
# print(url1.get_short_url())
# print(url2.get_short_url())
# print(url3.get_short_url())

app = UrlShortener(ShortUrl)
url_1 = app.get_short_url_obj("https://www.linkedin.com/in/miray-mustafov/", 35)
short_url = url_1.get_short_url()
print(url_1)
print(short_url)
print(app.redirect(short_url))
