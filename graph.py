from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from math import *
import re
import tkinter.messagebox as MessageBox


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
    x0, xn, step = float(x0), float(xn), float(step)
    if x0 > xn and step >= 0 or xn > x0 and step <= 0:
        return True


class Graph:
    def __init__(self, func, type_func, type_graph, first_point=0, last_point=10, step=1):
        self.type_func = type_func
        self.type_graph = type_graph
        if check_interval(first_point, last_point, step):
            self.error = 'Incorrect input interval'
            raise self.func_error()
        self.first_point = float(first_point)
        self.last_point = float(last_point)
        self.step = float(step)
        # before initiate func
        if type_func == 'x_y':                # перевірка на введення, залежно від типу функції, змінної
            if 'y' not in func:
                self.error = "Input function error. Function without 'y'"
                raise self.func_error()
            self.func = str(func).replace('y', 'x')

        elif type_func == 'y_x':
            if 'x' not in func:
                self.error = "Input function error. Function without 'x'"
                raise self.func_error()
            self.func = str(func)

        # else:
        #     if 'theta' not in func:
        #         self.error = "Input function error. Function without 'x'"
        #         raise self.func_error()
        #     self.func = str(func).replace('theta', 'x')

        if '^' in func:
            self.func = self.func.replace('^', '**')
        self.func = self.func.replace('(x)', 'x')       # усунення різниці де поставлені дужки навколо х, де ні
        self.func = self.func.replace('x', '(x)')
        if 'tan' in self.func:                          # розкладання тангенса на синус/косинус
            for m in re.findall(r'tan\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
                self.func = self.func.replace(m, f'(sin{m[3:]})/cos{m[3:]}')
        if 'ctg' in self.func:                          # розкладання тангенса на косинус/синус
            for m in re.findall(r'ctg\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
                self.func = self.func.replace(m, f'(cos{m[3:]})/sin{m[3:]}')
        if 'log' in self.func:                          # переведення скороченого формату логарифму на зручний програмі
            for m in re.findall(r'log\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):  # для обробки
                self.func = self.func.replace(m, f'{m[:-1]}, 2)')
        if 'lg' in self.func:                           # аналогічно
            for m in re.findall(r'lg\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
                self.func = self.func.replace(m, f'log{m[2:-1]}, 10)')
        if 'ln' in self.func:                           # аналогічно
            for m in re.findall(r'ln\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
                self.func = self.func.replace(m, f'log{m[2:-1]}, e)')
        if 'sqrt' in self.func:                         # переведення формату в зручний для програми формі, щоб уникнути
            for m in re.findall(r'sqrt\(.*?\(x\)[+-]?\d*\.?\d*\)+', self.func):     # зайвого повторення тих самих дій
                self.func = self.func.replace(m, f'{m[4:]}**0.5', 1)
        # end of initiate func
        if (self.last_point < self.first_point and step > 0) or self.step == 0:     # перевірка правильного введення
            self.error = 'Step error. Impossible to build graph '                   # інтервалу і кроку на безкінечність
            raise self.func_error()
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
        if re.search(r'\(.*?\(?x\)?[+-]?\d*\.?\d*\)+\*\*0.\d+', self.func):
            self.root_points_sqrt, self.list_rise_fall_sqrt, self.dictionary_rise_fall_plots_sqrt = self.check_sqrt()
            sqrt_is = True
        if re.search(r'log', self.func):
            self.root_points_log, self.list_rise_fall_log, self.dictionary_rise_fall_plots_log = self.check_log()
            log_is = True
        if sqrt_is and not log_is:
            self.root_points = self.root_points_sqrt
            self.list_rise_fall = self.list_rise_fall_sqrt
            self.dictionary_rise_fall_plots = self.dictionary_rise_fall_plots_sqrt
        elif log_is and not sqrt_is:
            self.root_points = self.root_points_log
            self.list_rise_fall = self.list_rise_fall_log
            self.dictionary_rise_fall_plots = self.dictionary_rise_fall_plots_log
        if sqrt_is and log_is:
            self.root_points = list(set(self.root_points_sqrt.extend(self.root_points_log)))
            self.list_rise_fall = list(set(self.list_rise_fall_sqrt.extend(self.list_rise_fall_log)))
            self.dictionary_rise_fall_plots = \
                self.dictionary_rise_fall_plots_sqrt.update(self.dictionary_rise_fall_plots_log)
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
        # elif self.type_graph == "polar":
        #     self.polar()


    def scatter(self):
        if self.type_func == 'y_x':             # побудова у(х)
            self.graph_func.scatter(x=self.x, y=self.y, c='blue')
            self.graph_func.xlabel("x")
            self.graph_func.ylabel("y(x)")
        if self.type_func == 'x_y':            # побудова х(у)
            self.graph_func.scatter(x=self.y, y=self.x, c='blue')
            self.graph_func.xlabel("y")
            self.graph_func.ylabel("x")

        # self.graph_func.grid(axis='both')

    def line(self):
        if self.type_func == 'y_x':
            self.graph_func.plot(self.x, self.y, c='blue')
            self.graph_func.xlabel("x")
            self.graph_func.ylabel("y(x)")
        if self.type_func == 'x_y':
            self.graph_func.plot(self.y, self.x, c='blue')
            self.graph_func.xlabel("y")
            self.graph_func.ylabel("x")
        # self.graph_func.grid(axis='both')

    # def polar(self):
    #     self.graph_func.polar(theta=self.x, r=self.y, c='blue')

    def check_sqrt(self):
        for m in re.findall(r'\(.*?\(?x\)?[+-]?\d*\.?\d*\)+\*\*0.\d+', self.func):  # перевірка на наявінсть х в степені менше 1
            multipliers_x = []                                              # для відкидування проміжків невизначеності функції,
            #                                                               # при яких вираз під степенем менше 0
            if re.search(r'\*\*\d+', m[:m.rfind(')')]):                                    # перевірка на наявінсть х в степені
                x_power_max = int(re.search(r'\*\*\d+', m).group(0)[2:])    # визначення максимального степеня
                flag = x_power_max                                          # передача максимального степені новій змінній
                for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)\*\*\d+', m):   # якщо є пропущенні степені, вони добавляються
                    flag_new = int(re.search(r'\*\*\d+', m2).group(0)[2:])  # у масив як нулі, щоб через numpy розрахувати
                    while flag != flag_new:                                 # корені рівняння x^n степенях
                        multipliers_x.append(0)                             #
                        flag -= 1                                           # в рядку 153 визначається степінь наступного х
                    multipliers_x.append(m2[:m2.find('*')])                 # якщо він не дорівнює максимальному, то додається
                    flag -= 1                                               # до масиву 0, і віднімається від прапорця 1, поки не досягне значення степеня х
                while len(multipliers_x) != x_power_max - 1:                # якщо розмір масиву менщий за максимальний степінь - 1,
                    multipliers_x.append(0)                                 # то масив заповнюється 0-ами поки не буде рівний
                if re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m):       # визначення останнього х в степені 1
                    num_x = re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m).group(0)
                    multipliers_x.append(num_x[1:num_x.find('*')])          # додавання множника х до масиву, якщо є
                else:
                    multipliers_x.append(0)                                 # інакше додавання 0-ля
            else:
                num_x = re.search(r'[+-]?\d+\.?\d*\*\(x\)', m).group(0)     # якщо вираз типу а*х+b
                multipliers_x.append(num_x[:num_x.find('*')])               # знаходження множника х і додавання в масив
            if re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m):                     # знаходження b для обох випадків однаково
                m2 = re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m)
                multipliers_x.append(m2.group(0)[1:-1])
            else:
                multipliers_x.append(0)

            multipliers_x = [float(i) for i in multipliers_x]
            print(multipliers_x)
            root_points = np.roots(multipliers_x)                       # знаходження коренів
            root_points = list(
                sorted([round(i, 2) for i in root_points if not isinstance(i, complex)]))   # відсіювання ірраціональних коренів і обрізання чисел після коми
            list_rise_fall = []
            if len(root_points) == 1:                                                       # якщо така точка одна, значить тільки в одному боці від точки функція на всьому проміжку не визначена
                list_rise_fall.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(root_points[0] - 1))) > 0, True])    # ключова різниця між цим методом check_sqrt і check_log
                list_rise_fall.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(root_points[0] + 1))) > 0, True])    # це те, що тут точки включно, в 0 функція все ще визначене
            elif len(root_points) == 0:                                                                                           # в логарифмах ні
                list_rise_fall.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', '0')) > 0, True])      # якщо нема коренів, а х є, то визначення, чи існує взагалі область значень
            else:
                for i in range(len(root_points)):
                    if i == 0:
                        calculate_point = root_points[i] - 1
                        list_rise_fall.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))) > 0, True])     # визначення на кожному проміжку знака функції
                        # print(eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))))                                 # +1 і -1 це для крайньої правої і крайньої лівого кореня
                    elif i == len(root_points) - 1:                                                                                 # де нема різниці на скільки більшу точку ставити для визначення знака
                        calculate_point = root_points[i] + 1
                        list_rise_fall.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))) > 0, True])
                        # print(eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))))
                        break
                    calculate_point = root_points[i] + (root_points[i + 1] - root_points[i]) / 2                            # визначення знака функції між коренями, обрахунок точки для підстановки х
                    list_rise_fall.append([eval(m[m.find('('):m.rfind(')') + 1].replace('x', str(calculate_point))) > 0, True])         # обраховується точно щоб опинився між коренями
        dictionary_rise_fall_plots = {k: v for k, v in zip(root_points, list_rise_fall[:-1])}
        return root_points, list_rise_fall, dictionary_rise_fall_plots

    def check_log(self):               # див попередній метод класу
        for m in re.findall(r'log\(.*?\(x\)[+-]?\d*\.?\d*, ?[0-9e]+\)+', self.func):
            multipliers_x = []
            if re.search(r'\*\*\d+', m):
                x_power_max = int(re.search(r'\*\*\d+', m).group(0)[2:])
                flag = x_power_max
                for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)\*\*\d+', m):
                    flag_new = int(re.search(r'\*\*\d+', m2).group(0)[2:])
                    while flag != flag_new:
                        multipliers_x.append(0)
                        flag -= 1
                    multipliers_x.append(m2[:m2.find('*')])
                    flag -= 1
                while len(multipliers_x) != x_power_max - 1:
                    multipliers_x.append(0)
                if re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m):
                    num_x = re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m).group(0)
                    multipliers_x.append(num_x[1:num_x.find('*')])
                else:
                    multipliers_x.append(0)
            else:
                num_x = re.search(r'[+-]?\d+\.?\d*\*\(x\)', m).group(0)
                multipliers_x.append(num_x[:num_x.find('*')])
            if re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m):
                m2 = re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m)
                multipliers_x.append(m2.group(0)[1:-1])
            else:
                multipliers_x.append(0)

            multipliers_x = [float(i) for i in multipliers_x]
            root_points = np.roots(multipliers_x)
            root_points = list(sorted([round(i, self.presicion) for i in root_points if not isinstance(i, complex)]))
            list_rise_fall = []
            if len(root_points) == 1:
                list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(root_points[0]-1))) > 0, False])
                list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(root_points[0]+1))) > 0, False])
            elif len(root_points) == 0:
                list_rise_fall.append([eval(m[4:m.find(',')].replace('x', '0')) > 0, False])
            else:
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
                    # list_rise_fall.append(eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0)
                    list_rise_fall.append([eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0, False])

            dictionary_rise_fall_plots = {k: v for k, v in zip(root_points, list_rise_fall[:-1])}
            return root_points, list_rise_fall, dictionary_rise_fall_plots

    def analysis_log_sqrt_x(self, x):                                # тут складно
        if not self.root_points:                            # якщо нема коренів то далі умова не приходить і переходить
            return False                                    # до наступної
        if len(self.root_points) == 0:                      # якщо коренів нема
            if not self.list_rise_fall[0][0]:                  # і функція невизначена при будь якому х, то викликається виключення
                self.error = 'Unresolved expression under log'
            else:
                return x                                    # інакше будь який х підходить
        for i in range(len(self.root_points)):
            if x < self.root_points[i] and self.dictionary_rise_fall_plots[self.root_points[i]][0]:  # якщо х менший кореня і проміжок дійсний
                return x
            elif not self.dictionary_rise_fall_plots[self.root_points[i]][0]:       # якщо х більший, і проміжок не дійсний
                if self.dictionary_rise_fall_plots[self.root_points[i]][1]:         # визначення чи точка включно, в цьому рядку включно
                    while x < self.root_points[i]:                                  # поки х менший за наступний корінь,
                        x += self.step                                              # додається крок поки не буде більшим чи рівним
                elif not self.dictionary_rise_fall_plots[self.root_points[i]][1]:   # в цьому рядку не включно(строго)
                    while x <= self.root_points[i]:
                        x += self.step
        if not self.list_rise_fall[-1][0]:                      # якщо справа від останнього кореня функція невизначена
            if x > self.root_points[-1][0]:                     # і х перетнув корінь, то побудова зупиняється
                return 'False'
        return x

    def analysis_data(self, func: str):                 # аналіз функції перед побудовою, перше це перевірка на наявність дробів з х
        gap_all = []
        for m in re.findall(r'/ ?\([+-]?.*?\(x\).*?[+-]?\d*\.?\d*\)+\)?', self.func):   # схоже на методи визначення коренів у check_sqrt i check_log
            multipliers_x = []                                                          # тільки тут не проміжки а тільки точки
            if re.search(r'\*\*\d', m):
                x_power_max = int(re.search(r'\*\*\d+', m).group(0)[2:])
                flag = x_power_max
                for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)\*\*\d+', m):
                    flag_new = int(re.search(r'\*\*\d+', m2).group(0)[2:])
                    while flag != flag_new:
                        multipliers_x.append(0)
                        flag -= 1
                    multipliers_x.append(m2[:m2.find('*')])
                    flag -= 1
                while len(multipliers_x) != x_power_max - 1:
                    multipliers_x.append(0)
                if re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m):
                    num_x = re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m).group(0)
                    multipliers_x.append(num_x[1:num_x.find('*')])
                else:
                    multipliers_x.append(0)
            else:
                num_x = re.search(r'[+-]?\d+\.?\d*\*\(x\)', m).group(0)
                multipliers_x.append(num_x[:num_x.find('*')])
            if re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m):
                m2 = re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m)
                multipliers_x.append(m2.group(0)[1:-1])
            else:
                multipliers_x.append(0)
            multipliers_x = [float(i) for i in multipliers_x]
            gap_points = np.roots(multipliers_x)
            gap_all.extend(gap_points)
        if '/sin' in self.func:                # в синусі і косинусі пошук коренів тільки в межах інтервалу, і тільки для виразів а*х+b
            multipliers_x = []
            for m in re.findall(r'/sin\([+-]?\d*\.?\d*\*?\(x\)[+-]?\d*\.?\d*\)', self.func):
                if re.search(r'\([+-]?\d*\.?\d*\*?\(x', m):
                    a = float(re.search(r'\([+-]?\d+\.?\d*\*', m).group(0)[1:-1])       # при наявності а, визначає його
                else:
                    a = 1                                                                # допускається sin(x) sin(x+b)
                if re.search(r'x\)[+-]?\d+\.?\d*\)', m):
                    b = float(re.search(r'x\)[+-]?\d+\.?\d*\)', m).group(0)[2:-1])      # визначення b
                else:
                    b = 0
                x0 = self.first_point                   # щоб не впливати на х0, копіюємо
                gap_point = ceil((a * x0 + b) / pi)     # формула знаходження першого кореня округленого вверх,
                while x0 < self.last_point:             # це є наш n з формули x = pi*n, при якому sin = 0
                    x0 = (pi * gap_point - b) / a       # і тут визначаємо значення х при наступних n, які натуральні,
                    multipliers_x.append(x0)            # при яких сінус = 0
                    gap_point += 1
                gap_all.extend(multipliers_x)

        if '/cos' in self.func:
            multipliers_x = []
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
                    multipliers_x.append(x0)
                    gap_point += 1
                gap_all.extend(multipliers_x)

        gap_all = list(set([round(i, self.presicion) for i in gap_all if not isinstance(i, complex)]))
        return gap_all  # всі повторювані розриви знищуються, і масив впорядковується, комплексні відсіюються

    def calculate_func(self, func: str, x1: float, xn: float, step: float):    # внесення  точок в масиви x і у для побудови

        if re.findall(r'/ ?\(.*?\(x\)[+-]?\d*\.?\d*\)+', func)\
                or '/sin' in func or '/cos' in func:
            root_point = sorted(self.analysis_data(func))       # при наявності виразів, що вносять розриви, створюється
            root_point = [i for i in root_point if i >= x1]     # масив цих точок, відсіюються ті, що менші першої точки інтервалу
            point = 0
            x = x1

            while x <= xn:
                if re.search(r'log', self.func):
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
            while x <= xn:
                if re.search(r'log', self.func):
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
        self.calculate_func(self.func, self.first_point, self.last_point, self.step)
        self.which_to_plot()
        self.graph_func.axhline(y=0, color='k')
        self.graph_func.axvline(x=0, color='k')
        self.graph_func.grid(axis='both')
        self.graph_func.show()

    def func_error(self):
        MessageBox.showinfo("Error", self.error)


