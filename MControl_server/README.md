# Remote control of some DAW functions.

Server runs on your PC, you must set the *port* to start the server and the server *ip* (ip of the machine at your LAN) will be displayed.

Sender (client) runs on the android phone using android app or python script executed via [Termux](https://termux.com/). You can connect to the server using your local *ip* and *port*.

If you using a termux with python script - be sure that required packages are installed.
```bash
pkg upgrade
pkg install python
```

The sender is now written to connect to 2 servers, it will be rewritten later to connect to an unlimited number of servers.

This will allow you to run various things on different devices at the same time. The *input lag* is about **5 ms**.