EE101A/Summer 2025

**Homework #4 Solutions\**
Due 11:59pm, July 20, 2025\
(Total: 78 points)

1.  **(24 points total) The DC equivalent circuit of a simple
    residential power distribution is shown below.**
    $\mathbf{R}_{\mathbf{w}}$ **represents the hot wire (typically
    black) resistance, and** $\mathbf{R}_{\mathbf{n}}$ **represents the
    neutral wire (typically white) resistance. The other resistances
    represent loads that are drawing power: *R*~1~ and *R*~2~ are loads
    on 120 V supplies while *R*~3~ is a load on a 240 V appliance such
    as a stove or a dryer.**

d

d

![d](.\media/media/image2.jpeg "A circuit, with resistances in ohms."){alt="The circuit has three loops, with the right segments of the left loops forming the left segment of the right loop. • Top-left loop: source = 12 volts, R sub w = 0.1, R sub 1 = 15, R sub n = 0.1 • Bottom-left loop: source = 120 volts, R sub n = 0.1, R sub 2 = 5, R sub w = 0.1 • Right loop: R sub 2 = 5 and R sub 1 = 15, no element, R sub 3 = 8, no element "
width="3.3068493000874892in" height="2.490764435695538in"}

(a) **If**
    $\mathbf{R}_{\mathbf{w}}\mathbf{=}\mathbf{R}_{\mathbf{n}}\mathbf{= 0.2\ \Omega}$**,**
    $\mathbf{R}_{\mathbf{1}}\mathbf{= 5\ \Omega}$**,**
    $\mathbf{R}_{\mathbf{2}}\mathbf{= 12\ \Omega}$**, and**
    $\mathbf{R}_{\mathbf{3}}\mathbf{= 13\ \Omega}$**, use mesh analysis
    to determine the voltage across each of the three loads. (12
    points)**

> Create three mesh loops (clockwise direction) for three currents.
> $i_{1}$in the top left, $i_{2}$in the bottom left, and $i_{3}$on the
> right-most loop. Using KVL around each loop, we can calculate:

![](.\media/media/image3.wmf)

> Note this can be written neatly in matrix form as:

$\begin{bmatrix}
\mathbf{R}_{\mathbf{w}}\mathbf{+}\mathbf{R}_{\mathbf{1}}\mathbf{+}\mathbf{R}_{\mathbf{n}} & \mathbf{-}\mathbf{R}_{\mathbf{n}} & \mathbf{-}\mathbf{R}_{\mathbf{1}} \\
\mathbf{-}\mathbf{R}_{\mathbf{n}} & \mathbf{R}_{\mathbf{w}}\mathbf{+}\mathbf{R}_{\mathbf{2}}\mathbf{+}\mathbf{R}_{\mathbf{n}} & \mathbf{-}\mathbf{R}_{\mathbf{2}} \\
\mathbf{-}\mathbf{R}_{\mathbf{1}} & \mathbf{-}\mathbf{R}_{\mathbf{2}} & \mathbf{R}_{\mathbf{1}}\mathbf{+}\mathbf{R}_{\mathbf{2}}\mathbf{+}\mathbf{R}_{\mathbf{3}}
\end{bmatrix}\begin{bmatrix}
\mathbf{i}_{\mathbf{1}} \\
\mathbf{i}_{\mathbf{2}} \\
\mathbf{i}_{\mathbf{3}}
\end{bmatrix}\mathbf{=}\begin{bmatrix}
\mathbf{120} \\
\mathbf{120} \\
\mathbf{0}
\end{bmatrix}$

> Plugging in the given values gives:

$\begin{bmatrix}
\mathbf{5.4} & \mathbf{-}\mathbf{0.2} & \mathbf{-}\mathbf{5} \\
\mathbf{-}\mathbf{0.2} & \mathbf{12.4} & \mathbf{-}\mathbf{12} \\
\mathbf{-}\mathbf{5} & \mathbf{-}\mathbf{12} & \mathbf{30}
\end{bmatrix}\begin{bmatrix}
\mathbf{i}_{\mathbf{1}} \\
\mathbf{i}_{\mathbf{2}} \\
\mathbf{i}_{\mathbf{3}}
\end{bmatrix}\mathbf{=}\begin{bmatrix}
\mathbf{120} \\
\mathbf{120} \\
\mathbf{0}
\end{bmatrix}$

> This can be solved swiftly using matrix inversion in MATLAB, or you
> can solve by hand: Multiply the second equation by 25 and subtract
> from the third equation to give $- 322i_{2} + 330i_{3} = - 3000$.
> Multiply the second equation by 27 and add to the first equation to
> give $334.6i_{2} - 329i_{3} = 3360$. From these last two equations, we
> can eliminate $i_{3}$ by multiplying the first by 329 and the second
> by 330 and adding the results. We get:

![](.\media/media/image4.wmf)

> Plugging this result back into either previous equation gives
> $i_{3} = \frac{279}{16}\text{ A.}$ We can then solve for the first
> loop current using any of the three original equations, and it is
> calculated that $i_{1} = \frac{315}{8}\text{ A.}$ To find the voltages
> across each load, we calculate:

$\mathbf{v}_{\mathbf{1}}\mathbf{=}\left( \mathbf{i}_{\mathbf{1}}\mathbf{-}\mathbf{i}_{\mathbf{3}} \right)\mathbf{R}_{\mathbf{1}}\mathbf{=}\left( \frac{\mathbf{315}}{\mathbf{8}}\mathbf{-}\frac{\mathbf{279}}{\mathbf{16}} \right)\left( \mathbf{5} \right)\mathbf{=}\frac{\mathbf{1755}}{\mathbf{16}}\mathbf{= 109.6875}\text{ V}\mathbf{
}$$$\mathbf{v}_{\mathbf{2}}\mathbf{=}\left( \mathbf{i}_{\mathbf{2}}\mathbf{-}\mathbf{i}_{\mathbf{3}} \right)\mathbf{R}_{\mathbf{2}}\mathbf{=}\left( \frac{\mathbf{435}}{\mathbf{16}}\mathbf{-}\frac{\mathbf{279}}{\mathbf{16}} \right)\left( \mathbf{12} \right)\mathbf{= 117}\text{ V}\mathbf{
}$$$\mathbf{v}_{\mathbf{3}}\mathbf{=}\mathbf{i}_{\mathbf{3}}\mathbf{R}_{\mathbf{3}}\mathbf{=}\left( \frac{\mathbf{279}}{\mathbf{16}} \right)\left( \mathbf{13} \right)\mathbf{=}\frac{\mathbf{3627}}{\mathbf{16}}\mathbf{= 226.6875}\text{ V.}$

(b) **If a wiring fault occurs such that the neutral becomes an open
    circuit, recalculate the voltages across the loads. (10 points)**

> Now we can just make $R_{n} = \infty$ and redo the loop analysis for
> the two remaining loops. Letting $i_{1}$be the clockwise current in
> the left-hand loop and $i_{2}$be the clockwise current in the
> right-hand loop, we can use KVL to find:

![](.\media/media/image5.wmf)

> Note this can be written neatly in matrix form as:

$\begin{bmatrix}
\mathbf{2}\mathbf{R}_{\mathbf{w}}\mathbf{+}\mathbf{R}_{\mathbf{1}}\mathbf{+}\mathbf{R}_{\mathbf{2}} & \mathbf{-}\mathbf{R}_{\mathbf{1}}\mathbf{-}\mathbf{R}_{\mathbf{2}} \\
\mathbf{-}\mathbf{R}_{\mathbf{1}}\mathbf{-}\mathbf{R}_{\mathbf{2}} & \mathbf{R}_{\mathbf{1}}\mathbf{+}\mathbf{R}_{\mathbf{2}}\mathbf{+}\mathbf{R}_{\mathbf{3}}
\end{bmatrix}\begin{bmatrix}
\mathbf{i}_{\mathbf{1}} \\
\mathbf{i}_{\mathbf{2}}
\end{bmatrix}\mathbf{=}\begin{bmatrix}
\mathbf{240} \\
\mathbf{0}
\end{bmatrix}$

> Plugging in the given values gives:

$\begin{bmatrix}
\mathbf{17.4} & \mathbf{-}\mathbf{17} \\
\mathbf{-}\mathbf{17} & \mathbf{30}
\end{bmatrix}\begin{bmatrix}
\mathbf{i}_{\mathbf{1}} \\
\mathbf{i}_{\mathbf{2}}
\end{bmatrix}\mathbf{=}\begin{bmatrix}
\mathbf{240} \\
\mathbf{0}
\end{bmatrix}$

> This can be solved swiftly using matrix inversion in MATLAB, or you
> can solve by hand: Multiply the first equation by 17 and the second by
> 17.4, and add the two equations. We get:$233i_{2} = 4080$, so
> $i_{2} = \frac{4080}{233} \approx 17.51\text{ A}$. Plugging back into
> either equation we can determine that
> $i_{1} = \frac{7200}{233} \approx 30.9\text{ A}$. To find the voltages
> across each load, we calculate:

$\mathbf{v}_{\mathbf{1}}\mathbf{=}\left( \mathbf{i}_{\mathbf{1}}\mathbf{-}\mathbf{i}_{\mathbf{2}} \right)\mathbf{R}_{\mathbf{1}}\mathbf{=}\left( \frac{\mathbf{7200}}{\mathbf{233}}\mathbf{-}\frac{\mathbf{4080}}{\mathbf{233}} \right)\left( \mathbf{5} \right)\mathbf{=}\frac{\mathbf{15600}}{\mathbf{233}}\mathbf{\approx 66.95}\text{ V}\mathbf{
}$$$\mathbf{v}_{\mathbf{2}}\mathbf{=}\left( \mathbf{i}_{\mathbf{1}}\mathbf{-}\mathbf{i}_{\mathbf{2}} \right)\mathbf{R}_{\mathbf{2}}\mathbf{=}\left( \frac{\mathbf{7200}}{\mathbf{233}}\mathbf{-}\frac{\mathbf{4080}}{\mathbf{233}} \right)\left( \mathbf{12} \right)\mathbf{=}\frac{\mathbf{13337}}{\mathbf{83}}\mathbf{\approx 160.69}\text{ V}\mathbf{
}$$$\mathbf{v}_{\mathbf{3}}\mathbf{=}\mathbf{i}_{\mathbf{2}}\mathbf{R}_{\mathbf{3}}\mathbf{=}\left( \frac{\mathbf{4080}}{\mathbf{233}} \right)\left( \mathbf{13} \right)\mathbf{=}\frac{\mathbf{19577}}{\mathbf{86}}\mathbf{\approx 227.64}\text{ V.}$

(c) **Postulate what might happen to a sensitive device represented by
    *R*~2~ if it is plugged into this faulty circuit. (2 points)**

> Rather than seeing the expected potential of 120 volts, the load now
> sees over 160 volts. This is quite possibly much too high and not
> within the expected tolerance of a sensitive device placed as a load.
> Overvoltage such as this can often damage componentry and cause
> devices to fail.

2.  **(10 points total) Calculate *v~x~* in the circuit below using
    superposition.**

> ![](.\media/media/image32.jpeg)![](.\media/media/image7.jpeg){width="5.544215879265092in"
> height="2.6034645669291336in"}

**4*i~x~***

***+***

***v~x~***

**~−~**

![***i~x~***](.\media/media/image8.png){width="3.0661712598425197in"
height="1.5in"}

First, we start by examining the contributions to *v~x~* from each
independent source acting alone. Recall that the dependent source is
[not]{.underline} zeroed out and must remain as part of the analysis for
each of three sources we examine. First, consider the 1-amp source
acting alone. The other current source becomes an open circuit, and the
3-volt source becomes a short. The circuit looks like:\
\
KCL at the top node gives $\text{1 A} = i_{x} + \frac{v_{x}}{10}$ . KVL
around the outer loop gives $v_{x} + 4i_{x} - i_{x}(1) = 0$. Eliminating
$i_{x}$
gives$\text{1 A} = - \frac{v_{x}}{3} + \frac{v_{x}}{10} = - \frac{7}{30}v_{x}$
and $v_{x} = - \frac{30}{7}\text{ V.}$ Next, consider the 2-amp source
acting alone. Again, the other current source is an open circuit, and
the 3-volt source becomes a short. The circuit looks like:

***i~x~***

***+***

***v~x~***

**~−~**

**4*i~x~***

***+***

***v~x~***

**~−~**

***i~x~***

**4*i~x~***

![](.\media/media/image9.png){width="3.0661712598425197in"
height="1.5in"}![](.\media/media/image10.png){width="2.7480916447944006in"
height="1.5in"}

KCL at the top node gives $\text{2 A} = i_{x} + \frac{v_{x}}{10}$ . KVL
around the outer loop gives $v_{x} + 4i_{x} - i_{x}(1) = 0$. Eliminating
$i_{x}$
gives$\text{2 A} = - \frac{v_{x}}{3} + \frac{v_{x}}{10} = - \frac{7}{30}v_{x}$
and $v_{x} = - \frac{60}{7}\text{ V.}$ Next, consider the 3-volt source
acting alone. Both current sources are open circuits; the circuit looks
like:\
\
KVL around the loop gives $i_{x}(1) - 4i_{x} - v_{x} - 3 = 0$, and we
can invoke Ohm's law since we know the current flowing through the 10Ω
resistor is $- i_{x}$ (recall the PSC): $v_{x} = - i_{x}(10)$.
Eliminating $i_{x}$ gives: $\frac{3v_{x}}{10} - v_{x} - 3 = 0$ so
$v_{x} = - \frac{30}{7}\text{ V.}$ Leveraging the rule of superposition,
we can sum all three contributions together to find the total voltage:
$v_{x} = - \frac{30}{7} - \frac{60}{7} - \frac{30}{7} = - \frac{120}{7} \approx - 17\text{ V}$
(well, maybe −17.1 V!).

3.  **(16 points total) Consider the circuit shown below. An ammeter
    with an internal resistance of *R~i~* is used to measure the current
    flowing through a 2 kΩ resistor between points *a* and *b*.**

![6](.\media/media/image11.jpeg){width="5.198323490813649in"
height="1.9538910761154855in"}

(a) How should the ammeter be connected between *a* and *b*? Show a
    sketch of the circuit (only include the portion between *a* and *b*)
    which includes the ammeter with its internal resistance. (3 points)

    The ammeter should be connected in series with the load resistor
    across *a* and *b* through which the current is to be measured, and
    it will look like the following:\
    ![](.\media/media/image12.png){width="0.6037150043744532in"
    height="2.2998950131233595in"}

(b) Find the Thévenin equivalent circuit at terminals *a* and *b*
    (without the 2 kΩ load). (5 points)

    To find the Thévenin resistance, we zero out all independent
    sources: the current source becomes an open circuit and the voltage
    source becomes a short circuit.

    ![](.\media/media/image13.wmf)

    To find the Thévenin voltage, consider the following representation
    of the circuit:\
    ![](.\media/media/image14.png){width="4.865324803149607in"
    height="1.4725929571303586in"}\
    First, convince yourself that no current can flow through the 6 kΩ
    resistor, so the voltage across it must be 0 V. Then the open
    circuit voltage from *a* to *b* is the voltage drop across the
    current source (value of $(4)(30) = 120\text{ V}$) and the negative
    of the voltage divider across the 20 kΩ resistor due to the 60 V
    source (value of $60\frac{20}{20 + 5} = 48\text{ V}$) so
    $V_{\text{th}} = 120 - 0 - 48 = 72\text{ V}$. The Thévenin
    equivalent circuit looks like:

    ![](.\media/media/image15.png){width="1.8878477690288713in"
    height="1.28498687664042in"}

(c) Find the Norton equivalent circuit at terminals *a* and *b* (without
    the 2 kΩ load). (3 points)

    With the Thévenin equivalent already calculated, this is
    straightforward.
    $I_{N} = \frac{V_{\text{th}}}{R_{\text{th}}} = \frac{72\text{ V}}{40\text{ k}\Omega} = 1.8\text{ mA}$
    and $R_{N} = R_{\text{th}} = 40\text{ k}\Omega$. The Norton
    equivalent circuit looks like:\
    ![](.\media/media/image16.png){width="2.1887423447069114in"
    height="1.4in"}

(d) What is the ammeter reading if
    $\mathbf{R}_{\mathbf{i}}\mathbf{= 300\ \Omega}$? (3 points)

    This question is simple if we already have the Thévenin equivalent.
    We just use Ohm's law:
    $V_{\text{th}} = IR_{\text{tot}} = I\left( R_{\text{th}} + R_{i} + R_{L} \right)$
    so

    $\mathbf{I =}\frac{\mathbf{V}_{\text{th}}}{\mathbf{R}_{\text{th}}\mathbf{+}\mathbf{R}_{\mathbf{i}}\mathbf{+}\mathbf{R}_{\mathbf{L}}}\mathbf{=}\frac{\mathbf{72}\text{ V}}{\left( \mathbf{40 + 0.3 + 2} \right)\text{ k}\mathbf{\Omega}}\mathbf{= 1.7}\text{ mA.}$

(e) What is the reading if
    $\mathbf{R}_{\mathbf{i}}\mathbf{= 0\ \Omega}$? (2 points)

> Now we have:

$\mathbf{I =}\frac{\mathbf{V}_{\text{th}}}{\mathbf{R}_{\text{th}}\mathbf{+}\mathbf{R}_{\mathbf{i}}\mathbf{+}\mathbf{R}_{\mathbf{L}}}\mathbf{=}\frac{\mathbf{72}\text{ V}}{\left( \mathbf{40 + 0 + 2} \right)\text{ k}\mathbf{\Omega}}\mathbf{= 1.71}\text{ mA.}$

> Note that this is not a significant deviation, and in general will not
> be as long as the internal resistances are kept much lower than the
> loads through which we wish to measure current flow.

4.  **(18 points total) Use source transformations to find the voltage
    *V~o~* in the circuit below.**

> ![](.\media/media/image17.png){width="5.215972222222222in"
> height="2.5821576990376203in"}

***+***

***V~o~***

![**~−~**](.\media/media/image18.png){width="5.346749781277341in"
height="1.2212981189851269in"}

We first transform the 3-volt source with the 2 Ω series resistance into
its Norton equivalent with a Norton source current of
$\frac{3\text{ V}}{2\ \Omega} = 1.5\text{ A}$, and a Norton resistance
of 2 Ω. Simultaneously, we can transform the 4-volt source with the 5 Ω
series resistance into its Norton equivalent with a Norton source
current of $\frac{\text{4 V}}{\text{5 }\Omega} = 0.8\text{ A}$, and a
Norton resistance of 5 Ω. Note the polarity of the two sources are
different, so the Norton current sources will be pointing in different
directions! The resulting circuit looks like:\
\
We can simplify the circuit considerably by combining the current
sources since they are in parallel to form a
$1 + 1.5 - 0.8 = 1.7\text{ A}$source. We can also combine the three
parallel resistors with a single resistor of value
$\frac{(2)(5)(6)}{(2)(5) + (2)(6) + (5)(6)} = \frac{60}{52} = \frac{15}{13}\ \Omega$.
The simplified circuit looks like:

***+***

***V~o~***

**~−~**

**Ω**

**V**

***+***

***V~o~***

**~−~**

**Ω**

![](.\media/media/image19.png){width="2.575851924759405in"
height="1.177020997375328in"}![](.\media/media/image20.png){width="2.1950470253718284in"
height="1.1167530621172352in"}

The next step is to apply another source transformation to a Thévenin
equivalent with a Thévenin voltage source of
$(1.7)\frac{15}{13} = \frac{51}{26}\text{ V}$with a Thévenin resistance
of $\frac{15}{13}\ \Omega$. The result looks like:\
\
The result is a simple voltage divider. We can easily find the voltage
across the 8 Ω resistor as:

$\mathbf{V}_{\mathbf{o}}\mathbf{=}\frac{\mathbf{51}}{\mathbf{26}}\frac{\mathbf{8}}{\mathbf{8 +}\frac{\mathbf{15}}{\mathbf{13}}\mathbf{+ 7}}\mathbf{=}\frac{\mathbf{34}}{\mathbf{35}}\text{ V.}$

5.  **(10 points total) A typical CR2032 3V coin-style battery (often
    used in watches or small electronic devices) has an internal source
    resistance *R~s~* of about 17 Ω (seriously!) at room temperature.
    (While this value typically increases as the battery is depleted, we
    will consider it constant for this problem.)**

$R_{s}$

*I~L~*

![$V_{\text{batt}}$](.\media/media/image21.jpeg "Two circuits."){alt="a. Original circuit with load. The two-terminal circuit has sources and resistances, including R sub L. b. A single-loop Thevenin equivalent circuit with load, with i sub L clockwise: V sub t, R sub t, terminal, R sub L, terminal. "
width="2.8315069991251094in" height="1.6794520997375328in"}

(a) Using this battery, what is the peak current that could be driven
    through an external load *R~L~*? What is *R~L~* in this scenario? (2
    points)

    The current is $I_{L} = \frac{V_{\text{batt}}}{R_{s} + R_{L}}$, and
    to make this as large as possible, we make the numerator as small as
    possible. With $R_{s}$ fixed, we make $R_{L} = 0$ so
    $I_{L} = \frac{V_{\text{batt}}}{R_{s}} = \frac{3\text{ V}}{17\ \Omega} = 176\text{ mA}$.

(b) Using this battery, what is the peak power that could be delivered
    through an external load *R~L~*? What is *R~L~* in this scenario? (4
    points)

    Maximum power transfer occurs when $R_{L} = R_{s} = 17\ \Omega$, and
    the value of the power is
    $\frac{{V_{L}}^{2}}{R_{L}} = \frac{\left( V_{\text{batt}}\frac{R_{L}}{R_{L} + R_{s}} \right)^{2}}{R_{L}} = \frac{{V_{\text{batt}}}^{2}R_{L}}{\left( R_{L} + R_{s} \right)^{2}} = \frac{{V_{\text{batt}}}^{2}}{4R_{s}} = \frac{3^{2}}{4(17)} = 132\text{ mW}$.

(c) Plot the power delivered to *R~L~* as a function of *R~L~*, from 0
    to 500 Ω. (4 points)

    In the previous part, we derived the formula for the power
    dissipated in the load as:

    $\mathbf{P}_{\mathbf{L}}\mathbf{=}\frac{{\mathbf{V}_{\mathbf{L}}}^{\mathbf{2}}}{\mathbf{R}_{\mathbf{L}}}\mathbf{=}\frac{{\mathbf{V}_{\text{batt}}}^{\mathbf{2}}\mathbf{R}_{\mathbf{L}}}{\left( \mathbf{R}_{\mathbf{L}}\mathbf{+}\mathbf{R}_{\mathbf{s}} \right)^{\mathbf{2}}}\mathbf{=}\frac{\mathbf{9}\mathbf{R}_{\mathbf{L}}}{\left( \mathbf{R}_{\mathbf{L}}\mathbf{+ 17} \right)^{\mathbf{2}}}$\
    this can be plotted using MATLAB or some equivalent graphing
    program; the figure is shown below.\
    ![](.\media/media/image22.png){width="5.608358486439195in"
    height="4.206268591426071in"}\
    Note the peak occurs at 17 Ω, as we expect. The power delivered to
    the load rolls off to zero as $R_{L}$ goes to zero.
