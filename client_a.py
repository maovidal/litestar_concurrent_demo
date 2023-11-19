import asyncio

from repo import Repo

class ClientA():
    """A process that executes every 2 seconds"""

    def __init__(self, repo: Repo):
        self.shared_repo = repo
        print(f"Client A initialized with repository created by: {self.shared_repo.creator} with current data: {self.shared_repo.current_values()}")

    async def loop(self):
        """This is the continuos task"""

        while True:
            got = self.shared_repo.increment_counter_a()
            print(f"A says: {got}")
            # Clears itself after a while
            if got[0] > 8:
                got = self.shared_repo.clear_counter_a()
                print(f"A cleared itself: {got}")
            await asyncio.sleep(2)

    async def dispose(self):
        """To be called when shutting down the app"""

        del self
        print("Client A disposed")
