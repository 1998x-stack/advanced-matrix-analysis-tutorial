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

    def test_svd_rank_k(self):
        singular=(5,2,0)
        self.assertEqual(math.sqrt(sum(s*s for s in singular[1:])),2)
        self.assertEqual(math.sqrt(sum(s*s for s in singular[2:])),0)
        self.assertAlmostEqual(25/29,0.8620689655172413)
    def test_schur_regular_pencil(self):
        self.assertEqual((2-2)*3,0)
        self.assertEqual((2-0)*3,6)
        self.assertEqual(((2,1),(3,0))[1][1],0)
        # 90 degree rotation has eigenvalues +i and -i
        self.assertEqual(complex(0,1)**2+1,0)
    def test_pseudoinverse_and_ridge(self):
        A=((2.,0.),(0.,0.)); P=((.5,0.),(0.,0.))
        def mm(X,Y): return [[sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        self.assertEqual(mm([[1,0],[0,0]],A),[[2.,0.],[0.,0.]])
        self.assertEqual(mm(A,P),[[1.,0.],[0.,0.]])
        # Penrose conditions for the diagonal pedagogical example
        self.assertEqual(mm(mm(A,P),A),[[2.,0.],[0.,0.]])
        self.assertEqual(mm(mm(P,A),P),[[.5,0.],[0.,0.]])
        AP=mm(A,P); PA=mm(P,A)
        self.assertEqual(AP,[list(row) for row in zip(*AP)])
        self.assertEqual(PA,[list(row) for row in zip(*PA)])
        self.assertEqual(4/(4+1),.8)
    def test_weyl_gap_nonnormal(self):
        eps=.2
        hi=1.5+math.sqrt(.25+eps**2)
        lo=1.5-math.sqrt(.25+eps**2)
        self.assertLessEqual(hi-2,eps)
        self.assertLessEqual(1-lo,eps)
        theta=.5*math.atan(2*eps)
        self.assertLessEqual(math.sin(theta),eps/(1-eps))
        perturbed_hi=(3+math.sqrt(1+24*.01))/2
        self.assertGreater(perturbed_hi-2,.01)
    def test_matrix_gradient_central_difference(self):
        def loss(x): return (1-x)**2
        h=1e-4
        central=(loss(h)-loss(-h))/(2*h)
        self.assertAlmostEqual(central,-2,places=9)
        # A=[[1,2],[0,1]], x=[0,1], b=[1,0]:
        # residual=[1,1], A^T residual=[1,3]
        self.assertEqual((1,2*1+1),(1,3))

    def test_random_matrix_densities(self):
        rho=lambda lam: math.sqrt(4-lam*lam)/(2*math.pi)
        self.assertAlmostEqual(rho(0.0),1/math.pi)
        self.assertAlmostEqual(rho(2.0),0.0)
        g=0.5; s=math.sqrt(g)
        a=(1-s)**2; b=(1+s)**2
        self.assertAlmostEqual(a,0.08578643762690495)
        self.assertAlmostEqual(b,2.914213562373095)
        self.assertAlmostEqual(a+b,2*(1+g))
    def test_tensor_unfolding(self):
        T=[[[1,7],[2,8],[3,9]],[[4,10],[5,11],[6,12]]]   # T[i][j][k]，形状 2×3×2
        flat=[T[i][j][k] for i in range(2) for j in range(3) for k in range(2)]
        self.assertEqual(sum(flat),78)
        self.assertEqual(sum(x*x for x in flat),650)
        self.assertAlmostEqual(math.sqrt(650),25.495097567963924)
        T1=[[T[i][j][k] for k in range(2) for j in range(3)] for i in range(2)]
        T2=[[T[i][j][k] for k in range(2) for i in range(2)] for j in range(3)]
        self.assertEqual(T1,[[1,2,3,7,8,9],[4,5,6,10,11,12]])
        self.assertEqual(T2,[[1,4,7,10],[2,5,8,11],[3,6,9,12]])
    def test_tensor_decompositions(self):
        a=[1,2]; b=[1,0,1]; c=[2,1]
        T=[[[a[i]*b[j]*c[k] for k in range(2)] for j in range(3)] for i in range(2)]
        self.assertEqual(T[0],[[2,1],[0,0],[2,1]])
        self.assertEqual(T[1],[[4,2],[0,0],[4,2]])
        self.assertEqual(1*(2+3+2),7)
        self.assertEqual(2*3*2,12)
        # Kruskal sufficiency: k_A+k_B+k_C >= 2R+2
        self.assertTrue(3+3+3 >= 2*2+2)
        # Tucker vs CP parameter counts for a 3x4x5 tensor, all ranks = r
        for r in (1,2,3):
            self.assertEqual(r*(3+4+5),12*r)
            self.assertEqual(r**3+r*(3+4+5),r**3+12*r)
    def test_tensor_train_storage(self):
        n, d, r = 10, 10, 5
        original = n ** d
        tt = d * n * r * r
        self.assertEqual(original, 10000000000)
        self.assertEqual(tt, 2500)
        self.assertEqual(original // tt, 4000000)
    def test_lora_params(self):
        m = n = 4096
        for r, ratio in ((8, 256.0), (64, 32.0)):
            lora = r * (m + n)
            self.assertEqual(lora, r * 2 * m)
            self.assertAlmostEqual((m * n) / lora, ratio)
        self.assertEqual(m * n, 16777216)
        self.assertEqual(8 * (m + n), 65536)
if __name__=='__main__': unittest.main(verbosity=2)
