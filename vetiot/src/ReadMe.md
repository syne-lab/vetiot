# Source code of VetIoT
This directory contains the source code of VetIoT. VetIoT consists of 4 main modules: Testbed Generator, Event Generator, Event Simulator, and Comparator. A short description about each file is given below.

- `vetiot.py` is the controller of the program. It creates all modules of VetIoT and controls the execution of the program.
- `toml_parser.py` reads and processes the configurations of the experiment.
- `restApiBasedVTgen.py` is the virtual testbed generator. It generates virtual testbed (consists of virtual IoT devices).
- `randomEventGen.py` is the event generator of VetIoT. It generates events based on the IoT testbed created earlier.
- `eventSimulation.py` is the module that feeds events to IoT platform sequentially. This file holds both the Event Simulator and Comparator module of VetIoT.
- `postProcessing.py` implements the debug mode analysis of VetIoT.
- `util.py`, `httpUtil.py`, `sshConnectionUtil.py` provides utility to the main modules of VetIoT.
