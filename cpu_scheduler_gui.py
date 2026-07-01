import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Scheduling algorithms implementations

def sjf_non_preemptive(arrival, burst, pid_list):
    n = len(burst)
    completed = [False]*n
    t = min(arrival)
    gantt = []
    metrics = {pid: {'arrival': a, 'burst': b} for pid, a, b in zip(pid_list, arrival, burst)}

    while not all(completed):
        # pick available with smallest burst
        candidates = [i for i in range(n) if (not completed[i]) and arrival[i] <= t]
        if not candidates:
            t = min([arrival[i] for i in range(n) if not completed[i]])
            continue
        idx = min(candidates, key=lambda i: burst[i])
        start = t
        end = t + burst[idx]
        gantt.append((pid_list[idx], start, end))
        t = end
        completed[idx] = True
        metrics[pid_list[idx]]['start'] = start
        metrics[pid_list[idx]]['end'] = end
        metrics[pid_list[idx]]['turnaround'] = end - arrival[idx]
        metrics[pid_list[idx]]['waiting'] = start - arrival[idx]
    return gantt, metrics


def sjf_preemptive(arrival, burst, pid_list):
    n = len(burst)
    remaining = burst[:]
    t = min(arrival)
    gantt = []
    metrics = {pid: {'arrival': a, 'burst': b} for pid, a, b in zip(pid_list, arrival, burst)}
    last_pid = None

    while any(r>0 for r in remaining):
        # find process with minimum remaining among available
        available = [i for i in range(n) if arrival[i] <= t and remaining[i] > 0]
        if not available:
            t = min([arrival[i] for i in range(n) if remaining[i] > 0 and arrival[i] > t])
            continue
        idx = min(available, key=lambda i: remaining[i])
        # run for 1 time unit
        if last_pid == pid_list[idx]:
            # extend last
            gantt[-1] = (gantt[-1][0], gantt[-1][1], gantt[-1][2]+1)
        else:
            gantt.append((pid_list[idx], t, t+1))
        remaining[idx] -= 1
        t += 1
        last_pid = pid_list[idx]
        if remaining[idx] == 0:
            metrics[pid_list[idx]]['end'] = t
            metrics[pid_list[idx]]['turnaround'] = t - arrival[idx]
            # waiting = turnaround - burst
            metrics[pid_list[idx]]['waiting'] = metrics[pid_list[idx]]['turnaround'] - burst[idx]
    # fill start times
    starts = {}
    for pid, s, e in gantt:
        if pid not in starts:
            starts[pid] = s
    for pid in pid_list:
        metrics[pid]['start'] = starts[pid]
    return gantt, metrics


def priority_non_preemptive(arrival, burst, priority, pid_list):
    n = len(burst)
    completed = [False]*n
    t = min(arrival)
    gantt = []
    metrics = {pid: {'arrival': a, 'burst': b, 'priority': p} for pid, a, b, p in zip(pid_list, arrival, burst, priority)}

    while not all(completed):
        candidates = [i for i in range(n) if (not completed[i]) and arrival[i] <= t]
        if not candidates:
            t = min([arrival[i] for i in range(n) if not completed[i]])
            continue
        idx = min(candidates, key=lambda i: priority[i])
        start = t
        end = t + burst[idx]
        gantt.append((pid_list[idx], start, end))
        t = end
        completed[idx] = True
        metrics[pid_list[idx]]['start'] = start
        metrics[pid_list[idx]]['end'] = end
        metrics[pid_list[idx]]['turnaround'] = end - arrival[idx]
        metrics[pid_list[idx]]['waiting'] = start - arrival[idx]
    return gantt, metrics


def priority_preemptive(arrival, burst, priority, pid_list):
    n = len(burst)
    remaining = burst[:]
    t = min(arrival)
    gantt = []
    metrics = {pid: {'arrival': a, 'burst': b, 'priority': p} for pid, a, b, p in zip(pid_list, arrival, burst, priority)}
    last_pid = None

    while any(r>0 for r in remaining):
        available = [i for i in range(n) if arrival[i] <= t and remaining[i] > 0]
        if not available:
            t = min([arrival[i] for i in range(n) if remaining[i] > 0 and arrival[i] > t])
            continue
        idx = min(available, key=lambda i: priority[i])
        if last_pid == pid_list[idx]:
            gantt[-1] = (gantt[-1][0], gantt[-1][1], gantt[-1][2]+1)
        else:
            gantt.append((pid_list[idx], t, t+1))
        remaining[idx] -= 1
        t += 1
        last_pid = pid_list[idx]
        if remaining[idx] == 0:
            metrics[pid_list[idx]]['end'] = t
            metrics[pid_list[idx]]['turnaround'] = t - arrival[idx]
            metrics[pid_list[idx]]['waiting'] = metrics[pid_list[idx]]['turnaround'] - burst[idx]
    starts = {}
    for pid, s, e in gantt:
        if pid not in starts:
            starts[pid] = s
    for pid in pid_list:
        metrics[pid]['start'] = starts[pid]
    return gantt, metrics


# GUI

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        root.title('CPU Scheduling Visualizer')
        root.geometry('1100x700')

        control = ttk.Frame(root)
        control.pack(side='left', fill='y', padx=8, pady=8)

        ttk.Label(control, text='Algorithm').pack(pady=4)
        self.alg = tk.StringVar(value='SJF Non-Preemptive')
        algs = ['SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive']
        ttk.OptionMenu(control, self.alg, self.alg.get(), *algs).pack()

        ttk.Label(control, text='Number of processes').pack(pady=4)
        self.n_entry = ttk.Entry(control)
        self.n_entry.pack()

        ttk.Button(control, text='Create table', command=self.create_table_inputs).pack(pady=6)
        ttk.Button(control, text='Run', command=self.run).pack(pady=6)

        ttk.Separator(control).pack(fill='x', pady=8)

        ttk.Label(control, text='Averages').pack()
        self.avg_wait = ttk.Label(control, text='Avg waiting: -')
        self.avg_wait.pack()
        self.avg_tat = ttk.Label(control, text='Avg turnaround: -')
        self.avg_tat.pack()

        # center area
        center = ttk.Frame(root)
        center.pack(side='left', fill='both', expand=True)

        top = ttk.Frame(center)
        top.pack(fill='x')

        self.table_frame = ttk.Frame(top)
        self.table_frame.pack(side='left', fill='x', padx=8, pady=8)

        # treeview
        cols = ('pid', 'arrival', 'burst', 'priority', 'start', 'end', 'turnaround', 'waiting')
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show='headings', height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90)
        self.tree.pack(fill='x')

        # plot area
        self.fig, self.ax = plt.subplots(figsize=(8,2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=center)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=8)

        # animation area
        bottom = ttk.Frame(center)
        bottom.pack(fill='x')
        ttk.Label(bottom, text='Process state animation').pack()
        self.anim_canvas = tk.Canvas(bottom, height=120)
        self.anim_canvas.pack(fill='x', padx=8, pady=8)

        self.inputs = []

    def create_table_inputs(self):
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror('Error', 'Enter valid positive integer for number of processes')
            return
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.table_frame)
        frame.pack()
        headers = ['PID', 'Arrival', 'Burst', 'Priority']
        for j,h in enumerate(headers):
            ttk.Label(frame, text=h).grid(row=0, column=j)
        self.inputs = []
        for i in range(n):
            pid = f'P{i+1}'
            ttk.Label(frame, text=pid).grid(row=i+1, column=0)
            a = ttk.Entry(frame, width=8)
            a.grid(row=i+1, column=1)
            b = ttk.Entry(frame, width=8)
            b.grid(row=i+1, column=2)
            p = ttk.Entry(frame, width=8)
            p.grid(row=i+1, column=3)
            self.inputs.append((pid, a, b, p))

    def run(self):
        if not self.inputs:
            messagebox.showerror('Error', 'Create the processes table first')
            return
        pid_list = []
        arrival = []
        burst = []
        priority = []
        try:
            for pid, a_e, b_e, p_e in self.inputs:
                pid_list.append(pid)
                a = int(a_e.get())
                b = int(b_e.get())
                pr = int(p_e.get()) if p_e.get() else 0
                if a < 0 or b <= 0:
                    raise ValueError
                arrival.append(a)
                burst.append(b)
                priority.append(pr)
        except Exception:
            messagebox.showerror('Error', 'Enter valid numeric values. Arrival >=0. Burst >0')
            return

        alg = self.alg.get()
        if alg == 'SJF Non-Preemptive':
            gantt, metrics = sjf_non_preemptive(arrival, burst, pid_list)
        elif alg == 'SJF Preemptive':
            gantt, metrics = sjf_preemptive(arrival, burst, pid_list)
        elif alg == 'Priority Non-Preemptive':
            gantt, metrics = priority_non_preemptive(arrival, burst, priority, pid_list)
        else:
            gantt, metrics = priority_preemptive(arrival, burst, priority, pid_list)

        # fill tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        total_wait = 0
        total_tat = 0
        for pid in pid_list:
            m = metrics[pid]
            wait = m.get('waiting', 0)
            tat = m.get('turnaround', 0)
            total_wait += wait
            total_tat += tat
            self.tree.insert('', 'end', values=(pid, m['arrival'], m['burst'], m.get('priority', ''), m.get('start', ''), m.get('end', ''), tat, wait))
        n = len(pid_list)
        self.avg_wait.config(text=f'Avg waiting: {total_wait/n:.2f}')
        self.avg_tat.config(text=f'Avg turnaround: {total_tat/n:.2f}')

        # draw gantt
        self.draw_gantt(gantt)

        # run animation
        threading.Thread(target=self.animate_states, args=(gantt, pid_list), daemon=True).start()

    def draw_gantt(self, gantt):
        self.ax.clear()
        if not gantt:
            self.canvas.draw()
            return
        pids = [g[0] for g in gantt]
        unique = []
        for p in pids:
            if p not in unique:
                unique.append(p)
        y_map = {pid: i for i, pid in enumerate(unique)}
        for pid, s, e in gantt:
            self.ax.barh(y_map[pid], e-s, left=s)
            self.ax.text((s+e)/2, y_map[pid], pid, va='center', ha='center')
        self.ax.set_yticks(list(y_map.values()))
        self.ax.set_yticklabels(list(y_map.keys()))
        self.ax.set_xlabel('Time')
        self.fig.tight_layout()
        self.canvas.draw()

    def animate_states(self, gantt, pid_list):
        # timeline states per time unit
        timeline = []
        if not gantt:
            return
        end_time = max(e for _,_,e in gantt)
        state_at = {t: None for t in range(end_time)}
        for pid, s, e in gantt:
            for t in range(s, e):
                state_at[t] = pid
        # prepare canvas
        self.anim_canvas.delete('all')
        width = self.anim_canvas.winfo_width() or 800
        lane_h = 25
        gap = 8
        pid_y = {pid: i*(lane_h+gap) for i, pid in enumerate(pid_list)}
        # draw labels
        for pid, y in pid_y.items():
            self.anim_canvas.create_text(30, y+lane_h/2, text=pid, anchor='w')
        # animate
        for t in range(end_time+1):
            # clear time marks
            self.anim_canvas.delete('time')
            x_unit = max(10, (width-100)/max(1,end_time))
            for pid in pid_list:
                y = pid_y[pid]
                # draw a small rect for each time unit showing state
                for tt in range(t):
                    owner = state_at.get(tt)
                    color = 'lightgray' if owner is None else ('green' if owner==pid else 'orange')
                    x1 = 100 + tt*x_unit
                    x2 = x1 + x_unit
                    self.anim_canvas.create_rectangle(x1, y, x2, y+lane_h, fill=color, outline='', tags='time')
            # draw current time marker
            self.anim_canvas.create_text(80, 100, text=f'Time {t}', tags='time')
            self.anim_canvas.update()
            time.sleep(0.3)


if __name__ == '__main__':
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
