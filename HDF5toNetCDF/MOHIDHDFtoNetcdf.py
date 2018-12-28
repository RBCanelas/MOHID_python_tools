# -*- coding: utf-8 -*-

import h5py
import numpy as np
import xarray as xr

# Change your filename here
#filename = 'C:\\Users\\administrator\\Documents\\GitHub\\Python_testing_grounds\\Hydrodynamic.hdf5'
def MOHIDHdf5toNetcdf(filename, dates= [['0']], in_t=0, file_stride=0, outdir=''):
    f = h5py.File(filename,'r')
    
    dims = ['lat','lon']
    coords={'lat': (('lat'),f['Grid']['Latitude'][0,:-1]),
            'lon': (('lon'),f['Grid']['Longitude'][:-1,0])}
    
    TimeList = f['Time'].keys()
    
    dates_in = dates
    
#    #Writing variables from 'Results'
    var_to_write=['U','V','Free surface level']
    var_to_read=['velocity U','velocity V','water level']    
    t=in_t
    #stride = file_stride
    timeindex=-1
    for timestep in TimeList:
        readtime = 1
        timeindex=timeindex+1
        date=f['Time'][TimeList[timeindex]][:].transpose()
        date=''.join(str(e) for e in date)
        for sublist in dates:
            if sublist == date:
                readtime = 0
        if readtime == 1:
            dates=np.vstack((dates,date))
            k=0
            #if stride == file_stride:
            for var in var_to_read:
                TimeVar = var+timestep[-6:]
                if f['Results'][var][TimeVar].ndim == 2:
                    temp=xr.DataArray(f['Results'][var][TimeVar][:,:].transpose(),coords=coords,dims=dims,encoding={'_FillValue':f['Results'][var][TimeVar][:,:].min()})
                elif f['Results'][var][TimeVar].ndim > 2:
                    temp=xr.DataArray(f['Results'][var][TimeVar][-1,:,:].transpose(),coords=coords,dims=dims)
                ds=xr.Dataset({var_to_write[k]:temp})
                if k == 0:
                    ds.to_netcdf(outdir+'hydrodynamic_'+str(t).zfill(4)+'.nc',mode='w')
                elif k > 0 :
                    ds.to_netcdf(outdir+'hydrodynamic_'+str(t).zfill(4)+'.nc',mode='a')
                k=k+1        
            t=t+1
             #   stride = 0
            #stride=stride+1
        
    #Writing variables from 'Grid'
    var_to_write=['Bathymetry']
    var_to_read=['Bathymetry']
    t=in_t
    dates = dates_in
    #stride = file_stride
    timeindex=-1
    for timestep in TimeList:
        readtime = 1
        timeindex=timeindex+1
        date=f['Time'][TimeList[timeindex]][:].transpose()
        date=''.join(str(e) for e in date)
        for sublist in dates:
            if sublist == date:
                readtime = 0
        if readtime == 1:
            dates=np.vstack((dates,date))
            k=0
            #if stride == file_stride:
            for var in var_to_read:
                TimeVar = var+timestep[-6:]
                if f['Grid'][var].ndim == 2:
                    temp=xr.DataArray(f['Grid'][var][:,:].transpose(),coords=coords,dims=dims,encoding={'_FillValue':f['Grid'][var][:,:].min()})
                elif f['Grid'][var].ndim > 2:
                    temp=xr.DataArray(f['Grid'][var][-1,:,:].transpose(),coords=coords,dims=dims)
                ds=xr.Dataset({var_to_write[k]:temp})        
                ds.to_netcdf(outdir+'hydrodynamic_'+str(t).zfill(4)+'.nc',mode='a')
                k=k+1
            t=t+1
             #   stride = 0
            #stride=stride+1
    
    #Writing computed variables
    #var_to_compute=['Uavg','Vavg']
    return t, dates