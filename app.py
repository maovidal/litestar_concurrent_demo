"""
PRELIMINAR 23-11-18

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
async def the_client_1(app: Litestar) -> AsyncGenerator[None, None]:
    """
    Runs an instance of the Client A
    """
    # Set an instance of the Shared Repository if it does not exists already
    repo = getattr(app.state, "repo", None)
    if repo is None:
        repo = Repo("A")
        app.state.repo = repo

    # Set an instance of the Client A with access to the Shared Repository
    client_a = getattr(app.state, "client_a", None)
    if client_a is None:
        client_a = ClientA(repo)
        app.state.client_a = client_a
        asyncio.create_task(client_a.loop())
    try:
        yield
    finally:
        await client_a.dispose()

@asynccontextmanager
async def the_client_2(app: Litestar) -> AsyncGenerator[None, None]:
    """
    Runs an instance of the Client B
    """
    # Set an instance of the Shared Repository if it does not exists already
    repo = getattr(app.state, "repo", None)
    if repo is None:
        repo = Repo("B")
        app.state.repo = repo

    # Set an instance of the Client B with access to the Shared Repository
    client_b = getattr(app.state, "client_b", None)
    if client_b is None:
        client_b = ClientB(repo)
        app.state.client_b = client_b
        asyncio.create_task(client_b.loop())
    try:
        yield
    finally:
        await client_b.dispose()


@get("/", sync_to_thread=False)
def current_state(state: State) -> tuple:
    """Handler function that returns a the current values on the shared data repository."""
    got = state.repo.current_values()
    logger.info("Repo value in handler from `State`: %s whose creator was %s", got, state.repo.creator)
    return got

@put("/clear_a", sync_to_thread=False)
def clear_a(state: State) -> tuple:
    """Handler function that clears the counter for A."""
    got = state.repo.clear_counter_a()
    logger.info("Repo value in handler from `State`: %s after clearing A", got)
    return got

@put("/clear_b", sync_to_thread=False)
def clear_b(state: State) -> tuple:
    """Handler function that clears the counter for B."""
    got = state.repo.clear_counter_b()
    logger.info("Repo value in handler from `State`: %s after clearing B", got)
    return got


app = Litestar(lifespan=[the_client_1, the_client_2], route_handlers=[current_state, clear_a, clear_b])


if __name__ == "__main__":

    print("The app is starting...")
    uvicorn.run(app, proxy_headers=True, host="0.0.0.0", port=81, log_level='warning')  # nosec: B104
    print("The app is stopping...")
