from math import sqrt
import codecs

import dsqss.hamiltonian
from dsqss.hamiltonian import Site, Interaction, MatElem

from dsqss.util import ERROR, get_as_list, extend_list

def creator_boson(n):
    return sqrt(n+1.0)
def annihilator_boson(n):
    return sqrt(n)

class BoseSite:
    def __init__(self, id, M, U, mu):
        '''
        M: max n
        U: n_i (n_i - 1)/2
        mu: -n_i
        '''
        M = int(M)
        NX = M+1

        sources = []
        elements = []
        for n in range(NX):
            elements.append(MatElem(state = n, value = -mu*n + 0.5*U*n*(n-1)))
            if n > 0:
                # annihilator
                sources.append(MatElem(istate = n, fstate = n-1,
                                       value = annihilator_boson(n)))
            if n < M:
                # creator
                sources.append(MatElem(istate = n, fstate = n+1,
                                       value = creator_boson(n)))
        super().__init__(id=id, N=NX, elements=elements, sources=sources)

class BoseBond:
    def __init__(self, id, M, t, V):
        '''
        M: max N
        t: c_1 a_2 + c_2 a_1
        V: n_1 n_2
        '''

        nbody = 2
        nx = M+1
        Ns = [nx,nx]

        N = [1.0*n for n in range(nx)]
        c = [creator_boson(n) for n in N]
        c[-1] = 0.0
        a = [annihilator_boson(n) for n in N]
        elements = []
        for i in range(self.nx):
            for j in range(self.nx):
                # diagonal
                w = V*i*j
                if w != 0.0:
                    elements.append(MatElem(state=[i,j], value=w))
                # offdiagonal
                w = -t*c[i]*a[j]
                if w != 0.0:
                    elements.append(MatElem(istate=[i,j],
                                            fstate=[i+1,j-1],
                                            value=w))
                w = -t*a[i]*c[j]
                if w != 0.0:
                    elements.append(MatElem(istate=[i,j],
                                            fstate=[i-1,j+1],
                                            value=w))
        super().__init__(id=id, nbody=nbody, Ns=Ns, elements=elements)

class BoseHubbard_hamiltonian:
    def __init__(self, param):
        M = param['M']
        Us = get_as_list(param, 'U', 0.0)
        mus = get_as_list(param, 'mu', 0.0)
        nstypes = max(len(Us), len(mus))
        extend_list(Us,  nstypes)
        extend_list(mus, nstypes)
        self.sites = [ BoseSite(i,M,U,mu)
                       for i,(U,mu) in enumerate(zip(Us, mus)) ]

        ts = get_as_list(param, 't', 0.0)
        Vs = get_as_list(param, 'V', 0.0)
        nitypes = max(len(ts), len(Vs))
        extend_list(ts, nitypes)
        extend_list(Vs, nitypes)
        self.interactions = [ BoseBond(i, M, t, V)
                              for i,(t,V) in enumerate(zip(ts, Vs))]
        self.name = 'Bose-Hubbard model'

    def to_dict(self):
        return {'name' : self.name,
                'sites' : list(map(lambda x: x.to_dict(), self.sites)),
                'interactions' : list(map(lambda x: x.to_dict(), self.interactions)),
                }
