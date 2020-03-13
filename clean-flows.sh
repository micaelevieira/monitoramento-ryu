#!/bin/bash

sudo ovs-ofctl -O OpenFlow13 del-flows s1
sudo ovs-ofctl -O OpenFlow13 del-flows s2
sudo ovs-ofctl -O OpenFlow13 del-flows s3
sudo ovs-ofctl -O OpenFlow13 del-flows s4