#!/usr/bin/env bash

# Prerequisites: swig, g++

PYTHON_VERSION="3.5"

swig -c++ -python -o LeapPython.cpp -interface LeapPython Leap.i
if [ "$(uname -m)" == "x86_64" ] ; then
  LIBLEAP="x64/libLeap.so"
else
  LIBLEAP="x86/libLeap.so"
fi
g++ -fPIC -I /usr/include/python"$PYTHON_VERSION"m/ LeapPython.cpp $LIBLEAP -shared -o LeapPython.so

sudo cp $LIBLEAP /usr/lib
touch __init__.py
