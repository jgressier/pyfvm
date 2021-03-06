# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:58:31 2013

@author: j.gressier
"""
import numpy as np
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("unable to import matplotlib, some features will be missing")

#import model
#import mesh


class fdata():
    """
    define field: neq x nelem data
      model : number of equations
      mesh  : mesh
      data  : data to initialize
    """
    def __init__(self, model, mesh, data=None, t=0.):
        self.model = model
        self.neq   = model.neq
        self.mesh  = mesh
        self.nelem = mesh.ncell
        self.time  = t
        if data!=None:
            self.data = data[:] # copy shape
            # and check
            for i, d in enumerate(data):
                if np.ndim(d) < self.model.shape[i]:
                    self.data[i] = np.repeat(np.expand_dims(d, axis=0), self.nelem, axis=0).T
                else:
                    self.data[i] = d.copy()
            #self.data = [ np.array(d).T*np.ones(self.nelem) for d in data ] # old version only working for scalars
        else:
            raise NotImplementedError("no more possible to get data signature")
            self.data = [ np.zeros(self.nelem) ] * self.neq
            # for i in range(self.neq):
            #     self.data.append(np.zeros(nelem))
                    
    def copy(self):
        new = fdata(self.model, self.mesh, self.data, t=self.time)
        # new.mesh  = self.mesh
        # new.nelem = self.nelem
        # new.data = [ d.copy() for d in self.data ]
        return new

    def set(self, f):
        self.__init__(f.model, f.mesh, f.data)
        self.time = f.time

    def zero_datalist(self, newdim=None):
        """returns a list of numpy.array with the same shape of self.data, possibly resizes to dim if provided"""
        if newdim:
            datalist = [ 0 for d in self.data]
            for i, d in enumerate(self.data):
                newshape = np.array(d.shape)
                newshape[-1] = newdim
                datalist[i]  = np.zeros(newshape)
        else:
            datalist = [ np.zeros(d.shape) for d in self.data]
        return datalist

    def isnan(self):
        return any([ np.any(np.isnan(d)) for d in self.data])

    def phydata(self, name):
        return self.model.nameddata(name, self.data)

    def plot(self, name, style='o', axes=plt):
        return axes.plot(self.mesh.centers(), self.phydata(name), style)

    def contour(self, name, style={}, axes=plt):
        xx, yy = self.mesh.centers()
        axes.set_aspect('equal')
        return axes.contour(xx.reshape((self.mesh.nx, self.mesh.ny)),
                             yy.reshape((self.mesh.nx, self.mesh.ny)), 
                             self.phydata(name).reshape((self.mesh.nx, self.mesh.ny)))

    def contourf(self, name, style={}, axes=plt):
        xx, yy = self.mesh.centers()
        axes.set_aspect('equal')
        return axes.contourf(xx.reshape((self.mesh.nx, self.mesh.ny)),
                             yy.reshape((self.mesh.nx, self.mesh.ny)), 
                             self.phydata(name).reshape((self.mesh.nx, self.mesh.ny)))

    def set_plotdata(self, line, name):
        line.set_data(self.mesh.centers(), self.phydata(name))
        return
