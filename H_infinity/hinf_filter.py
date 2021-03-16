import numpy as np


class HinfFilter:
    def __init__(self, x, P):
        """
        Args:
            x (numpy.array): state to estimate: [x_, y_, theta]^T
            P (numpy.array): estimation error covariance = error covariance
        """
        self.x = x  # [3,]
        self.P = P  # [3, 3]

    def update(self, z, Q, R):
        S = self.P
        L = np.eye(3)
        S_bar = L@S@L.T
        gamma = 0.025
        I  = np.eye(3)
        print("gamma : ", gamma)
        H = np.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 0.]
        ])  # Jacobian of observation function
        P_bar = I-gamma*S_bar@self.P+H.T@np.linalg.inv(R)@H@self.P
        K = self.P@np.linalg.inv(P_bar)@H.T@np.linalg.inv(R)
        satisfaction = np.linalg.inv(S)-gamma*S_bar+H.T@np.linalg.inv(R)@H
        if np.linalg.norm(satisfaction)<=0:
            print("not satisfied", np.linalg.norm(satisfaction))
        # nu  = z -H@self.x
        # Pinf = np.linalg.inv(I-(Q/gamma/gamma)+self.P@H.T@H)@Qbar;
        # Qbar = Pinf + Q
        #L = np.linalg.inv(I-(Q/gamma/gamma)@self.P + H.T@np.linalg.inv(Q)@H@self.P) 
        #K = self.P @ L @H.T@np.linalg.inv(Q)
        #K = Pinf@H.T

        # update state 
        x, y, theta = self.x
        z_ = np.array([x, y, theta])  # expected observation from the estimated state
        self.x = self.x + K @ (z - z_)

        # update covariance P
        self.P = self.P - K @ H @ self.P

    def propagate(self, u, dt, R):
        """propagate x and P based on state transition model defined as eq. (5.9) in [1]
        Args:
            u (numpy.array): control input: [v, omega]^T
            dt (float): time interval in second
            R (numpy.array): state transition noise covariance
        """
        # propagate state x
        x, y, theta = self.x
        v, omega = u
        r = v / omega  # turning radius

        dtheta = omega * dt
        dx = - r * np.sin(theta) + r * np.sin(theta + dtheta)
        dy = + r * np.cos(theta) - r * np.cos(theta + dtheta)

        self.x += np.array([dx, dy, dtheta])

        self.P = self.P + R