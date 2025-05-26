# MFGINFO Tool

This repository contains a tool that can be used to flash some manufacturing
information to Core Devices watches.

## Pre-requisites

It is recommended to use a Python virtual environment to install dependencies,
which can be installed by running:

```
pip install -r requirements.txt
```

## Usage

Before starting, make sure that the contents of `config.ini` is correct,
in particular:

- `datecode`: Adjust to current date
- `count`: Adjust to `0` if starting

A unit can be flashed by running:

```
python mfginfo-tool.py -p path/to/serial/port [-c path/to/config.ini]
```

Note that `count` will be automatically increased after each run.

Example of a successful run:

```
Erasing OTP                             OK
Writing S/N             S101220A0009    OK
Writing HWVER           asterix         OK
Writing PCBA S/N        S101220A0009    OK
Writing color code      34              OK
Writing model           C2D             OK
Locking OTP                             OK
```