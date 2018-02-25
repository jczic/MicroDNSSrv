
from network     import WLAN
from microDNSSrv import MicroDNSSrv

# ----------------------------------------------------------------------------

print()
print("=======================================================================")
print()

WLAN().init(mode=WLAN.AP, ssid='Test MicroDNSSrv', auth=(WLAN.WPA2, 'azerty123'))

if MicroDNSSrv.Create( {
  "test.com"   : "1.1.1.1",
  "*test2.com" : "2.2.2.2",
  "*google*"   : "192.168.4.1",
  "*.toto.com" : "192.168.4.1",
  "www.site.*" : "192.168.4.1" } ) :
  print("MicroDNSSrv started.")
else :
  print("Error to starts MicroDNSSrv...")

print()
print("=======================================================================")
print()

# ----------------------------------------------------------------------------
