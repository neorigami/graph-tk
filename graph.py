from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from math import *
import re
import tkinter.messagebox as MessageBox
import sympy


def is_digit(*args):           # перевірка на число
    for i in args:
        try:
            x = float(i)
        except ValueError:
            return False
    return True


def check_zero_division(string):                # перевірка на присутність ділення на 0
    if re.findall(r'/\([^x]*?\)', string):
        for i in re.findall(r'/\([^x]*?\)', string):
            if eval(i[1:]) == 0:
                return False
    return True


def check_interval(x0, xn, step):               # перевірка на число інтервали і крок
    if not is_digit(x0, xn, step):
        return True
    x0, xn, step = float(x0), float(xn), float(step)                        # перевірка правильного введення
    if (x0 > xn and step >= 0) or (xn > x0 and step <= 0) or step == 0:       # інтервалу і кроку на безкінечність
        return True


def find_roots(func):
    func = func[1:]
    x = sympy.Symbol('x')
    func = eval(func)
    root_x = []
    for i in sympy.solve(func, x):
        try:
            root_x.append(eval(str(i)))
        except:
            pass
    return root_x


class Graph:
    sympy.init_printing(use_unicode=True)
    def __init__(self, func, type_func, type_graph, first_point, last_point, step):
        self.type_func = type_func
        self.type_graph = type_graph
        if check_interval(first_point, last_point, step):
            self.error = 'Incorrect input interval or step'
            raise self.func_error()
        self.first_point = float(first_point)
        self.last_point = float(last_point)
        self.step = float(step)
        # before initiate func
        if type_func == 'y_x':                  # перевірка на введення, залежно від типу функції, змінної
            if 'x' not in func:
                self.error = "Input function error. Function without 'x'"
                raise self.func_error()
            self.func = str(func)

        else:
            if 't' not in func:
                self.error = "Input function error. Function without 't'"
                raise self.func_error()
            self.func = str(func).replace('t', 'x')

        if '^' in func:
            self.func = self.func.replace('^', '**')
        # self.func = self.func.replace('(x)', 'x')       # усунення різниці де поставлені дужки навколо х, де ні
        self.func = self.func.replace('x', '(x)')
        if "|" in self.func:                                    # перетворення модулів на прийнятну для програми функцію
            for m in re.findall(r'\|.*?\|', self.func): # tag(2*x**3+9*(x)**2+9*(x))+(4135+9*x-2*x**2)-tag(6*x+9)
                self.func = self.func.replace(m, f'abs({m[1:-1]})', 1)
        if 'tan' in self.func:                          # розкладання тангенса на синус/косинус
            for m in re.findall(r'tan\(.*?x(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):
                self.func = self.func.replace(m, f'(sin{m[3:]})/cos{m[3:]}', 1)
        if 'ctg' in self.func:                          # розкладання тангенса на косинус/синус
            for m in re.findall(r'ctg\(.*?x(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):
                self.func = self.func.replace(m, f'(cos{m[3:]})/sin{m[3:]}', 1)
        if 'log' in self.func:                          # переведення скороченого формату логарифму на зручний програмі
            for m in re.findall(r'log\(.*?x(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):  # для обробки
                self.func = self.func.replace(m, f'{m[:-1]}, 2)', 1)
        if 'lg' in self.func:                           # аналогічно
            for m in re.findall(r'lg\(.*?x(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):
                self.func = self.func.replace(m, f'log{m[2:-1]}, 10)', 1)
        if 'ln' in self.func:                           # аналогічно
            for m in re.findall(r'ln\(.*?x(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):
                self.func = self.func.replace(m, f'log{m[2:-1]}, e)', 1)
        if 'sqrt' in self.func:                         # переведення формату в зручний для програми формі, щоб уникнути
            for m in re.findall(r'sqrt\(.*?x(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):     # зайвого повторення тих самих дій
                self.func = self.func.replace(m, f'{m[4:]}**0.5', 1)
        # end of initiate func
        self.y = []
        self.x = []
        self.graph_func = plt                       # ініціалізація об'єкта matplotlib
        self.error = 'Incorrect input function'    # 'Unknown error'
        self.graph_func.title(label="Graph")
        if '.' in str(self.step):                   # визначення точності обрахунків
            self.presicion = len(str(self.step)[str(self.step).find('.'):])+2
        else:
            self.presicion = 2
        # For analysis acceptable x (for log(ax**2+bx+c, e)
        sqrt_is, log_is = False, False              # визначення недопустимих для побудови проміжків функції
        if re.search(r'\(.*?\)+\*\*0\.\d+', self.func):
            self.root_points_sqrt, self.list_plus_minus_sqrt, self.dictionary_plus_minus_plots_sqrt = self.check_sqrt()
            sqrt_is = True
        if re.search(r'log', self.func):
            self.root_points_log, self.list_plus_minus_log, self.dictionary_plus_minus_plots_log = self.check_log()
            log_is = True
        if sqrt_is and not log_is:
            self.root_points = self.root_points_sqrt
            self.list_plus_minus = self.list_plus_minus_sqrt
            self.dictionary_plus_minus_plots = self.dictionary_plus_minus_plots_sqrt
        elif log_is and not sqrt_is:
            self.root_points = self.root_points_log
            self.list_plus_minus = self.list_plus_minus_log
            self.dictionary_plus_minus_plots = self.dictionary_plus_minus_plots_log
        if sqrt_is and log_is:
            # self.root_points = list(set(self.root_points_sqrt.extend(self.root_points_log)))
            # self.list_rise_fall = list(set(self.list_rise_fall_sqrt.extend(self.list_rise_fall_log)))
            self.dictionary_plus_minus_plots = \
                self.dictionary_plus_minus_plots_sqrt.update(self.dictionary_plus_minus_plots_log)
            self.root_points = list(self.dictionary_plus_minus_plots.keys())
            self.list_plus_minus = list(self.dictionary_plus_minus_plots.values())
        if sqrt_is or log_is:
            array_delta = [abs(self.root_points[i] - self.root_points[i + 1]) for i in
                           range(len(self.root_points) - 1)]
            if array_delta and all(list(filter(lambda x: self.step > x, array_delta))):
                self.error = "Big step. Try smaller"          # перевірка на крок для уникнення перескакування розривів

    def which_to_plot(self):
        if self.type_graph == 'scatter':        # побудова по точках
            self.scatter()
        elif self.type_graph == 'line':         # по лініях
            self.line()
        elif self.type_graph == "polar":        # в полярній системі по точках
            self.polar()

    def scatter(self):
        # побудова у(х)
        self.graph_func.scatter(x=self.x, y=self.y, c='blue')
        self.graph_func.xlabel("x")
        self.graph_func.ylabel("y(x)")

    def line(self):
        self.graph_func.plot(self.x, self.y, c='blue')
        self.graph_func.xlabel("x")
        self.graph_func.ylabel("y(x)")

    def polar(self):
        self.graph_func = self.graph_func.figure()
        self.ax = self.graph_func.add_subplot(projection='polar')
        for x, y in zip(self.x, self.y):
            self.ax.scatter(x, y, color='blue')

    def arcsin_arccos_points(self):
        allowed_points = []
        if 'asin' in self.func:
            for m in re.findall(r'asin\(.*?\(?x\)?(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):
                m = m[m.find('('):]
                local_allowed_points = []
                x0, xn, step = self.first_point, self.last_point, self.step
                while x0 <= xn:
                    solve = eval(m.replace('x', str(x0)))
                    if -1 < solve < 1:
                        local_allowed_points.append(x0)
                    x0 += step
                allowed_points.extend(local_allowed_points)
        if 'acos' in self.func:
            for m in re.findall(r'acos\(.*?\(?x\)?(?:\*\*\d+[+-]\d+\.?\d*\)|\*\*\d+\)|[-+]\d+\.?\d*\))', self.func):
                m = m[m.find('('):]
                local_allowed_points = []
                x0, xn, step = self.first_point, self.last_point, self.step
                while x0 <= xn:
                    solve = eval(m.replace('x', str(x0)))
                    if -1 < solve < 1:
                        local_allowed_points.append(x0)
                    x0 += step
                allowed_points.extend(local_allowed_points)
        allowed_points = [round(i, self.presicion) for i in allowed_points]
        first_x = allowed_points[0]
        i = 1
        next_x = allowed_points[i]
        allowed_points_intervals = []
        while next_x != allowed_points[-1]:
            if allowed_points[i+1] - allowed_points[i] > step*1.1:
                allowed_points_intervals.append([first_x, next_x])
                first_x = allowed_points[i+1]
            i += 1
            next_x = allowed_points[i]
        else:
            # if allowed_points[i-1] - allowed_points[i] < step*1.1:
            allowed_points_intervals.append([first_x, next_x])
        return allowed_points_intervals

    def check_x_by_arc(self, intervals, x):
        for interval in intervals:
            if interval[0] < x < interval[1]:
                pass
            else:
                return False
        return True

    def check_sqrt(self):
        for m in re.findall(r'\(.*?\)+\*\*0.\d+', self.func):  # перевірка на наявінсть х в степені менше 1
            # multipliers_x = []                                              # для відкидування проміжків невизначеності функції,
            #                                                               # при яких вираз під степенем менше 0
            root_x = find_roots(m[:m.rfind(')')])

            root_points = list(
                sorted([round(i, 2) for i in root_x]))   # відсіювання ірраціональних коренів і обрізання чисел після коми
            list_plus_minus = []
            if len(root_points) == 1:                                                       # якщо така точка одна, значить тільки в одному боці від точки функція на всьому проміжку не визначена
                list_plus_minus.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(root_points[0] - 1))) > 0, True])    # ключова різниця між цим методом check_sqrt і check_log
                list_plus_minus.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(root_points[0] + 1))) > 0, True])    # це те, що тут точки включно, в 0 функція все ще визначене
            elif len(root_points) == 0:                                                                                           # в логарифмах ні
                list_plus_minus.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', '0')) > 0, True])      # якщо нема коренів, а х є, то визначення, чи існує взагалі область значень
            else:
                for i in range(len(root_points)):
                    if i == 0:
                        calculate_point = root_points[i] - 1
                        list_plus_minus.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))) > 0, True])     # визначення на кожному проміжку знака функції
                        # print(eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))))                                 # +1 і -1 це для крайньої правої і крайньої лівого кореня
                    elif i == len(root_points) - 1:                                                                                 # де нема різниці на скільки більшу точку ставити для визначення знака
                        calculate_point = root_points[i] + 1
                        list_plus_minus.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))) > 0, True])
                        # print(eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))))
                        break
                    calculate_point = root_points[i] + (root_points[i + 1] - root_points[i]) / 2                            # визначення знака функції між коренями, обрахунок точки для підстановки х
                    list_plus_minus.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))) > 0, True])         # обраховується точно щоб опинився між коренями
        dictionary_plus_minus_plots = {k: v for k, v in zip(root_points, list_plus_minus[:-1])}
        return root_points, list_plus_minus, dictionary_plus_minus_plots

    def check_log(self):               # див попередній метод класу
        for m in re.findall(r'log\(.*?, ?[0-9e]+\)', self.func):
            roots_x = find_roots(m[m.find('('):m.rfind(',')])

            root_points = list(sorted([round(i, self.presicion) for i in roots_x]))
            list_rise_fall = []
            # if len(root_points) == 1:
            #     list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(root_points[0]-1))) > 0, False])
            #     list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(root_points[0]+1))) > 0, False])
            # elif len(root_points) == 0:
            #     list_rise_fall.append([eval(m[4:m.find(',')].replace('x', '0')) > 0, False])
            # else:
            #     for i in range(len(root_points)):
            #         if i == 0:
            #             calculate_point = root_points[i] - 1
            #             list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])
            #             # print(eval(m[4:m.find(',')].replace('x', str(calculate_point))))
            #         elif i == len(root_points)-1:
            #             calculate_point = root_points[i] + 1
            #             list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])
            #             # print(eval(m[4:m.find(',')].replace('x', str(calculate_point))))
            #             break
            #         calculate_point = root_points[i] + (root_points[i+1]-root_points[i]) / 2
            #         list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])
            if len(root_points) > 1:
                for i in range(len(root_points)):
                    if i == 0:
                        calculate_point = root_points[i] - 1
                        list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])
                        # print(eval(m[4:m.find(',')].replace('x', str(calculate_point))))
                    elif i == len(root_points)-1:
                        calculate_point = root_points[i] + 1
                        list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])
                        # print(eval(m[4:m.find(',')].replace('x', str(calculate_point))))
                        break
                    calculate_point = root_points[i] + (root_points[i+1]-root_points[i]) / 2
                    list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])
            elif len(root_points) == 1:
                list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(root_points[0] - 1))) > 0, False])
                list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(root_points[0] + 1))) > 0, False])
            else:
                list_rise_fall.append([eval(m[4:m.find(',')].replace('x', '0')) > 0, False])

            dictionary_rise_fall_plots = {k: v for k, v in zip(root_points, list_rise_fall[:-1])}
            return root_points, list_rise_fall, dictionary_rise_fall_plots

    def analysis_log_sqrt_x(self, x):                                # тут складно
        # if not self.root_points:                            # якщо нема коренів то далі умова не приходить і переходить
        #     return False                                    # до наступної
        if len(self.root_points) == 0:                      # якщо коренів нема
            if not self.list_plus_minus[0][0]:                  # і функція невизначена при будь якому х, то викликається виключення
                self.error = 'Unresolved expression under log'
                raise self.func_error()
            else:
                return x                                    # інакше будь який х підходить
        for i in range(len(self.root_points)):
            if x < self.root_points[i] and self.dictionary_plus_minus_plots[self.root_points[i]][0]:  # якщо х менший кореня і проміжок дійсний
                return x
            elif not self.dictionary_plus_minus_plots[self.root_points[i]][0] or x == self.root_points[i]:       # якщо х більший, і проміжок не дійсний
                if self.dictionary_plus_minus_plots[self.root_points[i]][1]:         # визначення чи точка включно, в цьому рядку включно
                    while x < self.root_points[i]:                                  # поки х менший за наступний корінь,
                        x += self.step                                              # додається крок поки не буде більшим чи рівним
                elif not self.dictionary_plus_minus_plots[self.root_points[i]][1]:   # в цьому рядку не включно(строго)
                    while x <= self.root_points[i]:
                        x += self.step
        if not self.list_plus_minus[-1][0]:                      # якщо справа від останнього кореня функція невизначена
            if x > self.root_points[-1][0]:                     # і х перетнув корінь, то побудова зупиняється
                return 'False'
        return x

    def analysis_data(self, func: str):                 # аналіз функції перед побудовою, перше це перевірка на наявність дробів з х
        gap_all = []
        for m in re.findall(r'/\(.*?x(?:\)\*\*\d+[+-]\d+\.?\d*\)|\)\*\*\d+\)|\)[-+]\d+\.?\d*\))', self.func):   # схоже на методи визначення коренів у check_sqrt i check_log
            # multipliers_x = []                                                          # тільки тут не проміжки а тільки точки
            m = m.replace('x', '(x)')
            root_x = find_roots(m)

            gap_all.extend(root_x)
        if '/sin' in self.func:                # в синусі і косинусі пошук коренів тільки в межах інтервалу, і тільки для виразів а*х+b
            gap_sin = []
            for m in re.findall(r'/sin\([+-]?\d*\.?\d*\*?\(x\)[+-]?\d*\.?\d*\)', self.func):
                if re.search(r'\([+-]?\d*\.?\d*\*?\(x', m):
                    a = float(re.search(r'\([+-]?\d+\.?\d*\*', m).group(0)[1:-1])       # при наявності а, визначає його
                else:
                    a = 1                                                                # допускається sin(x) sin(x+b)
                if re.search(r'x\)[+-]\d+\.?\d*\)', m):
                    b = float(re.search(r'x\)[+-]\d+\.?\d*\)', m).group(0)[2:-1])      # визначення b
                else:
                    b = 0
                x0 = self.first_point                   # щоб не впливати на х0, копіюємо
                gap_point = ceil((a * x0 + b) / pi)     # формула знаходження першого кореня округленого вверх,
                while x0 < self.last_point:             # це є наш n з формули ax+b = pi*n, при якому sin = 0
                    x0 = (pi * gap_point - b) / a       # і тут визначаємо значення х при наступних n, які натуральні,
                    gap_sin.append(x0)            # при яких сінус = 0
                    gap_point += 1
                gap_all.extend(gap_sin)

        if '/cos' in self.func:
            gap_cos = []
            for m in re.findall(r'/cos\([+-]?\d*\.?\d*\*?\(x\)[+-]?\d*\.?\d*\)', self.func):
                if re.search(r'\([+-]?\d*\.?\d*\*?\(x', m):
                    a = float(re.search(r'\([+-]?\d+\.?\d*\*', m).group(0)[1:-1])
                else:
                    a = 1
                if re.search(r'x\)[+-]?\d+\.?\d*\)', m):
                    b = float(re.search(r'x\)[+-]?\d+\.?\d*\)', m).group(0)[2:-1])
                else:
                    b = 0
                x0 = self.first_point
                gap_point = ceil((a * x0 + b - pi/2) / pi)  # x = pi/2 + pi*n
                while x0 < self.last_point:
                    x0 = (pi * gap_point - b + pi/2) / a
                    gap_cos.append(x0)
                    gap_point += 1
                gap_all.extend(gap_cos)

        gap_all = list(set([round(i, self.presicion) for i in gap_all if not isinstance(i, complex)]))
        return gap_all  # всі повторювані розриви знищуються, і масив впорядковується, комплексні відсіюються

    def calculate_func(self, func: str, x1: float, xn: float, step: float):    # внесення  точок в масиви x і у для побудови
        arc_flag = False
        if 'asin' in func or 'acos' in func:
            arc_flag = True
            allowed_points_intervals = self.arcsin_arccos_points()

        if re.findall(r'/\(.*?x(?:\)\*\*\d+[+-]\d+\.?\d*\)|\)\*\*\d+\)|\)[-+]\d+\.?\d*\))', func)\
                or '/sin' in func or '/cos' in func:
            root_point = sorted(self.analysis_data(func))       # при наявності виразів, що вносять розриви, створюється
            root_point = [i for i in root_point if i >= x1]     # масив цих точок, відсіюються ті, що менші першої точки інтервалу
            point = 0
            x = x1
            func = func.replace('x', '(x)')
            while x <= xn:
                if arc_flag and not self.check_x_by_arc(allowed_points_intervals, x):
                    self.which_to_plot()
                    self.x = []
                    self.y = []
                    x += step
                    continue
                if re.search(r'log', self.func) or re.search(r'\(.*?\)+\*\*0.\d+', self.func):
                    if self.analysis_log_sqrt_x(x) == 'False':  # якщо функція більше не визначеня, зупиняється побудова
                        self.which_to_plot()
                        break

                    else:
                        if x != self.analysis_log_sqrt_x(x):    # побудова тільки тоді, якщо х входить в область значень
                            self.which_to_plot()                # побудова графіка до цієї точки не включно
                            self.x = []                         # перевизначення масивів х і у
                            self.y = []

                        x = self.analysis_log_sqrt_x(x)         # перевизначення х

                if root_point and point < len(root_point) and x >= root_point[point]:   # якщо х перейшов точку розриву
                    point += 1
                    self.which_to_plot()
                    self.x = []
                    self.y = []
                    # x += step  # correct step after critical point because of value between left and right from point
                    x += 2 * (root_point[point-1] - (x - step)) - step    # х підбирається таким, щоб був симетричний графік до розриву
                    continue

                y = func.replace('x', str(x))       # підстановка х
                self.x.append(x)                    # додавання до масиву х
                self.y.append(eval(y))              # розрахунок функції і додавання до масиву у
                x += step

        else:       # якщо нема дробів, то визначення на логарифм і вирази з х степеня менше 1 залишається на перевірку
            x = x1
            func = func.replace('x', '(x)')
            while x <= xn:
                if arc_flag and not self.check_x_by_arc(allowed_points_intervals, x):
                    self.which_to_plot()
                    self.x = []
                    self.y = []
                    x += step
                    continue
                if re.search(r'log', self.func) or re.search(r'\(.*?\)+\*\*0.\d+', self.func):

                    if self.analysis_log_sqrt_x(x) == 'False':
                        self.which_to_plot()
                        break

                    else:
                        if x != self.analysis_log_sqrt_x(x):
                            self.which_to_plot()
                            self.x = []
                            self.y = []
                        x = self.analysis_log_sqrt_x(x)

                y = func.replace('x', str(x))
                self.x.append(x)
                self.y.append(eval(y))
                x += step

    def draw(self):
        # self.func = self.func.replace('(x)', 'x')       # усунення різниці де поставлені дужки навколо х, де ні
        # self.func = self.func.replace('x', '(x)')
        self.calculate_func(self.func, self.first_point, self.last_point, self.step)
        self.which_to_plot()
        if self.type_func != 'r_theta':
            self.graph_func.axhline(y=0, color='k')
            self.graph_func.axvline(x=0, color='k')
            self.graph_func.grid(axis='both')
        self.graph_func.show()

    def func_error(self):
        MessageBox.showinfo("Error", self.error)


