#!/usr/bin/python3

# Copyright : Felix GENSOLLEN

# This file is part of BugnBuzz.
#
# BugnBuzz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BugnBuzz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BugnBuzz.  If not, see <https://www.gnu.org/licenses/>.


import jack

class ConnectionList:

    def __init__(self):
        self.data = []
        
        self.client = jack.Client('bnb_autoconnect')
        self.client.activate()

        self.data.append(['system:capture_1','REAPER:in1'])
        self.data.append(['system:capture_11','REAPER:in2'])
        self.data.append(['system:capture_2','REAPER:in3'])
        self.data.append(['system:capture_3','REAPER:in4'])
        self.data.append(['system:capture_4','REAPER:in5'])
        self.data.append(['system:capture_13','REAPER:in6'])
        self.data.append(['system:capture_14','REAPER:in7'])
        self.data.append(['LinuxSampler:Cravatte L','REAPER:in8'])
        self.data.append(['LinuxSampler:Cravatte R','REAPER:in9'])
        self.data.append(['LinuxSampler:Cuisse L','REAPER:in10'])
        self.data.append(['LinuxSampler:Cuisse R','REAPER:in11'])
        self.data.append(['LinuxSampler:Table BnB L','REAPER:in12'])
        self.data.append(['LinuxSampler:Table BnB R','REAPER:in13'])
        self.data.append(['LinuxSampler:Table 1 L','REAPER:in14'])
        self.data.append(['LinuxSampler:Table 1 R','REAPER:in15'])
        self.data.append(['LinuxSampler:Table 2 L','REAPER:in16'])
        self.data.append(['LinuxSampler:Table 2 R','REAPER:in17'])
        self.data.append(['LinuxSampler:Table 3 L','REAPER:in18'])
        self.data.append(['LinuxSampler:Table 3 R','REAPER:in19'])
        self.data.append(['LinuxSampler:Table 4 L','REAPER:in20'])
        self.data.append(['LinuxSampler:Table 4 R','REAPER:in21'])
        self.data.append(['LinuxSampler:Table 5 L','REAPER:in22'])
        self.data.append(['LinuxSampler:Table 5 R','REAPER:in23'])
        self.data.append(['LinuxSampler:Table 6 L','REAPER:in24'])
        self.data.append(['LinuxSampler:Table 6 R','REAPER:in25'])
        self.data.append(['LinuxSampler:Table 7 L','REAPER:in26'])
        self.data.append(['LinuxSampler:Table 7 R','REAPER:in27'])
        self.data.append(['sooperlooper:loop0_out_1','REAPER:in28'])
        self.data.append(['sooperlooper:loop0_out_2','REAPER:in29'])
        self.data.append(['sooperlooper:loop0_out_3','REAPER:in30'])
        self.data.append(['sooperlooper:loop0_out_4','REAPER:in31'])
        self.data.append(['sooperlooper:loop1_out_1','REAPER:in32'])
        self.data.append(['sooperlooper:loop1_out_2','REAPER:in33'])
        self.data.append(['sooperlooper:loop1_out_3','REAPER:in34'])
        self.data.append(['sooperlooper:loop1_out_4','REAPER:in35'])
        self.data.append(['sooperlooper:loop2_out_1','REAPER:in36'])
        self.data.append(['sooperlooper:loop2_out_2','REAPER:in37'])
        self.data.append(['sooperlooper:loop2_out_3','REAPER:in38'])
        self.data.append(['sooperlooper:loop2_out_4','REAPER:in39'])
        self.data.append(['sooperlooper:loop3_out_1','REAPER:in40'])
        self.data.append(['sooperlooper:loop3_out_2','REAPER:in41'])
        self.data.append(['sooperlooper:loop3_out_3','REAPER:in42'])
        self.data.append(['sooperlooper:loop3_out_4','REAPER:in43'])
        self.data.append(['ardour:Master/audio_out 1','REAPER:in44'])
        self.data.append(['ardour:Master/audio_out 2','REAPER:in45'])
        self.data.append(['ardour:Master/audio_out 3','REAPER:in46'])
        self.data.append(['ardour:Master/audio_out 4','REAPER:in47'])
        
        self.data.append(['REAPER:out1','ardour:REC/audio_in 1'])
        self.data.append(['REAPER:out2','ardour:REC/audio_in 2'])

    def getConnection(self, i):
        return self.data[i]

    def getConnectionCount(self):
        return len(self.data)

    
    def connect(self):
        for connectionName in self.data:
            self.client.connect(connectionName[0],connectionName[1])
            
    def disconnectAllPortsFromClient(self, clientName):
        
        #Outputs in first :
        for port1 in self.client.get_ports('^'+clientName+':', is_output=True):
                for port2 in self.client.get_all_connections(port1):
                        self.client.disconnect(port1, port2)
                        
        #Inputs after..
        for port1 in self.client.get_ports('^'+clientName+':', is_input=True):
                for port2 in self.client.get_all_connections(port1):
                        self.client.disconnect(port2, port1)
    
    
