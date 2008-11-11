# -*- coding: iso-8859-1 -*-

__revision__ = "$Id: Compound.py,v 1.7 2008-11-11 12:19:10 rliebscher Exp $"


from fuzzy.operator.Operator import Operator

class Compound(Operator):
    """Take values of input operators  and process them
       through the given norm.
    """ 

    def __init__(self, norm, *inputs):
        """Constructor.
        norm:   how combine inputs. (eg. Min,Max,...)
        inputs: list of inputs (subclassed from Operator).
        """
        super(Compund, self).__init__()
        self.norm = norm
        self.inputs = inputs

    def __call__(self):
        """Get current value of input and combine them with help of norm."""
        return self.norm(*[x() for x in self.inputs])

    def printDot(self,out,system,parent_name):
        norm_name = self.norm.printDot(out,system,parent_name)
        for i in self.inputs:
            i.printDot(out,system,norm_name)
        return norm_name

