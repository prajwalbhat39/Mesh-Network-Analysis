# MeshNetworkAnalysis
Approach to detect mesh networks among other networks


### Creating Mesh Network
 <code>sudo service network-manager stop</code> / <code>systemctl stop NetworkManager</code>
 <br/>
 <code>sudo ip link set wlo1 down</code>
 <br/>
<br/>
<code>sudo iwconfig wlo1 mode ad-hoc</code>
<br/>
<code>sudo iwconfig wlo1 channel 1</code>
<br/>
<code>sudo iwconfig wlo1 essid Kavach</code>
<br/>
<code>sudo iwconfig wlo1 key 1234567890</code>
<br/>
<code>sudo iwconfig wlo1 ap 12:3E:30:39:BE:A1</code>
<br/>
<code>sudo ip link set wlo1 up</code>
<br/>
<code>sudo ip addr add 169.254.34.2/16 dev wlo1</code>
<br/>
<code>ping 169.254.34.2</code>
<br/>
<br/>
https://bbs.archlinux.org/viewtopic.php?id=230151
<br/>
https://help.ubuntu.com/community/WifiDocs/Adhoc
