""" ----------------------------------------------------------------------------
Shared data repository
---------------------------------------------------------------------------- """

class Repo:
    """
    Shared data repository.
    Methods are used to prevent data inconsistency during updates.
    """
    def __init__(self, creator: str):
        self.creator = creator
        self._counter_a: int = 0
        self._counter_b: int = 0
        print(f"Data repository initialized by {creator}")

    def current_values(self) -> (int, int):
        """
        Returns the current values.
        """
        return (self._counter_a, self._counter_b)

    def increment_counter_a(self) -> (int, int):
        """
        Add 1 to the value of counter A
        """
        self._counter_a = self._counter_a + 1
        return self.current_values()

    def increment_counter_b(self) -> (int, int):
        """
        Add 1 to the value of counter B
        """
        self._counter_b = self._counter_b + 1
        return self.current_values()

    def clear_counter_a(self) -> (int, int):
        """
        Set 0 to the value of counter A
        """
        self._counter_a = 0
        return self.current_values()

    def clear_counter_b(self) -> (int, int):
        """
        Set 0 to the value of counter B
        """
        self._counter_b = 0
        return self.current_values()
