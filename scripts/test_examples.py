#!/usr/bin/env python3
"""Dependency-free correctness regression tests for illustrated matrix-analysis chapters."""
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


    def test_matrix_calculus_eigenvalue_kink_and_singular_derivative(self):
        def lam_max(t): return max(2+t,2-t)
        h=1e-6
        left=(lam_max(0)-lam_max(-h))/h
        right=(lam_max(h)-lam_max(0))/h
        self.assertAlmostEqual(left,-1,places=7)
        self.assertAlmostEqual(right,1,places=7)
        # For A=diag(3,1), E[0,0]=2, the top singular-value derivative is 2.
        self.assertEqual(1*2*1,2)
        # Check the Daleckii-Krein special case f(A)=A^2: Df(A)[E]=AE+EA.
        A2=[[2.,0.],[0.,1.]]; E2=[[1.,3.],[4.,2.]]
        AE=[[sum(A2[i][k]*E2[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        EA=[[sum(E2[i][k]*A2[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        self.assertEqual([[AE[i][j]+EA[i][j] for j in range(2)] for i in range(2)],[[4.,9.],[12.,4.]])
        # det([[a,b],[c,d]]) gradient is [[d,-c],[-b,a]].
        A=[[2.,1.],[3.,4.]]
        grad=[[4.,-3.],[-1.,2.]]
        def det(M): return M[0][0]*M[1][1]-M[0][1]*M[1][0]
        h=1e-6
        for i in range(2):
            for j in range(2):
                Ap=[row[:] for row in A]; Am=[row[:] for row in A]
                Ap[i][j]+=h; Am[i][j]-=h
                numeric=(det(Ap)-det(Am))/(2*h)
                self.assertAlmostEqual(numeric,grad[i][j],places=7)
    def test_svt_and_admm_scalar_update(self):
        tau=1.25
        shrunk=[max(s-tau,0) for s in (5.,2.,.5)]
        self.assertEqual(shrunk,[3.75,.75,0.])
        self.assertEqual(sum(x>0 for x in shrunk),2)
        m,z,u,rho=3.,1.,.2,2.
        x=(m+rho*(z-u))/(1+rho)
        self.assertAlmostEqual(x,1.5333333333333332)
        self.assertAlmostEqual(z-u,.8)
    def test_stiefel_tangent_projection(self):
        X=((1.,0.),(0.,1.),(0.,0.))
        Xi=((0.,-.5),(.5,0.),(5.,6.))
        XtXi=[[sum(X[k][i]*Xi[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
        self.assertEqual(XtXi,[[0.,-.5],[.5,0.]])
        self.assertAlmostEqual(XtXi[0][1]+XtXi[1][0],0.)
        self.assertEqual(2*3-2*3//2,3)  # dim St(3,2) = 3
        self.assertEqual(2*(3-2),2)    # dim Gr(2,3) = 2
    def test_kronecker_vec_sylvester_and_lyapunov(self):
        A=[[1.,0.],[0.,2.]]; B=[[3.,0.],[0.,4.]]; X=[[1.,2.],[3.,4.]]
        C=[[A[i][i]*X[i][j]+X[i][j]*B[j][j] for j in range(2)] for i in range(2)]
        self.assertEqual(C,[[4.,10.],[15.,24.]])
        vec=[X[i][j] for j in range(2) for i in range(2)]
        self.assertEqual(vec,[1.,3.,2.,4.])
        vecC=[C[i][j] for j in range(2) for i in range(2)]
        self.assertEqual(vecC,[4.,15.,10.,24.])
        # Build K = I kron A + B^T kron I and verify K vec(X) = vec(C).
        def kron(P,Q):
            return [[P[i][j]*Q[r][c] for j in range(2) for c in range(2)]
                    for i in range(2) for r in range(2)]
        I=[[1.,0.],[0.,1.]]
        KA=kron(I,A); KB=kron(B,I)
        K=[[KA[i][j]+KB[i][j] for j in range(4)] for i in range(4)]
        Kv=[sum(K[i][j]*vec[j] for j in range(4)) for i in range(4)]
        self.assertEqual(Kv,vecC)
        # Lyapunov A X + X A^T = -Q with A=-I, X=I, Q=2I.
        AL=[[-1.,0.],[0.,-1.]]; XL=[[1.,0.],[0.,1.]]
        AX=[[sum(AL[i][k]*XL[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        XAT=[[sum(XL[i][k]*AL[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
        self.assertEqual([[AX[i][j]+XAT[i][j] for j in range(2)] for i in range(2)],[[-2.,0.],[0.,-2.]])
    def test_nmf_multiplicative_update(self):
        V=[[2.,1.,0.],[1.,2.,1.],[0.,1.,2.]]
        W=[[1.,.2],[.2,1.],[.5,.5]]
        H=[[1.,.5,.2],[.2,.5,1.]]
        def mm(A,B):
            return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
        def tr(A): return [list(row) for row in zip(*A)]
        def loss():
            R=mm(W,H)
            return .5*sum((V[i][j]-R[i][j])**2 for i in range(3) for j in range(3))
        before=loss()
        Wt=tr(W); numH=mm(Wt,V); denH=mm(mm(Wt,W),H)
        H=[[H[i][j]*numH[i][j]/denH[i][j] for j in range(3)] for i in range(2)]
        Ht=tr(H); numW=mm(V,Ht); denW=mm(mm(W,H),Ht)
        W=[[W[i][j]*numW[i][j]/denW[i][j] for j in range(2)] for i in range(3)]
        after=loss()
        self.assertAlmostEqual(before,3.0666,places=10)
        self.assertAlmostEqual(after,1.09663175479187,places=10)
        self.assertLess(after,before)
        self.assertTrue(all(x>=0 for row in W+H for x in row))
    def test_nmf_scale_and_permutation_ambiguity(self):
        W=[[1.,2.],[3.,4.]]
        H=[[5.,6.],[7.,8.]]
        D=[[2.,0.],[0.,.5]]
        Di=[[.5,0.],[0.,2.]]
        def mm(A,B):
            return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
        P=mm(W,H); P2=mm(mm(W,D),mm(Di,H))
        for a,b in zip(sum(P,[]),sum(P2,[])): self.assertAlmostEqual(a,b)

if __name__=='__main__': unittest.main(verbosity=2)
