from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')
        h10 = self.addHost('h10')
        h11 = self.addHost('h11')
        # h3 = self.addHost('h3')
        # h4 = self.addHost('h4')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        # s3 = self.addSwitch('s3')
        # s4 = self.addSwitch('s4')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)
        self.addLink(h5, s1)
        self.addLink(h6, s1)
        self.addLink(h7, s1)
        self.addLink(h8, s1)
        self.addLink(h9, s1)
        self.addLink(h10, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h11)
        # cls=TCLink, bw=5
        # self.addLink(s3, s2)
        # self.addLink(s1, s2)
        # self.addLink(s2, s3)
        # self.addLink(s3, s4)
        # self.addLink(s4, s1)


topos = { 'topo-teste-new': ( lambda: MyTopo() ) }
