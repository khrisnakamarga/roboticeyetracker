% Plotting the Calibration Map
% input: csv file, containing the calibration map

clear all; close all; clc;

screen_coordinate = zeros(5, 16, 2);

%%
close all; clc;
X_map = csvread('testx.csv');
Y_map = csvread('testy.csv');

[row column] = size(X_map);
screen_coordinate = zeros(row, column, 2);

screen_coordinate(:,:,1) = X_map;
screen_coordinate(:,:,2) = Y_map;



%%

X = [];
for i = 1:column
    X = [X linspace(1,row,row)];
end

Y = [];
for i = 1:row
    Y = [Y linspace(1,column,column)];
end

[x, y] = meshgrid(1:column, 1:row);

figure(1)
plot3(X, Y, reshape(screen_coordinate(:,:,1),row*column, 1))
figure(2)
surf(x, y, screen_coordinate(:,:,1))
title('2D Horizontal Servo Map')
c = colorbar;
c.Label.String = 'horizontal servo coordinate';
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')
figure(3)
pcolor(x, y, screen_coordinate(:,:,1)); shading interp;
c = colorbar;
c.Label.String = 'horizontal servo coordinate';
title('2D Horizontal Servo Spectrogram')
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')

figure(4)
plot3(X, Y, reshape(screen_coordinate(:,:,2),row*column, 1))
figure(5)
surf(x, y, screen_coordinate(:,:,2))
c = colorbar;
title('2D Vertical Servo Map')
c.Label.String = 'vertical servo coordinate';
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')
figure(6)
pcolor(x, y, screen_coordinate(:,:,2)); shading interp;
c = colorbar;
c.Label.String = 'vertical servo coordinate';
title('2D Vertical Servo Spectrogram')
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')

