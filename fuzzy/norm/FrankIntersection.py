# -*- coding: iso-8859-1 -*-
#
# Copyright (C) 2009  Rene Liebscher
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free 
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>. 
#

__revision__ = "$Id: FrankIntersection.py,v 1.6 2009-10-27 19:26:05 rliebscher Exp $"

from fuzzy.norm.ParametricNorm import ParametricNorm
from math import log
from fuzzy.utils import inf_p

class FrankIntersection(ParametricNorm):
    """Frank 1979"""
    
    _range = [ (0.,1.),(1.,inf_p) ]
    
    def __init__(self, param=0.5):
        super(FrankIntersection, self).__init__(ParametricNorm.T_NORM, param)

    def __call__(self, *args):
        x, y = self.checkArgs2(args)
        p = self.p
        return log(1.0+(pow(p,x)-1.0)*(pow(p,y)-1.0)/(p-1.0))/log(p)
