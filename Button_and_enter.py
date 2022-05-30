import tkinter as tk
import graph
import tkinter.messagebox as MessageBox
import numpy as np
import re
from math import *
import sympy


def call():
    global group_type_graph, group_type_func
    if not (any(group_type_graph.values()) and any(group_type_func.values())):
        MessageBox.showinfo("Error", "Choose all parameters.")
    else:
        global lbl_flag
        if lbl_flag:
            global lbl_recommend_first_point, lbl_recommend_last_point, lbl_recommend_step
            lbl_recommend_first_point.destroy()
            lbl_recommend_last_point.destroy()
            lbl_recommend_step.destroy()
            lbl_flag = False
        try:

            graph_func = graph.Graph(func_entry.get(),
                                    list(({k: v for k, v in group_type_func.items() if v == 1}).keys())[0],
                                    list(({k: v for k, v in group_type_graph.items() if v == 1}).keys())[0],
                                    first_point=entry_first_point.get(),
                                    last_point=entry_last_point.get(),
                                    step=entry_step.get())

            try:
                graph_func.draw()

            except:
                # MessageBox.showinfo("Error", "Incorrect input.\nTry again.")
                graph_func.func_error()

        except ZeroDivisionError:
            MessageBox.showinfo("Error", "Division error.\nTry again.")
        except NameError:
            MessageBox.showinfo("Error", "Incorrect input.\nTry again.")


def analysis_data(func: str):
        n_all = []
        for m in re.findall(r'/ ?\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+', func):
            n = []
            for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)', m):
                n.append(m2[:m2.find('*')])
            if re.search(r'\)[+-]?\d*\.?\d*\)', m):
                m2 = re.search(r'\)[+-]?\d*\.?\d*\)', m)
                if m2.group(0) != '))':
                    n.append(m2.group(0)[1:-1])
                else:
                    n.append(0)
            n = [float(i) for i in n]
            n = np.roots(n)
            n_all.extend(n)
        n_all = list(set(n_all))
        n_all = [round(i, 2) for i in n_all if not isinstance(i, complex)]
        return n_all


def analysis():
    func = func_entry.get()
    if '^' in func:
        func = func.replace('^', '**')
    if 'x' not in func:
        graph.Graph.error = "Input function error. Function without 'x'"
        raise graph.Graph.func_error()
    x = sympy.Symbol('x', real=True)
    f = eval(func)
    fprime = f.diff(x)
    cryt_points = sympy.solve(fprime, x)
    cryt_points_out = ', '.join([str(i) for i in cryt_points])
    fprimeprime = f.diff(x).diff(x)
    intervals_points_concave_convex = sympy.solve(fprimeprime, x)
    if '/' in func:
        indefinite_points = analysis_data(func)
        cryt_points.extend(indefinite_points)
        intervals_points_concave_convex.extend(indefinite_points)
        if len(indefinite_points) == 1:
            indefinite_points_out = ', '.join([str(i) for i in indefinite_points])
        else:
            indefinite_points_out = indefinite_points[0]

    max_min_point = []
    for i in cryt_points:
        i_l = eval(str(fprime).replace('x', str(i - 0.001)))
        i_r = eval(str(fprime).replace('x', str(i + 0.001)))
        max_min_point.append([i_l >= 0, i_r >= 0])

    dictionary_cryt_point = {k: v for k, v in zip(cryt_points, max_min_point)}
    for k in dictionary_cryt_point:
        if '/' in func and k in indefinite_points:
            dictionary_cryt_point[k].append(False)
        else:
            dictionary_cryt_point[k].append(True)

    str_rise = ''
    str_fall = ''

    for k in sorted(dictionary_cryt_point.keys())[:-1]:
        if k == min(dictionary_cryt_point.keys()):
            if not dictionary_cryt_point[k][2]:
                if dictionary_cryt_point[k][0]:
                    str_rise += f'(-∞; {k}) & ({k}; '
                else:
                    str_fall += f'(-∞; {k}) & ({k}; '
            else:
                if dictionary_cryt_point[k][0]:
                    str_rise += f'(-∞; {k}] & '
                    str_fall += f'[{k}; '
                else:
                    str_fall += f'(-∞; {k}] & '
                    str_rise += f'[{k}; '
        else:
            if not dictionary_cryt_point[k][2]:
                if dictionary_cryt_point[k][0]:
                    str_rise += f'{k}) & ({k}; '
                else:
                    str_fall += f'{k}) & ({k}; '
            else:
                if dictionary_cryt_point[k][0]:
                    str_rise += f'[{k}; '
                    str_fall += f'{k}] & '
                else:
                    str_fall += f'[{k}; '
                    str_rise += f'{k}] & '

    last_point = sorted(dictionary_cryt_point.keys())[-1]
    if len(dictionary_cryt_point.keys()) == 1:
        if not dictionary_cryt_point[last_point][2]:
            if dictionary_cryt_point[last_point][0]:
                str_rise += f'(-∞; {last_point}) & ({last_point}; '
            else:
                str_fall += f'(-∞; {last_point}) & ({last_point}; '
        else:
            if dictionary_cryt_point[last_point][0]:
                str_rise += f'(-∞; {last_point}] & '
                str_fall += f'[{last_point}; '
            else:
                str_fall += f'(-∞; {last_point}] & '
                str_rise += f'[{last_point}; '
    if not dictionary_cryt_point[last_point][2]:
        if dictionary_cryt_point[last_point][0]:
            str_rise += f'{last_point}) & ({last_point}; +∞)'
            # str_fall.rstrip(' & ')
            str_fall = str_fall[:-3]
        else:
            str_fall += f'{last_point}) & ({last_point}; +∞)'
            # str_rise.rstrip(' & ')
            str_rise = str_rise[:-3]
    else:
        if dictionary_cryt_point[last_point][0]:
            str_rise += f'{last_point}]'
            # str_fall.rstrip(' & ')
            str_fall += f'[{last_point}; +∞)'
        else:
            str_fall += f'{last_point}]'
            # str_rise.rstrip(' & ')
            str_rise += f'[{last_point}; +∞)'

    intervals_points_concave_convex = sorted(intervals_points_concave_convex)
    intervals_concave_convex = []
    for i in intervals_points_concave_convex:
        i_l = eval(str(fprimeprime).replace('x', str(i - 0.001)))
        i_r = eval(str(fprimeprime).replace('x', str(i + 0.001)))
        intervals_concave_convex.append([i_l >= 0, i_r >= 0])

    dictionary_inflection_point = {k: v for k, v in zip(intervals_points_concave_convex, intervals_concave_convex)}
    for k in dictionary_inflection_point:
        if '/' in func and k in indefinite_points:
            dictionary_inflection_point[k].append(False)
        else:
            dictionary_inflection_point[k].append(True)

    str_concave = ''  # увігнутий
    str_convex = ''  # опуклий

    for k in sorted(dictionary_inflection_point.keys())[:-1]:
        if k == min(dictionary_inflection_point.keys()):
            if not dictionary_inflection_point[k][2]:
                if dictionary_inflection_point[k][0]:
                    str_concave += f'(-∞; {k}) & '
                    str_convex += f'({k}; '
                else:
                    str_convex += f'(-∞; {k}) & '
                    str_concave += f'({k}; '
            else:
                if dictionary_inflection_point[k][0]:
                    str_concave += f'(-∞; {k}] & '
                    str_convex += f'[{k}; '
                else:
                    str_convex += f'(-∞; {k}] & '
                    str_concave += f'[{k}; '
        else:
            if not dictionary_inflection_point[k][2]:
                if dictionary_inflection_point[k][0]:
                    str_concave += f'{k}) & '
                    str_convex += f'({k}; '
                else:
                    str_convex += f'{k}) & '
                    str_concave += f'({k}; '
            else:
                if dictionary_inflection_point[k][0]:
                    str_concave += f'[{k}; '
                    str_convex += f'{k}] & '
                else:
                    str_convex += f'[{k}; '
                    str_concave += f'{k}] & '

    last_point = sorted(dictionary_inflection_point.keys())[-1]
    if len(dictionary_inflection_point.keys()) == 1:
        if not dictionary_inflection_point[last_point][2]:
            if dictionary_inflection_point[last_point][0]:
                str_concave += f'(-∞; '
                # str_convex += f'({last_point}; '
            else:
                str_convex += f'(-∞; '
                # str_concave += f'({last_point}; '
        else:
            if dictionary_inflection_point[last_point][0]:
                str_concave += f'(-∞; '
                # str_convex += f'[{last_point}; '
            else:
                str_convex += f'(-∞; '
                # str_concave += f'[{last_point}; '
    if not dictionary_inflection_point[last_point][2]:
        if dictionary_inflection_point[last_point][0]:
            str_concave += f'{last_point})'
            # str_convex.rstrip(' & ')
            str_convex += f'({last_point}; +∞)'
        else:
            str_convex += f'{last_point})'
            # str_concave.rstrip(' & ')
            str_concave += f'({last_point}; +∞)'
    else:
        if dictionary_inflection_point[last_point][0]:
            str_concave += f'{last_point}]'
            # str_convex.rstrip(' & ')
            str_convex += f'[{last_point}; +∞)'
        else:
            str_convex += f'{last_point}]'
            # str_concave.rstrip(' & ')
            str_concave += f'[{last_point}; +∞)'

    analysis_window = tk.Tk()
    analysis_window.title('Analysis')
    analysis_window.resizable(width=False, height=False)
    lbl_first_prime = tk.Label(master=analysis_window, text=f'Перша похідна: y\'(x)={fprime}')
    lbl_second_prime = tk.Label(master=analysis_window, text=f'Друга похідна: y\'\'(x)={fprimeprime}')
    if '/' in func:
        lbl_indefinite_points = tk.Label(master=analysis_window, text=f'Точки невизначеності функції: {indefinite_points_out}')
    lbl_crytical_point = tk.Label(master=analysis_window, text=f'Критичні точки: {cryt_points_out}')
    lbl_intervals_rise_fall = tk.Label(master=analysis_window, text=f'При х є {str_rise} функція зростає\n'
                                                                    f'При х є {str_fall} функція спадає')   # intervals_point_rise_fall
    lbl_intervals_points_up_down = tk.Label(master=analysis_window, text=f'Точки перегину кривої: {intervals_points_concave_convex}')  # intervals_points_up_down
    lbl_intervals_up_down = tk.Label(master=analysis_window, text=f'При х є {str_concave} функція опукла\n'
                                                                  f'При х є {str_convex} функція увігнута')        # intervals_up_down
    lbl_first_prime.pack()
    lbl_second_prime.pack()
    if '/' in func:
        lbl_indefinite_points.pack()
    lbl_crytical_point.pack()
    lbl_intervals_rise_fall.pack()
    lbl_intervals_points_up_down.pack()
    lbl_intervals_up_down.pack()
    # Recommendation to build
    recommend_first_point = sorted(cryt_points)[0] - 1
    recommend_last_point = sorted(cryt_points)[-1] + 1
    analysis_step_array = [cryt_points[i+1] - cryt_points[i] for i in range(len(cryt_points)-1)]
    recommend_step = round((sum(analysis_step_array) / len(analysis_step_array) / 5), 5)
    global lbl_flag, lbl_recommend_first_point, lbl_recommend_last_point, lbl_recommend_step
    lbl_recommend_first_point = tk.Label(master=window, text=f'Рекомендована перша точка: {recommend_first_point}')
    lbl_recommend_last_point = tk.Label(master=window, text=f'Рекомендована остання точка: {recommend_last_point}')
    lbl_recommend_step = tk.Label(master=window, text=f'Рекомендований крок побудови: {recommend_step}')
    lbl_recommend_first_point.grid(row=10, column=1, pady=2, sticky='e')
    lbl_recommend_last_point.grid(row=11, column=1, pady=2, sticky='e')
    lbl_recommend_step.grid(row=12, column=1, pady=2, sticky='e')
    lbl_flag = True


def check_state(group, key):
    if group[key] == 1:
        group[key] = 0
        return group
    elif any(group.values()):
        for k, v in group.items():
            if v == 1:
                group[k], group[key] = 0, 1
                return group
    else:
        group[key] = 1
        return group


def x_y():
    global group_type_func
    group_type_func = check_state(group_type_func, 'x_y')
    func_func.config(text='x(y)=')
    but_x_y.config(relief=state_button[group_type_func['x_y']])
    but_y_x.config(relief=state_button[group_type_func['y_x']])


def y_x():
    global group_type_func
    group_type_func = check_state(group_type_func, 'y_x')
    # if group_type_func['x_y'] == 1:
    #     but_x_y.config(relief=tk.GROOVE)
    # else:
    #     but_x_y.config(relief=tk.RAISED)
    # if group_type_func['y_x'] == 1:
    #     but_y_x.config(relief=tk.GROOVE)
    # else:
    #     but_y_x.config(relief=tk.RAISED)
    func_func.config(text='y(x)=')
    but_x_y.config(relief=state_button[group_type_func['x_y']])
    but_y_x.config(relief=state_button[group_type_func['y_x']])


def scatter():
    global group_type_graph
    group_type_graph = check_state(group_type_graph, 'scatter')
    but_scat.config(relief=state_button[group_type_graph['scatter']])
    but_line.config(relief=state_button[group_type_graph['line']])
    entry_hist.config(state='disabled')


def line():
    global group_type_graph
    group_type_graph = check_state(group_type_graph, 'line')
    but_scat.config(relief=state_button[group_type_graph['scatter']])
    but_line.config(relief=state_button[group_type_graph['line']])
    entry_hist.config(state='disabled')


window = tk.Tk()
window.title("Graph")
# window.config(bg="pink")
window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=200, weight=1)
window.resizable(width=False, height=False)
# func_frame = tk.Frame(master=window, height=50)
# func_entry = tk.Entry(master=func_frame, width=50)
# func_label = tk.Label(master=func_frame, text="Put function")

func_entry = tk.Entry(master=window, width=50)
func_label = tk.Label(master=window, text="Put function")
func_func = tk.Label(master=window, text='y(x)=')
label_empty = tk.Frame(master=window)
lbl_type_func = tk.Label(master=window, text="Type of function")

but_y_x = tk.Button(
    master=window,
    text="y(x)=x",
    command=y_x,
    relief=tk.RAISED
)
but_x_y = tk.Button(
    master=window,
    text="x(y)=y",
    command=x_y
)

lbl_type_graph = tk.Label(master=window, text="Type of build graph")

entry_hist = tk.Entry(master=window, width=5, state="disabled")
entry_hist.insert(0, '1')
but_scat = tk.Button(
    master=window,
    text="Scatter",
    command=scatter
)

but_line = tk.Button(
    master=window,
    text="Line",
    command=line
)

## delta
frame_step = tk.Frame(master=window)
lbl_step = tk.Label(master=frame_step, text="Step")
entry_step = tk.Entry(master=frame_step, width=10)
entry_step.insert(0, '1')
frame_first_point = tk.Frame(master=window)
lbl_firts_point = tk.Label(master=frame_first_point, text="Start")
entry_first_point = tk.Entry(master=frame_first_point, width=10)
entry_first_point.insert(0, '0')
frame_last_point = tk.Frame(master=window)
lbl_last_point = tk.Label(master=frame_last_point, text="End")
entry_last_point = tk.Entry(master=frame_last_point, width=10)
entry_last_point.insert(0, '10')

btn_call_graph = tk.Button(
    master=window,
    text='call function',
    command=call
)

but_anal = tk.Button(
    master=window,
    text="Analysis",
    command=analysis
)

# instruction for entry function
frm_for_instr = tk.Frame(master=window)
lbl_instr_1 = tk.Label(master=frm_for_instr, text='Інструкція заповнення поля функції')
lbl_instr_2 = tk.Label(master=frm_for_instr, text='1. Обов\'язково записувати х в дужки - (х)')
lbl_instr_3 = tk.Label(master=frm_for_instr, text='2. Недопускати запис під тригонометричними, логарифмічними виразами,\n'
                                           'в знаменнику інші тригонометричні, логарифмічні вирази, дроби')
lbl_instr_4 = tk.Label(master=frm_for_instr, text='3. Скорочувати всі множники х однакових степенів, вводити члени виразу ,\n'
                                           'функції в знаменнику дробу і логарифму в порядку спадання степеня х')
lbl_instr_5 = tk.Label(master=frm_for_instr, text='4. Недопускати пробіли, записувати всю функцію без пробілів')
lbl_instr_6 = tk.Label(master=frm_for_instr, text='5. Під дужкою логарифму записувати спочатку функцію, потім базу через кому')
lbl_instr_7 = tk.Label(master=frm_for_instr, text='Неправильно: log(1*sin(x)); 1/(1*(x)+sin(x)); sin(5*(x)**2+log(x, e)),\n'
                                           'Правильно: 10*(x)+1/(-3*(x)**3+0*(x)**2+5*(x))-log(1*(x)+4, e)+sin(1*(x))')

# lbl_instr_8 = tk.Label(master=frm_for_instr, text='Іноді ')
# state of press dictionary
lbl_flag = False
group_type_func = {'y_x': 0, 'x_y': 0}
group_type_graph = {'scatter': 0, 'line': 0}
state_button = {1: tk.GROOVE, 0: tk.RAISED}

# y= or x= depends of buuton
frm_for_instr.grid(row=0, column=1, pady=2)
lbl_instr_1.grid(row=0, column=0, sticky='w', pady=2)
lbl_instr_2.grid(row=1, column=0, sticky='w', pady=2)
lbl_instr_3.grid(row=2, column=0, sticky='w', pady=2)
lbl_instr_4.grid(row=3, column=0, sticky='w', pady=2)
lbl_instr_5.grid(row=4, column=0, sticky='w', pady=2)
lbl_instr_6.grid(row=5, column=0, sticky='w', pady=2)
lbl_instr_7.grid(row=6, column=0, sticky='w', pady=2)

func_label.grid(row=1, column=1, sticky='s')
func_entry.grid(row=2, column=1, sticky='w')
func_func.grid(row=2, column=0, sticky='e')
label_empty.grid(row=3, column=1)
# func_frame.grid(row=0, column=1, pady=10)
lbl_type_func.grid(row=4, column=1, padx=10, pady=5)
# frame_but_y_x.grid(row=2, column=0, padx=10)
but_y_x.grid(row=5, column=0, padx=10, sticky='e')
but_x_y.grid(row=5, column=2, padx=10, sticky='w')
lbl_type_graph.grid(row=6, column=1, padx=10, pady=5)
but_line.grid(row=7, column=0, padx=10, sticky='e')
but_scat.grid(row=7, column=2, padx=10, sticky='w')
frame_first_point.grid(row=8, column=0, padx=20, pady=5)
lbl_firts_point.grid(row=0, column=0, padx=5)
entry_first_point.grid(row=0, column=1)
frame_last_point.grid(row=8, column=1, padx=20, pady=5)
lbl_last_point.grid(row=0, column=0, padx=5)
entry_last_point.grid(row=0, column=1)
frame_step.grid(row=8, column=2, padx=20, pady=5)
lbl_step.grid(row=0, column=0, padx=5)
entry_step.grid(row=0, column=1)
btn_call_graph.grid(row=9, column=1, pady=20, sticky='e')
but_anal.grid(row=9, column=1, pady=20, sticky='w')
window.mainloop()

