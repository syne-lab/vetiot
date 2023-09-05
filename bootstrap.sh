export DEBIAN_FRONTEND=noninteractive
downloadDir="/home/vagrant/vetiot/env-setup"
openhabVersion="3.2.0"
javaVersion="11.0.19"
echo "##START: installing java with azul zulu based jdk"
echo "step: Downloading jdk-11.0.19 from azul"
javaDownloadLink=https://cdn.azul.com/zulu/bin/zulu11.64.19-ca-jdk11.0.19-linux_amd64.deb
wget $javaDownloadLink -O "$downloadDir"/zulujdk-"$javaVersion".deb
sudo apt install -y "$downloadDir"/zulujdk-"$javaVersion".deb
echo "step: verify java version"
java --version
echo "##END: Java Installation"

echo "##START: Downloading openhab"
ls "$downloadDir"/openhab-"$openhabVersion"
returnCode=$?
if [ $returnCode == 0 ]; then 
    rm -rf "$downloadDir"/openhab-"$openhabVersion"
fi

echo "##START: Downloading openhab"
openhabDownloadLink=https://github.com/openhab/openhab-distro/releases/download/3.2.0/openhab-3.2.0.zip
wget $openhabDownloadLink -O "$downloadDir"/openhab-"$openhabVersion".zip
unzip "$downloadDir"/openhab-"$openhabVersion".zip -d "$downloadDir"/openhab-"$openhabVersion"
rm "$downloadDir"/openhab-"$openhabVersion".zip
