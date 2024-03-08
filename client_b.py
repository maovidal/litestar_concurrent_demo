import asyncio

from repo import Repo


class ClientB():
    """A process that executes every 4 seconds"""

    def __init__(self, repo: Repo):
        self.shared_repo = repo
        print(f"Client B initialized using repository with current data: {self.shared_repo.current_values()}")
        self._is_active = True

    async def loop(self) -> None:
        """This is the continuous task"""

        while self._is_active:
            got = self.shared_repo.increment_counter_b()
            print(f"B says: {got}")
            # Clears itself after a while
            if got[0] > 6:
                got = self.shared_repo.clear_counter_b()
                print(f"B cleared itself: {got}")
            await asyncio.sleep(4)

    def dispose(self) -> None:
        """To be called when shutting down the app"""

        self._is_active = False
        print("Client B disposed")
