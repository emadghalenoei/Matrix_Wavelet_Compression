
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 23:22:13 2020

@author: emad ghalenoei
"""
import numpy as np
from scipy.sparse import csr_matrix
import pywt

def Kernel_compressor(Ndatapoints,CX,CY,CZ,Kernel_Grv):
    
    # inputs are:
    # Ndatapoints: number of data point. make sure they are power of 2 like 32
    # CX, CY, CZ are number of prisms in x , y , and z axis. Make sure they are power of 2 like 64 
    # Kernel_Grv: original kernel matrix that is going to be compressed
    
    wname = 'db4'               # name of wavelet
    wv = pywt.Wavelet(wname)    
    Nlevel = 2                  # level of wavelet comprerssion
    thrg = 0.001                # thresholding value
    Wmode = 'periodization'     # mode of wavelet compression
    
    Gkernel = np.zeros((Ndatapoints*Ndatapoints,CX*CY*CZ)) # will contain wavelet coefficients

    for irow in np.arange(Ndatapoints*Ndatapoints):

        Kernelsplit = Kernel_Grv[irow,:].copy()   # take one row of kernel
        Gi = Kernelsplit.reshape((CX,CY,CZ))      # reshape kernel to 3D array
        Gi_coeff  = pywt.wavedecn(Gi, wv, mode= Wmode, level=Nlevel) # apply 3D wavelet compression
        Gi_3D_coeff = pywt.coeffs_to_array(Gi_coeff)[0] # extract wavelet coeff and insert to array
        Gi_3D_coeff[abs(Gi_3D_coeff)<thrg] = 0  # zeroing values under thrg
        Gi_3D_coeff_row = Gi_3D_coeff.reshape((1,CX*CY*CZ)) # reshape back to 1D array
        Gkernel[irow,:] = Gi_3D_coeff_row  # put values to the corresponding row

    Gkernelsp = csr_matrix(Gkernel) # sparness

    
    return Gkernelsp
    
    
    
    