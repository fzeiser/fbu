import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy import mean,std,arange,array
from scipy.stats import norm

def plothistandtrace(name,xx,lower,upper):
    ax = plt.subplot(211)
    mu = mean(xx) if 'truth' in name else 0.
    sigma = std(xx) if 'truth' in name else 1.
    n, bins, patches = plt.hist(xx, bins=50, normed=1, facecolor='green',
                                alpha=0.5, histtype='stepfilled')
    yy = norm.pdf(bins,mu,sigma)
    plt.plot(bins,yy,'r-')
    plt.ylabel('Probability')
    plt.xlabel('Bin content')
    ymean = mean(ax.get_ylim())
    plt.hlines(ymean,lower,upper,linestyles='dashed',colors='m',label='hyperbox')
    plt.subplot(212)
    x = arange(len(xx))
    plt.plot(x,xx,label='trace of %s'%name)
    plt.savefig('%s.png'%name)
    plt.close()


def plot(dirname,data,bkgd,resmat,trace,nuisancetrace,lower=[],upper=[]):
    import os
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    dirname = os.path.normpath(dirname) + os.sep

    plt.imshow(resmat,interpolation='none',origin='lower',alpha=0.5)
    plt.savefig(dirname+'resmat.png')
    plt.close()

    ndim = len(data)
    # overlay data and background
    x = arange(0.5,ndim+0.5)
    plt.plot(x,data,'k',label='data',drawstyle='steps-mid')
    if len(bkgd)>0:
        plt.plot(x,array(bkgd).sum(axis=0),'b',label='background',drawstyle='steps-mid')
    plt.ylim([0.,max(data)*1.3])
    plt.xlim([0.,len(data)])
    plt.savefig(dirname+'databckg.png')
    plt.close()

    for name,nuisance in nuisancetrace.items():
        plothistandtrace(dirname+name,nuisance,-5.,5.)

    nbins = len(trace)
    for bin in range(nbins):
        plothistandtrace(dirname+'bin%d'%bin,trace[bin],lower[bin],upper[bin])

        for name,nuisance in nuisancetrace.items():
            plt.plot(trace[bin],nuisance,',')
            plt.savefig(dirname+'%s_bin%d.png'%(name,bin))
            plt.close()
