# Example configurations for VetIoT

This directory works as a configuration repository for VetIoT. VetIoT selects a configuration from this directory based on the command line input(Name of the Defense and Name of the configuration) it receives at the beginning of starting vetiot.

Currently there are 3 configurations in this directory. We provided 2 test configs to evaluate `ExPAT` with both manual and automatically generated testcases. There is a additional configuration for VetIoT in the `sampleIoTDefense` directory which we are using to guide the user about the process of creating configurations for vetiot.

## How to configure VetIoT?

To configure VetIoT follow these steps:
 
1. Create a directory inside `vetiot/test-configs/` directory with the name of the IoT defense which is a user may want to evaluate with VetIoT. For example, we created `sampleIoTdefense` directory.

2. Inside the directory of the IoT defense(`sampleIoTdefense`)create another directory with the name of the configuration. For example we created `sample-config` directory.


3. Inside the `sample-config` directory:
    
    1. Create a file with the name `testbed-config.toml` and define IoT devices in this file. Definition of each IoT device follows this format
        ```
        [<DeviceName>]
        Label=<A string that would be used as Label while creating the Virtual Device>
        Type=<ItemType>
        ```
        For example we created
        ```
        [SampleSwitch]
        Label="Sample Switch"
        Type="Switch"
        ```
        OpenHAB supports only 12 types of virtual IoT devices (called items). Accepted types are: Switch, Number, String, Color, Group, Image, Location, Player, Contact, Dimmer, Rollershutter, DateTime

    2. Create a file with the name `target-defense-config.toml`. Define a toml dictionary with the name `defense-info`, this disctionary has three keys name, hosts, connectioninfo.
        - name:"Name of the IoT defense"
        - hosts: Some IoT defense may require more than one host. This hosts key holds a list of hosts used by IoT defenses. Most of the IoT defense such as ExPAT uses only one host. We named the host as `au`(Short of automation unit) in our provided configs.
        - connectionInfo: This key holds the additional configurations an IoT defense might need. For example: an IoT defense named `IoTGuard` enforces policy through an offsore server. To control `IoTGuard`'s policy enforcement server, a user provides information to connect to `IoTGuard`'s policy enforcement server.

        Check the example `target-defense-config.toml` in the `sample-config` directory.

    3. Create file with the name `platform-config.toml`. This file holds a toml dictionary with the name "au". This dictionary holds rest api token and other configurations to communicate with the IoT Platform. Carefully check the `platform-config.toml` in the `sample-config` directory.

    4. Create a directory with the name `rules` and store uninstrumented rules in this directory.

    5. Create a directory with the name `inst_rules` and store instrumented rules in this directory. Instrumented rules are generated by the IoT defense mechanism VetIoT is evaluating. To generate instrumented rules a user need to follow the instructions mentioned in the repository of that IoT defense.
    
        We created instrumented rules to evaluate ExPAT by following the instructions mentioned in [github repository of ExPAT](https://github.com/expat-paper/expat/tree/master)

    6. Create a directory with the name `config_rules` and store additional rules to create default system state. `config_rules` are triggered by changing state of a special device called `Reset`. Once triggered the `config_rule` will change the state of all devices to a default state.

    7. Create a directory with the name `exps`. This directory holds testcases. If users want VetIoT to generate testcases automatically, it will generate testcases and store testcases in this directory.
    If users want to provide testcases manually, they can add their testcases in this directory. Each testcase is essentially a sequence of events stored in a file with the extension `".events"`.


During runtime VetIoT will ask the user to type the name of the IoT defense and name of the configuration. VetIoT will select config based on the provided names and copy the configuration to the `vetiot/config` directory.