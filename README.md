# Assigning tasks aware of criticality levels in edge systems

### Project Description:
- Design an algorithm to receive users' tasks with different criticality level and assign them to edge servers, considering servers' load balance and tasks' priority based on criticality level
- In this system, we have some user devices that send a task to edge system to be processed. Base Station receive these tasks and control the servers' load and task assigning
- Task Properties: number of clocks to be done, data amount, deadline, criticality level(S = {S0, S1, S2, S3}, S3 is highest level) : ti = (ci, di, Ti, pi)
- Server Properties: processing frequency, data transmission rate, number of cores, productivity : mi = (fi, vi, zi, ui)
- Server's productivity will be updated every time a task is assigned
- Base Station store the number of tasks for each server based on the task criticality
- Assign the received task to a server with the least productivity
- If task's productivity + server's productivity > server's number of cores then the task can't be assigned to this server, because it won't meet the deadline
- In case of no server meet the deadline of task ti, assign ti to the server with the least number of tasks with criticality level more or equal than pi,
when ti is assigned, all tasks with criticality less than pi will be suspended till completion of ti 
