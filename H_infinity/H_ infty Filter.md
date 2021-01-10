# H_\infty Filter

## 12.1 Mixed Kalman / $H_\infty$

Kalman filter가 가지는 특징과 H infinity filter가 가지는 특징들을 합친 형태이다.

합치는 부분은 다양한 방법으로 진행할 수 있는데,

먼저 steady-state Kalman filter로 최소화된 cost function을 확인해보자.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled.png)

(12.1)

그리고 Steady state H infinity filter로 최소화 된 cost function을 보자.

($S_k$과 $L_k$는 identity matrix이다.)

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%201.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%201.png)

(12.2)

식을 보게 되면 각 필터가 가지는 특징을 확인할 수 있다.

- 칼만 필터는 estimation error의 RMS를 줄이는 방향으로 진행된다.
- H infinity 필터는 worst-case estimation error를 줄이는 방향으로 진행 된다.

기본적으로 H infinity filter는 w와 v라는 특성을 알지 못하는 noise가 만들 수 있는 maximun estimation error를 minimize 하려고 한다. 이에 따라 minmax filter라고도 불린다. 

 칼만필터의 식은 직관적으로 느껴지지만, H inifnity 필터는 직관적으로 느껴지지 않기 때문에 조금 더 이야기 해보자.

 worst case는 단순히 노이즈 값을 크게 만들면 된다. 즉, w와 v가 maximize 되면 estimation $\hat x$와 $x$값의 차이는 매우 커지게 된다. 이를  방지하기 위해서 cost function에서 w와 v의 합을 분모로 넣어준다. 그러면 노이즈 값이 매우 커져도 cost function 값 자체는 작아지는 방향으로 진행되기 때문이다. 

우리가 사용할 시스템은 n-state의 observable 한 LTI system이다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%202.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%202.png)

(12.3)

여기서 $\left\{w_{k}\right\}$ and $\left\{v_{k}\right\}$은 uncorrelated zero-mean 화이트 노이즈이며, 공분산 값은 $Q, R$이다.

Estimator 형태는 아래와 같다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%203.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%203.png)

(12.4)

$\hat F$는 stable matrix이며 estimator도 stable하다.

$H_\infty$ cost function은 우리가 정한 파라미터로 bounded 되어 있다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%204.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%204.png)

(12.5)

### Method

1. 칼만 gain을 찾기 위한 Riccati equation

    ![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%205.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%205.png)

    (12.6)

$P_a, V$의 경우 아래와 같이 정의 된다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%206.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%206.png)

(12.7)

  2.  Estimator에 사용 된 $\hat F$와 $K$  행렬을 구한다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%207.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%207.png)

(12.8)

3. $\hat F$가 stable 해야지만 mixed Kalman / $H_\infty$ estimation 문제를 만족한다. 그래야 상태에 대한 estimation error는 아래와 같은 제약 조건을 만족하게 된다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%208.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%208.png)

(12.9)

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%209.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%209.png)

(12.11)

기본적인 리카티 방정식 형태에서 (12.6) 앞선 시스템 식의 리카티 방정식을 정리하면 이와 같은 형태가 된다. 식의 해는 $K$  형태가 (12.12)와 같고 $P \geq 0,$$|1-K|<1$라면 $J_\infty$는 $1/\theta$로 bound 되고, state estimation error의 분산은 $P$ 값에 의해 bounded 된다. 

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2010.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2010.png)

(12.12)

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2011.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2011.png)

그래프에서는 bound parameter인 $\theta$값과 gain K와 performance 값에 대한 경향성을 보여준다. 

- bound parameter가 0인 경우($\theta=0$) 에 estimator gain 은 작다. $K \approx 0.62$. 이 경우는 일반적인 kalman filter라고 볼 수 있다. $\theta=0$인 경우에 $J_{\infty}$에서의 worst case performance에 대한 값은 없기 때문이다.
- 반대로 bound paramter를 증가할 경우 Kalman performance 자체는 안 좋아지지만, $\mathrm{H}_{\infty}$의 performance 는 worst case에 대한 방지를 하게 되면서 좋아진다.
- 기존에 단순히 $\mathrm{H}_{\infty}$ filter만 사용했을 경우 동일 $\theta$값에서 $K=1$이었다면, mixed filter에서는 $K=0.76$으로 결론적으로 단순 $\mathrm{H}_{\infty}$ filter보다 mixed filter의 성능이 더 좋은 것을 알 수 있다.

문제는 리카티 방정식을 푸는 게 쉽지 않기 때문에, 조금 더 직접적으로 접근하여 

hybrid filter gain이라는 걸 만들어서 사용하게 된다.

$K_2$는 steady-state Kalman filter gain이고 $K_\infty$는 steady-state H infilty gain이다. 

$$⁍ $$

- Hybrid filter gain은 두 필터의 convex combination이다. 이 gain은 앞서 말한 Kalman filter의 장점인 RMS를 줄이는 것과 H infinity filter의 장점인 worst-case performacne를 줄이는 것에 밸런스를 맞춰준다.
- 다만, stability가 numerical하게 확인되어야 하고, Kalman or $\mathrm{H}_{\infty}$ performance measures에 대한 이전 bound값을 알지 못하기 때문에 문제가 된다.

## 12.2 Robust H infinity filter

주어진 시스템 매트릭스에 오차(혹은 uncertainties)가 있을 경우에 사용된다.

$x_{k+1}=(F_k+\bigtriangleup F_k)x_k+w_k$

$y_k=(H_k+\bigtriangleup H_K)x_k+v_k$

여기서는 uncertainties를 아래와 같이 표현한다. 

$\begin{bmatrix}
\bigtriangleup F_k   \\
\bigtriangleup H_k  \\ 
\end{bmatrix}=\begin{bmatrix}
\bigtriangleup M_{1k}   \\
\bigtriangleup M_{2k}  \\ 
\end{bmatrix}\gamma_kN_k (\gamma_k\gamma_k^T<=I)$

감마 매트릭스는 알지 못하는 매트릭스지만, 위와 같은 bound 조건을 만족한다. 

시작하기 전에 몇가지 가정한다.

- $F_k$는 nonsingular 행령이다.
- 이 가정은 실제 시스템에서는 $F_k$가 항상 nonsigular해야 하는데,  matrix expoential의 경우 항상 non singular하고 이는 continuous time 시스템에서의 시스템 행렬로 구해지기 때문이다.
- state estimator의 형태는 아래와 같다.

    ![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2012.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2012.png)

    (12.17)

- state estimator는 3가지 특징을 가진다.
    1. estimator는 stable하다.
    2. estimator error $\tilde{x}_{k}$는 아래의 worst case bound를 만족한다.

    ![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2013.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2013.png)

    (12.18)

      3. estimator error $\tilde{x}_{k}$는 아래의 RMS bound를 만족한다.

    ![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2014.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2014.png)

    (12.19)

### Method

1. scalar 값인 $\alpha_{k}>0$과 $\epsilon>0$ 를 정한다.
2. 아래 행렬들을 정의한다

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2015.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2015.png)

(12.20)

  3. $P_k$와$\tilde{P}_{k}$를 아래와 같이 초기화 한다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2016.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2016.png)

(12.21)

  4. 리카티 방정식을 만족하는 Positive definite 한 $P_k$ 과$\tilde{P}_{k}$ 해를 구한다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2017.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2017.png)

(12.22)

  5. 이때 행렬 $R_{1 k}, R_{2 k}, F_{1 k}, H_{1 k},T_k$들은 아래와 같이 정의 된다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2018.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2018.png)

(12.23)

  6. 리카티 방정식 해가 아래 조건들을 만족하는지 확인한다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2019.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2019.png)

(12.24)

  7. 만족한다면 estimator 식을 아래 식들을 이용하여 푼다.

![H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2020.png](H_%20infty%20Filter%2055d64662cef1467d9e96942fa920cc18/Untitled%2020.png)

(12.25)

- 파라미터 $\epsilon$는 일반적으로 매우 작은 값으로 정한다. 반대로 $\alpha_{k}$값은 리카티 방정식 해 조건(12. 24)를 만족하기 위해 큰 값으로 정한다. (단, $\alpha_{k}$를 증가시키면, $P_k$값도 증가하게 되고 이는 RMS estimation error에 대한 boud값이 넓어지게 된다.)
- 위 방법에서 steady-state robust filter를 얻으려면, $P_{k+1}=P_{k}$으로 만들고 $\tilde{P}_{k+1}=\tilde{P}_{k}$으로 만들면 된다.

## Mixed Kalman / $H_\infty$ filtering

칼만 필터링과 $H_\infty$ 필터링의 장점들만 뽑아서 섞은 필터가 된다. 

steady-state kalman filter를 통해 cost function을 구하는 방법이 있다.

$$J_2=\lim_{x\to\infty}\sum_{k=0}^{N}E(\| x_k-\hat{x}_k\|_2 )$$

$H_\infty$ state estimator로도 cost function을 구할 수 있다.

이때 게임 이론 접근 방식을 사용했다는 내용이 있다.

칼만 필터는 RMS estimation error를 최소화하는 것을 찾고

$H_\infty$ 필터는 estimation error가 가장 안좋을 때를 최소화하는 방향으로 간다.  

관측 가능한 LTI 시스템의 objective function 2개 성능을 합친다. 

estimator는 $\hat{x}_{k+1}=\hat{F}x_k+Ky_k$ 이런 형태인데, 여기서 따르는 표준은

$F$ 는 stable한 매트릭스이고, $H_\infty$ cost function 은 $\theta$ (user-specified parameter)에 bounded 되어 있다고 본다.

$J_{\infty}<1/\theta$

위의 표준들을 만족하면서 필터가 칼만필터의 cost function인 $J_2$ 를 줄이는 방향으로 가야 한다. 

결국 worst-case estimation error에 bound 되면서도 RMS estimation error 중 가장 최적을 찾는 해가 나오게 된다. 

이 필터를 푸는 방법에 대해서 이야기 해보자.

1. 리카티 방정식을 만족하는 semi-definite한 행렬 $P$ ($n\times n$)을 찾는다.

 $P_a = FPH^T+FP(I/\theta^2-P)^{-1}PH^T$

$V=R+HPH^T+HP(I/\theta^2-P)^{-1}PH^T$

이런 형태로 나오는데 식을 보면 우리가 정하는 파라미터가 들어가 있는 걸 볼 수 있다.

$$⁍$$

$$⁍$$

이를 이용해 Kalman gain과 estimated system matrix를 구하게 된다.

이때 estimated system matrix는 stable해야 된다. 그래야 state estimation error가 bound 될 수 있다.

$$\lim_{x\to\infty}E(\| x_k-\hat{x}_k\|_2 )<=Tr(P)$$

위 리카티 방정식을 만족하는 $n \times n$ positive semidefinite한 P 행렬을 구한다.

model의 uncertainty가 있는 상태에서 사용된다. 

1. mixed kalman filter and h infinity estimation problem.
    - $H_\infty$ 는 worst case를, 칼만필터는 best case를 추정하므로 적당히 섞어서 하면 잘 된다.
2. robust 시스템에서 mixed kalman/H infinity estimation problem
    - 시스템 매트릭스에 추가적인 uncertainties.
3. constrained H infinity filter 

여기서 $\theta=0$ 이라면 단순 칼만필터다.

$\theta$를 키우면서 $H_\infty$ 필터를 얼마나 사용할지 정하게 된다. 

문제는 리카티 방정식을 푸는게 쉽지 않다. 따라서 hybrid filter gain을 만들어서 사용하게 된다.

$$⁍ $$

(convex optimization) 

### Robust H infinity filter

주어진 시스템 매트릭스에 오차(혹은 uncertainties)가 있을 경우에 사용된다.

$x_{k+1}=(F_k+\bigtriangleup F_k)x_k+w_k$

$y_k=(H_k+\bigtriangleup H_K)x_k+v_k$

여기서는 uncertainties를 아래와 같이 표현한다. 

$\begin{bmatrix}
\bigtriangleup F_k   \\
\bigtriangleup H_k  \\ 
\end{bmatrix}=\begin{bmatrix}
\bigtriangleup M_{1k}   \\
\bigtriangleup M_{2k}  \\ 
\end{bmatrix}\gamma_kN_k (\gamma_k\gamma_k^T<=I)$

감마 매트릭스는 알지 못하는 매트릭스지만, 위와 같은 bound 조건을 만족한다.