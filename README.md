# MicroDNSSrv

### A Micro DNS Server for MicroPython to simply respond to A queries (principally used on ESP32 and [Pycom](http://www.pycom.io) modules)

Very easy to integrate and very light with one file only :
- `"microDNSSrv.py"`

Simple but effective :
- Use it to embed a fast DNS server in yours modules
- Simply responds to A queries (only)
- Use a list of multiple domains
- Include wildcards in the scheme of names
- Use it to make a captive portal simply

### Using *microDNSSrv* main class :

| Name  | Function |
| - | - |
| Constructor | `mds = MicroDNSSrv()` |
| Start DNS server | `mds.Start()` |
| Stop DNS server | `mds.Stop()` |
| Check if DNS server is running | `mds.IsStarted()` |
| Set the domain names list | `mds.SetDomainsList(domainsList)` |

### Basic example :
```python
from microDNSSrv import MicroDNSSrv
domainsList = {
  "test.com"   : "1.1.1.1",
  "*test2.com" : "2.2.2.2",
  "*google*"   : "192.168.4.1",
  "*.toto.com" : "192.168.4.1",
  "www.site.*" : "192.168.4.1" }
mds = MicroDNSSrv(domainsList)
if mds.Start() :
  print("MicroDNSSrv started.")
else :
  print("Error to starts MicroDNSSrv...")
```

### Using *microDNSSrv* speedly creation of the class :
```python
from microDNSSrv import MicroDNSSrv
if MicroDNSSrv.Create( {
  "test.com"   : "1.1.1.1",
  "*test2.com" : "2.2.2.2",
  "*google*"   : "192.168.4.1",
  "*.toto.com" : "192.168.4.1",
  "www.site.*" : "192.168.4.1" } ) :
  print("MicroDNSSrv started.")
else :
  print("Error to starts MicroDNSSrv...")
```

### Using for a captive portal :
```python
MicroDNSSrv.Create({ '*' : '192.168.0.254' })
```
- Can be used with [MicroWebSrv](https://github.com/jczic/MicroWebSrv) easily.



### By JC`zic ;')

*Keep it simple, stupid* :+1: