
from network     import WLAN
from microDNSSrv import MicroDNSSrv

# ----------------------------------------------------------------------------

print()
print("=======================================================================")
print()

WLAN().init(mode=WLAN.AP, ssid='Test MicroDNSSrv', auth=(WLAN.WPA2, 'azerty123'))

srv = MicroDNSSrv.Create( {
	"test.com"	 : "123.123.123.123",
	"google.com" : "50.50.50.50",
	"*"			 : "192.168.4.1" } )

if srv :
	print("MicroDNSSrv started.")
else :
	print("Error to start MicroDNSSrv...")

print()
print("=======================================================================")
print()

# ----------------------------------------------------------------------------
