#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

__revision__ = "$Id: demo_merge.py,v 1.8 2009-01-09 22:04:42 rliebscher Exp $"

try:
    # If the package has been installed correctly, this should work:
    import Gnuplot, Gnuplot.funcutils, Gnuplot.PlotItems
except ImportError:
    print "Sorry, you need Gnuplot to use this."
    import sys
    sys.exit(1)

def makePlotItem(points,title):
    # extend polygon so its is in [0:60]
    points.insert(0,(0,points[0][1]))
    points.append((60,points[-1][1]))
    l=[]
    for i in points:
        l.append(list(i))
    return Gnuplot.PlotItems.Data(l,title=title)

def plotPlotItems(items,title,filename):
    print "Plot %s => %s" % (title,filename)
    g = Gnuplot.Gnuplot()
    g("set terminal png small transparent truecolor")
    g("set output 'merge/%s.png'" % filename)
    g('set style fill transparent solid 0.25 border')
    g('set style data filledcurves y1=0')
    g('set noautoscale xy')
    g('set xrange [0:60]')
    g('set yrange [-0.2:1.2]')
    g("set title '%s'" % title)
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    g.plot(*unique_items)
    g.close()
    g = None

def main():
    """Show examples merge and norm function using some example sets and norms"""
    import fuzzy
    import fuzzy.System
    import fuzzy.Variable
    import fuzzy.OutputVariableCOG
    import fuzzy.Adjective
    import fuzzy.Rule
    import fuzzy.operator
    import fuzzy.operator.Input
    import fuzzy.norm
    import fuzzy.norm.Min
    import fuzzy.norm.Max
    import fuzzy.norm.AlgebraicProduct
    import fuzzy.norm.AlgebraicSum
    import fuzzy.set
    import fuzzy.set.Polygon
    import fuzzy.set.Trapez
    import fuzzy.set.Triangle
    import fuzzy.set.Singleton
    import fuzzy.set.Function
    import fuzzy.set.SFunction
    import fuzzy.set.ZFunction
    import fuzzy.set.PiFunction

    from fuzzy.set.Set import Set,norm,merge

    class helper(object):
        def __init__(self,set,plotItems):
            self.set = set
            self.plotItems = plotItems

    def define_set(set,name):
        if isinstance(set,fuzzy.set.Polygon.Polygon):
            pi = makePlotItem(set.points,name)
        else:
            pi = Gnuplot.PlotItems.Data([(i,set(i)) for i in range(0,61)],title=name)
        return helper(set,pi)

    set_a = define_set(fuzzy.set.PiFunction.PiFunction(a=30.,delta=20.),"a: Pi a=30, delta=20")
    set_b = define_set(fuzzy.set.ZFunction.ZFunction(a=21.,delta=10.),"b: Z  a=21, delta=10")
    set_c = define_set(fuzzy.set.SFunction.SFunction(a=42.,delta=15.),"c: S  a=42, delta=15")
    set_d = define_set(fuzzy.set.Triangle.Triangle(m=30.,alpha=20.,beta=25.),"d: Triangle m=30, alpha=20,beta=25")
    set_e = define_set(fuzzy.set.Polygon.Polygon([(25.,0.),(25.,0.45)]),"e: (25,0),(25,0.45)")
    set_f = define_set(fuzzy.set.Polygon.Polygon([(25.,0.65),(25.,0.)]),"f: (25,0.65),(25,0)")
    set_g = define_set(fuzzy.set.Polygon.Polygon([(32.,0.),(32.,0.55)]),"g: (32,0),(32,0.55)")
    set_h = define_set(fuzzy.set.Polygon.Polygon([(32.,0.35),(32.,0.)]),"h: (32,0.35),(32,0)")
    set_i = define_set(fuzzy.set.Singleton.Singleton(25.),": Singleton x=25")

    def define_const(value,name):
        return helper(value,Gnuplot.PlotItems.Data([(i,value) for i in (0,60)],title=name))

    const_05 = define_const(0.5,"constant value 0.5")

    # Graphische Darstellung

    Min = fuzzy.norm.Min.Min()
    Max = fuzzy.norm.Max.Max()
    AlgebraicProduct = fuzzy.norm.AlgebraicProduct.AlgebraicProduct()
    AlgebraicSum = fuzzy.norm.AlgebraicSum.AlgebraicSum()

    tests = [
        # norm, set1, set2, item name, plot name, file name

        # test norm of in_set2 with different norm and 0.5
        (Min,set_a,const_05,"Min(a,0.5)","Min(a,0.5)","Min_a_0.5"),
        (Max,set_a,const_05,"Max(a,0.5)","Max(a,0.5)","Max_a_0.5"),
        (AlgebraicProduct,set_a,const_05,"AlgebraicProduct(a,0.5)","AlgebraicProduct(a,0.5)","AlgebraicProduct_a_0.5"),
        (AlgebraicSum,set_a,const_05,"AlgebraicSum(a,0.5)","AlgebraicSum(a,0.5)","AlgebraicSum_a_0.5"),

        # test merge of a_set and b_set with different norms
        (Min,set_a,set_b,"Min(a,b)","Min(a,b)","Min_a_b"),
        (Max,set_a,set_b,"Max(a,b)","Max(a,b)","Max_a_b"),
        (AlgebraicProduct,set_a,set_b,"AlgebraicProduct(a,b)","AlgebraicProduct(a,b)","AlgebraicProduct_a_b"),
        (AlgebraicSum,set_a,set_b,"AlgebraicSum(a,b)","AlgebraicSum(a,b)","AlgebraicSum_a_b"),

        (AlgebraicProduct,set_e,set_h,"AlgebraicProduct(e,h)","AlgebraicProduct(e,h)","AlgebraicProduct_e_h"),
        (AlgebraicSum,set_e,set_h,"AlgebraicSum(e,h)","AlgebraicSum(e,h)","AlgebraicSum_e_h"),

        (AlgebraicProduct,set_f,set_g,"AlgebraicProduct(f,g)","AlgebraicProduct(f,g)","AlgebraicProduct_f_g"),
        (AlgebraicSum,set_f,set_g,"AlgebraicSum(f,g)","AlgebraicSum(f,g)","AlgebraicSum_f_g"),


        (AlgebraicProduct,set_a,set_a,"AlgebraicProduct(a,a)","AlgebraicProduct(a,a)","AlgebraicProduct_a_a"),
        (AlgebraicSum,set_a,set_a,"AlgebraicSum(a,a)","AlgebraicSum(a,a)","AlgebraicSum_a_a"),


        (AlgebraicProduct,set_e,set_f,"AlgebraicProduct(e,f)","AlgebraicProduct(e,f)","AlgebraicProduct_e_f"),
        (AlgebraicSum,set_e,set_f,"AlgebraicSum(e,f)","AlgebraicSum(e,f)","AlgebraicSum_e_f"),

        (AlgebraicProduct,set_e,set_i,"AlgebraicProduct(e,i)","AlgebraicProduct(e,i)","AlgebraicProduct_e_i"),
        (AlgebraicSum,set_e,set_i,"AlgebraicSum(e,i)","AlgebraicSum(e,i)","AlgebraicSum_e_i"),

        (AlgebraicProduct,set_f,set_i,"AlgebraicProduct(f,i)","AlgebraicProduct(f,i)","AlgebraicProduct_f_i"),
        (AlgebraicSum,set_f,set_i,"AlgebraicSum(f,i)","AlgebraicSum(f,i)","AlgebraicSum_f_i"),



    ]
    for norm_,set1,set2,item_name,plot_name,file_name in tests:
        if isinstance(set2.set,fuzzy.set.Set.Set):
            p = merge(norm_,set1.set,set2.set)
        else:
            # set2 is float value!
            p = norm(norm_,set1.set,set2.set)
        plotPlotItems([set1.plotItems,set2.plotItems,makePlotItem(p.points,item_name)],plot_name,file_name)



    p = merge(fuzzy.norm.AlgebraicProduct.AlgebraicProduct(),set_d.set,set_d.set,1.0)
    p2 = merge(fuzzy.norm.AlgebraicProduct.AlgebraicProduct(),set_d.set,set_d.set,8.0)
    plotPlotItems([set_d.plotItems,makePlotItem(p2.points,"AlgebraicProduct(d,d) => merge(...,8)"),makePlotItem(p.points,"AlgebraicProduct(d,d) => merge(...,1)")],"AlgebraicProduct(d,d)","AlgebraicProduct_d_d")
    p = merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),set_d.set,set_d.set,1.0)
    p2 = merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),set_d.set,set_d.set,8.0)
    plotPlotItems([set_d.plotItems,makePlotItem(p2.points,"AlgebraicSum(d,d) => merge(...,8)"),makePlotItem(p.points,"AlgebraicSum(d,d) => merge(...,1)")],"AlgebraicSum(d,d)","AlgebraicSum_d_d")

    p = merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),set_c.set,merge(fuzzy.norm.AlgebraicProduct.AlgebraicProduct(),set_a.set,set_b.set))
    plotPlotItems([set_a.plotItems,set_b.plotItems,set_c.plotItems,makePlotItem(p.points,"AlgebraicSum(c,AlgebraicProduct(a,b))")],"AlgebraicSum(c,AlgebraicProduct(a,b))","AlgebraicSum_c_AlgebraicProduct_a_b")

    p = merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),set_c.set,merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),set_a.set,set_b.set))
    plotPlotItems([set_a.plotItems,set_b.plotItems,set_c.plotItems,makePlotItem(p.points,"AlgebraicSum(c,AlgebraicSums(a,b))")],"AlgebraicSum(c,AlgebraicSum(a,b))","AlgebraicSum_c_AlgebraicSum_a_b")

    p = merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),merge(fuzzy.norm.AlgebraicSum.AlgebraicSum(),set_c.set,set_a.set),set_b.set)
    plotPlotItems([set_a.plotItems,set_b.plotItems,set_c.plotItems,makePlotItem(p.points,"AlgebraicSum(AlgebraicSums(c,a),b))")],"AlgebraicSum(AlgebraicSum(c,a),b))","AlgebraicSum_AlgebraicSum_c_a_b")

# when executed, just run main():
if __name__ == '__main__':
    main()

