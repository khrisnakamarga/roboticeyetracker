clear all; close all; clc;

x = [2721; 2780; 2830; 2870; 2920];

grid on
plot(x,'--')
hold on
plot(x,'o')
xlabel("y screen coordinate");
ylabel("vertical eye servo coordinate");
grid on

%%
clear all; close all; clc;

screen_coordinate_2 = zeros(4, 10, 2);
% for i = linspace(1,5,5)
%     for j = linspace(1,16,16)
%         for k = [1 2]
%             screen_coordinate(i,j,k) = [i, j, k];
%         end
%     end
% end

calibration_map = zeros(4, 10, 2);
for i = linspace(1,4,4)
    for j = linspace(1,10,10)
        for k = [1 2]
            screen_coordinate_2(i,j,k) = input("insert " + k + " servo coordinate = ");
        end
        display("next point")
    end
    clc;
    display("first row done!")
end

%%
close all; clc;
load('calibration map 2.mat')

X = [];
for i = 1:10
    X = [X linspace(1,4,4)];
end

Y = [];
for i = 1:4
    Y = [Y linspace(1,10,10)];
end

[x, y] = meshgrid(1:10, 1:4);

figure(1)
plot3(X, Y, reshape(screen_coordinate_2(:,:,1),10*4, 1))
figure(2)
surf(x, y, screen_coordinate_2(:,:,1))
title('2D Horizontal Servo Map')
c = colorbar;
c.Label.String = 'horizontal servo coordinate';
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')
figure(3)
pcolor(x, y, screen_coordinate_2(:,:,1)); shading interp;
c = colorbar;
c.Label.String = 'horizontal servo coordinate';
title('2D Horizontal Servo Spectrogram')
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')

figure(4)
plot3(X, Y, reshape(screen_coordinate_2(:,:,2),10*4, 1))
figure(5)
surf(x, y, screen_coordinate_2(:,:,2))
c = colorbar;
title('2D Vertical Servo Map')
c.Label.String = 'vertical servo coordinate';
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')
figure(6)
pcolor(x, y, screen_coordinate_2(:,:,2)); shading interp;
c = colorbar;
c.Label.String = 'vertical servo coordinate';
title('2D Vertical Servo Spectrogram')
xlabel('X coordinate of the screen')
ylabel('Y coordinate of the screen')

