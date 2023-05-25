import numpy as np

def extended_tdoa(mic_positions, r12, r13, r14, r23, r24, r34):
    p1, p2, p3, p4 = mic_positions
    A = np.array([
        [2 * (p2 - p1).T[0], -2 * r12, 2 * (p3 - p1).T[0], -2 * r13, 2 * (p4 - p1).T[0], -2 * r14],
        [2 * (p3 - p2).T[0], -2 * r23, 2 * (p4 - p2).T[0], -2 * r24, 0, 0],
        [0, 0, 2 * (p4 - p3).T[0], -2 * r34, 0, 0]
    ])
    b = np.array([
        r12**2 - np.linalg.norm(p1)**2 + np.linalg.norm(p2)**2,
        r13**2 - np.linalg.norm(p1)**2 + np.linalg.norm(p3)**2,
        r14**2 - np.linalg.norm(p1)**2 + np.linalg.norm(p4)**2,
        r23**2 - np.linalg.norm(p2)**2 + np.linalg.norm(p3)**2,
        r24**2 - np.linalg.norm(p2)**2 + np.linalg.norm(p4)**2,
        r34**2 - np.linalg.norm(p3)**2 + np.linalg.norm(p4)**2
    ])
    x = np.linalg.lstsq(A, b, rcond=None)[0]
    return x