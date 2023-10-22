# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 09:58:49 2023

@author: astephen
"""

import sys

if not sys.version_info > (2,7):
    print("Python2 went end of life at Jan 1 2020.  Time to upgrade yourself.")
    sys.exit(42)
elif not sys.version_info >= (3,7):
    print("Using dataclasses which requires >= 3.7")
    sys.exit(37)
    
from dataclasses import dataclass

@dataclass
class T:
    t: float = 3.14
        
    def __repr__(self):
        return 'T object with T.t = %f' % self.t
        
if __name__ == '__main__':
    t = T(6.28)
    print(t)