c1=${1:-1}
c2=${2:-1}
c3=${3:-1}
c4=${4:-1}

sudo su <<EOF 
sudo echo $c1 > /sys/devices/system/cpu/cpu0/online
sudo echo $c2 > /sys/devices/system/cpu/cpu1/online
sudo echo $c3 > /sys/devices/system/cpu/cpu2/online
sudo echo $c4 > /sys/devices/system/cpu/cpu3/online
EOF
