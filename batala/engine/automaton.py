from abc import ABC, abstractmethod


class HybridAutomaton(ABC):
    @abstractmethod
    def discrete_step(self):
        raise NotImplemented

    @abstractmethod
    def continuous_step(self, delta_time):
        raise NotImplemented
