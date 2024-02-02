import queue
import copy

total_time = 2 #hours
IAT_rate = 60 #60 students per hour
ST_rate = 60 #60 students per hour
rho = IAT_rate/ST_rate

#Initializing

qu = queue.Queue()
curr_process = None
IAT = []
ST = []
AT = []
wait_time = []
server_busy = False
list_wait = []
list_delay = []
num_processes_served = 0


IAT.append(0)
i = 1

while np.sum(IAT) < total_time * 60 * 60:
    i += 1
    temp = np.random.exponential(1/IAT_rate) * 60 * 60
    IAT.append(int(temp - temp%1))
num_processes = i

while not len(ST) == num_processes:
    temp = np.random.exponential(1/ST_rate) * 60 * 60
    if not int(temp-temp%1) < 1:
        ST.append(int(temp - temp%1))

ST_copy = copy.deepcopy(ST)

for i in range(num_processes):
    if i == 0:
        AT.append(0)
    else:
        AT.append(AT[i-1] + IAT[i])
    wait_time.append(0)

queue_size = np.zeros(total_time * 60 * 60)
empty_system = 0
#num_processed_server_seconds = num_processes_served * 60 * 60


for i in range(total_time * 60 * 60):
    queue_size[i] = qu.qsize()
    if server_busy:
        for item in list(qu.queue):
            wait_time[item] += 1
        ST[curr_process] -= 1
        if ST[curr_process] == 0:
            server_busy = False
            num_processes_served += 1
            
    
    for j in range(num_processes):
        if i == AT[j]:
            qu.put(j)
    
    if not server_busy and not qu.empty():
        curr_process = qu.get()
        server_busy = True
    
    if not server_busy and qu.empty():
        empty_system += 1
    
    sum_wait = 0
    sum_delay = 0
    
    for i in range(num_processes_served):
        sum_wait += wait_time[i]
        sum_delay += wait_time[i] + ST_copy[i]
    
    if num_processes_served == 0:
        list_wait.append(0)
        list_delay.append(0)
    else:
        list_wait.append(sum_wait/num_processes_served * 60 * 60)
        list_delay.append(sum_delay/num_processes_served * 60 * 60)
        
#Analytical

display(rho) 

QWT = 1/((1-rho) * ST_rate) - 1/ST_rate
WT = 1/((1-rho) * ST_rate)

time_hours = np.linspace(0, total_time, total_time * 60 * 60)

plt.figure(figsize=(14, 5))
plt.plot(time_hours, queue_size, 'ok')

plt.figure(figsize=(14, 5))
plt.plot(time_hours, list_wait)
#plt.plot([0, total_time], [QWT, QWT])

plt.figure(figsize=(14,5))
plt.plot(time_hours, list_delay)
#plt.plot([0, total_time], [WT, WT])
plt.ylabel("Avg Delay Times")
plt.show()

plt.figure(figsize=(14,5))
n_bins = np.max(queue_size)
##
plt.hist(queue_size,n_bins.astype(int),density=True)
x = np.arange(0, n_bins+1)
p_analytical = (1-rho)*rho**x
p_analytical[1]= p_analytical[0] + p_analytical[1]
p_analytical[0]= 0
plt.step(p_analytical,'r')
plt.show()

print('Idle ratio:',empty_system/(total_time*60*60))
print('Empty queue probability:', 1 -  rho)
print('Wait time in queue',QWT)
print('Delay time in system',WT)
