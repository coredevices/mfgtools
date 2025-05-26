import argparse
import sys

from pebble import pulse2, commander


def main(port):
    iface = pulse2.Interface.open_dbgserial(port)
    prompt = commander.apps.Prompt(iface.get_link())

    r = prompt.command_and_response("flash sec wipe")
    if r[0] != "OK":
        print(f"Flash security wipe failed: {r}")
        sys.exit(1)

    serial = input("Enter serial number: ")
    r = prompt.command_and_response(f"serial write {serial}")
    if r[0] != "OK":
        print(f"Serial write failed: {r}")
        sys.exit(1)

    hwver = input("Enter hardware version: ")
    r = prompt.command_and_response(f"hwver write {hwver}")
    if r[0] != "OK":
        print(f"Hardware version write failed: {r}")
        sys.exit(1)

    pcbaserial = input("Enter PCBA serial number: ")
    r = prompt.command_and_response(f"pcbaserial write {pcbaserial}")
    if r[0] != "OK":
        print(f"PCBA serial write failed: {r}")
        sys.exit(1)
    
    color = input("Enter color code: ")
    r = prompt.command_and_response(f"color write {color}")
    if r[0] != "OK":
        print(f"Color write failed: {r}")
        sys.exit(1)

    model = input("Enter model name: ")
    r = prompt.command_and_response(f"model write {model}")
    if r[0] != "OK":
        print(f"Model write failed: {r}")
        sys.exit(1)

    # WARNING! This will burn flash OTP!
    # r = prompt.command_and_response("flash sec lock l0ckm3f0r3v3r")
    # if r[0] != "OK":
    #     print(f"Flash security lock failed: {r}")
    #     sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MFG Command Line Interface")
    parser.add_argument(
        "-p", "--port", required=True, help="Serial port to connect to the device"
    )
    args = parser.parse_args()

    main(args.port)
