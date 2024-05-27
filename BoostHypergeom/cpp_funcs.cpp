#include <pybind11/pybind11.h>
#include <vector>
#include <bits/stdc++.h>
#include <pybind11/stl.h>

#include <iostream>
#include <pybind11/operators.h>
#include <boost/math/special_functions/hypergeometric_pFq.hpp>
#include <cmath>

namespace py = pybind11;

double hypergeometric_pFq(std::vector<double>& a, std::vector<double>& b, double z)
{
    return boost::math::hypergeometric_pFq(a, b, z);
}

double b_c_hypergeom(double a, double m, double n) {
    std::vector<double> avec({(m+n+1)/2, (m+n+1)/2, (m+n)/2+1, (m+n)/2+1});
    std::vector<double> bvec({m+1, n+1,m+n+1});
    double foa2 = 4.0/a/a;
    double log_v = -(m+n + 1) * std::log(2*a) + std::lgamma(m+n+1) - std::lgamma(m+1) - std::lgamma(n+1);
    return boost::math::hypergeometric_pFq(avec, bvec, foa2)*std::exp(log_v);
}

double sum_to_g_k(int k, int n, int m, double ratio, double alpha, double lbd)
{
    double res = 0;
    for (int i = 0; i < k; i++) {
        int diff = i - n - m;
        double tmp_res = 0;
        if (diff >= 0 && diff % 2 == 0) {
            int d_end = diff / 2;
            for (int l = 0; l <= d_end; l++) {
                double log_v = std::lgamma(i+1) - std::lgamma(l+1) - std::lgamma(d_end - l+1) - lgamma(d_end - l + m+1) - lgamma(n+l+1) - std::log(lbd)*i + std::log(alpha) * (n + 2*l);
                tmp_res += std::exp(log_v);
            }
            
        }
        res += std::pow(ratio, i) * tmp_res;
    }
    return res*ratio/lbd;
}

PYBIND11_MODULE(cpp_funcs, m){
    m.def("hypergeometric_pFq", &hypergeometric_pFq);
    m.def("sum_to_g_k", &sum_to_g_k);
    m.def("b_c_hypergeom", &b_c_hypergeom);
}