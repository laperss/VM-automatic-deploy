function log1 = import_log_monitor(filename, startRow, endRow)
%IMPORTFILE1 Import numeric data from a text file as a matrix.
%   LOG1 = IMPORTFILE1(FILENAME) Reads data from text file FILENAME for the
%   default selection.
%
%   LOG1 = IMPORTFILE1(FILENAME, STARTROW, ENDROW) Reads data from rows
%   STARTROW through ENDROW of text file FILENAME.
%
% Example:
%   log1 = importfile1('log.tsv', 1, 371);
%
%    See also TEXTSCAN.

% Auto-generated by MATLAB on 2017/12/05 17:56:30

%% Initialize variables.
delimiter = '\t';
if nargin<=2
    startRow = 1;
    endRow = inf;
end

%% Format for each line of text:
%   column1: datetimes (%{yyyy-MM-dd HH:mm:ss}D)
%	column2: text (%s)
%   column3: text (%s)
%	column4: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%{yyyy-MM-dd HH:mm:ss}D%s%s%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, endRow(1)-startRow(1)+1, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines', startRow(1)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
for block=2:length(startRow)
    frewind(fileID);
    dataArrayBlock = textscan(fileID, formatSpec, endRow(block)-startRow(block)+1, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines', startRow(block)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
    for col=1:length(dataArray)
        dataArray{col} = [dataArray{col};dataArrayBlock{col}];
    end
end

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Create output variable
log1 = table(dataArray{1:end-1}, 'VariableNames', {'time','command','ip','load'});

% For code requiring serial dates (datenum) instead of datetime, uncomment
% the following line(s) below to return the imported dates as datenum(s).

% log1.time=datenum(log1.time);

