import os
import subprocess
from argparse import ArgumentParser, HelpFormatter
from dotenv import load_dotenv

if __name__ == "__main__":
    # Load ENV
    load_dotenv()
    PYTHON_APPLICATION = os.getenv("PYTHON_APPLICATION")
    PORT = int(os.getenv("PORT"))
    NUMBER_OF_WORKERS = int(os.getenv("NUMBER_OF_WORKERS"))
    LOG_LEVEL = os.getenv("LOG_LEVEL")

    # Parse command line arguments
    parser = ArgumentParser(description=__doc__, formatter_class=lambda prog: HelpFormatter(prog, max_help_position=80, width=80))
    parser.add_argument('-app', '--python_application', required=False, type=str, default=PYTHON_APPLICATION, help='Application to be started by uvicorn')
    parser.add_argument('-p', '--port', required=False, type=int, default=PORT, help='Application port')
    parser.add_argument('-w', '--workers', required=False, type=int, default=NUMBER_OF_WORKERS, help='Number of workers')
    parser.add_argument('-ll', '--log_level', required=False, type=str, default=LOG_LEVEL, help='Log level')
    args = parser.parse_args()

    application = args.python_application
    bind_address = "0.0.0.0"
    bind_port = args.port
    number_of_workers = args.workers

    gunicorn_command = [
        "gunicorn",
        "-w", str(number_of_workers),
        "-k", "uvicorn.workers.UvicornWorker",
        "-b", f"{bind_address}:{bind_port}",
        "--log-level", LOG_LEVEL,
        "--reload",
        "--proxy-protocol",
        application
    ]

    try:
        subprocess.run(gunicorn_command)
    except KeyboardInterrupt:
        pass

