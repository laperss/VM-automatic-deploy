%% Import Log files
clear; clc; close all;

log_clients = import_log_clients('data/log_clients.tsv');
log_monitor = import_log_monitor('data/log_monitor.tsv');

%% Number of requests/completions per second
requests = log_clients(log_clients.command == "request", :);
acks = log_clients(log_clients.command == "ack", :);
dv_req = datevec(requests.time);
dv_req = dv_req(:, 4) * 3600 + dv_req(:,5) * 60 + dv_req(:, 6);
dv_req = (dv_req - dv_req(1))/60;
dv_ack = datevec(acks.time);
dv_ack = dv_ack(:, 4) * 3600 + dv_ack(:,5) * 60 + dv_ack(:, 6);
dv_ack = (dv_ack - dv_ack(1))/60;
bins = max([max(fix(dv_ack)); max(fix(dv_req))]);
req_hist = hist(fix(dv_req), bins);
ack_hist = hist(fix(dv_ack), bins);
histval = [req_hist' ack_hist'];

figure(1); box on;
bar(histval)
axis tight
xlabel('time [min]')
ylabel('number of requests/completions')
legend('number of requests', 'number of completed')

print('requests_time.eps','-depsc')

%% Processing time over time
ids = unique(log_clients.id);
ptime = [];
deltas = [];
for i = 1:length(ids)
    times = log_clients(log_clients.id == ids(i), :);
    if height(times) == 2
        delta = times.time(2) - times.time(1);
        ptime = [ptime times.time(2)];
        deltas = [deltas delta];
    end
end
figure(2); box on; hold on;
plot(ptime, deltas, 'b')
xlabel('time')
ylabel('processing time')

print('processing_time_time.eps','-depsc')

%% Load/scaling over time
close all
% Order the number of backends
backends = unique(log_monitor.ip);
backends(strcmp('',backends)) = [];

load_data = log_monitor(log_monitor.command=="load",:);
avgload_data = log_monitor(log_monitor.command=="avgload",:);
terminate_data = log_monitor(log_monitor.command=="backend_terminate",:);
create_data = log_monitor(log_monitor.command=="backend_create",:);
number_backends_data = log_monitor(log_monitor.command=="number_backends",:);

figure(3); box on; hold on;
yyaxis left
for i = 1:length(backends)
    backend = backends(i);
    data = load_data(load_data.ip==backend,:);
    a = plot(data.time, data.load, 'Color', [0.8 0.8 0.8]);
end
b = plot(avgload_data.time, avgload_data.load, 'o-');
yyaxis right
c = plot(number_backends_data.time, str2double(number_backends_data.ip));
legend([a b c], {'real-time load', 'average load', 'number of backends'})
yl=xlim(gca); % retrieve auto y-limits
axis tight   % set tight range
ylim(gca);  % restore y limits 
print('load_scaling_time.eps','-depsc')
