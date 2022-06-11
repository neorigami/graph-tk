import re
from math import *
import numpy as np
import sympy
from sympy import *
import graph
import tkinter as tk
import tkinter.messagebox as MessageBox
sympy.init_printing(use_unicode=True)


def analysis(func_entry, window, group_type_func, group_type_graph, entry_first_point, entry_last_point, entry_step):
    # group_type_func = "x_y"
    # group_type_graph = "line"

    # initialisation function

    graph_func = graph.Graph(func_entry.get(),
                             "x_y",
                             "line",
                             first_point=entry_first_point.get(),
                             last_point=entry_last_point.get(),
                             step=entry_step.get())

    func = graph_func.func  # використання ініціалізації для початкової обробки функції перед аналізом
    if 'x' not in func:
        graph_func.error = "Input function error. Function without 'x'"
        raise graph_func.func_error()
    x = Symbol('x')        # з бібліотеки sympy визначення змінної у фукнції
    init_printing(use_unicode=True)
    cryt_points = []
    intervals_points_concave_convex = []
    try:
        f = eval(func)          # надання можливості sympy вираховувати похідну
        fprime = f.diff(x)      # знаходження похідної
        cryt_points = list(filter(lambda x: not isinstance(complex, x), sympy.solve(fprime, x)))  # знаходження нулів похідної, відсіювання комлексних
        cryt_points = [round(eval(str(i)), graph_func.presicion) for i in cryt_points]  # переведення дробових виразів у десяткові
        cryt_points_out = ', '.join([str(i) for i in cryt_points])  # виведення критичних точок через кому
        if len(sympy.solve(fprime, x)) == 1:
            cryt_points_out = cryt_points[0]     # якщо перша похідна одна, то виведення одного числа
        fprimeprime = f.diff(x).diff(x)     # друга похідна
        intervals_points_concave_convex = list(filter(lambda x: not isinstance(complex, x), sympy.solve(fprimeprime, x)))  # знаходження нулів другої похідної, відсіювання комлексних
        intervals_points_concave_convex = [round(eval(str(i)), graph_func.presicion) for i in intervals_points_concave_convex]  # знаходження нулів другої похідної, переведення дробових виразів у десяткові
        intervals_points_concave_convex_out = ', '.join([str(i) for i in intervals_points_concave_convex])  # виведення точок перегину через кому
        if len(sympy.solve(fprimeprime, x)) == 1:
            intervals_points_concave_convex_out = intervals_points_concave_convex[0]     # якщо друга похідна одна, то виведення одного числа

    except:
        MessageBox.showinfo("Error", "Analysis error.\nTry again.")

    if '/' in func or 'tan' in func or 'ctg' in func:           # якщо присутні вирази, що створюють точки невизначеності функції
        indefinite_points = graph_func.analysis_data(func)      # визначення точок
        cryt_points.extend(indefinite_points)
        intervals_points_concave_convex.extend(indefinite_points)       # додавання для подальшого розподілу по проміжках
        if len(indefinite_points) != 1:
            indefinite_points_out = ', '.join([str(i) for i in indefinite_points])
        else:
            indefinite_points_out = indefinite_points[0]


    # if re.search(r'\(.*?\(?x\)?[+-]?\d*\.?\d*\)+\*\*0.\d+', func):
    #
    # if re.search(r'log', func):
    fprime = str(fprime).replace('x', '(x)')
    max_min_point = []
    for i in cryt_points:
        i_l = eval(str(fprime).replace('x', str(i - 0.001)))
        i_r = eval(str(fprime).replace('x', str(i + 0.001)))
        max_min_point.append([i_l >= 0, i_r >= 0])              # визначення знака першої похідної на кожному проміжку
                                                                # перед і після точки, True для додатнього
    dictionary_cryt_point = {k: v for k, v in zip(cryt_points, max_min_point)}      # кожній точці присвоюється значення true, false
    for k in dictionary_cryt_point:                                                 # або false, true, що означатиме зростання чи спадання перед і після точки
        if '/' in func or 'tan' in func or 'ctg' in func and k in indefinite_points:
            dictionary_cryt_point[k].append(False)
        else:                                           # якщо критична точка є точкою невизначеності функції, позначається фалз, як точка "не включно"
            dictionary_cryt_point[k].append(True)

    str_rise = ''                                               # наступні рядки для побудови виразів зростання і
    str_fall = ''                                               # спадання функції на проміжках. Для основи обрано дві
    if len(dictionary_cryt_point) > 0:                          # змінні до яких будуть додаватися значення типу string
        for k in sorted(dictionary_cryt_point.keys())[:-1]:     # спершу визначення чи точка входять в область
            if k == min(dictionary_cryt_point.keys()):          # визначення, потім чи є точка першою, для підставлення
                if not dictionary_cryt_point[k][2]:             # безкінечності
                    if dictionary_cryt_point[k][0]:             # в рядку 74 перевірка на те, що точка перша
                        str_rise += f'(-∞; {k}) & ({k}; '       # в рядку 75 перевірка чи функція у точці визначена
                    else:                                       # через булінове значення
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
                        # str_rise += f'[{k}; '
                        # str_fall += f'{k}] & '
                        str_fall += f'[{k}; '
                        str_rise += f'{k}] & '
                    else:
                        # str_fall += f'[{k}; '
                        # str_rise += f'{k}] & '
                        str_rise += f'[{k}; '
                        str_fall += f'{k}] & '

        last_point = sorted(dictionary_cryt_point.keys())[-1]               # потім підстановка чи є точка останньою
        if len(dictionary_cryt_point.keys()) == 1:                          # в попередніх рядках була умова допущення
            if not dictionary_cryt_point[last_point][2]:                    # до виразів, якщо кількість критичних точок
                if dictionary_cryt_point[last_point][0]:                    # більше 0. Якщо ж ні, то жодна з умов не
                    str_rise = f'(-∞; {last_point}) & ({last_point}; +∞)'   # виконається. Якщо тільки 1 критична точка,
                else:                                                       # то відповідна перевірка буде перевірена
                    str_fall = f'(-∞; {last_point}) & ({last_point}; +∞)'   # як в попередньому, але з включенням з
            else:                                                           # з додатньою безкінечністю
                if dictionary_cryt_point[last_point][0]:
                    str_rise += f'(-∞; {last_point}]'
                    str_fall += f'[{last_point}; +∞)'
                else:
                    str_fall += f'(-∞; {last_point}]'
                    str_rise += f'[{last_point}; +∞)'
        else:
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
                    # str_fall = str_fall[:-3]
                    str_fall += f'{last_point}]'
                    # str_rise.rstrip(' & ')
                    str_rise += f'[{last_point}; +∞)'

    fprimeprime = str(fprimeprime).replace('x', '(x)')
    intervals_concave_convex = []
    if isinstance(intervals_points_concave_convex, list):
        intervals_points_concave_convex = sorted(intervals_points_concave_convex)   # аналогічно з попередніми,
        for i in intervals_points_concave_convex:                                   # визначення знака другої похідної
            i_l = eval(str(fprimeprime).replace('x', str(i - 0.001)))               # зліва і справа від точки перегину
            i_r = eval(str(fprimeprime).replace('x', str(i + 0.001)))
            intervals_concave_convex.append([i_l >= 0, i_r >= 0])
        dictionary_inflection_point = {k: v for k, v in zip(intervals_points_concave_convex, intervals_concave_convex)}
    else:                                                                        # умова, якщо точка перегину лише одна
        i_l = eval(str(fprimeprime).replace('x', str(intervals_points_concave_convex - 0.001)))
        i_r = eval(str(fprimeprime).replace('x', str(intervals_points_concave_convex + 0.001)))
        intervals_concave_convex.append([i_l >= 0, i_r >= 0])
        dictionary_inflection_point = {intervals_points_concave_convex: intervals_concave_convex[0]}

    for k in dictionary_inflection_point:                       # аналогічні операції при першій похідній і аналіз
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
                str_concave += '+∞)'
                # str_convex += f'({last_point}; '
            else:
                str_convex += '+∞)'
                # str_concave += f'({last_point}; '
        else:
            if dictionary_inflection_point[last_point][0]:
                str_concave += f'(-∞; {last_point}]'
                str_convex += f'[{last_point}; +∞)'
            else:
                str_convex += f'[{last_point}; +∞)'
                str_concave += f'(-∞; {last_point}]'
    else:
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
                # str_concave += f'{last_point}]'
                # # str_convex.rstrip(' & ')
                # str_convex += f'[{last_point}; +∞)'
                str_convex += f'{last_point}]'
                # str_concave.rstrip(' & ')
                str_concave += f'[{last_point}; +∞)'
            else:
                # str_convex += f'{last_point}]'
                # # str_concave.rstrip(' & ')
                # str_concave += f'[{last_point}; +∞)'
                str_concave += f'{last_point}]'
                # str_convex.rstrip(' & ')
                str_convex += f'[{last_point}; +∞)'

    analysis_window = tk.Tk()
    analysis_window.title('Analysis')
    analysis_window.minsize(width=300, height=100)
    analysis_window.resizable(width=False, height=False)
    lbl_first_prime = tk.Label(master=analysis_window, text=f'Перша похідна: y\'(x)={fprime}')
    lbl_second_prime = tk.Label(master=analysis_window, text=f'Друга похідна: y\'\'(x)={fprimeprime}')
    if '/' in func:
        lbl_indefinite_points = tk.Label(master=analysis_window,
                                         text=f'Точки невизначеності функції: {indefinite_points_out}')
    else:
        lbl_indefinite_points = tk.Label(master=analysis_window,
                                         text=f'Точки невизначеності функції: x є R')
    if len(cryt_points) == 0:
        lbl_crytical_point = tk.Label(master=analysis_window, text=f'Критичні точки: відсутні')
        if ('x' in str(fprime) and eval(fprime.replace('x', 0)) >= 0) or fprime >= 0:
            lbl_intervals_rise_fall = tk.Label(master=analysis_window, text=f'При х є R функція зростає\n')
        else:
            lbl_intervals_rise_fall = tk.Label(master=analysis_window, text=f'При х є R функція спадає\n')
    else:
        lbl_crytical_point = tk.Label(master=analysis_window, text=f'Критичні точки: {cryt_points_out}')
        lbl_intervals_rise_fall = tk.Label(master=analysis_window, text=f'При х є {str_rise} функція зростає\n'
                                                                        f'При х є {str_fall} функція спадає')  # intervals_point_rise_fall
    lbl_intervals_points_up_down = tk.Label(master=analysis_window,
                                            text=f'Точки перегину кривої: {intervals_points_concave_convex_out}')  # intervals_points_up_down
    lbl_intervals_up_down = tk.Label(master=analysis_window, text=f'При х є {str_concave} функція опукла\n'
                                                                  f'При х є {str_convex} функція увігнута')  # intervals_up_down
    lbl_first_prime.pack()
    lbl_second_prime.pack()
    lbl_indefinite_points.pack()
    lbl_crytical_point.pack()
    lbl_intervals_rise_fall.pack()
    lbl_intervals_points_up_down.pack()
    lbl_intervals_up_down.pack()
    # Recommendation to build
    if cryt_points:                                                    # визначення рекомендованих точок побудови,
        recommend_first_point = sorted(cryt_points)[0] - 1             # в межах яких видно зміну поведінки функції
        recommend_last_point = sorted(cryt_points)[-1] + 1             # це охоплює критичні точки, точки невизначеності
        if len(cryt_points) > 1:                                       # і невеликий проміжко навколо крайніх точок
            analysis_step_array = [cryt_points[i + 1] - cryt_points[i] for i in range(len(cryt_points) - 1)]
            recommend_step = round((sum(analysis_step_array) / len(analysis_step_array) / 5), 5)
        else:                         # визначення рекомендованого кроку, щоб не було пропущено критичних точок через
            recommend_step = 0.5      # "перескок"
        global lbl_flag, lbl_recommend_first_point, lbl_recommend_last_point, lbl_recommend_step
        lbl_recommend_first_point = tk.Label(master=window, text=f'Рекомендована перша точка: {recommend_first_point}')
        lbl_recommend_last_point = tk.Label(master=window, text=f'Рекомендована остання точка: {recommend_last_point}')
        lbl_recommend_step = tk.Label(master=window, text=f'Рекомендований крок побудови: {recommend_step}')
        lbl_recommend_first_point.grid(row=10, column=1, pady=2, sticky='e')
        lbl_recommend_last_point.grid(row=11, column=1, pady=2, sticky='e')
        lbl_recommend_step.grid(row=12, column=1, pady=2, sticky='e')
        lbl_flag = True

