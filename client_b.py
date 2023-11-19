import asyncio

from repo import Repo

class ClientB():
    """A process that executes every 4 seconds"""

    def __init__(self, repo: Repo):
        self.shared_repo = repo
        print(f"Client B initialized with repository created by: {self.shared_repo.creator} with current data: {self.shared_repo.current_values()}")

    async def loop(self):
        """This is the continuos task"""

        while True:
            got = self.shared_repo.increment_counter_b()
            print(f"B says: {got}")
            # Clears itself after a while
            if got[1] > 6:
                got = self.shared_repo.clear_counter_b()
                print(f"B cleared itself: {got}")
            await asyncio.sleep(4)

    async def dispose(self):
        """To be called when shutting down the app"""

        del self
        print("Client B disposed")
