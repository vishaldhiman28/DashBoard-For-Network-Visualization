import numpy as np

def to_numpy_array(G):
    nodelist=None
    multigraph_weight = sum
    nonedge=0.0
    weight='weight'

    if nodelist is None:
        nodelist = list(G)
    nodeset = set(nodelist)
    if len(nodelist) != len(nodeset):
        msg = "Ambiguous ordering: `nodelist` contained duplicates."

    nlen = len(nodelist)
    undirected = True
    index = dict(zip(nodelist, range(nlen)))

    # Graph or DiGraph, this is much faster than above
    A = np.full((nlen, nlen), np.nan, order=order)
    for u, nbrdict in G.adjacency():
        for v, d in nbrdict.items():
            try:
                A[index[u], index[v]] = d.get(weight, 1)
            except KeyError:
                # This occurs when there are fewer desired nodes than
                # there are nodes in the graph: len(nodelist) < len(G)
                pass
    A[np.isnan(A)] = nonedge
    A = np.asarray(A)
    return A

def _fruchterman_reingold(A, k, pos, fixed, iterations,
                          threshold, dim, seed):

    # Position nodes in adjacency matrix A using Fruchterman-Reingold
    # Entry point for NetworkX graph is fruchterman_reingold_layout()

    nnodes, _ = A.shape
    if pos is None:
        # random initial positions
        pos = np.asarray(np.random.RandomState(seed).rand(nnodes, dim), dtype=A.dtype)
 

    # optimal distance between nodes
    if k is None:
        k = np.sqrt(1.0 / nnodes)

    # the initial "temperature"  is about .1 of domain area (=1x1)
    # this is the largest step allowed in the dynamics.
    # We need to calculate this in case our fixed positions force our domain
    # to be much bigger than 1x1

    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1])) * 0.1
    
    # simple cooling scheme.
    # linearly step down by dt on each iteration so last iteration is size dt.

    dt = t / float(iterations + 1)
    delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)
    # the inscrutable (but fast) version
    # this is still O(V^2)
    # could use multilevel methods to speed this up significantly
    for iteration in range(iterations):
        # matrix of difference between points
        delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        # distance between points
        distance = np.linalg.norm(delta, axis=-1)
        # enforce minimum distance of 0.01
        np.clip(distance, 0.01, None, out=distance)
        # displacement "force"
        displacement = np.einsum('ijk,ij->ik',
                                 delta,
                                 (k * k / distance**2 - A * distance / k))
        # update positions
        length = np.linalg.norm(displacement, axis=-1)
        length = np.where(length < 0.01, 0.1, length)
        delta_pos = np.einsum('ij,i->ij', displacement, t / length)
        if fixed is not None:
            # don't change positions of fixed nodes
            delta_pos[fixed] = 0.0
        pos += delta_pos
        # cool temperature
        t -= dt
        err = np.linalg.norm(delta_pos) / nnodes
        if err < threshold:
            break
        
return pos


def fruchterman_reingold_layout(G,k,iterations,weight='weight'):
    fixed=None
    pos=None
    scale=1
    center=None
    seed=None
    threshold=1e-4
    pos=None
    dim=2
    
    if center is None:
        center = np.zeros(dim)

    if len(center) != dim:
        msg = "[Error]: The length of center coordinates must match dimension of layout."
        raise ValueError(msg)

    pos_arr = None
    dom_size = 1

    if len(G) == 0:
        return {}

    # Sparse matrix
    if len(G) < 500:  
        A = to_numpy_array(G, weight=weight)
        pos = _fruchterman_reingold(A, k, pos_arr, fixed, iterations,
                                    threshold, dim, seed)
    if fixed is None and scale is not None:
        pos = rescale_layout(pos, scale=scale) + center
    pos = dict(zip(G, pos))
    return pos

