from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from math import *
import re
import tkinter.messagebox as MessageBox


def is_digit(*args):
    for i in args:
        try:
            x = float(i)
        except ValueError:
            return False
    return True


def check_zero_division(string):
    if re.findall(r'/\([^x]*?\)', string):
        for i in re.findall(r'/\([^x]*?\)', string):
            if eval(i[1:]) == 0:
                return False
    return True


def check_interval(x0, xn, step):
    if not is_digit(x0, xn, step):
        return True
    x0, xn, step = float(x0), float(xn), float(step)
    if x0 > xn and step >= 0 or xn > x0 and step <= 0:
        return True
# def check_input_func(string):
#     if re.search(r'[sincolgh]', string):
#         for i in re.findall(r's|c|l', string):
#             if not re.search(r'sin|cos|log|sinh|cosh', string):
#                 print('inrocerct inut')
#         print('norm')
#     if re.search(r'\s|[^-+*/.,()sincolghxe0-9]', string) or re.search(r'[-+/.,]{2,}|\*{3,}', string) \
#             or string.count('(') != string.count(')'):
#         print('hui')
#     print('norm')


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
        if type_func == 'y(x)=':
            if 'y' not in func:
                self.error = "Input function error. Function without 'y'"
                raise self.func_error()
            self.func = str(func).replace('y', 'x')
        else:
            if 'x' not in func:
                self.error = "Input function error. Function without 'x'"
                raise self.func_error()
            self.func = str(func)
        if '^' in func:
            self.func = self.func.replace('^', '**')
        self.func = self.func.replace('(x)', 'x')
        self.func = self.func.replace('x', '(x)')
        if (self.last_point < self.first_point and step > 0) or self.step == 0:
            self.error = 'Step error. Impossible to build graph '
            raise self.func_error()
        self.y = []
        self.x = []
        self.graph_func = plt
        self.error = 'Incorrect input function'    # 'Unknown error'
        self.graph_func.title(label="Graph")
        if '.' in str(self.step):
            self.presicion = len(str(self.step)[str(self.step).find('.'):])+2
        else:
            self.presicion = 2
        # For analysis acceptable x (for log(ax**2+bx+c, e)
        if 'tan' in self.func:
            for m in re.findall(r'tan\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
                self.func = self.func.replace(m, f'(sin{m[3:]})/cos{m[3:]}')
        if 'ctg' in self.func:
            for m in re.findall(r'ctg\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
                self.func = self.func.replace(m, f'(cos{m[3:]})/sin{m[3:]}')
        if re.search(r'log', self.func):
            for m in re.findall(r'log\(.*?\(x\)[+-]?\d*\.?\d*, ?[0-9e]+\)+', self.func):
                critical_points = []
                for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)', m):
                    critical_points.append(m2[:m2.find('*')])
                if re.search(r'\)[+-]?\d*\.?\d*,', m):
                    m2 = re.search(r'\)[+-]?\d*\.?\d*,', m)
                    if m2.group(0) != '),':
                        critical_points.append(m2.group(0)[1:-1])
                    else:
                        critical_points.append(0)
                critical_points = [float(i) for i in critical_points]
                # if len(n) == 1:
                #     n.append(0)
                critical_points = np.roots(critical_points)
                critical_points = list(sorted([round(i, self.presicion) for i in critical_points if not isinstance(i, complex)]))
                list_rise_fall = []
                if len(critical_points) == 1:
                    list_rise_fall.append(eval(m[4:m.find(',')].replace('x', str(critical_points[0]-1))) > 0)
                    list_rise_fall.append(eval(m[4:m.find(',')].replace('x', str(critical_points[0]+1))) > 0)
                elif len(critical_points) == 0:
                    list_rise_fall.append(eval(m[4:m.find(',')].replace('x', '0')) > 0)
                else:
                    for i in range(len(critical_points)):
                        if i == 0:
                            calculate_point = critical_points[i] - 1
                            list_rise_fall.append(eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0)
                            print(eval(m[4:m.find(',')].replace('x', str(calculate_point))))
                        elif i == len(critical_points)-1:
                            calculate_point = critical_points[i] + 1
                            list_rise_fall.append(eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0)
                            print(eval(m[4:m.find(',')].replace('x', str(calculate_point))))
                            break
                        calculate_point = critical_points[i] + (critical_points[i+1]-critical_points[i]) / 2
                        list_rise_fall.append(eval(m[4:m.find(',')].replace('x', str(calculate_point))) > 0)
                dictionary_rise_fall_plots = {k: v for k, v in zip(critical_points, list_rise_fall[:-1])}
                self.critical_points, self.list_rise_fall, self.dictionary_rise_fall_plots = critical_points, list_rise_fall, dictionary_rise_fall_plots
            array_delta = [abs(critical_points[i]-critical_points[i+1]) for i in range(len(critical_points)-1)]
            if all(list(filter(lambda x: self.step > x, array_delta))):
                self.error = "Big step. Try smaller"

    def scatter(self):
        if self.type_func == 'y_x':
            self.graph_func.scatter(x=self.x, y=self.y, c='blue')
            self.graph_func.xlabel("x")
            self.graph_func.ylabel("y(x)")
        if self.type_func == 'x_y':
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

    # def analysis_tan_x(self):
    #     range_x = []
    #     x = self.first_point
    #     while x < self.last_point:
    #         range_x.append(x)
    #         x += self.step / 10
    #     calculate_tan = []
    #     for m in re.findall(r'tan\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
    #         for i in range_x:
    #             tan_value = eval(m.replace('x', str(i)))
    #             calculate_tan.append((tan_value, i))
    #     gap_point = []
    #     for i in range(len(calculate_tan) - 1):
    #         if calculate_tan[i][0] > 0 and calculate_tan[i + 1][0] < 0:
    #             gap_point.append((round(calculate_tan[i+1][1], self.presicion), round(calculate_tan[i][1], self.presicion)))
    #     return gap_point

    # def analysis_ctg_x(self):
    #     range_x = []
    #     x = self.first_point
    #     while x < self.last_point:
    #         range_x.append(x)
    #         x += self.step / 10
    #     calculate_tan = []
    #     for m in re.findall(r'ctg\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+\)?', self.func):
    #         for i in range_x:
    #             ctg_value = eval(m.replace('x', str(i)))
    #             calculate_tan.append((ctg_value, i))
    #     gap_point = []
    #     for i in range(len(calculate_tan) - 1):
    #         if calculate_tan[i][0] < 0 and calculate_tan[i + 1][0] > 0:
    #             gap_point.append((round(calculate_tan[i+1][1], self.presicion), round(calculate_tan[i][1], self.presicion)))
    #     return gap_point

    def analysis_log_x(self, x):
        if not self.critical_points:
            return False
        if len(self.critical_points) == 0:
            if not self.list_rise_fall[0]:
                self.error = 'Unresolved expression under log'
            else:
                return x
        for i in range(len(self.critical_points)):
            if x < self.critical_points[i] and self.dictionary_rise_fall_plots[self.critical_points[i]]:
                return x
            elif not self.dictionary_rise_fall_plots[self.critical_points[i]]:
                while x <= self.critical_points[i]:
                    x += self.step
        if not self.list_rise_fall[-1]:
            if x > self.critical_points[-1]:
                return 'False'
        return x

    def analysis_data(self, func: str):
        gap_all = []
        for m in re.findall(r'/ ?\([+-]?.*?\(x\).*?[+-]?\d*\.?\d*\)+\)?', self.func):
            gap_points = []
            if re.search(r'\*\*\d', m):
                x_power_max = int(re.search(r'\*\*\d', m).group(0)[2:])
                flag = x_power_max
                for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)\*\*\d', m):
                    flag_new = int(re.search(r'\*\*\d', m2).group(0)[2:])
                    while flag != flag_new:
                        gap_points.append(0)
                        flag -= 1
                    gap_points.append(m2[:m2.find('*')])
                    flag -= 1
                while len(gap_points) != x_power_max - 1:
                    gap_points.append(0)
                if re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m):
                    # num_x = re.search(r'[+-]?\d+\.?\d*\*\(x\)[^*]', m).group(0)
                    num_x = re.search(r'\d[+-]\d+\.?\d*\*\(x\)[^*]?.*?\)', m).group(0)
                    gap_points.append(num_x[1:num_x.find('*')])
                else:
                    gap_points.append(0)
            else:
                num_x = re.search(r'[+-]?\d+\.?\d*\*\(x\)', m).group(0)
                gap_points.append(num_x[:num_x.find('*')])
            if re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m):
                m2 = re.search(r'\)?\d?[+-]?\d+\.?\d*\)', m)
                gap_points.append(m2.group(0)[1:-1])
            else:
                gap_points.append(0)
            gap_points = [float(i) for i in gap_points]
            gap_points = np.roots(gap_points)
            gap_all.extend(gap_points)
        if '/sin' in self.func:
            gap_points = []
            for m in re.findall(r'/sin\([+-]?\d*\.?\d*\*?\(x\)[+-]?\d*\.?\d*\)', self.func):
                if re.search(r'\([+-]?\d*\.?\d*\*?\(x', m):
                    a = float(re.search(r'\([+-]?\d+\.?\d*\*', m).group(0)[1:-1])
                else:
                    a = 1
                if re.search(r'x\)[+-]?\d+\.?\d*\)', m):
                    b = float(re.search(r'x\)[+-]?\d+\.?\d*\)', m).group(0)[2:-1])
                else:
                    b = 0
                x0 = self.first_point
                gap_point = ceil((a * x0 + b) / pi)
                while x0 < self.last_point:
                    x0 = (pi * gap_point - b) / a
                    gap_points.append(x0)
                    gap_point += 1
                gap_all.extend(gap_points)

        if '/cos' in self.func:
            gap_points = []
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
                gap_point = ceil((a * x0 + b - pi/2) / pi)
                while x0 < self.last_point:
                    x0 = (pi * gap_point - b + pi/2) / a
                    gap_points.append(x0)
                    gap_point += 1
                gap_all.extend(gap_points)

        gap_all = list(set(gap_all))
        gap_all = [round(i, self.presicion) for i in gap_all if not isinstance(i, complex)]
        return gap_all

    def calculate_func(self, func: str, x1: float, xn: float, step: float):
        # if 'tan' in self.func:
        #     period_point_tan = 0
        #     gap_point_tan = self.analysis_tan_x()
        # else:
        #     period_point_tan = 0
        #     gap_point_tan = [(xn, xn)]
        # if 'ctg' in self.func:
        #     period_point_ctg = 0
        #     gap_point_ctg = self.analysis_ctg_x()
        # else:
        #     period_point_ctg = 0
        #     gap_point_ctg = [(xn, xn)]

        if re.findall(r'/ ?\(.*?\(x\)[+-]?\d*\.?\d*\)+', func)\
                or '/sin' in func or '/cos' in func:
            critical_point = sorted(self.analysis_data(func))
            critical_point = [i for i in critical_point if i >= x1]
            point = 0
            x = x1

            while x <= xn:
                if re.search(r'log', self.func):
                    if self.analysis_log_x(x) == 'False':
                        if self.type_graph == 'scatter':
                            self.scatter()
                        elif self.type_graph == 'line':
                            self.line()
                        break

                    else:
                        if x != self.analysis_log_x(x):
                            if self.type_graph == 'scatter':
                                self.scatter()
                            elif self.type_graph == 'line':
                                self.line()
                            self.x = []
                            self.y = []

                        x = self.analysis_log_x(x)

                # if period_point_tan != len(gap_point_tan) and x >= gap_point_tan[period_point_tan][0]:
                #     x = gap_point_tan[period_point_tan][1]
                #     y = func.replace('x', str(x))
                #     self.x.append(x)
                #     self.y.append(eval(y))
                #     if self.type_graph == 'scatter':
                #         self.scatter()
                #     elif self.type_graph == 'line':
                #         self.line()
                #     x = gap_point_tan[period_point_tan][0]
                #     period_point_tan += 1
                #     self.x = []
                #     self.y = []
                #     continue
                #
                # if period_point_ctg != len(gap_point_ctg) and x >= gap_point_ctg[period_point_ctg][0]:
                #     x = gap_point_ctg[period_point_ctg][1]
                #     y = func.replace('x', str(x))
                #     self.x.append(x)
                #     self.y.append(eval(y))
                #     if self.type_graph == 'scatter':
                #         self.scatter()
                #     elif self.type_graph == 'line':
                #         self.line()
                #     x = gap_point_ctg[period_point_ctg][0]
                #     period_point_ctg += 1
                #     self.x = []
                #     self.y = []
                #     continue

                if critical_point and point < len(critical_point) and x >= critical_point[point]:
                    point += 1
                    if self.type_graph == 'scatter':
                        self.scatter()
                    elif self.type_graph == 'line':
                        self.line()
                    self.x = []
                    self.y = []
                    # x += step  # correct step after critical point because of value between left and right from point
                    x += 2 * (critical_point[point-1] - (x - step)) - step
                    continue

                y = func.replace('x', str(x))
                self.x.append(x)
                self.y.append(eval(y))
                x += step

        else:
            x = x1
            while x <= xn:
                if re.search(r'log', self.func):
                    if self.analysis_log_x(x) == 'False':
                        if self.type_graph == 'scatter':
                            self.scatter()
                        elif self.type_graph == 'line':
                            self.line()
                        break

                    else:
                        if x != self.analysis_log_x(x):
                            if self.type_graph == 'scatter':
                                self.scatter()
                            elif self.type_graph == 'line':
                                self.line()
                            self.x = []
                            self.y = []
                        x = self.analysis_log_x(x)

                # if period_point_tan != len(gap_point_tan) and x >= gap_point_tan[period_point_tan][0]:
                #     x = gap_point_tan[period_point_tan][1]
                #     y = func.replace('x', str(x))
                #     self.x.append(x)
                #     self.y.append(eval(y))
                #     if self.type_graph == 'scatter':
                #         self.scatter()
                #     elif self.type_graph == 'line':
                #         self.line()
                #     x = gap_point_tan[period_point_tan][0]
                #     period_point_tan += 1
                #     self.x = []
                #     self.y = []
                #     continue
                #
                # if period_point_ctg != len(gap_point_ctg) and x >= gap_point_ctg[period_point_ctg][0]:
                #     x = gap_point_ctg[period_point_ctg][1]
                #     y = func.replace('x', str(x))
                #     self.x.append(x)
                #     self.y.append(eval(y))
                #     if self.type_graph == 'scatter':
                #         self.scatter()
                #     elif self.type_graph == 'line':
                #         self.line()
                #     x = gap_point_ctg[period_point_ctg][0]
                #     period_point_tan += 1
                #     self.x = []
                #     self.y = []
                #     continue

                y = func.replace('x', str(x))
                self.x.append(x)
                self.y.append(eval(y))
                x += step

    def draw(self):
        self.calculate_func(self.func, self.first_point, self.last_point, self.step)
        if self.type_graph == 'scatter':
            self.scatter()
        elif self.type_graph == 'line':
            self.line()
        self.graph_func.axhline(y=0, color='k')
        self.graph_func.axvline(x=0, color='k')
        # Graph.type_build_fun(self.type_graph)
        self.graph_func.grid(axis='both')
        self.graph_func.show()

    def func_error(self):
        MessageBox.showinfo("Error", self.error)


