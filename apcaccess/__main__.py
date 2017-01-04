"""
apcaccess.__main__

Provides the command-line functionalty similar to the original apcaccess cmd.
"""

import argparse

from apcaccess import status


def main():
    """Get status from APC NIS and print output on stdout."""
    # No need to use "proper" names on such simple code.
    # pylint: disable=invalid-name
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=3551)
    p.add_argument("--strip-units", action="store_true", default=False)
    args = p.parse_args()
    status.print_status(
        status.get(args.host, args.port),
        strip_units=args.strip_units
    )


if __name__ == "__main__":
    main()
