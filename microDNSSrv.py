
from    _thread import start_new_thread
import  socket

class MicroDNSSrv :

    # ============================================================================
    # ===( Speed Creation )=======================================================
    # ============================================================================

    def Create(domainsList) :
        mds = MicroDNSSrv()
        if mds.SetDomainsList(domainsList) and mds.Start() :
            return mds
        return None

    # ============================================================================
    # ===( Constructor )==========================================================
    # ============================================================================

    def __init__(self) :
        self._domList = { }
        self._started = False

    # ============================================================================
    # ===( Server Thread )========================================================
    # ============================================================================

    def _serverProcess(self) :
        self._started = True
        while True :
            try :
                packet, cliAddr = self._server.recvfrom(256)
            except :
                break
            domName = self._getAskedDomainName(packet)
            if domName is not None :
                ipB = self._domList.get(domName.lower(), None)
                if ipB is None :
                    ipB = self._domList.get('*', None)
                if ipB is not None :
                    packet = self._getPacketAnswerA(packet, ipB)
                    if packet is not None :
                        self._server.sendto(packet, cliAddr)
        self._started = False

    # ============================================================================
    # ===( Functions )============================================================
    # ============================================================================

    def Start(self) :
        if not self._started :
            self._server = socket.socket( socket.AF_INET,
                                          socket.SOCK_DGRAM,
                                          socket.IPPROTO_UDP )
            self._server.setsockopt( socket.SOL_SOCKET,
                                     socket.SO_REUSEADDR,
                                     1 )
            self._server.bind(('0.0.0.0', 53))
            self._server.setblocking(True)
            start_new_thread(self._serverProcess, ())
            return True
        return False

    # ----------------------------------------------------------------------------

    def Stop(self) :
        if self._started :
            self._server.close()
            return True
        return False

    # ----------------------------------------------------------------------------

    def SetDomainsList(self, domainsList) :
        if domainsList is not None and isinstance(domainsList, dict) :
            o = { }
            for dom, ip in domainsList.items() :
                if isinstance(dom, str) and len(dom) > 0 :
                    ipB = self._ipV4StrToBytes(ip)
                    if ipB is not None :
                        o[dom.lower()] = ipB
                        continue
                break
            if len(o) == len(domainsList) :
                self._domList = o
                return True
        return False

    # ============================================================================
    # ===( Utils )================================================================
    # ============================================================================

    def _ipV4StrToBytes(self, ipStr) :
        try :
            parts = ipStr.split('.')
            if len(parts) == 4 :
                return bytes( [ int(parts[0]),
                                int(parts[1]),
                                int(parts[2]),
                                int(parts[3]) ] )
        except :
            pass
        return None

    # ----------------------------------------------------------------------------

    def _getAskedDomainName(self, packet) :
        try :
            queryType = (packet[2] >> 3) & 15
            qCount    = (packet[4] << 8) | packet[5]
            if queryType == 0 and qCount == 1 :
                pos     = 12
                domName = ''
                while True :
                    domPartLen = packet[pos]
                    if (domPartLen == 0) :
                        break
                    domName += ('.' if len(domName) > 0 else '') \
                             + packet[ pos+1 : pos+1+domPartLen ].decode()
                    pos     += 1+domPartLen
                return domName
        except :
            pass
        return None

    # ----------------------------------------------------------------------------

    def _getPacketAnswerA(self, packet, ipV4Bytes) :
        try :
            return b''.join( [
                packet[:2],             # Query identifier
                b'\x81\x80',            # Flags and codes
                packet[4:6],            # Query question count
                b'\x00\x01',            # Query question count
                b'\x00\x00',            # Authority record count
                b'\x00\x00',            # Additional record count
                packet[12:],            # Query question
                b'\xc0\x0c',            # Answer name as pointer
                b'\x00\x01',            # Answer type A
                b'\x00\x01',            # Answer class IN
                b'\x00\x00\x00\x1E',    # Answer TTL 30 secondes
                b'\x00\x04',            # Answer data length
                ipV4Bytes ] )           # Answer data
        except :
            pass
        return None

    # ============================================================================
    # ============================================================================
    # ============================================================================

