import asyncio
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from worker import run_worker_loop

async def health(request):
    return JSONResponse({"status": "ok"})

@asynccontextmanager
async def lifespan(app):
    worker_task = asyncio.create_task(run_worker_loop())
    try:
        yield
    finally:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

routes = [Route("/health", health)]
app = Starlette(routes=routes, lifespan=lifespan)