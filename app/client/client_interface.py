from typing import Protocol, Mapping, Any


class Response(Protocol):
    def json(self) -> Any: ...

    def raise_for_status(self) -> None: ...

    @property
    def status_code(self) -> int: ...


class Client(Protocol):
    def get(self, url: str, *, params: Mapping[str, Any] | None = None) -> Response: ...
