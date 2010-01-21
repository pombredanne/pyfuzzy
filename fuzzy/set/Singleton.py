# -*- coding: utf-8 -*-
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

__revision__ = "$Id: Singleton.py,v 1.15 2010-01-21 20:58:57 rliebscher Exp $"


from fuzzy.set.Polygon import Polygon
from fuzzy.utils import prop
from fuzzy.Exception import FuzzyException

# use Polygon as base class so we dont need write all
# methods again
class Singleton(Polygon):
    """This set represents a non-fuzzy number.
    
    Its membership is only for x equal 1.::
    
              *
              |
              |
              |
         -----+-----
              x
      
    See also U{http://pyfuzzy.sourceforge.net/demo/set/Singleton.png}
    """

    def __init__(self, x=0.0):
        super(Singleton, self).__init__()
        self._x = float(x) # so it is defined and makes pychecker & Co. happy
        self.x = float(x) # update polygon (_x would be defined here in any case)

    # pylint: disable-msg=E0202,E0211
    #ID:E0211 Singleton.x: Method has no argument
    #ID:E0202 Singleton.x: An attribute inherited from Singleton hide this method
    @prop
    def x(): #@NoSelf
        """x
        @type: float"""
        def fget(self):
            return self._x
        def fset(self, value):
            self._x = float(value)
            self._update()
        return locals()

    def _update(self):
        """update polygon"""
        p = super(Singleton, self)
        p.clear()
        p.add(self._x, 0.0)
        p.add(self._x, 1.0)
        p.add(self._x, 0.0)

    def __call__(self, x):
        """Get membership of value x."""
        if x == self._x:
            return 1.0
        else:
            return 0.0

    def getCOG(self):
        """Return center of gravity."""
        return self._x

    def add(self, x, y, where=Polygon.END):
        """Don't let anyone destroy our singleton."""
        raise FuzzyException()

    def remove(self, x, where=Polygon.END):
        """Don't let anyone destroy our singleton."""
        raise FuzzyException()

    def clear(self):
        """Don't let anyone destroy our singleton."""
        raise FuzzyException()

