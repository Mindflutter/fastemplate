from typing import Annotated, cast

from fastapi import Depends
from starlette.datastructures import State
from starlette.requests import Request

from fastemplate.repositories.engine import Engine
from fastemplate.settings import Settings


async def state_dep(request: Request) -> State:
    return cast("State", request.app.state)


async def settings_dep(state: Annotated[State, Depends(state_dep)]) -> Settings:
    return cast("Settings", state.settings)


async def engine_dep(state: Annotated[State, Depends(state_dep)]) -> Engine:
    return cast("Engine", state.engine)
