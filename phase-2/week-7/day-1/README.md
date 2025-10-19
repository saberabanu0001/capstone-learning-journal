# 🧠 Capstone Robotics — Jetson Remote Setup via Tailscale (OAK-D Lite)
## Overview

**This guide documents how Sabera Banu connected her MacBook Air to the Jetson (Ubuntu) board remotely using Tailscale, verified the DepthAI setup, and confirmed successful camera operation of the OAK-D Lite module.**

## 🛰️ 1. Remote Connection Setup (Tailscale)
### ✅ What We Used:

- Tailscale for private VPN connection (Mac ↔ Jetson).

- Shared team account: rovercapstone@gmail.com

- Password (team-shared): **********

- Three connected devices:

- bakhtiyors-mac-mini

- saberas-macbook-air

- ubuntu (Jetson board)





## ⚙️ Setup Steps:

- Installed Tailscale on both Mac and Jetson.

- Logged in using the shared Tailscale account (rovercapstone@gmail.com).

- Verified connection on Tailscale Admin Panel:

- - All machines showed as Connected (green dot ✅).

- SSH connection was established from Mac to Jetson:

- - - ssh root@100.87.198.86


- Confirmed successful connection with:

- - Welcome to Ubuntu 20.04.6 LTS (Jetson)