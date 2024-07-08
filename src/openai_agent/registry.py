from typing import Generic, TypeVar


__all__ = ['RegistryValue']

T = TypeVar('T')


class RegistryValue(Generic[T]):
    _value: T

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value
