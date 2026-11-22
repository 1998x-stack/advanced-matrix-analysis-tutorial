#!/usr/bin/env python3
"""Dependency-free correctness regression tests for chapters 04–10."""
import math
import unittest
class MatrixExamples(unittest.TestCase):
    def test_norms(self):
        x=(3,4)
        self.assertEqual(sum(map(abs,x)),7)
        self.assertEqual(math.hypot(*x),5)
        self.assertEqual(max(map(abs,x)),4)
    def test_eigen_power(self):
        a=3**6
        r=(3*a*a+1)/(a*a+1)
        self.assertTrue(2.99<r<3)
    def test_jordan(self):
        J=((2,1),(0,2))
        x=(0,1)
        for _ in range(3):
            x=(2*x[0]+x[1],2*x[1])
        self.assertEqual(x,(12,8))
    def test_matrix_exponential_semigroup(self):
        def expm(t): return ((math.exp(2*t),t*math.exp(2*t)),(0,math.exp(2*t)))
        def mul(A,B):
            return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        lhs=mul(expm(.5),expm(.7)); rhs=expm(1.2)
        for i in range(2):
            for j in range(2): self.assertTrue(math.isclose(lhs[i][j],rhs[i][j],rel_tol=1e-14))
    def test_lu_pivot(self):
        A=((0,2),(1,3)); P=((0,1),(1,0))
        PA=[[sum(P[i][k]*A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        self.assertEqual(PA,[[1,3],[0,2]])
    def test_qr(self):
        Q=((.6,.8),(.8,-.6)); R=((5,.6),(0,.8))
        product=[[sum(Q[i][k]*R[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        for row,expected in zip(product,((3,1),(4,0))):
            for a,b in zip(row,expected):self.assertAlmostEqual(a,b)
    def test_spectral(self):
        s=1/math.sqrt(2)
        Q=((s,s),(s,-s)); lambdas=(3,1)
        A=[[sum(Q[i][k]*lambdas[k]*Q[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
        for row,expected in zip(A,((2,1),(1,2))):
            for a,b in zip(row,expected):self.assertAlmostEqual(a,b)
        for deg in (0,15,30,45,60,90):
            r=1+2*math.cos(math.radians(deg))**2
            self.assertTrue(1-1e-12<=r<=3+1e-12)
if __name__=='__main__': unittest.main(verbosity=2)
