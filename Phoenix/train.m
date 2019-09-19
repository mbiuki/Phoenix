%% Train and refine to find a Lypunov function
% ==============================================================================
% $ University of British Columbia (UBC) $
% $ Security of IoT Systems Lab $
% $  $
% $ Date: October 2018 $
% ==============================================================================
function [ P, Gam, lypFound, decisionMetricThreshold ] = train( trainFolder, ...
                                                fixedRows, ...
                                                dimension, ...
                                                Eps, ...
                                                initTrainThresh )
% Goal: Find a valid Lyapunov Polynomial
%   This function given a set of traces will find the Lypunov function

    if ~isdir(trainFolder)
      errorMessage = ...
        sprintf('Error: The following folder does not exist:\n%s', trainFolder);
      uiwait(warndlg(errorMessage));
      return;
    end
    filePattern = fullfile(trainFolder, '*.csv');
    theFiles = dir(filePattern);
    numOfFiles = length(theFiles);

    for k = 1 : numOfFiles
      fileName = theFiles(k).name;
      % Every File is a Trace
      Temp=csvread(fullfile(trainFolder, fileName),1,1);
      Trace(k,:,:)=Temp(1:fixedRows,:);
    end

    % Some initial set of traces, e.g., Trace_list=[1 2 3 4];
    Trace_list=[1];
    
    % list of decision metrics for evaluation
    decisionMetricThreshold = initTrainThresh;
    
    % default Flags
    lypFound = false;
    loopFlag = false;
    falsifierFlag = false;
    
    Trace_Counter = length(Trace_list)-1;
    
    % counter and the time recording params
    startFindingNewLyp = 0;
    total_algorithmTime = 0; 

    
    dlmwrite('decisionMetric.csv','metric','delimiter',',','-append');
    
    while(( false == lypFound) && (false == loopFlag) )
        Trace_Counter = Trace_Counter+1;
        tStart = tic;
        cvx_begin
            variable P(dimension,dimension);
            variable Gam;
            v=@(x) x'*P*x;
            func=@(ind_i,ind_j,x) v(x(ind_i, :).') - ...
                                  v(x(ind_i+ind_j,:).') - ...
                                  Gam*norm(x(ind_i,:),2)^2;
            subject to
                for nm=1:length(Trace_list)
                    for ind_i= 1:size(permute(Trace(Trace_list(nm),:,:), [2 3 1]),1)
                        v(permute(Trace(Trace_list(nm),ind_i,:), [2 3 1]).') >= 0;
                        for ind_j=1:size(permute(Trace(Trace_list(nm),:,:), [2 3 1]),1)-ind_i
                            func(ind_i,ind_j,permute(Trace(Trace_list(nm),:,:), [2 3 1])) >= 0;
                        end
                    end
                end
                Gam >= Eps;
        cvx_end
        algorithmTime = toc(tStart);
        dlmwrite('algorithmTime.csv',algorithmTime,'delimiter',',','-append');
        fclose('all');
        total_algorithmTime = total_algorithmTime + algorithmTime;
        
        %----------Flasifier part--------------------------
        % Apply to the rest of training traces, if any
        cprintf('Text', 'cvx_status= %s\n', cvx_status);
        if cvx_status=='Solved'
            for m = Trace_Counter+1 : numOfFiles
                PHI_Falsifier = permute(Trace(m,:,:), [2 3 1]);
                v=@(x) x'*P*x;
                func=@(ind_i,ind_j) v(PHI_Falsifier(ind_i, :).') - ...
                                    v(PHI_Falsifier(ind_i+ind_j,:).') - ...
                                    Gam*norm(PHI_Falsifier(ind_i,:),2)^2;
                for ind_i=1:size(PHI_Falsifier,1)-1
                     J_var(ind_i) = func(ind_i,1);
                end
                 
%                 Decision_Metric = mean( (J_var/max(J_var)) < ...
%                                          trainerDecisionMetric_Thd )

                cprintf('Strings', 'max(J_var)=%0.4f\n',max(J_var));
                cprintf('red', 'min(J_var)=%0.4f\n',min(J_var));
                cprintf('_Cyan', 'NORMALIZED:\n');
                cprintf('*Green', 'J_var=%0.4f\n', J_var/(max(J_var) - min(J_var)));

                % only sum the negatives
                % I want my negatives accumulation small since
                % the objective function func > 0 at every point
                % number x boolean === This means only keep the negatives
                Decision_Metric = sum((J_var/(max(J_var) - min(J_var)))...
                                  .* ( J_var < 0 ));
                cprintf('*Green', 'Decision_Metric=%f\n',...
                                 Decision_Metric);
                
                % add and redo
                % will break if the negative is big, go and add it, 
                % if not go to the next trace to certiry it
                 cprintf('_Blue', 'decisionMetricThreshold=%f\n',...
                                 decisionMetricThreshold);

                dlmwrite('decisionMetric.csv',decisionMetricThreshold,'delimiter',',','-append');
                if Decision_Metric < -0.0001 % TODO: see if can be auto-guessed
                    if Decision_Metric < decisionMetricThreshold 
                        cprintf('*Blue','Add trace %d to training and start over\n', m);
                        Trace_list = [Trace_list m];
                        falsifierFlag = true;                    
                        startFindingNewLyp = startFindingNewLyp + 1;                  
                        break; 
                    else
                        decisionMetricThreshold = Decision_Metric;
                   end
                end

            end
            
            if  falsifierFlag==false
                display(['LYAP. is found'])
                lypFound = true;
                break;
            else
                display(['Trace number ', num2str(m), ...
                          ' added to the trace list for new LF finding...']);
                falsifierFlag = false;
            end
        else
            display('No Lyapunov solution found');
            break;
        end
    end
    cprintf('Text', 'new starovers = %d\n ', startFindingNewLyp);
    algorithmTime
    total_algorithmTime   
end
%% EoF
