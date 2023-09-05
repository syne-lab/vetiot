#Include every command that does not need dynamic control here
projectRootDir="$HOME"/vetiot
configRepository="test-configs"
resultDirectory="generated"
srcDirectory="src"
envDirectory="env-setup"
openhabVersion="3.2.0"

runtimeConfigDir="config"

lsoutput=$(ls ./venv 2> /dev/null)
lsReturnCode=$?
if [ $lsReturnCode != 0 ]; then 
    python3.9 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

source venv/bin/activate

cd $envDirectory
python3 replaceAPItokens.py
cd $projectRootDir

read -p 'Name of the Defense:' defenseName
# read -p 'configstyle(rest):' configStyle
read -p 'Testcase generation type (A for automatic, M for Manual):' testCaseGenType 
testCaseCount=0
if [ "$testCaseGenType" == "A" ]; then
read -p 'Testcase count (5, 10, 15, 25, 35, 50):' testCaseCount
fi
read -p "Name of the configuration:" configName

configStyle="rest"
outputDirName="$defenseName"-"$configName"
configDirName="$configRepository"/"$defenseName"/"$configName"/*

lsoutput=$(ls $configDirName 2> /dev/null)
lsReturnCode=$?
if [ $lsReturnCode != 0 ]; then 
    echo "config directory $configDirName does not exist in the $configRepository directory"
    exit
fi

lsoutput=$(ls $runtimeConfigDir 2> /dev/null)
lsReturnCode=$?
if [ $lsReturnCode == 0 ]; then 
    rm -r "$runtimeConfigDir"/* 2> /dev/null
else
    mkdir "$runtimeConfigDir" 2> /dev/null
fi
cp -r $configDirName "$runtimeConfigDir"/
cd $srcDirectory
python3.9 vetiot.py $configStyle $testCaseGenType $testCaseCount $configName > ./vetiot.log
cd $projectRootDir
mv "$projectRootDir"/"$srcDirectory"/vetiot.log "$projectRootDir"/"$resultDirectory"/"$outputDirName"/vetiot.log
cp "$projectRootDir"/"$envDirectory"/openhab-"$openhabVersion"/userdata/logs/events.log "$projectRootDir"/"$resultDirectory"/"$outputDirName"/openhab-event.log
cp "$projectRootDir"/"$envDirectory"/openhab-"$openhabVersion"/userdata/logs/openhab.log "$projectRootDir"/"$resultDirectory"/"$outputDirName"/openhab.log