from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo ( Topo ):
    def __init__(self):
        Topo.__init__ ( self )
        h1 = self.addHost('client')
        h2 = self.addHost('server_1')
        h3 = self.addHost('server_2')
        h4 = self.addHost('server_3')
        #h5 = self.addHost('h5')
        #h6 = self.addHost('h6')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')


        self.addLink(h1, s1)
        self.addLink(h2, s3)
        self.addLink(h3, s3)
        self.addLink(h4, s3)
        #self.addLink(h5, s1)
        #self.addLink(h6, s3)
        self.addLink(s1, s2, cls=TCLink, bw=5)
        self.addLink(s2, s3, cls=TCLink, bw=5)
        self.addLink(s3, s4, cls=TCLink, bw=5)
        self.addLink(s4, s1, cls=TCLink, bw=5)

topos = { 'topo-teste': ( lambda: MyTopo() ) }