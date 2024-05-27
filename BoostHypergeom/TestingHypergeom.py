import sys
import os
import scipy
from scipy.stats import binom 
from scipy.stats import multinomial
import numpy as np

import mpmath as mp

import time


#print('Original sys.path:', sys.path)

sys.path.append(os.path.abspath('/home/whou/Softwares/PybindTests/BoostHypergeom/build'))

#print('Original sys.path:', sys.path)

import cpp_funcs

n_trial = 1
n_sq = 20

n_inner = 0

eps = 1e-10

c = 0.5
alpha = 0.9
lbd = 2 + 2*alpha
c_ratio = lbd/(lbd+c**2)
a = 1 + alpha + c**2/2
foa2 = 4/a**2

t0 = time.time()
avec = []
k_max = 100
n_term = int(np.ceil(np.log(eps*c*c)/np.log(c_ratio)))
print(n_term)

exp_v = np.zeros((n_sq, n_sq))
for k in range(n_trial):
    for i in range(n_inner, n_sq):
        for j in range(n_inner, n_sq):

            exp_v[i,j] = cpp_funcs.sum_to_g_k(n_term, i, j, c_ratio, alpha, lbd)
            #for k in range(n_term):
                #k_res = k - i - j
                #if (k_res < 0 or k_res % 2 != 0):
                    #continue
                #for l in range(int(np.floor(k - i - j)/2) + 1):
                    #mult_vec = [i+l, l, int((k - i - 2*l - j)/2), int((k - i - 2*l + j)/2)]
                    #exp_v[i,j] += multinomial.pmf(mult_vec, k, [0.25, 0.25, 0.25, 0.25])
                    #exp_v[i,j] += 11
                    #exp_v[i,j] +=  (binom.pmf(i+2*l, k, 0.5)*binom.pmf(l,i+2*l,0.5)*
                            #binom.pmf(int((k - i - 2*l - j)/2),k - i - 2*l,0.5))
            #res += scipy.stats.binom.pmf(1, 1, 0.5)

            #res = scipy.special.gamma(n_term-m)
        if (i % 50 == 0):
            print(i)
            print(exp_v[i,i])
    

t1 = time.time()
total = t1-t0
print("Time: ", total)


#t0 = time.time()
#avec = []
#np_Hyper_v = np.zeros((n_sq, n_sq))
#for k in range(n_trial):
#    for i in range(n_inner, n_sq):
#        for j in range(n_inner, n_sq):
            #np_Hyper_v[i,j] = Hypergeom_Boost.hypergeometric_pFq(avec, bvec, foa2)*scipy.stats.binom.pmf(m, m+n, 0.5)/(a**(m+n))
            #np_Hyper_v[i,j] = cpp_funcs.hypergeometric_pFq(avec, bvec, foa2)*scipy.stats.binom.pmf(m, m+n, 0.5)
            #np_Hyper_v[i,j] = cpp_funcs.hypergeometric_pFq(avec, bvec, foa2)
#            np_Hyper_v[i,j] = cpp_funcs.b_c_hypergeom(a, i, j)
            #res = 0
#        if (i % 50 == 0):
#            print(i)
    

#t1 = time.time()
#total = t1-t0
#print("Time: ", total)

np_Hyper_mp = np.zeros((n_sq, n_sq))
for k in range(n_trial):
    for i in range(n_inner, n_sq):
        for j in range(n_inner, n_sq):
            n = i
            m = j
            avec = [(m+n+1)/2, (m+n)/2+1, n+1, m+1]
            #bvec = [m+1, n+1,m+n+1]

            alpha_a = (alpha/a)**2
            One_a = (1/a)**2

            #np_Hyper_mp[i,j] = mp.hyper(avec, bvec, foa2)*scipy.stats.binom.pmf(m, m+n, 0.5)/(a**(m+n))
            #np_Hyper_mp[i,j] = mp.hyper(avec, bvec, foa2)*mp.binomial(m+n, n)*mp.power(a*2, -m-n - 1)
            np_Hyper_mp[i,j] = mp.appellf4(avec[0], avec[1], avec[2], avec[3], alpha_a, One_a) * mp.binomial(m+n, n)*mp.power(2, -m-n - 1) / a *(alpha/a)**n * (1/a)**m 
            #res = 0
        if (i % 50 == 0):
            print(i)
    

t1 = time.time()
total = t1-t0
print("Time: ", total)

np_Hyper_mp_h = np.zeros((n_sq, n_sq))
for k in range(n_trial):
    for i in range(n_inner, n_sq):
        for j in range(n_inner, n_sq):
            m = i
            n = j
            avec = [(m+n+1)/2, (m+n+1)/2, (m+n)/2 + 1, (m+n)/2+1]
            bvec = [m+1, n+1,m+n+1]

            alpha_a = (alpha/a)**2
            One_a = (1/a)**2

            #np_Hyper_mp[i,j] = mp.hyper(avec, bvec, foa2)*scipy.stats.binom.pmf(m, m+n, 0.5)/(a**(m+n))
            np_Hyper_mp_h[i,j] = mp.hyper(avec, bvec, foa2)*mp.binomial(m+n, n)*mp.power(a*2, -m-n - 1)
            #np_Hyper_mp[i,j] = mp.appellf4(avec[0], avec[1], avec[2], avec[3], alpha_a, One_a) * mp.binomial(m+n, n)*mp.power(a*2, -m-n - 1) / a *(alpha/a)**n * (1/a)**m 
            #res = 0
        if (i % 50 == 0):
            print(i)
    

t1 = time.time()
total = t1-t0
print("Time: ", total)

#print(np.max(np.abs(np_Hyper_v - np_Hyper_mp)))
print(np.max(np.abs(exp_v - np_Hyper_mp)))
print(np.max(np.abs(exp_v)))
print(np.max(np.abs(np_Hyper_mp)))
print(np.max(np.abs(np_Hyper_mp_h)))



