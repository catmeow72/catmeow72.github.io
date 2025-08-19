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

## macOS
### Clearing Icon Cache
```sh
sudo rm -rfv /Library/Caches/com.apple.iconservices.store
sudo find /private/var/folders/ \( -name com.apple.dock.iconcache -or -name com.apple.iconservices \) -exec rm -rfv {} \; ; sleep 3;sudo touch /Applications/* ; killall Dock; killall Finder
```
The errors returned are normal and don't affect anything.
### Flush DNS cache
From memory:
```sh
dscacheutil -flushcache
sudo killall mDNSResponder
```