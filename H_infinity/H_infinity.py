# -*- coding: utf-8 -*-
import numpy as np
from numpy.linalg import inv
import math as m
import matplotlib as plt

class HInfinityFilter:
    def __init__(self, gamma, F=None, B=None, H=None, D=None, P=None, Q=None, R=None, x0=None):
        self.n = F.shape[1]
        self.m = H.shape[1]

        self.F = F
        self.H = H
        self.B = 0 if B is None else Q
        self.D = 0 if D is None else D
        self.P = np.eye(self.n)        if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0
        self.gamma = gamma

        self.Q = np.eye(self.n) if Q is None else Q   # process noise covariance
        self.R = np.eye(self.n) if R is None else R    # measurement noise covariance
        self.Q_sqrt = np.sqrt(self.Q)    # (m, m, m/sce, m/sec)
        self.R_sqrt = np.sqrt(self.R)    # (m, m)

        self.theta = m.pi/3              # heading angle (Measured CCW from east)
        self.tan_theta = m.tan(self.theta)

        #for visualize
        self.xarray = []
        self.xhatarray = []


    def k_predict(self, u):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x

    def k_update(self, z):
        nu = z - np.dot(self.H, self.x)  # residual
        S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # kalman gain
        self.x = self.x + np.dot(K, nu)  # stat update
        I = np.eye(self.n)
        self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P), (I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R),

    def h_predict(self, u):
        ##

    def h_update(self, z):

def define_problem():
    head_ang = m.pi/3
    tan_theta = m.tan(head_ang)
    gamma = 40
    dt = 1 #need to be changed
    F = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]]) # system matrix
    B = np.array([0, 0, dt*m.sin(head_ang), dt*m.cos(head_ang)]).reshape(1, 4) # Input matrix
    Q = np.diag([4, 4, 1, 1]) # process noise covariance
    R = np.diag([900, 900]) # measurement noise covariance
    R_sqrt = np.sqrt(R)
    H = np.array([[1,0, 0, 0],[0, 1, 0, 0]]) + inv(R_sqrt)#Normarlized measurement matrix
    D = 0

    AccelDecelFalg = 1

    P = np.diag([900, 900, 4, 4])
    Qbar = P # estimation error covariance for H inf
    Qtilde = P # estimation error covariance for H inf

    x = np.array([0, 0, tan_theta, 1]).reshape(1, 4)
    h_inf = HInfinityFilter(gamma=gamma, F = F, B = B, H = H, D = D, P = P, Q = Q, R = R)
    for dt in range(0,120,1):
        z = H * x # get the noise-corrupted measurement
        MeasErr = np.randn(z.size)
        z = z + MeasErr
        if AccelDecelFalg == 1:
            if x(3) > 30 or x(4) > 30:
                AccelDecelFalg = -1
        else:
            if x(3) < 5 or x(4) < 5:
                AccelDecelFalg = -1
        u = 1 * AccelDecelFalg
        h_inf.k_predict(u)
        h_inf.k_update(z)


    Pinf = inv(np.eye(4) - Qbar)






if __name__ == '__main__':






