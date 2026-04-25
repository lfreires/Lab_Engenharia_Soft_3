from __future__ import annotations

from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    @abstractmethod
    def begin(self) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
