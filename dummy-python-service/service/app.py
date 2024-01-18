import os, sys
import asyncio
import threading
import logging
import logging_loki
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from service.logging_handler import set_uvicorn_logger, get_uvicorn_logger
from service.routers.main_router import main_router

# Get env vars
load_dotenv()
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
SERVICE_NAME = os.getenv("SERVICE_NAME")
LOGGER_NAME = os.getenv("LOGGER_NAME")
LOG_DELAY_START = int(os.getenv("LOG_DELAY_START"))
LOG_DELAY_DELTA = int(os.getenv("LOG_DELAY_DELTA"))

# Get PID, TID
pid = os.getpid()
tid = threading.get_ident()


# Init Loki logger
def init_loki_logger():
    # workaround for Grafana
    logging_loki.emitter.LokiEmitter.level_tag = "level"
    # create loki handler
    loki_handler = logging_loki.LokiHandler(
        url="http://loki:3100/loki/api/v1/push",
        tags={"deployment": DEPLOYMENT_NAME, "tid": f"{tid}", "pid": f"{pid}", "uid": f"{DEPLOYMENT_NAME}.{SERVICE_NAME}.{pid}.{tid}"},
        auth=("username", "password"),
        version="1",
    )
    # create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    console_handler.setFormatter(console_formatter)
    # create a new named logger instance
    loki_logger = logging.getLogger(LOGGER_NAME)
    # add loki handler
    loki_logger.addHandler(loki_handler)
    # add console handler
    loki_logger.addHandler(console_handler)
    # make all levels visible in grafana
    loki_logger.setLevel(logging.DEBUG)
    return loki_logger


def init_prometheus_logger():
    return None


def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logger = get_uvicorn_logger()
    logger.error(f"Caught exception: {msg}")


async def periodic(loki_logger, prometheus_logger):
    count = 0
    await asyncio.sleep(LOG_DELAY_START)
    loki_logger.debug("Entering log emitter loop...")
    while True:
        pid = os.getpid()
        if count > 0:
            loki_logger.info(f"Info event from {SERVICE_NAME}, count={count}", extra={"tags": {"service": SERVICE_NAME}})
        if count % 5 == 0:
            loki_logger.warning(f"Warning event from {SERVICE_NAME}, count={count}", extra={"tags": {"service": SERVICE_NAME}})
        if count % 10 == 0:
            loki_logger.error(f"Error event from {SERVICE_NAME}, count={count}", extra={"tags": {"service": SERVICE_NAME}})
        count += 1
        await asyncio.sleep(LOG_DELAY_DELTA)
    loki_logger.debug("Terminating log emitter loop...")
    loki_logger.critical("Log emitter loop terminated!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init uvicorn logger
    set_uvicorn_logger()
    logger = get_uvicorn_logger()
    logger.info("Starting up service...")

    # Init loki logger
    loki_logger = init_loki_logger()

    # Init Prometheus
    prometheus_logger = init_prometheus_logger()

    # Get loop
    loop = asyncio.get_event_loop()

    # Set exception handler
    loop.set_exception_handler(handle_exception)

    # Add Periodic Task to loop
    loop.create_task(periodic(loki_logger, prometheus_logger))

    yield

    # Reset
    logger.info("Shutting down service...")


# App
app = FastAPI(title=f"{DEPLOYMENT_NAME}.{SERVICE_NAME}", openapi_version="3.0.3", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
