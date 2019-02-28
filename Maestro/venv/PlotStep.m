% Khrisna Kamarga
% Step Response Plot - Robotic Eyes
clear all; close all; clc;

cd 'C:\Users\Khrisna Adi Kamarga\PycharmProjects\Maestro\venv';
load step9 %lead lag looking

pos = double(pos);

dx = pos(2:end) - pos(1:end-1);
dt = t(2:end) - t(1:end-1);
v = dx./dt;
v = v(~isnan(v))
v(v==0) = [];

figure(1)
plot(t, pos)
xlim([0 4])


L = max(t); % spatial domain
n = length(v); % Fourier modes
x2 = linspace(0,L,n+1); x = x2(1:n); % not used
k = (2*pi/(L))*[0:(n/2-1) -n/2:-1]; ks = fftshift(k);

figure(2)
plot(ks, real(fftshift(fft(v(1:length(k))))))
grid on
% xlim([-20 20])

figure(3)
plot(t(1:length(v)), v);