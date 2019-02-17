import os, sys, inspect, threading, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]
import Leap

from matchASL import *