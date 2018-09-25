%% Function Name: main Lyapunov runner function
%
% Assumptions: dimensions are known
%
% Inputs:
%   Eps and dimensions of the state-space matrix
%   ss <- correlate system dynamics and location
%   CVX cost function optimization for Laypunov function P
%
% Outputs:
%   none
%
%
% $Date: September 27, 2018
% ________________________________________
format long g
clc;
close all;
findLyap_fromScratch = false;
if (findLyap_fromScratch)
    clear all;
end

LypAlreaduCalculated = logical( exist( 'P' ,'var') && exist( 'Gam' ,'var') );

%----------------------------------------
% === Train and Test Folders ===========
testFolder = '.\Test_dataSet\72datapts';
trainFolder = '.\Train_datset';
% =======================================
% === Parameters ========================
Eps = 0.01;
dimension = 6;

if (~LypAlreaduCalculated || findLyap_fromScratch)
    [P, Gam, LYP_FOUND] = train(trainFolder, dimension, Eps);
end

if true == LYP_FOUND
    check(testFolder, P, Gam);
end

%% EoF
