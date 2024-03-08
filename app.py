"""
After feedback from @provinzkraut
24-03-08

Objective: Implement an efficient app with two clients and Litestar running
concurrently. All of them should be able to retrieve and store information in
the same shared object.
"""

import logging

import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

# Repo is the intended shared data repository
from repo import Repo

# Two clients, that access the shared data repository at different rates
from client_a import ClientA
from client_b import ClientB

import uvicorn
from litestar import Litestar, get, put
from litestar.datastructures import State


logger = logging.getLogger(__name__)


@asynccontextmanager
async def manage_client_lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    """
    Runs instances of the Clients A and B
    """
    # Set an instance of the Shared Repository if it does not exists already
    repo = getattr(app.state, "repo", None)
    if repo is None:
        app.state.repo = Repo()

    # Set instances of the Clients with access to the Shared Repository
    client_a = app.state.client_a = ClientA(app.state.repo)
    client_b = app.state.client_b = ClientB(app.state.repo)

    # The TaskGroup keeps a reference to the tasks, will await them when its
    # exited and cancels them on errors
    async with asyncio.TaskGroup() as tg:
        tg.create_task(client_a.loop())
        tg.create_task(client_b.loop())
        try:
            yield
        finally:
            client_a.dispose()
            client_b.dispose()


@get("/", sync_to_thread=False)
def current_state(state: State) -> tuple[int, int]:
    """Handler function that returns a the current values on the shared data repository."""
    got = state.repo.current_values()
    logger.info("Repo value: %s", got)
    return got

@put("/clear_a", sync_to_thread=False)
def clear_a(state: State) -> tuple[int, int]:
    """Handler function that clears the counter for A."""
    got = state.repo.clear_counter_a()
    logger.info("Repo value in handler from `State`: %s after clearing A", got)
    return got

@put("/clear_b", sync_to_thread=False)
def clear_b(state: State) -> tuple[int, int]:
    """Handler function that clears the counter for B."""
    got = state.repo.clear_counter_b()
    logger.info("Repo value in handler from `State`: %s after clearing B", got)
    return got


app = Litestar(lifespan=[manage_client_lifespan], route_handlers=[current_state, clear_a, clear_b])


if __name__ == "__main__":

    print("The app is starting...")
    uvicorn.run(app, proxy_headers=True, host="0.0.0.0", port=81, log_level='warning')  # nosec: B104
    print("The app is stopping...")
