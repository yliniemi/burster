# Burster



These Python 3 scripts can be used to test the network throughput and packet loss.



## Usage

### burst_sender.py

```
$ ./burst_sender.py --help
usage: BDS - Burst Data Sender [-h] [--ip IPv4 Addr.] [-p PORT] [-b INT] [-n INT] [-i INT] [-s INT]
                               [-d INT]

Send data bursts.

options:
  -h, --help            show this help message and exit
  --ip IPv4 Addr.       Target IP.
  -p PORT, --port PORT  Target port.
  -b INT, --burst-length INT
                        Length of a single burst.
  -n INT, --bursts-to-send INT
                        Amount of bursts to send before exiting.
  -i INT, --interval INT
                        Time interval between bursts in microseconds.
  -s INT, --packet-size INT
                        Packet size in bytes.
  -d INT, --debug-interval INT
                        Interval for debug logging in seconds.
```



### burst_receiver.py

```
$ ./burst_receiver.py --help
usage: BDR - Burst Data Receiver [-h] [-p PORT] [-d INT]

Receive data bursts.

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Target port.
  -d INT, --debug-interval INT
                        Interval for debug logging in seconds.
```


