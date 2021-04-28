

""" ************************************************************************************************
*   halohalo
*
*   This is a general purpose utility library.
*
"   ************************************************************************************************ """




import pickle, copy
""" ************************************************************************************************
*   mUle
*
*   This class calculates the population average and population standard deviation.
*   The mUle data object can be saved off and loaded again at a future time as new datapoints
*   need to be added. The population list is not stored; just the relavant information for
*   calculating the population average and population standard deviation.
*
*   Properties:
*       average
*       stdev_p:    Population Deviation
*       stdev_s:    Sample Deviation
*
*       stdev:      rdefault to stdev_s
*
"   ************************************************************************************************ """
class mUle():

    __DATA__ = (('n',0), ('min',float('inf')), ('max',float('-inf')), ('last',0), ('average',0), ('average_x_sqr',0))

    """ **************************************************************************************
    "   Constructor
    "   ************************************************************************************** """
    def __init__(self,obj = None):
        obj_type = type(obj)
        if obj_type == type(None): return None
        if obj_type in (type(0), type(0.0), type(float('inf'))):
            self.add(obj)
        if obj_type in (type(()), type([])) and type(obj[0]) in (type(0), type(0.0), type(float('inf'))):
            self.add(obj)
        if obj_type == type(mUle):
            obj = obj.data()
            obj_type = type(obj)
        if obj_type == type({}):
            self.__DATA__ = set((i[0],i[1]) for i in (obj).items())

    """ **************************************************************************************
    "   Operators
    "   ************************************************************************************** """
    def __add__(self, other):
        d1 = self.data
        d2 = other.data

        d3 = {}

        d3['n'] = d1['n'] + d2['n']
        d3['min'] = min(d1['min'], d2['min'])
        d3['max'] = max(d1['max'], d2['max'])
        d3['last'] = None
        d3['average'] = ((d1['average']*(d1['n']/d3['n'])) + (d2['average']*(d2['n']/d3['n'])))
        d3['average_x_sqr'] = ((d1['average_x_sqr']*(d1['n']/d3['n'])) + (d2['average_x_sqr']*(d2['n']/d3['n'])))

        return mUle(d3)

    def __sub__(self, other):
        d3 = self.data
        d2 = other.data
        if d3['n'] > d2['n']: d1 = d3
        else:
            d1 = d2
            d2 = d3

        d3 = {}

        d3['n'] = d1['n'] - d2['n']
        d3['min'] = max(d1['min'], d2['min'])
        d3['max'] = min(d1['max'], d2['max'])
        d3['last'] = None
        d3['average'] = ((d1['average']*(d1['n']/d3['n'])) - (d2['average']*(d2['n']/d3['n'])))
        d3['average_x_sqr'] = ((d1['average_x_sqr']*(d1['n']/d3['n'])) - (d2['average_x_sqr']*(d2['n']/d3['n'])))

        return mUle(d3)

    """ **************************************************************************************
    "   Properties
    "   ************************************************************************************** """
    def getdata(self): return {i[0]:i[1] for i in sorted(list(self.__DATA__))}
    def getaverage(self): return round(self.data['average'],13)
    def getstdev_p(self):
        return (self.data['average_x_sqr'] - (self.data['average']**2))**0.5
    def getstdev_s(self):
        return ((self.data['average_x_sqr']*((self.data['n']+1)/self.data['n'])) - ((self.data['average'])**2))**0.5
    def getstdev(self): return self.stdev_s

    data = property(getdata)
    average = property(getaverage)
    stdev = property(getstdev)
    stdev_p = property(getstdev_p)
    stdev_s = property(getstdev_s)


    """ **************************************************************************************
    "   Methods
    "   ************************************************************************************** """
    def add(self, _x):
        if type(_x) in (type(0), type(0.0), type(float('inf'))): _x = [_x]

        d = self.data
        try:
            for x in _x:
                d['n'] += 1
                d['min'] = min(d['min'], x)
                d['max'] = max(d['max'], x)
                d['last'] = x
                d['average'] = (((d['average'] * (d['n']-1)) + x) / d['n'])
                d['average_x_sqr'] = (((d['average_x_sqr'] * (d['n']-1)) + (x**2)) / d['n'])
        except: d = None

        if d:
            self.__DATA__ = set((i[0],i[1]) for i in d.items())
        return self.data


    """ **************************************************************************************
    "   Class Methods
    "   ************************************************************************************** """
    def __add(_d, _x):
        if type(_x) in (type(0), type(0.0), type(float('inf'))) and _d: _x = [_x]
        d = _d.copy()
        try:
            for x in _x:
                d['n'] += 1
                d['min'] = min(d['min'], x)
                d['max'] = max(d['max'], x)
                d['last'] = x
                d['average'] = (((d['average'] * (d['n']-1)) + x) / d['n'])
                d['average_x_sqr'] = (((d['average_x_sqr'] * (d['n']-1)) + (x**2)) / d['n'])
        except: d = _d

        return d
