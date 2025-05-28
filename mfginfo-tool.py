import argparse
from pathlib import Path
import sys

from pebble import pulse2, commander


SERIAL_LEN = 12
HWVER_MAX_LEN = 9


def main(port: str, serial: str, hwver: str, no_lock: bool) -> None:
    if len(serial) != SERIAL_LEN:
        raise ValueError("Invalid serial length")

    if len(hwver) > HWVER_MAX_LEN:
        raise ValueError("Invalid hardware version length")

    iface = pulse2.Interface.open_dbgserial(port)
    link = iface.get_link(timeout=5.)
    if not link:
        raise TimeoutError("Could not obtain link")
    prompt = commander.apps.Prompt(link)

    sys.stdout.write("Erasing OTP\t\t\t\t")
    r = prompt.command_and_response("flash sec wipe")
    if r[0] != "OK":
        print(f"Flash security wipe failed: {r}")
        sys.exit(1)
    sys.stdout.write("OK\n")

    sys.stdout.write(f"Writing S/N\t\t{serial}\t")
    r = prompt.command_and_response(f"serial write {serial}")
    if r[0] != "OK":
        print(f"Serial write failed: {r}")
        sys.exit(1)
    sys.stdout.write("OK\n")

    sys.stdout.write(f"Writing HWVER\t\t{hwver}\t\t")
    r = prompt.command_and_response(f"hwver write {hwver}")
    if r[0] != "OK":
        print(f"Hardware version write failed: {r}")
        sys.exit(1)
    sys.stdout.write("OK\n")

    sys.stdout.write(f"Writing PCBA S/N\t{serial}\t")
    r = prompt.command_and_response(f"pcbaserial write {serial}")
    if r[0] != "OK":
        print(f"PCBA serial write failed: {r}")
        sys.exit(1)
    sys.stdout.write("OK\n")

    sys.stdout.write("Locking OTP\t\t\t\t")
    if no_lock:
        sys.stdout.write("SKIPPED\n")
    else:
        r = prompt.command_and_response("flash sec lock l0ckm3f0r3v3r")
        if r[0] != "OK":
            print(f"Flash security lock failed: {r}")
            sys.exit(1)
        sys.stdout.write("OK\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MFG Command Line Interface")
    parser.add_argument(
        "-p",
        "--port",
        required=True,
        type=str,
        help="Serial port to connect to the device",
    )
    parser.add_argument(
        "-s",
        "--serial",
        required=True,
        type=str,
        help="Serial number",
    )
    parser.add_argument(
        "-v",
        "--hwver",
        required=True,
        type=str,
        help="Hardware version",
    )
    parser.add_argument(
        "--no-lock",
        action="store_true",
        help="Do not lock the OTP after writing",
    )

    args = parser.parse_args()

    main(args.port, args.serial, args.hwver, args.no_lock)
