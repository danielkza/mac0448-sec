#!/usr/bin/env python
import sys
import OpenSSL
from twisted.python import log
from twisted.internet import reactor, protocol, ssl
from twisted.protocols.basic import LineReceiver

sys.stdout.write(OpenSSL.SSL.SSLeay_version(OpenSSL.SSL.SSLEAY_VERSION) + '\n')


log.startLogging(sys.stdout, setStdout=False)

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write('connected\n')

    def dataReceived(self, data):
        sys.stdout.write(data)

class EchoClientFactory(protocol.ClientFactory):
    def read_input(self, protocol):
        try:
            while True:
                s = raw_input()
                reactor.callFromThread(protocol.transport.write, s + '\n')
        except EOFError:
            protocol.transport.loseConnection()

    def buildProtocol(self, addr):
        protocol = EchoClient()
        reactor.callInThread(self.read_input, protocol)
        return protocol

if __name__ == '__main__':
    host = sys.argv[1]

    try:
        port = int(sys.argv[2])
    except:
        port = 8080

    try:
        with open('certs/ca_cert.pem', 'rb') as fp:
            authority = ssl.Certificate.loadPEM(fp.read())
    except Exception as e:
        raise RuntimeError(
            "Failed to load CA certificate from {0}: {1}".format(
                'certs/ca_cert.pem', e))

    ssl_options = ssl.CertificateOptions(caCerts=[authority])
    reactor.connectSSL(host, port, EchoClientFactory(), ssl_options)
    reactor.run()
