from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def verify_payment(self):
        pass