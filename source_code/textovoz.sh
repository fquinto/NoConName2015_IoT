#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.es/translate_tts?&client=t&ie=UTF-8&tl=es&q=$*"; }
say $*

# curl 'http://translate.google.es/translate_tts?ie=UTF-8&q=intruso+detectado&tl=es&client=t' -H 'Referer: http://translate.google.es/' -H 'User-Agent: stagefright/1.2 (Linux;Android 5.0)' > intruso_detectado.mp3