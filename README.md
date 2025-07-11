# MFGTOOLS

This repository contains a set of tools that can be used to flash some
manufacturing information, recovery firmware, etc. to Core Devices watches.

## Pre-requisites

It is recommended to use a Python virtual environment to install dependencies,
which can be installed by running:

```
pip install -r requirements.txt
```

Device needs to be running the PRF (recovery) firmware.

## Usage

### `mfginfo-tool.py`

This tool is used to flash unique information to each device such as serial
numbers.

A device can be flashed by running:

```
python mfginfo-tool.py -p path/to/serial/port -s $SERIAL -v $HWVER
```

where `$SERIAL` is a 12-character serial number and `$HWVER` is the hardware
version, e.g. `asterix`.

**NOTE**: You can also pass `--no-lock` if you want to skip locking OTP.
It can be useful while testing, so you can retry as many times as you want.

Example of a successful run:

```
Erasing OTP                             OK
Writing S/N             S101220A0009    OK
Writing HWVER           asterix         OK
Writing PCBA S/N        S101220A0009    OK
Locking OTP                             OK
```

### `mfgrecovery-flash.py`

This tool is used to flash the PRF (recovery) firmware into the external flash.

PRF can be flashed by running:

```
python mfgrecovery-flash.py -t path/to/serial/port -p firmware path/to/prf.bin
```

Example of a successful run:

```
Erasing... done.
...............RRR................R.R.R..............RR.R..............R...R..............R.RR................RR..R.............R...R..............R.RR................RR................RR...............R..R................RR...............RRR................RR.......R..........R......R..........R.......R.........R....R.R.
Success!
```

### `pulse_console.py`

This tool allows to access the PULSE console available on the serial port.

It can be used like this:

```
python pulse_console.py --tty path/to/serial/port
```

If using a firmware with log hashing, you can provide a dictionary file:

```
python pulse_console.py --tty path/to/serial/port --log-dict path/to/loghash_dict.json
```
