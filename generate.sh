#!/bin/bash

for i in *.svg; do
	inkscape $i -C -e "${i%.svg}.png"
done

