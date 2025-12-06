import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from worker import run_worker_loop

async def health(request):
    return JSONResponse({"status": "ok"})

routes = [Route("/health", health)]
app = Starlette(routes=routes)

@app.on_event("startup")
async def start_worker():
    asyncio.create_task(run_worker_loop())