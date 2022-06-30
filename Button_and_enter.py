import tkinter as tk
import graph
import tkinter.messagebox as MessageBox
from analysis import analysis
from PIL import ImageTk, Image


def call_analysis():
    analysis(func_entry, window, group_type_func, group_type_graph, entry_first_point, entry_last_point, entry_step)


def call():
    global group_type_graph, group_type_func, graph_flag
    if not (any(group_type_graph.values()) and any(group_type_func.values())):
        MessageBox.showinfo("Error", "Choose all parameters.")
    else:


        graph_func = graph.Graph(func_entry.get(),
                                    list(({k: v for k, v in group_type_func.items() if v == 1}).keys())[0],
                                    list(({k: v for k, v in group_type_graph.items() if v == 1}).keys())[0],
                                    first_point=entry_first_point.get(),
                                    last_point=entry_last_point.get(),
                                    step=entry_step.get())

        try:
            graph_func.draw()

        except:
            graph_func.func_error()
        # except NameError:
        #     MessageBox.showinfo("Error", "Incorrect input.\nTry again.")


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


def y_x():
    global group_type_func
    group_type_func = check_state(group_type_func, 'y_x')
    func_func.config(text='y(x)=')
    # but_x_y.config(relief=state_button[group_type_func['x_y']])
    but_y_x.config(relief=state_button[group_type_func['y_x']])
    but_polar.config(relief=state_button[group_type_func['r_theta']])
    but_scat.config(state='normal')
    but_line.config(state='normal')
    but_anal.config(state='normal')


def r_theta():
    global group_type_func, group_type_graph
    group_type_func = check_state(group_type_func, 'r_theta')
    # but_x_y.config(relief=state_button[group_type_func['x_y']])
    but_y_x.config(relief=state_button[group_type_func['y_x']])
    but_polar.config(relief=state_button[group_type_func['r_theta']])
    if group_type_func['r_theta']:
        but_scat.config(state='disabled')
        but_line.config(state='disabled')
        but_anal.config(state='disabled')
    else:
        but_scat.config(state='normal')
        but_line.config(state='normal')
        but_anal.config(state='normal')
    func_func.config(text='r(t)=')
    group_type_graph = check_state(group_type_graph, 'polar')
    but_scat.config(relief=state_button[group_type_graph['scatter']])
    but_line.config(relief=state_button[group_type_graph['line']])


def scatter():
    global group_type_graph
    group_type_graph = check_state(group_type_graph, 'scatter')
    but_scat.config(relief=state_button[group_type_graph['scatter']])
    but_line.config(relief=state_button[group_type_graph['line']])


def line():
    global group_type_graph
    group_type_graph = check_state(group_type_graph, 'line')
    but_scat.config(relief=state_button[group_type_graph['scatter']])
    but_line.config(relief=state_button[group_type_graph['line']])


def show_instruction():
    instruction_window = tk.Tk()
    frm_for_instr = tk.Frame(master=instruction_window)
    lbl_instr_1 = tk.Label(master=frm_for_instr, justify='left', text='Інструкція заповнення поля функції')
    lbl_instr_2 = tk.Label(master=frm_for_instr, justify='left',
                           text='1. Допустимі вирази запису логарифмів: log-, lg-, ln-, log(a*x^n...+c, base).\n'
                                ' Недопускати запис х без множника, якщо він не 0 ')
    lbl_instr_3 = tk.Label(master=frm_for_instr, justify='left',
                           text='2. Допустимі вирази для запису тригонометричних виразів: sin(a*x+b), cos(a*x+b), tan(a*x+b), ctg(a*x+b), \n'
                                'acosh(a*x^n...+c), asinh(a*x^n...+c), atanh(a*x^n...+c), tanh(a*x^n...+c)')
    lbl_instr_4 = tk.Label(master=frm_for_instr, justify='left',
                           text='3. Скорочувати всі множники х однакових степенів, вводити члени виразу ,\n'
                                'функції в знаменнику дробу, логарифму, виразу зі змінною під степенем <1 в порядку спадання степеня х')
    lbl_instr_5 = tk.Label(master=frm_for_instr, justify='left',
                           text='4. Недопускати пробіли, записувати всю функцію без пробілів')
    lbl_instr_6 = tk.Label(master=frm_for_instr, justify='left',
                           text='5. Не записувати під логарифмами дроби з х, під дробами логарифми під х,\n'
                                ' під логарифмами з х інші логарифми з х, аналогічно з дробами.')
    lbl_instr_7 = tk.Label(master=frm_for_instr, justify='left',
                           text='6. Дроби, тангенси так котангенси, логарифми, sqrt чи вирази з степенями менше 0 -\n'
                                'Якщо число с відсутнє, то замість нього записуйте +0')
    frm_for_instr.grid(row=0, column=1, pady=2)
    lbl_instr_1.grid(row=0, column=0, sticky='w', pady=2)
    lbl_instr_2.grid(row=1, column=0, sticky='w', pady=2)
    lbl_instr_3.grid(row=2, column=0, sticky='w', pady=2)
    lbl_instr_4.grid(row=3, column=0, sticky='w', pady=2)
    lbl_instr_5.grid(row=4, column=0, sticky='w', pady=2)
    lbl_instr_6.grid(row=5, column=0, sticky='w', pady=2)
    lbl_instr_7.grid(row=6, column=0, sticky='w', pady=2)
    instruction_window.mainloop()


window = tk.Tk()
window.title("Graph")
window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=200, weight=1)
window.resizable(width=False, height=False)


func_entry = tk.Entry(master=window, width=50)
func_label = tk.Label(master=window, text="Put function")
func_func = tk.Label(master=window, text='y(x)=')
lbl_type_func = tk.Label(master=window, text="Type of function")

but_y_x = tk.Button(
    master=window,
    text="Decart",
    command=y_x,
    relief=tk.RAISED
)

but_polar = tk.Button(
    master=window,
    text='Polar',
    command=r_theta
)
lbl_type_graph = tk.Label(master=window, text="Type of build graph")

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

frame_step = tk.Frame(master=window)
lbl_step = tk.Label(master=frame_step, text="Step")
entry_step = tk.Entry(master=frame_step, width=10)
entry_step.insert(0, '0.1')
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
    command=call_analysis
)

but_instruction = tk.Button(
    master=window,
    text='Instruction',
    command=show_instruction
)

# state of press dictionary
group_type_func = {'y_x': 0, 'r_theta': 0}
group_type_graph = {'scatter': 0, 'line': 0, 'polar': 0}
state_button = {1: tk.GROOVE, 0: tk.RAISED}

but_instruction.grid(row=0, column=2, sticky='w')
func_label.grid(row=1, column=1, sticky='s')
func_entry.grid(row=2, column=1, sticky='w')
func_func.grid(row=2, column=0, sticky='e')
lbl_type_func.grid(row=3, column=1, padx=10, pady=5)
but_y_x.grid(row=4, column=0, padx=10, sticky='e')
but_polar.grid(row=4, column=2, padx=10, sticky='w')
lbl_type_graph.grid(row=5, column=1, padx=10, pady=5)
but_line.grid(row=6, column=0, padx=10, sticky='e')
but_scat.grid(row=6, column=2, padx=10, sticky='w')
frame_first_point.grid(row=7, column=0, padx=20, pady=5)
lbl_firts_point.grid(row=0, column=0, padx=5)
entry_first_point.grid(row=0, column=1)
frame_last_point.grid(row=7, column=1, padx=20, pady=5)
lbl_last_point.grid(row=0, column=0, padx=5)
entry_last_point.grid(row=0, column=1)
frame_step.grid(row=7, column=2, padx=20, pady=5)
lbl_step.grid(row=0, column=0, padx=5)
entry_step.grid(row=0, column=1)
btn_call_graph.grid(row=8, column=1, pady=20, sticky='e')
but_anal.grid(row=8, column=1, pady=20, sticky='w')
window.mainloop()

