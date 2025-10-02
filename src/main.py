"""Heartbeat counter entrypoint."""

from __future__ import annotations

import datetime
import sys
import time
from typing import NoReturn

MAX_COUNT: int = 100


class HeartbeatError(Exception):
    """Raised when the heartbeat loop encounters an unexpected error."""


def format_line(timestamp: datetime.datetime, count: int) -> str:
    """Return a formatted heartbeat line with timestamp and count."""
    iso = timestamp.isoformat(timespec="seconds")
    return f"[{iso}] count={count}"


def next_count(current: int, max_count: int = MAX_COUNT) -> int:
    """Return the next counter value, wrapping to 0 after max_count."""
    return 0 if current >= max_count else current + 1


def heartbeat_loop(max_count: int = MAX_COUNT) -> None:
    """Emit heartbeat lines once per second with a wrapping counter."""
    count = 0
    while True:
        now = datetime.datetime.now()
        print(format_line(now, count), flush=True)
        time.sleep(1.0)
        count = next_count(count, max_count)


def run() -> None:
    """Start the heartbeat loop and handle termination signals and errors."""
    try:
        heartbeat_loop()
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("Interrupted by user", flush=True)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        sys.stdout.flush()
        message = f"Unexpected error: {exc}" if exc else "Unexpected error occurred"
        print(message, file=sys.stderr, flush=True)
        raise HeartbeatError("Heartbeat loop failed") from exc


def main() -> NoReturn:
    """Execute the run function and exit with appropriate status code."""
    try:
        run()
    except HeartbeatError:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
