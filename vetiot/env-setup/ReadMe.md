# Required components to setup environment to run VetIoT

This directory contains the files required for setting up environments to run VetIoT.

`setup-env.sh` file generates the environment(starting IoT Platform such as `OpenHAB`) to run VetIoT. It is the controller script.

`restapitoken.txt` file stores OpenHAB REST-API token. This token is used to communicate with the IoT platform (e.g., OpenHAB). 

While setting up environment, VetIoT downloads OpenHAB-3.2.0(an open source IoT platform) and keep it in this directory.
While running VetIoT checks whether java is properly installed. If java is properly installed it will start OpenHAB. After that VetIoT can conduct IoT experiment automatically.