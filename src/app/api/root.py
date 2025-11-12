from fastapi import APIRouter

ROUTERS: list[APIRouter] = []


def get_root_router() -> APIRouter:
    root_router = APIRouter(prefix='/api')

    for router in ROUTERS:
        root_router.include_router(router)

    return root_router
