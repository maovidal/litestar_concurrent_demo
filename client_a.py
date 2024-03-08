import asyncio

from repo import Repo


class ClientA():
    """A process that executes every 2 seconds"""

    def __init__(self, repo: Repo):
        self.shared_repo = repo
        print(f"Client A initialized using repository with current data: {self.shared_repo.current_values()}")
        self._is_active = True

    async def loop(self) -> None:
        """This is the continuous task"""

        while self._is_active:
            got = self.shared_repo.increment_counter_a()
            print(f"A says: {got}")
            # Clears itself after a while
            if got[0] > 8:
                got = self.shared_repo.clear_counter_a()
                print(f"A cleared itself: {got}")
            await asyncio.sleep(2)

    def dispose(self) -> None:
        """To be called when shutting down the app"""

        self._is_active = False
        print("Client A disposed")
