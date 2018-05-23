#!/bin/sh

linuxsampler --exec-after-init "cat SamplerSession.lscp | netcat localhost 8888"  --lscp-addr localhost --lscp-port 8888
