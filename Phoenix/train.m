%% Train and refine to find a Lypunov function
% ==============================================================================
% $ University of British Columbia (UBC) $
% $ Security of IoT Systems Lab $
% $  $
% $ Date: October 2018 $
% ==============================================================================
function [ P,Gam, LYP_FOUND ] = train( trainFolder, dimension, Eps )
% Goal: Find a valid Lyapunov Polynomial
%   This function given a set of traces will find the Lypunov function

    if ~isdir(trainFolder)
      errorMessage = ...
        sprintf('Error: The following folder does not exist:\n%s', trainFolder);
      uiwait(warndlg(errorMessage));
      return;
    end
    filePattern = fullfile(trainFolder, '*.csv'); % Change to whatever pattern you need.
    theFiles = dir(filePattern);

    for k = 1 : length(theFiles)
      baseFileName = theFiles(k).name;
      %fullFileName = fullfile(myFolder, baseFileName);
      %fprintf(1, 'Now reading %s\n', fullFileName);
      Trace(k,:,:)=csvread(fullfile(trainFolder, baseFileName),1,1);
    end

    Trace_list=[1 2 3 4];
    LYP_FOUND = false;
    Trace_Counter = length(Trace_list)-1;
     while(false == LYP_FOUND)         
         Trace_Counter=Trace_Counter+1;
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
         
         %----------Flasifier part--------------------------         
         if cvx_status=='Solved'
             for m = Trace_Counter+1 : length(theFiles)
                 PHI_Falsifier=permute(Trace(m,:,:), [2 3 1]);
                 v=@(x) x'*P*x;
                 func=@(ind_i,ind_j) v(PHI_Falsifier(ind_i, :).') - ...
                                     v(PHI_Falsifier(ind_i+ind_j,:).') - ...
                                     Gam*norm(PHI_Falsifier(ind_i,:),2)^2;
                 for ind_i=1:size(PHI_Falsifier,1)-1
                     J_var(ind_i)=func(ind_i,1);
                 end
                 Decision_Metric = mean((J_var/max(J_var)) < -0.01)
                 if Decision_Metric > 0
                     Trace_list = [Trace_list m];
                     break; 
                 end
             end
             
             if  m==length(theFiles)
                 display(['LYAP. is found'])
                 LYP_FOUND = true;
                 break;
             else
                 display(['Trace number ', num2str(m), ...
                          ' added to trce list for LF finding...']);
                      
                 %  LYP_FOUND= flase;
                 %  fprintf('NO LYAPUNOV found')
             end
         else
             display('No solution found');
             break;
         end
     end
end
%% EoF
