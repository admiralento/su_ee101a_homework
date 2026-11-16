# Concept tags

The vocabulary of concept tags used by the question bank. Each question lists its tags on the
`Concepts:` line near the top of its `version_history.md`, for example:

    Concepts: diode-models, load-line, datasheet

How to maintain this file:
- **Add a tag:** add a line `` - `tag-id` — description `` under the right heading. Tag ids are
  lowercase words joined by `-`. The heading groups tags in the catalog's concept index.
- **Rename a tag:** `python tools/check.py --rename-tag old-id new-id` (updates this file and every
  question), then `python tools/check.py --catalog`.
- **Remove a tag:** delete its line here; `tools/check.py` then lists the questions still using it.
- Headings can be renamed or reordered freely; they only affect how the index is grouped.

## 1. Course Introduction
- `lab-safety` — Lab and soldering safety training

## 2. Circuit Abstraction
- `circuit-quantities` — Charge, current, voltage and their relationships (incl. drift velocity)
- `power-energy` — Power and energy, passive sign convention, power balance (Tellegen)
- `resistance-resistivity` — Resistivity, wire resistance, temperature coefficient
- `resistor-color-code` — Reading resistor color codes and tolerances
- `circuit-topology` — Counting nodes, branches, loops; series and parallel elements
- `rms-waveforms` — Periodic waveforms: amplitude, frequency, RMS value

## 3. Resistive Networks
- `kcl-kvl` — Kirchhoff's laws and Ohm's law on a whole circuit
- `series-parallel` — Series/parallel combination, voltage and current dividers
- `equivalent-resistance` — Equivalent resistance of networks (series/parallel reduction, symmetry)
- `nodal-analysis` — Node-voltage analysis
- `mesh-analysis` — Mesh-current analysis
- `wye-delta` — Wye–delta transformations
- `dependent-sources` — Circuits with controlled sources
- `standard-resistor-values` — Choosing standard (E24) resistor values

## 4. Network Theorems
- `superposition` — Superposition
- `source-transformation` — Source transformations
- `thevenin-norton` — Thévenin and Norton equivalents
- `max-power-transfer` — Maximum power transfer and source resistance
- `instrument-loading` — Models of meters, function generators and probes, and their loading effects
- `ideal-transformer` — Ideal transformers and resistance transformation

## 5. Diode Circuits
- `diode-physics` — pn junction: doping, carriers, depletion region
- `diode-models` — Ideal, constant-drop and exponential diode models
- `load-line` — Graphical load-line analysis
- `diode-temperature` — Temperature dependence of diodes, derating, thermal runaway
- `zener-regulator` — Zener diodes and voltage regulation
- `led` — Light-emitting diodes
- `rectifiers` — Half- and full-wave rectifiers
- `diode-small-signal` — Linearized (piecewise-linear and small-signal) diode models

## 6. Energy Storage Elements
- `capacitors` — Capacitor i–v relation, stored energy
- `inductors` — Inductor i–v relation, stored energy
- `capacitor-networks` — Series/parallel capacitor networks at DC steady state
- `first-order-transients` — RC and RL step responses

## 7. MOSFETs
- `mosfet-iv` — MOSFET i–v characteristics and operating regions
- `mosfet-process` — Process parameters: C_ox, k', W/L, channel resistance
- `mosfet-dc-bias` — DC bias point analysis
- `pmos` — PMOS devices and sign conventions
- `diode-connected-mosfet` — Diode-connected transistors

## 8. DC and AC Analysis of MOSFET Amplifiers
- `transfer-characteristic` — Voltage transfer characteristic and bias point
- `small-signal-model` — Small-signal model: g_m, r_o, equivalent circuits
- `signal-swing` — Allowed signal swing and distortion limits
- `channel-length-modulation` — Channel-length modulation (λ, V_A, r_o)

## 9. Single-Stage MOSFET Amplifiers
- `amplifier-models` — Amplifier models: gain, input and output resistance
- `common-source` — Common-source amplifiers
- `common-drain` — Common-drain (source-follower) amplifiers
- `common-gate` — Common-gate amplifiers
- `multistage-amplifiers` — Cascaded / multistage amplifiers
- `amplifier-bandwidth` — Amplifier frequency response, cutoff frequencies and gain–bandwidth trade-off
- `source-degeneration` — Source degeneration and linearity

## 10. Sinusoidal Circuit Analysis
- `complex-numbers` — Complex numbers: Cartesian, polar and Euler forms
- `phasors-impedance` — Phasors, impedance and admittance
- `transfer-functions` — Frequency response and transfer functions
- `bode-plots` — Bode magnitude and phase plots
- `filters` — First-order filters and corner frequency
- `resonance` — RLC resonance

## Skills and format
- `design` — Open-ended design with constraints or bounds
- `datasheet` — Requires reading a datasheet or part search
- `measurement` — Lab context or interpreting measurements
- `conceptual` — Mostly conceptual / explanation
- `software` — Requires plotting or numerical software (MATLAB, Excel, solvers)
- `symbolic` — Symbolic derivation
- `application` — Real-world application scenario
