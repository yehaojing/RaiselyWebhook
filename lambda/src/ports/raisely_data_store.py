from abc import ABC, abstractmethod


class RaiselyDataStore(ABC):
    @abstractmethod
    def intialise(self) -> None:
        raise NotImplementedError
