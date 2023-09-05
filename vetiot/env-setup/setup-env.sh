#!/bin/bash
# echo "##START: installing java-11 with azul zulu based jdk"
# sysname=$(uname)
# absDirPath=$(pwd)

# if [ "$sysname" == "Linux" ]; then
#     echo "setting java path in Linux"
#     javaPath="$absDirPath"/linux-zulu-java-11
#     export JAVA_HOME=$javahome
#     export PATH="$javaPath":"$PATH"
# else
#     echo "setting java path in Mac"
#     javahome="$absDirPath"/mac-m1-zulu-java-11
#     export JAVA_HOME=$javahome
#     export PATH="$JAVA_HOME":"$PATH"
# fi

echo "Testing java version"
javaVersion=$(java --version)
if [[ "$javaVersion" == *"11"* ]]; then
    echo "java is found in path"
else
    echo "java is not found in path, you probably need to fix that."
    echo "Install Zulu jdk-11.0.19. If you set up vagrant using the provided Vagrantfile, there is a zulujdk-11.0.19.deb in the env-setup directory."
    exit
fi
echo "Done setting up Java, starting OpenHAB"
echo "Use logout to logout from openhab then ctrl-c to exit"
cd openhab-3.2.0
./start.sh
openhabPID=$!
exit