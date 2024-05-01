import time
from nest_asyncio import apply
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from src.configs.index import CLIENT_BASE_URL, SERVER_BASE_URL
from src.datasources.prisma import prisma
from src.apis.index import router
from fastapi.middleware.cors import CORSMiddleware

apply()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan, title="Server", openapi_url="/openapi.json")

app.include_router(router=router)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = [SERVER_BASE_URL, CLIENT_BASE_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
