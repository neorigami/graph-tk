# import re
# from math import *
# import numpy as np
import sympy
import graph
import tkinter as tk
import tkinter.messagebox as MessageBox


def analysis(func_entry, window, group_type_func, group_type_graph, entry_first_point, entry_last_point, entry_step):
    group_type_func = "x_y"
    group_type_graph = "line"

    # initialisation function

    graph_func = graph.Graph(func_entry.get(),
                             group_type_func,
                             group_type_graph,
                             first_point=entry_first_point.get(),
                             last_point=entry_last_point.get(),
                             step=entry_step.get())

    func = graph_func.func
    # if '^' in func:
    #     func = func.replace('^', '**')
    if 'x' not in func:
        graph_func.error = "Input function error. Function without 'x'"
        raise graph_func.func_error()
    # if not '(x)**' in func:
    #     graph_func.error = "Analisys isn't available"
    #     raise graph_func.func_error()
    x = sympy.Symbol('x', real=True)
    try:
        f = eval(func)
        fprime = f.diff(x)
        cryt_points = sympy.solve(fprime, x)
        cryt_points_out = ', '.join([str(i) for i in cryt_points])
        fprimeprime = f.diff(x).diff(x)
        intervals_points_concave_convex = sympy.solve(fprimeprime, x)
        if len(sympy.solve(fprimeprime, x)) == 0:
            intervals_points_concave_convex = f.diff(x).diff(x)
    except:
        MessageBox.showinfo("Error", "Analysis error.\nTry again.")

    if '/' in func or 'tan' in func or 'ctg' in func:
        # indefinite_points = analysis_data(func)
        indefinite_points = graph_func.analysis_data(func)
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
        if '/' in func or 'tan' in func or 'ctg' in func and k in indefinite_points:
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
        lbl_indefinite_points = tk.Label(master=analysis_window,
                                         text=f'Точки невизначеності функції: {indefinite_points_out}')
    lbl_crytical_point = tk.Label(master=analysis_window, text=f'Критичні точки: {cryt_points_out}')
    lbl_intervals_rise_fall = tk.Label(master=analysis_window, text=f'При х є {str_rise} функція зростає\n'
                                                                    f'При х є {str_fall} функція спадає')  # intervals_point_rise_fall
    lbl_intervals_points_up_down = tk.Label(master=analysis_window,
                                            text=f'Точки перегину кривої: {intervals_points_concave_convex}')  # intervals_points_up_down
    lbl_intervals_up_down = tk.Label(master=analysis_window, text=f'При х є {str_concave} функція опукла\n'
                                                                  f'При х є {str_convex} функція увігнута')  # intervals_up_down
    lbl_first_prime.pack()
    lbl_second_prime.pack()
    if '/' in func or 'tan' in func or 'ctg' in func:
        lbl_indefinite_points.pack()
    lbl_crytical_point.pack()
    lbl_intervals_rise_fall.pack()
    lbl_intervals_points_up_down.pack()
    lbl_intervals_up_down.pack()
    # Recommendation to build
    recommend_first_point = sorted(cryt_points)[0] - 1
    recommend_last_point = sorted(cryt_points)[-1] + 1
    analysis_step_array = [cryt_points[i + 1] - cryt_points[i] for i in range(len(cryt_points) - 1)]
    recommend_step = round((sum(analysis_step_array) / len(analysis_step_array) / 5), 5)
    global lbl_flag, lbl_recommend_first_point, lbl_recommend_last_point, lbl_recommend_step
    lbl_recommend_first_point = tk.Label(master=window, text=f'Рекомендована перша точка: {recommend_first_point}')
    lbl_recommend_last_point = tk.Label(master=window, text=f'Рекомендована остання точка: {recommend_last_point}')
    lbl_recommend_step = tk.Label(master=window, text=f'Рекомендований крок побудови: {recommend_step}')
    lbl_recommend_first_point.grid(row=10, column=1, pady=2, sticky='e')
    lbl_recommend_last_point.grid(row=11, column=1, pady=2, sticky='e')
    lbl_recommend_step.grid(row=12, column=1, pady=2, sticky='e')
    lbl_flag = True

