%% Function Name: main Lyapunov runner function
% Mehdi Karimi -- UBC IoT Security Lab
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
% Modified: Sept 18, 2019
% ________________________________________

% if you want to create a stability function from scratch
findLyap_fromScratch = true;
% ========================
format long g
clc; 
close all;

% TODO: Would need to run CVX_begin in cvx folder first
if (findLyap_fromScratch)
    clear all;
    addpath cprintf;
    addpath sosopt;
end

LypAlreadyCalculated = logical( exist( 'P' ,'var') && exist( 'Gam' ,'var') );

%----------------------------------------
% === Train and Test Folders ===========
trainFolder ='.\trainData\1_UBC\noWind\one';
testFolder = '.\testData\1_UBC\one';

% =======================================
% === Parameters ========================
Eps = 0.00001;
dimension = 6;

% fixedRows = 70;
fixedRows = 50;
testFileFixedRows = 50;
% ======================================

% ===== Thresholds =====================
initTrainThresh = -0.001; % initial threshold of the trainer
%checkerDecisionMetric_Thd = -0.1; % TODO, remove threshold of the checker
% =====================================

% Training Section:
if (~LypAlreadyCalculated || findLyap_fromScratch)
    overalT = tic;
    [P, Gam, lypFound, decisionMetricThreshold] = train( trainFolder, ...
                                 fixedRows, ...
                                 dimension, ...
                                 Eps, ...
                                 initTrainThresh );
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
                             decisionMetricThreshold );
    cprintf('*Red', 'Number of Fakes = %d\n', fake);
    cprintf('*Blue','Number of Corrects = %d\n', correct);
    toc
    cprintf('*Blue','Traces that was identified to be correct = %%%0.2f\n', (correct / (fake+correct))*100); 
    cprintf('*Red','Traces that was identified to be false = %%%0.2f\n', (fake / (fake+correct))*100); 

end

%% EoF
