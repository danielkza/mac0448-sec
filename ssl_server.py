#!/usr/bin/env python

import sys
import OpenSSL
from twisted.python import log
from twisted.internet import reactor, protocol, ssl
from twisted.protocols.basic import LineReceiver

sys.stdout.write(OpenSSL.SSL.SSLeay_version(OpenSSL.SSL.SSLEAY_VERSION) + '\n')

log.startLogging(sys.stdout, setStdout=False)

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        sys.stdout.write(data)
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    protocol = Echo

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 8080

    reactor.listenSSL(port, EchoFactory(),
        ssl.DefaultOpenSSLContextFactory(
            'certs/server_key.pem', 'certs/server_cert.pem'))
    reactor.run()
