# -*- coding: utf-8 -*-
import numpy as np
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


    def predict(self, u=0):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x

    def update(self, z):
        nu = y - np.dot(self.H, self.x)  # residual
        S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # kalman gain
        self.x = self.x + np.dot(K, y)  # stat update
        I = np.eye(self.n)
        self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P), (I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R),

def define_problem(head_ang):
    dt = 0.03 #need to be changed
    F = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
    H = np.array([0, 0, dt*m.sin(head_ang), dt*m.cos(head_ang)]).reshape(1, 4)
    Q = np.diag([4, 4, 1, 1])
    R = np.diag([900, 900])


if __name__ == '__main__':






