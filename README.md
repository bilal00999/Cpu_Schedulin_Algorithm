# Cpu_Schedulin_Algorithm

1. Project Overview
The CPU Scheduling Visualizer is a Python-based GUI application developed using Tkinter and Matplotlib to simulate and visualize different CPU scheduling algorithms. It allows users to enter process data, select a scheduling algorithm, and observe the resulting Gantt chart and process states in real-time animation.
The project is designed for educational purposes, helping students understand how scheduling algorithms manage CPU processes.
________________________________________
2. Features
1.	Supported Scheduling Algorithms:
o	SJF (Shortest Job First) Non-Preemptive
o	SJF Preemptive (Shortest Remaining Time First)
o	Priority Non-Preemptive
o	Priority Preemptive
2.	Dynamic Table Input:
o	Users can specify the number of processes.
o	Dynamically generated table to enter Arrival Time, Burst Time, and Priority.
3.	Gantt Chart Visualization:
o	Visual representation of process execution timelines.
o	Processes displayed on horizontal bars with start and end times labeled.
4.	Process State Animation:
o	Animates process execution over time.
o	Shows which process is currently running and idle periods.
5.	Automatic Metrics Calculation:
o	Waiting Time
o	Turnaround Time
o	Average Waiting Time
o	Average Turnaround Time
6.	Intelligent Input Handling:
o	Priority column disabled for SJF algorithms (since priority is irrelevant).
o	Validates user inputs (arrival ≥ 0, burst > 0).
________________________________________
3. Scheduling Algorithms Details
3.1 SJF Non-Preemptive
•	Selects the process with the shortest burst time among processes that have arrived.
•	Once a process starts execution, it runs to completion.
•	Computes:
o	Start Time: When process begins
o	End Time: When process finishes
o	Waiting Time: Start Time − Arrival Time
o	Turnaround Time: End Time − Arrival Time
TEST CASE 1 — SJF Corner Case  



3.2 SJF Preemptive
•	Also called Shortest Remaining Time First (SRTF).
•	At every time unit, selects the process with shortest remaining burst time.
•	Can preempt a running process if a new process with shorter burst arrives.
TEST CASE 2 — SJF Corner Case  












3.3 Priority Non-Preemptive
•	Chooses process with highest priority (lowest numerical value).
•	Process runs to completion once started.
•	Priority input is considered.
TEST CASE 3 — All Processes Arrive at Zero  












3.4 Priority Preemptive
•	Selects process with highest priority among available processes at each time unit.
•	A currently running process can be preempted if a higher priority process arrives.
TEST CASE 4 — Priority Starvation Case
 

TEST CASE 8 — Randomized Case
 
Priority Preemptive Scheduling – Test Case (20 Processes)
It takes 15.24 seconds to complete 20 process.
 
4. GUI Design
4.1 Layout
•	Left Panel (Controls):
o	Algorithm selection (OptionMenu)
o	Number of processes input
o	Buttons: Create table and Run
o	Average waiting and turnaround time display
•	Center Panel:
o	Top: Dynamic table for process input
o	Middle: Gantt chart using Matplotlib
o	Bottom: Process state animation canvas
•	Dynamic Behavior:
o	Priority input is automatically disabled for SJF algorithms.
o	Table adapts to the number of processes.
4.2 Components
Component	Description
ttk.Entry	For user input of arrival, burst, priority
ttk.Treeview	Displays process metrics like start, end, waiting, turnaround
Matplotlib FigureCanvasTkAgg	Draws Gantt chart
tk.Canvas	Animates process state over time
tk.StringVar	Tracks selected scheduling algorithm
ttk.OptionMenu	Algorithm selection dropdown
________________________________________
5. Code Structure
5.1 Algorithm Functions
•	sjf_non_preemptive(arrival, burst, pid_list)
•	sjf_preemptive(arrival, burst, pid_list)
•	priority_non_preemptive(arrival, burst, priority, pid_list)
•	priority_preemptive(arrival, burst, priority, pid_list)
Each function returns:
•	gantt: List of tuples (pid, start_time, end_time) for visualization.
•	metrics: Dictionary of process metrics including start, end, waiting, turnaround, and priority.
5.2 GUI Class
•	SchedulerApp: Main application class
o	__init__: Initialize GUI components
o	create_table_inputs: Dynamically creates process input table
o	run: Reads user input, runs selected algorithm, updates metrics, draws Gantt chart, starts animation
o	draw_gantt: Plots Gantt chart
o	animate_states: Animates process execution on canvas
o	toggle_priority_state: Enables/disables priority input based on algorithm
o	set_style: Configures GUI colors for light/dark mode (if implemented)
________________________________________
6. User Workflow
1.	Launch the application.
2.	Select a scheduling algorithm from the dropdown.
o	If SJF selected → Priority column is disabled.
o	If Priority selected → Priority column enabled.
3.	Enter the number of processes and click Create table.
4.	Fill in Arrival Time, Burst Time, and Priority (if applicable) for each process.
5.	Click Run.
6.	Observe:
o	Process metrics in the table
o	Gantt chart visualization
o	Animated process state timeline
7.	Review average waiting time and average turnaround time at the left panel.
________________________________________
7. Input Validation
•	Arrival Time: Must be integer ≥ 0
•	Burst Time: Must be integer > 0
•	Priority: Optional; default = 0
•	Number of processes: Integer > 0
•	Invalid inputs trigger a message box error.
________________________________________
8. Technologies Used
•	Python 3.x
•	Tkinter – GUI framework
•	ttk – Modern themed widgets
•	Matplotlib – Plotting Gantt charts
•	Threading – Animating process execution without freezing GUI
________________________________________
9. Potential Improvements
•	Add Round Robin scheduling algorithm.
•	Allow dynamic time quantum input for Round Robin.
•	Enhance animation colors for better visualization.
•	Save results as CSV or image.
•	Add dark/light mode toggle button.
•	Include average CPU utilization calculation.
________________________________________
10. Conclusion
This project visually demonstrates how different CPU scheduling algorithms operate. It provides clear insights into process waiting times, turnaround times, and how preemptive vs non-preemptive algorithms affect CPU execution order. It is an excellent tool for OS students to learn scheduling concepts interactively.

