#!/bin/bash

pulseaudio --start

pacmd unload-module module-jackdbus-detect

pacmd load-module module-jackdbus-detect channels=2 connect=0

pacmd set-default-sink jack_out

jack_connect 'PulseAudio JACK Sink:front-left' 'ardour:Zik/audio_in 1'
jack_connect 'PulseAudio JACK Sink:front-right' 'ardour:Zik/audio_in 2'



