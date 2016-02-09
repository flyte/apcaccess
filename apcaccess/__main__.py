import argparse

from apcaccess import status


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=3551)
    args = p.parse_args()
    status.print_status(status.get(args.host, args.port))
