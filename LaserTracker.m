% Khrisna Kamarga
% Robotic Eyes - Laser Tracker

clear all; close all; clc;

v = VideoReader("C:\Users\Khrisna Adi Kamarga\Desktop\RoboticEyes\test.mp4")
video = double(read(v));
[m, n, rgb, t] = size(video);

%% visualize the motion for each dataset
clc;
for i = 1:t
    bwVideo = video(:,:,1,i);
    pcolor((bwVideo)), shading interp, colormap(gray);
    drawnow
    display(i)
end

%%

%% crop location for 1_1 & 1_2 & 1_3 & 1_4
isolate = zeros(m,n);
jStart = 1;
iStart = 150;
jEnd = 640;
iEnd = 480;
for i = iStart:iEnd
    for j = jStart:jEnd
        isolate(i,j) = 1;
    end
end
clc;
for i = 1:50
    bwVideo = video(:,:,1,i);
    pcolor(flipud(double(bwVideo).*isolate)), shading interp, colormap(gray);
    drawnow
end

%%

% find characteristic frequency
% set up the fourier coefficients
xaxis2 = linspace(0,m,m+1); x = xaxis2(1:m);
yaxis2 = linspace(0,n,n+1); y = yaxis2(1:n);
kx = (2*pi/(2*m))*[0:(m/2-1) -m/2:-1]; ksx = fftshift(kx);
ky = (2*pi/(2*n))*[0:(n/2-1) -n/2:-1]; ksy = fftshift(ky);
% set up the 3D coordinate points
[X,Y] = meshgrid(x,y); % spatial coordinates
[Kx,Ky] = meshgrid(ksx,ksy); % wave numbers
X = X';
Y = Y';
Kx = Kx';
Ky = Ky';

UtnAve = zeros(m,n); % kernel for the averaged frequency domain signal
for i = 1:t
    bwVideo = double((video(:,:,1,i))).*isolate;
    Un = bwVideo; % gets the 2D coordinate representation of the sample
    Utn = fftn(Un); % fourier transform of the data
    UtnAve = UtnAve + Utn; % cummulative sum of the frequency domain signal
end

% find the indices of the max magnitude in the frequency domain
[ind1 ind2] = ind2sub([m,n], find(fftshift(UtnAve) == max(fftshift(UtnAve), [], 'all')));
% look up the frequency domain coordinate of the strongest signal
Kc = [Kx(ind1, ind2), Ky(ind1, ind2)];

%% plot the spectrogram
% plot the resulting normalized averaged data in the frequency domain
pcolor(abs(fftshift(UtnAve))/max(abs(UtnAve), [], 'all')), shading interp, colormap(gray);
xlabel("Kx"); ylabel("Ky");
title("Averaged Data in the Frequency Domain");
%%

% applying the filter and recovering x and y
close all; clc;
% 2D gaussian filter
tau = 100; % bandwith of the filter (good: 0.2)
[kux, kuy] = meshgrid(ky,kx); % unshifted wave numbers
filter = exp(-tau*((kux - Kc(1)).^2+(kuy - Kc(2)).^2));

%% plot the resulting normalized averaged data in the frequency domain
pcolor(abs(fftshift(filter))/max(abs(filter), [], 'all')), shading interp, colormap(gray);
xlabel("Kx"); ylabel("Ky");
title("Averaged Data in the Frequency Domain");
%%

laser = zeros(t, 2); % kernel for the coordinates of the bucket
for i = 1:t
    bwVideo = double((video(:,:,1,i))).*isolate; drawnow
    Utn = fftn(bwVideo); %Utn = fftshift(Utn);
    UtnFilter = Utn.*filter; % filtered frequency domain signal
    UnFilter = real(ifftn(UtnFilter)); % obtain the spatial filtered data
    
    % draw the resulting spatial filtered data
    pcolor(flipud(UnFilter))
    shading interp, colormap(gray); 
    grid on

    % find the coordinate of the center of the bucket
    [ind1 ind2] = ind2sub([m,n], round(mean(find(abs(UnFilter) == max(abs(UnFilter), [], 'all')))));
    laser(i,:) = [X(ind1, ind2), Y(ind1, ind2)];
    
    hold on
    plot(laser(i,2), -(laser(i,1)-m), 'm.-', 'MarkerSize', 20);
    hold off
    drawnow
end