## Config Directory of VetIoT

VetIoT uses file-based configuration. Structure of `config` directory is presented here:
```
config_rules/ 
exps/ 
rules/
inst_rules/ 
platform-config.toml
target-defense-config.toml
testbed-config.toml
``` 

Purpose of each item in config directory:

- config_rules: This directory holds config rules that are used to create default system state for each experiment.

- exps: This directory stores test-suites. Each test-suite may contain multiple test-cases.

- rules: This directory stores uninstrumented rules(IoT apps without any security mechanism enabled).

- inst_rules: This directory store instrumented rules(IoT apps with a security mechanism enabled).

- platform-config.toml:  This file stores the http configuration for the IoT platform (e.g. OpenHAB). VetIoT uses information from this file to communicate to IoT platform via REST-API.

- target-defense-config.toml: This file stores additional configurations that an IoT defense might need. For example, `IoTGuard` enforces policy policy via an external server. To control(enable/disable) `IoTGuard`'s policy enforcement, VetIoT needs to communicate with `IoTGuard`'s policy enforcement server. HTTP configurations to communicate with `IoTGuard`'s server is stored in this file.

- testbed-config.toml: This file stores the configuration of IoT devices. VetIoT uses this file to create virtual testbed (consist of IoT devices).

