% Thomas Hayden Clark
% ECE 4900 AU21
% Normalization of input data
clear all; clc

%% Append pupil size, change of pupil size, response variable

%read in data
%filename = 'Cog.Load_Hayden_easy_11_4_COMPLETE.xlsx';
prompt = 'What is the file name? (type included, expecting nx3 matrix)';
filename = input(prompt)
M = readmatrix(filename);

%normalize the data
normal = ( mean(M,2) )/( length(M) );
normalizedData = M(:,2)./normal;

completeData = normalizedData;

%find derivative of future data
der = 0;
for i = 6:length(M)
    der = ( (M(i,3)) - (M(i-5,3)) )/( (M(i,2)) - (M(i-5,2)) );
    completeData(i,2) = der;
    completeData(i,3) = M(i,3);
end

%write matrix to csv file
writematrix(completeData,'normalizedData_Hayden.csv') 