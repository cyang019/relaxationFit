#!/usr/bin/python3
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def t2_buildup(t,c0,t2):
    return c0*(np.exp(-t/t2))

def t1_buildup(t,c0,t1):
    return c0*(1.0-np.exp(-t/t1))

def t1rho_buildup(t,c0,t1rho):
    return c0*(np.exp(-t/t1rho))

def fit_all_peaks(fn, ts, peaks):
    '''Fit all peaks in a pandas dataframe with each column
    coresponds to a series of intensities for fitting a t value.

    Parameters
    -------------------------------
    fn: a function that represents the equation for fitting
    ts: time series for x-axis
    peaks: a pd.Dataframe with each column intensities of a peak 
           (buildup curve)

    Returns
    A list containing fitted results in the same order as columns
    in the input pd.Dataframe.
    '''

    params = []
    p0 = [1e4,1.0]
    for peak in peaks:
        peak_pts = peak['val'].tolist()
        p0[0] = max(peak_pts)
        popt, pcov = curve_fit(fn, ts, peak_pts, p0)
        params.append((popt,pcov))
    return params

def plot_all_fittings(fn, ts, peaks, params,\
    sharex=True,sharey=False,figsize=(10,20), titleunit="s",\
    xrange=(0,15),yrange=(0,60000),yrange_axis=[],\
    savefig=False,figname="demo.png"):
    fig, axarr = plt.subplots(len(peaks)//2 + len(peaks) % 2, 2, \
            sharex=sharex, sharey=sharey)
    '''Plot fittings from a list of parameters fitted from a table of
    peaks stored in pd.Dataframe.
    '''
    for i in range(len(peaks)):
        popt, pcov = params[i]
        xx = np.linspace(xrange[0]-0.1, xrange[-1]+0.5, 50)
        yy = fn(xx,*popt)
        axarr[i//2,i%2].plot(xx,yy)
        axarr[i//2,i%2].scatter(ts,peaks[i]['val'].tolist())
        txt = str(popt[-1]) + " " + titleunit
        axarr[i//2,i%2].set_title(txt)
        ymax = max(yy)
        ymin = min(xx)
        axarr[i//2,i%2].set_ylim([ymin*1.1,ymax*1.1])
    axarr[0,0].set_xlim(xrange)
    for ya in yrange_axis:
        axarr[ya//2,ya%2].set_ylim(yrange)
    fig.set_figheight(figsize[1])
    fig.set_figwidth(figsize[0])
    plt.savefig(figname)
    plt.show()

# save peaks to txt file
def save_peaks(peak_locs, ts, peaks, fname):
    '''Save specified peaks to a txt file from a pseudo-2d data output from 
    nmrpipe in ascii format.
    
    Parameters:
    -----------------------------------
    peak_locs: a list of indexes to extract slices from the pseudo-2d
               data
    ts: corresponding time sequence for the series of experiments
    peaks: extracted peak intensities stored in a pd.Dataframe
    fname: output filename.
    '''
    with open(fname,'w') as f:
        for i in range(len(peak_locs)):
            intensities = peaks[i].loc[peak_locs[i],'val'].tolist()
            pts = [(pos,intensity) \
                    for (pos,intensity) in zip(ts,intensities)]
            rank = 'th'
            if(i == 0):
                rank = 'st'
            elif(i == 1):
                rank = 'nd'
            elif(i == 2):
                rank = 'rd'

            f.write('The {nth}{r} slice:\n'.format(nth=str(i+1),r=rank))
            f.writelines(["%f,%f\n" % (pos,intensity) \
                for (pos,intensity) in pts])
            f.write('---------------------\n')


if __name__ == '__main__':
    print("file contain functions for fitting, plotting, \
             and saving T1,T1rho, and T2 fittings.")
