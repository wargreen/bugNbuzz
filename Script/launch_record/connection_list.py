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

        self.data.append(['ardour:Voix/audio_out 1','REAPER:in1'])
        self.data.append(['ardour:DPA/audio_in 1','REAPER:in2'])
        self.data.append(['ardour:CravateAudio/audio_out 1','REAPER:in3'])
        self.data.append(['ardour:CuisseAudio/audio_out 1','REAPER:in4'])
        self.data.append(['ardour:Table1Audio/audio_out 1','REAPER:in5'])
        self.data.append(['ardour:Table2Audio/audio_out 1','REAPER:in6'])
        self.data.append(['ardour:TableBnB Audio/audio_out 1','REAPER:in7'])
        self.data.append(['ardour:TableBnB Audio/audio_out 1','REAPER:in8'])
        self.data.append(['sooperlooper:loop0_out_1','REAPER:in9'])
        self.data.append(['sooperlooper:loop0_out_2','REAPER:in10'])
        self.data.append(['sooperlooper:loop0_out_3','REAPER:in11'])
        self.data.append(['sooperlooper:loop0_out_4','REAPER:in12'])
        self.data.append(['sooperlooper:loop1_out_1','REAPER:in13'])
        self.data.append(['sooperlooper:loop1_out_2','REAPER:in14'])
        self.data.append(['sooperlooper:loop1_out_3','REAPER:in15'])
        self.data.append(['sooperlooper:loop1_out_4','REAPER:in16'])
        self.data.append(['sooperlooper:loop2_out_1','REAPER:in17'])
        self.data.append(['sooperlooper:loop2_out_2','REAPER:in18'])
        self.data.append(['sooperlooper:loop2_out_3','REAPER:in19'])
        self.data.append(['sooperlooper:loop2_out_4','REAPER:in20'])
        self.data.append(['sooperlooper:loop3_out_1','REAPER:in21'])
        self.data.append(['sooperlooper:loop3_out_2','REAPER:in22'])
        self.data.append(['sooperlooper:loop3_out_3','REAPER:in23'])
        self.data.append(['sooperlooper:loop3_out_4','REAPER:in24'])
        self.data.append(['ardour:Master/audio_out 1','REAPER:in25'])
        self.data.append(['ardour:Master/audio_out 2','REAPER:in26'])
        self.data.append(['ardour:Master/audio_out 3','REAPER:in27'])
        self.data.append(['ardour:Master/audio_out 4','REAPER:in28'])
        
        self.data.append(['REAPER:out1','ardour:REC/audio_in 1'])
        self.data.append(['REAPER:out2','ardour:REC/audio_in 2'])

    def getConnection(self, i):
        return self.data[i]

    def getConnectionCount(self):
        return len(self.data)

    
    def connect(self):
        for connectionName in self.data:
            self.client.connect(connectionName[0],connectionName[1])
