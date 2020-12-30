# Kalman Filter Tutorial

A Kalman Filter, in essence, is a state estimation technique for noisy measurements. By implementing ‘Prediction’ and ‘Correction’ steps for each timestep, the Kalman Filter produces an unbiased and consistent estimate for normally distributed samples making it BLUE (best linear unbiased estimator).

* Unbiased: the average error is zero at a particular time step, k, over many trials

* Consistent: the filter covariance, Pk, is equal to the expected value of the square of the error

To implement a Kalman Filter, we need to have 3 things.

* A linear model of our system (motion model);

* A measurement model that relates our measurements, y, and our state variable, x;

* And covariance estimates of noise in the motion and measurement models. (Q and R respectively)

### Some book-keeping:

We denote our state variable (i.e. what we are interested in) as x and our measurement as y. Ideally we want to measure the state variables directly, but often times this is not possible, hence the need for a measurement model that relates the two.

We may be interested in multiple variables such as position and velocity, so we express the state as a vector.

$$\bold{x}_{k}=
\begin{bmatrix}
p_{k}\\v_{k}
\end{bmatrix}$$

In most applications of the Kalman Filter, we want some way of controlling the state variables. We do this via a control input, $u$, that updates the state in the motion model.

From this, we obtain:

$$\bold{x}_{k} = \bold{F}_{k}\bold{x}_{k-1} + \bold{B}_{k}\bold{u}_{k}$$

The state variables that we are interested in are often related to one another and we can show the correlation by a covariance matrix P:

­­­___

## Prediction Step

We really need an example to explain the Kalman Filter and the typical textbook example is a 1D cart system. The motion of the cart when no force is applied to it can be modelled by simple SUVAT equations.
$$
p_{k} = p_{k-1} + v_{k}t\\
v_{k} = v_{k-1}
$$

Let’s say we’re interested in the position and velocity of the cart and we can control the position and velocity by applying a force F to the cart with mass m. We can relate F to acceleration, so we rewrite our motion model in vector form as below:

­­­$$
\bold{x}_{k}=\begin{bmatrix}1&dt\\0&1\end{bmatrix}\bold{x}_{k-1} + \begin{bmatrix}dt^2/2\\dt\end{bmatrix}\bold{u}_{k}
$$

Every timestep we introduce uncertainty in our model because we know our idealised linear model of the world isn’t perfect. We account for this by adding $\bold{Q}$ to our covariance matrix $\bold{P}$.

Now that we have an estimate of the state variables in the next time step, we can estimate what measurements we expect to obtain with the measurement model. We denote the expected measurement value as $µ_{expected}$ and the expected uncertainty as $Σ_{expected}$.

As we’re relying on a predefined model to predict how our model will react to control inputs u, we call the above process the ‘Prediction’ step.

## Correction Step
If we relied on the motion model alone, you can see that the covariance matrix will increase due to added uncertainties in every timestep.

Hence, we need a correction step that can somehow reduce the uncertainty of our state estimates from the motion model.

The measurements we obtain from a sensor has mean, $µ$, and variance, $Σ$.

We combine the two Gaussian estimates by simply multiplying the two together, to achieve the corrected measurements that have a much small covariance. One thing you should also note is that the product of two Gaussians is a Gaussian, so we can obtain $µ_{corrected}$ and $Σ_{corrected}$

In matrix form,
$$
\hat\mu=\mu_{0}+\dfrac{\sigma_{0}^2(\mu_{1}-\mu_{0})}{\sigma_{0}^{2}+\sigma_{1}^{2}} \\
\hat\sigma^2=\sigma_{0}^2-\dfrac{\sigma_{0}^{4}}{\sigma_{0}^{2}+\sigma_{1}^2}
$$

$$
k = \dfrac{\sigma_{0}^{2}}{\sigma_{0}^2+\sigma_{1}^2} \\
\hat\mu=\mu_{0}+k(\mu_{1}-\mu_{0}) \\
\hat\sigma=\sigma_{0}^2-k\sigma_{0}^2
$$
