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

% if you want to create a stability function from scratch
findLyap_fromScratch = false;
% ========================
format long g
clc;
addpath cprintf;
close all;
if (findLyap_fromScratch)
    clear all;
end

LypAlreadyCalculated = logical( exist( 'P' ,'var') && exist( 'Gam' ,'var') );

%----------------------------------------
% === Train and Test Folders ===========
% testFolder = '.\Test_dataSet\72datapts';
% testFolder = '.\Test_dataSet\1_UBC\detour\noWind';
% testFolder = '.\Train_datset\1_UBC\real\1';
% testFolder = '.\Test_dataSet\oneUBC';
testFolder = '.\Test_dataSet\oneMonash';
% testFolder = '.\Test_dataSet\oneCMAC';
% testFolder = '.\Test_dataSet\oneCarstensz';
% testFolder = '.\Test_dataSet\oneSnarbyeidet';

%  testFolder = '.\Test_dataSet\forDemo';
% testFolder = '.\Test_dataSet\path4_Snarbyeidet';
% testFolder = '.\Test_dataSet\Snarbyeidet_wind';
% testFolder = '.\Test_dataSet\snarbyeidet';
% testFolder = '.\Test_dataSet\snarbyeidet2';
% testFolder = '.\Train_datset\UBC_3_61E';

% trainFolder = '.\Train_datset\initial';
% trainFolder = '.\Train_datset\path4_Snarbyeidet';
% trainFolder = '.\Test_dataSet\snarbyeidet';
% trainFolder = '.\Train_datset\sample_real';
trainFolder = '.\Train_datset\1_UBC\noWind\1';
% =======================================
% === Parameters ========================
Eps = 0.01;
dimension = 6;

fixedRows = 70;
testFileFixedRows = 30;
% ======================================

% ax^2 + bx + c --> find the roots, beine do rishe

% ===== Variables ===================
% checkerDecisionMetric_Thd = -0.4; % threshold of the checker
checkerDecisionMetric_Thd = -1e-3; % threshold of the checker
trainerDecisionMetric_Thd = -1e-3; % threshold of the trainer
% ===================================

% Training Section:
if (~LypAlreadyCalculated || findLyap_fromScratch)
    overalT = tic;
    [P, Gam, maxJVar, lypFound] = train( trainFolder, ...
                                 fixedRows, ...
                                 dimension, ...
                                 Eps, ...
                                 trainerDecisionMetric_Thd );
    timeTrained = toc(overalT);
    dlmwrite('timeTrained.csv',timeTrained,'delimiter',',','-append');
    fclose('all');
end

% Check Section:
if true == lypFound
    tic
    [fake, correct] = check( testFolder, ...
                             testFileFixedRows, ...
                             P, ...
                             Gam, ...
                             maxJVar, ...
                             checkerDecisionMetric_Thd );
    cprintf('*Red', 'Number of Fakes = %d\n', fake);
    cprintf('*Blue','Number of Corrects = %d\n', correct);
    toc
%     cprintf('false positive','%s\n', correct / (fake+correct));
    cprintf('*Blue','false negative = %f\n', (correct / (fake+correct))*100);    
end

%% EoF
