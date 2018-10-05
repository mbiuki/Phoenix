%% Check the validity of traces
% ==============================================================================
% $ University of British Columbia (UBC) $
% $ Security of IoT Systems Lab $
% $ Author: Mehdi Karimi $
% $ Date: October 2018 $
% ==============================================================================
function [ fake, correct ] = check( testFolder, ...
                                    testFileFixedRows, ...
                                    P, ...
                                    Gam, ...
                                    maxJVar, ...
                                    checkerDecisionMetric_Thd )
% Checking Traces in the Test Folder
%   This function checks if the data are fake or real
    display(['Checking Traces in the Test Folder > > >'])
    if ~isdir(testFolder)
        errorMessage = ...
         sprintf('Error: The following folder does not exist:\n%s', ...
        uiwait(warndlg(errorMessage)));
        return;
    end
    filePattern = fullfile(testFolder, '*.csv');
    theFiles = dir(filePattern);
    
    fake = 0;
    correct = 0;

    for k = 1 : length(theFiles)
        testFileName = theFiles(k).name;    
        
        Temp = csvread(fullfile(testFolder, testFileName),1,1);
        PHI_Falsifier_v = Temp(1:testFileFixedRows,:);
%         PHI_Falsifier_v=csvread(fullfile(testFolder, testFileName),1,1);
        % accuracy maximum - 
        %accuracy 10 meter https://en.wikipedia.org/wiki/Decimal_degrees
        %PHI_Falsifier(:,[2])=PHI_Falsifier(:,[2]) + ...
        %           0.0001*randn(size(PHI_Falsifier,1),1);
        v_v=@(x) x'*P*x;
        % 71 number - normalized and sum of all negatives average -
        % average sum % machine learning even better than machine
        % learning no processing power needed, low 
        % drone limited resource-constrained no nueral net needed
        func_v=@(ind_i,ind_j) v_v(PHI_Falsifier_v(ind_i, :).') - ...
                              v_v(PHI_Falsifier_v(ind_i+ind_j,:).') - ...
                              Gam*norm(PHI_Falsifier_v(ind_i,:),2)^2; 
                   
        for ind_i = 1:size(PHI_Falsifier_v,1)-1
            J_var_v(ind_i) = func_v(ind_i,1);
        end
        
        % 
%         Decision_Metric_v = sum( J_var_v/max(J_var_v) .* ...
%                                ( (J_var_v/max(J_var_v)) < 0 ) );
        Decision_Metric_v = sum(  J_var_v/maxJVar .* ...
                               ( (J_var_v/max(J_var_v)) < 0 ));

        cprintf('> Trace is = ')
        if Decision_Metric_v < checkerDecisionMetric_Thd
            cprintf('Errors','Fake');
            fake = fake +1;
        else
            cprintf('Comments','Correct');
            correct = correct + 1;
        end
        cprintf('Text',', ');
        cprintf('Text','Decision_Metric = %s', num2str(Decision_Metric_v));
        cprintf('Text','. File= ');
        cprintf('Hyperlinks','%s\n', testFileName);
    end
end
%% EoF
