"""
This module gives simple implementation of GEM under GMM.
"""

import numpy as np
import random
import statistics as st
import math
from sklearn import metrics
import sklearn
import pandas as pd


def mahalanobis(x,mu,phi=1): 
    """
    Args:
         x: numpy array
         mu: numpy array
         phi: float magnitude of covariance 
    Returns:
         Mahalanobis distance between x and mu scaled by -0.5
         assuming covariance matrix is phi*Id
    """
    return(-0.5*(1/phi)*np.inner(x-mu,x-mu))


def rescaled_GEM_score(x,mean,phi=1):
    """
    Args:
         x: numpy array
         mean: list of numpy arrays
               holds the means of in-distribution data
         phi: float magnitude of covariance 
    Returns:
         rescaled GEM score of vector x 
    """
    energy=0
    for mu in mean:
        energy+=np.exp(mahalanobis(x,mu,phi))
    return energy


def mean_generator(d,k, beta,normalize=0):
    """
    Args:
         d: int holds input dimension
         k: int number of non-zero entries
         phi: float magnitude of covariance 
    Returns:
         a list of means according to the setting explained in the paper 
    """
    means=[]#holds the number of centers
    q=d//k
    m1=[beta]*k+[0]*(d-k)
    w=[]
    for i in range(q):
        a=m1[-i*k:]+m1[:-i*k]
        if normalize!=0: #checks if normalization is needed
            aa=np.array(a)
            n=np.linalg.norm(aa) #holds norm of the vector
            normalized=[(i/n)*normalize for i in aa] #holds normalized vector
            means.append(np.array(normalized))
        else:
            means.append(np.array(a))
    return means


def fpr_95_tpr(fpr,tpr):
    """
    Helper method for FPR at TPR 95 computation
    """
    a=[i for i,v in enumerate(tpr) if v > 0.95]
    index=a[0]
    return fpr[index]

def out_distribution_generate(m_out,sigma,n=1):
    """
    Args:
         m_out: numpy array mean of OOD
         sigma: numpy array covariance matrix
         n: int number of samples to generate 
    Returns:
         a list of numpy array generated from corresponding gaussian
    """
    return list(np.random.multivariate_normal(m_out, sigma, n))


def in_distribution_generate(mean,sigma,n=1):
    """
    Args:
         mean: list of numpy array means of ID
         sigma: numpy array covariance matrix
         n: int number of samples to generate 
    Returns:
         a list ofnumpy array generated from corresponding GMM 
    """
    k=len(mean)
    my_list=[]
    for i in range(n):
        data_class=random.randint(0,k-1)
        class_mean=mean[data_class]
        my_list.append(np.random.multivariate_normal(class_mean, sigma, 1)[0])
    return my_list

def generate(alpha,mean,m_out,phi=1,n=1):
    """
    Args:
         alpha: float controls how often a sample is ID
         mean: list of numpy arrays means of ID
         m_out: numpy array mean of OOD
         n: int number of sample to be generated
    Returns:
         three list correspond to samples generated from joint model 
    """
    d=len(m_out)
    sigma_in=phi*np.identity(d)
    sigma_out=sigma_in
    my_list=[]#holds sample data with its label
    feature_list=[]#holds sample data
    label_list=[]#holds the labels
    for i in range(n):
        #label 1 corresponds to in-distribution and label 0 corresponds to out-distribution
        label=np.random.binomial(1,alpha,1) #draw 1 smaple according to bernulli with parameter alpha 
        if label==1:#draws from in distribution
            a=in_distribution_generate(mean,sigma_in)
            sample_data=[a[0],1]
            my_list.append(sample_data)
            feature_list.append(a[0])
            label_list.append(1)
        else:
            if label==0: #draws from out-distribution
                a=out_distribution_generate(m_out,sigma_out)
                sample_data=[a[0],0]
                my_list.append(sample_data)
                feature_list.append(a[0])
                label_list.append(0)
    return my_list,feature_list, label_list


def simulate(d,nz,beta,alpha,n,phi=1,normalized=0):
    """
    Args:
         d: int dimension
         nz: int number of non-zero entries 
         beta: float the value of each non-zero entry (if normalized is 0)
         n: int number of sample to be generated from joint model
         phi: float magnitude of covariance
         normalized: float if non-zero it holds the magnitude of od ID mean
    Returns:
         performance of GEM OOD when n samples are generated from the joint model  
    """
    mean=mean_generator(d,nz,beta,normalized)
    #holds the mean of out-distribution data
    m_out=np.array([0]*d)
    k=len(mean)
    my_list,feat,label=generate(alpha,mean,m_out,phi,n)
    my_energy_score=[rescaled_GEM_score(x,mean,phi) for x in feat]
    fpr_energy, tpr_energy, thresholds_eng=sklearn.metrics.roc_curve(label,my_energy_score)
    return (fpr_95_tpr(fpr_energy, tpr_energy))