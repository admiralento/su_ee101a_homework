% Capacitor Analysis
clear

t_0 = 0;
t_1 = 1e-3;
t_2 = 3e-3;
t_3 = 3e-3;
t_4 = 5e-3;
t_5 = 6e-3;

C = 2e-7;
vi = -16;

curr = 5e-3;

t = linspace(0, t_5, 100000);
current = zeros(size(t)); % Initialize voltage array
current(t >= t_1 & t < t_2) = curr;
current(t >= t_3 & t < t_4) = -curr;

close all
tiledlayout(2,2)

% Plot the current
nexttile
plot(t * 1e3, current *1e3, 'LineWidth', 2.5);
title("Current")
xlabel("Time (ms)")
ylabel("Current (mA)")
hold on

% Plot the voltage
nexttile
voltage = cumtrapz(t, current / C) + vi;
plot(t * 1e3, voltage, 'LineWidth', 2.5);
title("Voltage")
xlabel("Time (ms)")
ylabel("Voltage (V)")

% Plot the power
nexttile
power = current .* voltage;
plot(t * 1e3, power * 1e3, 'LineWidth', 2.5);
title("Power")
xlabel("Time (ms)")
ylabel("Power (mW)")

% Plot the energy
nexttile
energy = 0.5 * C * voltage.^2;
plot(t * 1e3, energy * 1e6, 'LineWidth', 2.5);
title("Energy")
xlabel("Time (ms)")
ylabel("Energy (\muJ)")

