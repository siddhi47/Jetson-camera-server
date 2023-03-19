#!/bin/sh
c1=${1:-921600}
c2=${2:-921600}
c3=${3:-921600}
c4=${4:-921600}
g=${5:-921600000}
sudo su <<EOF 
sudo echo $c1 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
sudo echo $c2 > /sys/devices/system/cpu/cpu1/cpufreq/scaling_max_freq
sudo echo $c3 > /sys/devices/system/cpu/cpu2/cpufreq/scaling_max_freq
sudo echo $c4 > /sys/devices/system/cpu/cpu3/cpufreq/scaling_max_freq
sudo echo $g >  /sys/devices/57000000.gpu/devfreq/57000000.gpu/max_freq
exit
EOF
