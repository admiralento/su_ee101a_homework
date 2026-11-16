clear
close all

kp = 2.5e-3;
Vtp = -0.3;

figure
hold on
legend('AutoUpdate', 'on')
vds = linspace(-5, 0, 100);
for vgs = 0:-1:-5
    vov = vgs-Vtp;
    if vov > 0
        id = 0 * vds; % Cutoff
    else
        id = kp * (vov.*vds - vds.^2*0.5); % Linear
        id(vds < vov) = (0.5 * kp * vov^2); % Saturation
    end
    plot(vds, id*1e3, 'DisplayName', sprintf('v_{GS}=%dV', vgs))
    hold on
end
legend('AutoUpdate', 'off')

% Plot boundary region
boundary = 0.5 * kp *(vds.^2);
plot(vds, boundary*1e3, 'LineStyle', '--', 'Color', 'black')
text(-4.5, 6, 'Saturation', 'FontSize', 12, 'FontWeight', 'bold');
text(-3.2, 20, 'Linear', 'FontSize', 12, 'FontWeight', 'bold');

ylabel("Current i_D (mA)")
xlabel("Voltage v_{DS} (V)")
title("PMOS Current Curves")