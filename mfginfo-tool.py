import argparse
import configparser
from pathlib import Path
import re
import sys

from pebble import pulse2, commander


COUNT_SYMS = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
COUNT_BASE = len(COUNT_SYMS)
COUNT_ENC = dict((i, ch) for (i, ch) in enumerate(COUNT_SYMS))
COUNT_LEN = 4


def count_encode(number: int) -> str:
    if number == 0:
        return "0" * COUNT_LEN

    symbol_string = ""
    while number > 0:
        remainder = number % COUNT_BASE
        number //= COUNT_BASE
        symbol_string = COUNT_ENC[remainder] + symbol_string

    if len(symbol_string) > COUNT_LEN:
        raise ValueError("Number too large to encode in fixed length")

    return "0" * (COUNT_LEN - len(symbol_string)) + symbol_string


def serial_generate(mf: str, model: str, datecode: str, line: str, count: int) -> str:
    if not re.match(r"^[A-Z]{1}$", mf):
        raise ValueError(f"Invalid manufacurer code: {mf}")

    if not re.match(r"^[A-Z0-9]{2}$", model):
        raise ValueError(f"Invalid model code: {model}")

    if not re.match(r"^[0-9]{4}$", datecode):
        raise ValueError(f"Invalid date code: {datecode}")

    if not re.match(r"^[A-Z0-9]{1}$", line):
        raise ValueError(f"Invalid line code: {line}")

    count_str = count_encode(count)

    return f"{mf}{model}{datecode}{line}{count_str}"


def main(port: str, config: Path, no_lock: bool) -> None:
    cfg = configparser.ConfigParser()
    cfg.read(config)

    count = cfg.getint("serial", "count")
    serial = serial_generate(
        cfg["serial"]["manufacturer"],
        cfg["serial"]["model"],
        cfg["serial"]["datecode"],
        cfg["serial"]["line"],
        count,
    )

    hwver = cfg["hwver"]["name"]
    color = cfg["color"]["code"]
    model = cfg["model"]["name"]

    iface = pulse2.Interface.open_dbgserial(port)
    prompt = commander.apps.Prompt(iface.get_link())

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

    sys.stdout.write(f"Writing color code\t{color}\t\t")
    r = prompt.command_and_response(f"color write {color}")
    if r[0] != "OK":
        print(f"Color write failed: {r}")
        sys.exit(1)
    sys.stdout.write("OK\n")

    sys.stdout.write(f"Writing model\t\t{model}\t\t")
    r = prompt.command_and_response(f"model write {model}")
    if r[0] != "OK":
        print(f"Model write failed: {r}")
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

    count += 1
    cfg.set("serial", "count", str(count))
    with open(config, "w") as f:
        cfg.write(f)


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
        "-c",
        "--config",
        default="config.ini",
        type=Path,
        help="Configuration file path",
    )
    parser.add_argument(
        "--no-lock",
        action="store_true",
        help="Do not lock the OTP after writing",
    )

    args = parser.parse_args()

    main(args.port, args.config, args.no_lock)
