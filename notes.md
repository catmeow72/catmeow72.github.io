---
layout: notes
title: "Useful Notes"
author: Catmeow72
permalink: /notes.html
tags: netgear a6210 wifi usb openwrt network router notes catmeow72
date: 2025-08-19 13:22:34 -0700
---

* Table of Contents
{:toc}

## How to get a Netgear A6210 USB wifi adapter working on OpenWRT
First, set up OpenWRT as usual and make sure you have a working USB port and internet connection. Then, install the `kmod-mt76x2u` package.

Source: [OpenWRT forum post](https://forum.openwrt.org/t/openwrt-not-support-netgear-a6210/126000/8)

## Thethering from phone to OpenWRT
1. Enable bluetooth by changing AutoEnable in /etc/bluetooth/main.conf to true
    ```
    AutoEnable=true
    ```
2. Modify /etc/dbus-1/system.d/bluetooth.conf to add to the root policy block:
    ```xml
      <allow send_type="method_call" />
      <allow send_type="method_return" />
    ```
    Example after modification of root policy block:
    ```xml
      <policy user="root">
        <allow own="org.bluez"/>
        <allow send_destination="org.bluez"/>
        <allow send_interface="org.bluez.Agent1"/>
        <allow send_interface="org.bluez.MediaEndpoint1"/>
        <allow send_interface="org.bluez.MediaPlayer1"/>
        <allow send_interface="org.bluez.Profile1"/>
        <allow send_interface="org.bluez.GattCharacteristic1"/>
        <allow send_interface="org.bluez.GattDescriptor1"/>
        <allow send_interface="org.bluez.LEAdvertisement1"/>
        <allow send_interface="org.freedesktop.DBus.ObjectManager"/>
        <allow send_interface="org.freedesktop.DBus.Properties"/>
        <allow send_type="method_call"/>
        <allow send_type="method_return"/>
      </policy>
    ```
3. Use bluetoothctl to pair and connect to the phone.
    1. Start by logging in via SSH
    2. Run `bluetoothctl` to enter the bluetoothctl command line
    3. Wait for your phone to appear
    4. Type `pair XX:XX:XX:XX:XX:XX` where the X's are replaced with your phone's MAC address shown along with your phone name
        <div class="tip">
            You can use tab completion by pressing <span class="key">Tab</span> while typing the address.
            If there are no other possible choices up to a certain point, this will complete up to that point,
            and if there's no other possible choices at all, you will have the complete MAC address.
            If there is ambiguity, press <span class="key">Tab</span> again to see the possible choices.
        </div>
    5. Type `trust XX:XX:XX:XX:XX:XX` where the X's are replaced with the same MAC address.
### Steps to connect once phone is paired
1. If not logged into SSH on your router, log in.
2. Connect via Bluetooth with the following command:
    ```sh
    dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX org.bluez.Network1.Connect string:'NAP'
    ```
    Where the XX is replaced with the digits of your phone's MAC address you found when pairing.
3. If you hvaen't yet, set up your router to route your internet traffic through the phone by typing these commands:
    ```sh
    uci set network.wan=interface
    uci set network.wan.proto=dhcp
    uci set network.wan.ifname='bnep0'
    uci commit
    ifup wan
    ```
    <div class="command-desc">
        This creates (`network.wan=interface`) and sets up the WAN network to use the phone's bluetooth connection (`network.wan.ifname='bnep0'`) via DHCP (`network.wan.proto=dhcp`).
        It then commits the changes (`uci commit`), and triggers the WAN interface to reload (`ifup wan`).
    </div>
Source: [OpenWRT docs](openwrt.org/docs/guide-user/hardware/bluetooth/bluetooth.tether) (Date: <span class="date">2025-10-25T19:54:33Z</span>; [Archive](https://web.archive.org/web/20250706143356/openwrt.org/docs/guide-user/hardware/bluetooth/bluetooth.tether), <span class="date">2025-07-06T13:33:56Z</span>)

## macOS
### Clearing Icon Cache
```sh
sudo rm -rfv /Library/Caches/com.apple.iconservices.store
sudo find /private/var/folders/ \( -name com.apple.dock.iconcache -or -name com.apple.iconservices \) -exec rm -rfv {} \; ; sleep 3;sudo touch /Applications/* ; killall Dock; killall Finder
```
The errors returned are normal and don't affect anything.

Also note that this will restart the Dock and Finder.
### Flush DNS cache
From memory:
```sh
dscacheutil -flushcache
sudo killall mDNSResponder
```
