"""
@author: emad ghalenoei
"""
import numpy as np
#import scipy.sparse
import pywt

def Model_compressor(DensityModel,Gkernelsp):
    
    # inputs are:
    # DensityModel: 3D matrix as an input model
    # Gkernelsp: compressed kernel matrix (output of Kernel_compressor.py)
    
    wname = 'db4'               # name of wavelet
    wv = pywt.Wavelet(wname)    
    Nlevel = 2                  # level of wavelet comprerssion
    Wmode = 'periodization'     # mode of wavelet compression
     
    # CX, CY, CZ are number of prisms in x , y , and z axis. Make sure they are power of 2 like 64 
    CX = int(np.cbrt(DensityModel.size))
    CY = CX  # assuming here that CX = CY = CZ
    CZ = CX  # assuming here that CX = CY = CZ
    CToT = CX*CX*CX 

    DensityModel_3D = DensityModel.reshape((CX,CX,CX))
    Model_coeff  = pywt.wavedecn(DensityModel_3D, wv, mode=Wmode, level=Nlevel)
    Model_3D_coeff = pywt.coeffs_to_array(Model_coeff)[0]
    Model_3D_coeff_row = Model_3D_coeff.reshape((CToT,1))
    data_g_wave = Gkernelsp @ Model_3D_coeff_row  # generated data in real domain. Note that the multiplication of two matrices in the wavelet domain gives output in the real domain
    
    data_g = np.squeeze(data_g_wave)
 
    return data_g
    
    