from redis import Redis

from app.config import settings


class RedisHelper:
    def __init__(self) -> None:
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
        )

    def ping(self) -> bool:
        return self.redis.ping()

    def set_data(
        self,
        key: str,
        value: str | float | bool,
        expire_sec: int | None = None,
    ) -> None:
        if isinstance(value, bool):
            value = int(value)

        if expire_sec is None:
            self.redis.set(
                name=key,
                value=value,
            )
        else:
            self.redis.setex(
                name=key,
                time=expire_sec,
                value=value,
            )

    def delete_data(self, key: str) -> None:
        self.redis.delete(key)

    def get_boolean(self, key: str) -> bool | None:
        value = self.redis.get(key)
        if value is not None:
            decoded_value = int(value.decode("utf-8"))
            decoded_value = bool(decoded_value)
        return decoded_value

    def get_data(self, key: str) -> str | None:
        value = self.redis.get(key)
        if value is not None:
            value = value.decode("utf-8")
        return value
