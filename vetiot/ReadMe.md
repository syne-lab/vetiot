## Running/Testing VetIoT

VetIoT evaluates policy enforcing IoT defenses such as ExPAT.
To evaluate an IoT defense, VetIoT uses OpenHAB-3.2.0 as the IoT platform. VetIoT interacts with OpenHAB-3.2.0 via REST-API. To interact via REST-API, VetIoT need a REST-API `token` from the running OpenHAB instance.

### Steps to collect OpenHAB REST-API token

1. Open terminal at the root directory(`vetiot-release`) and log into the virtual machine (named `vetiot`) with this command
    ```
    vagrant ssh vetiot
    ```
    i. Inside the virtual machine, go to `vetiot/env-setup` directory and run `setup-env.sh`

    ```
    cd vetiot/env-setup/
    ./setup-env.sh
    ```
    
    `setup-env.sh` script will check whether Java installation was proper. If Java installation is proper, it will start an OpenHAB instance.

2. Once OpenHAB is running, open a browser in the host machine and go to [http://192.168.56.10:8080](http://192.168.56.10:8080)
3. On the webpage follow these steps:
    1. Create a user(any username and password will work) for OpenHAB.

    2. Select `Begin Setup` to start the process of setting up OOpenHAB
    3. For location, select `configure in settings later`
    4. Click `Select Add-ons to Install` button
    5. Search `JSONPath Transformation` and select it.
    6. Click the `close` button to close the `Select Add-on to install` prompt
    7. Click `Select 1 Add-on` and wait for installations.
    8. Select `Get Started` button
    9. At the bottom-left of the screen it will show the user account details (created in step 1)
    10. Select the `user` at the bottom-left of the screen.
    11. Select `Create new API token`
    12. In the new page, fill `User Name`, `Password`, `Token Name` and click `Create API token`.
    13. Copy the `API token` and save it to `vetiot-release/vetiot/env-setup/restapitoken.txt` file.

### After collecting REST-API token, user is ready to evaluate IoT defenses with VetIoT

To evaluate an IoT defense with VetIoT follow these steps:

1. Open a second terminal, and log in to the virtual machine with
    ```
    vagrant ssh vetiot
    ```
    i. Inside the virtual machine, go to `vetiot/` and run VetIoT with the command `./run.sh`
    ```
    cd vetiot
    ./run.sh
    ```

    ii. `run.sh` will provide a prompt, where user provide defense-name (such as ExPAT), testcase generation type (automatic or manual), number of testcases and name of the test-config VetIoT should use.

    For example: while evaluating ExPAT with randomly generated testcases VetIoT looks like this:

    ```
    vagrant@vetiot:~/vetiot$ ./run.sh 
    Name of the Defense:expat
    Testcase generation type (A for automatic, M for Manual):A
    Testcase count (5, 10, 15, 25, 35, 50):5
    Name of the configuration:ST
    ```