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

def check_x_with_brackets(string):
    for m in re.findall(r'\(?x\)?', string):
        if m != '(x)':
            return False
    return True


class Graph:
    def __init__(self, func, type_func, type_graph, first_point=0, last_point=10, step=1):
        self.type_func = type_func
        self.type_graph = type_graph
        if not is_digit(first_point, last_point, step):
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
        if not check_x_with_brackets(self.func):
            self.error = "Input error. Variable without brackets"
            raise self.func_error()
        if '^' in func:
            self.func = self.func.replace('^', '**')
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




        if re.search(r'log', self.func):
            for m in re.findall(r'log\(.*?\(x\)[+-]?\d*\.?\d*, ?[0-9e]+\)+', self.func):
                n = []
                print(m)
                for m2 in re.findall(r'[+-]?\d+\.?\d*\*\(x\)', m):
                    n.append(m2[:m2.find('*')])
                if re.search(r'\)[+-]?\d*\.?\d*,', m):
                    m2 = re.search(r'\)[+-]?\d*\.?\d*,', m)
                    if m2.group(0) != '),':
                        n.append(m2.group(0)[1:-1])
                    else:
                        n.append(0)
                n = [float(i) for i in n]
                # if len(n) == 1:
                #     n.append(0)
                n = np.roots(n)
                n = list(sorted([round(i, self.presicion) for i in n if not isinstance(i, complex)]))
                l_n = []
                if len(n) == 1:
                    l_n.append(eval(m[4:m.find(',')].replace('x', str(n[0]-1))) > 0)
                    l_n.append(eval(m[4:m.find(',')].replace('x', str(n[0]+1))) > 0)
                elif len(n) == 0:
                    l_n.append(eval(m[4:m.find(',')].replace('x', '0')) > 0)
                else:
                    for i in range(len(n)):
                        if i == 0:
                            m_i = n[i] - 1
                            l_n.append(eval(m[4:m.find(',')].replace('x', str(m_i))) > 0)
                            print(eval(m[4:m.find(',')].replace('x', str(m_i))))
                        elif i == len(n)-1:
                            m_i = n[i] + 1
                            l_n.append(eval(m[4:m.find(',')].replace('x', str(m_i))) > 0)
                            print(eval(m[4:m.find(',')].replace('x', str(m_i))))
                            break
                        m_i = n[i] + (n[i+1]-n[i]) / 2
                        l_n.append(eval(m[4:m.find(',')].replace('x', str(m_i))) > 0)
                d_l_n = {k: v for k, v in zip(n, l_n[:-1])}
                self.n, self.l_n, self.d_l_n = n, l_n, d_l_n




            array_delta = [abs(n[i]-n[i+1]) for i in range(len(n)-1)]
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

    # def analysis_tan_x(self, x):
    #     l_m = []
    #     for m in re.findall(r'tan\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+', self.func):
    #
    #         n = eval(m[3:].replace('x', str(x)))
    #         print(n)
    #         l_m.append(abs(n / pi - n // pi) < (self.step / 10))
    #         print(abs(n / pi - n // pi))
    #     return all(l_m)




    def analysis_log_x(self, x):
        if len(self.n) == 0:
            if not self.l_n[0]:
                self.error = 'Unresolved expression under log'
            else:
                return x
        for i in range(len(self.n)):
            if x < self.n[i] and self.d_l_n[self.n[i]]:
                return x
            elif not self.d_l_n[self.n[i]]:
                while x <= self.n[i]:
                    x += self.step
        if not self.l_n[-1]:
            if x > self.n[-1]:
                return 'False'
        return x




    def analysis_data(self, func: str):
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
        n_all = [round(i, self.presicion) for i in n_all if not isinstance(i, complex)]
        return n_all




    def calculate_func(self, func: str, x1: float, xn: float, step: float):
        if re.findall(r'/ ?\(.*?\(x\)[+-]?\d*\.?\d*\)+', func) or \
                re.findall(r'tan\([+-]?.*?\(x\)[+-]?\d*\.?\d*\)+', self.func):
            critical_point = sorted(self.analysis_data(func))
            critical_point = [i for i in critical_point if i > x1]
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
                        x = self.analysis_log_x(x)  ##

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


