# Omega Calculator 11.0 - main.py (Tablet Optimized)
# Author: Amirmahdi Ghorbani
# Larger UI elements, bigger fonts, tablet-friendly touch targets

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import dp
from engine import *

Window.clearcolor = (0.05, 0.05, 0.15, 1)
Window.size = (720, 1280)

class ColoredButton(Button):
    def __init__(self, color=(0.2, 0.6, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = color
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(65)
        self.font_size = dp(18)

class ResultPopup(Popup):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.title_size = dp(22)
        self.size_hint = (0.9, 0.6)
        self.separator_height = dp(3)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        scroll = ScrollView()
        self.label = Label(text=str(content), size_hint_y=None, halign='left', valign='top', color=(1, 1, 1, 1), font_size=dp(18))
        self.label.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))
        self.label.text_size = (dp(600), None)
        scroll.add_widget(self.label)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Close', size_hint_y=None, height=dp(55), font_size=dp(18), on_press=self.dismiss))
        self.content = layout

class OmegaApp(App):
    def build(self):
        self.title = 'Omega Calculator 11.0'
        main = BoxLayout(orientation='vertical')
        header = Label(text='[b]Omega Calculator 11.0[/b]', markup=True, size_hint_y=None, height=dp(70), color=(1, 0.8, 0.2, 1), font_size=dp(28))
        main.add_widget(header)
        self.tabs = TabbedPanel(do_default_tab=False, tab_width=dp(120), tab_height=dp(50))
        self.add_basic_tab()
        self.add_algebra_tab()
        self.add_geometry_tab()
        self.add_numbers_tab()
        self.add_stats_tab()
        self.add_calculus_tab()
        self.add_physics_tab()
        self.add_chemistry_tab()
        self.add_convert_tab()
        self.tabs.default_tab = self.tabs.tab_list[0]
        main.add_widget(self.tabs)
        footer = Label(text='By Amirmahdi Ghorbani | v11.0 Tablet Edition', size_hint_y=None, height=dp(35), color=(0.5, 0.5, 0.5, 1), font_size=dp(14))
        main.add_widget(footer)
        return main

    def show_result(self, title, result):
        ResultPopup(title=title, content=str(result)).open()

    def make_label(self, text):
        return Label(text=text, color=(1,1,1,1), size_hint_y=None, height=dp(50), font_size=dp(18))

    def make_input(self, hint=''):
        return TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(55), font_size=dp(18), padding=[dp(15), dp(10)])

    def make_spinner(self, values):
        return Spinner(text=values[0], values=values, size_hint_y=None, height=dp(55), font_size=dp(18))

    def add_basic_tab(self):
        tab = TabbedPanelItem(text='Basic')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Expression:'))
        expr_input = self.make_input('e.g. 2+3*4')
        layout.add_widget(expr_input)
        
        layout.add_widget(self.make_label('Power Base:'))
        power_base = self.make_input('base')
        layout.add_widget(power_base)
        layout.add_widget(self.make_label('Exponent:'))
        power_exp = self.make_input('exponent')
        layout.add_widget(power_exp)
        
        layout.add_widget(self.make_label('Root Number:'))
        root_num = self.make_input('number')
        layout.add_widget(root_num)
        layout.add_widget(self.make_label('Root Degree:'))
        root_n = self.make_input('degree')
        layout.add_widget(root_n)
        
        layout.add_widget(self.make_label('Factorial n:'))
        fact_input = self.make_input('n!')
        layout.add_widget(fact_input)
        
        layout.add_widget(self.make_label('Absolute |x|:'))
        abs_input = self.make_input('x')
        layout.add_widget(abs_input)
        
        buttons_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(250))
        
        def calc_expr(instance):
            try:
                e = expr_input.text.replace('×','*').replace('÷','/')
                r = eval(e, {"__builtins__": {}}, {'sin':math.sin,'cos':math.cos,'tan':math.tan,'sqrt':math.sqrt,'log':math.log,'pi':math.pi,'e':math.e})
                self.show_result('Result', f'{expr_input.text} = {r}')
            except: self.show_result('Error', 'Invalid expression!')
        
        def calc_power(instance):
            try:
                b, e = float(power_base.text), float(power_exp.text)
                self.show_result('Power', f'{b}^{e} = {b**e}')
            except: self.show_result('Error', 'Invalid!')
        
        def calc_root(instance):
            try:
                n, d = float(root_num.text), float(root_n.text)
                self.show_result('Root', f'{d}√{n} = {n**(1/d)}')
            except: self.show_result('Error', 'Invalid!')
        
        def calc_fact(instance):
            try:
                n = int(fact_input.text)
                if n < 0: raise ValueError
                self.show_result('Factorial', f'{n}! = {math.factorial(n)}')
            except: self.show_result('Error', 'Enter non-negative integer!')
        
        def calc_abs(instance):
            try:
                self.show_result('Absolute', f'|{abs_input.text}| = {abs(float(abs_input.text))}')
            except: self.show_result('Error', 'Invalid!')
        
        buttons_layout.add_widget(ColoredButton(text='Calculate Expression', on_press=calc_expr))
        buttons_layout.add_widget(ColoredButton(text='Power', on_press=calc_power))
        buttons_layout.add_widget(ColoredButton(text='Root', on_press=calc_root))
        buttons_layout.add_widget(ColoredButton(text='Factorial', on_press=calc_fact))
        buttons_layout.add_widget(ColoredButton(text='Absolute', on_press=calc_abs))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(buttons_layout)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_algebra_tab(self):
        tab = TabbedPanelItem(text='Algebra')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Linear (a,b,c,d):'))
        lin = self.make_input('ax+b=cx+d → a,b,c,d')
        layout.add_widget(lin)
        
        layout.add_widget(self.make_label('2-Var (a1,b1,c1,a2,b2,c2):'))
        var2 = self.make_input('6 values')
        layout.add_widget(var2)
        
        layout.add_widget(self.make_label('Quadratic (a,b,c):'))
        quad = self.make_input('a,b,c')
        layout.add_widget(quad)
        
        layout.add_widget(self.make_label('Cubic (a,b,c,d):'))
        cub = self.make_input('a,b,c,d')
        layout.add_widget(cub)
        
        layout.add_widget(self.make_label('Polynomial Coeffs:'))
        poly = self.make_input('c0,c1,c2,...')
        layout.add_widget(poly)
        
        layout.add_widget(self.make_label('Matrix A:'))
        mat_a = self.make_input('1,2;3,4')
        layout.add_widget(mat_a)
        layout.add_widget(self.make_label('Matrix B:'))
        mat_b = self.make_input('for add/mul')
        layout.add_widget(mat_b)
        
        mat_op = self.make_spinner(['Add','Multiply','Determinant','Inverse'])
        layout.add_widget(self.make_label('Operation:'))
        layout.add_widget(mat_op)
        
        def solve_lin(instance):
            try:
                a,b,c,d = map(float, lin.text.split(','))
                x = (d-b)/(a-c) if a!=c else None
                self.show_result('Linear Eq', f'x = {x}' if x else 'No unique solution')
            except: self.show_result('Error', 'Invalid!')
        
        def solve_2var(instance):
            try:
                vals = list(map(float, var2.text.split(',')))
                r = EquationEngine.solve_linear_2var(*vals)
                self.show_result('2-Var', f'x={r[0]}, y={r[1]}' if r else 'No solution')
            except: self.show_result('Error', 'Invalid!')
        
        def solve_quad(instance):
            try:
                a,b,c = map(float, quad.text.split(','))
                r = EquationEngine.solve_quadratic(a,b,c)
                if not r: self.show_result('Error', 'a=0!')
                elif r[0]=='complex': self.show_result('Quadratic', f'Complex: {r[1]}+{r[2]}i, {r[1]}-{r[2]}i')
                elif r[0]=='double': self.show_result('Quadratic', f'Double: x={r[1]}')
                else: self.show_result('Quadratic', f'x1={r[1]}, x2={r[2]}')
            except: self.show_result('Error', 'Invalid!')
        
        def solve_cub(instance):
            try:
                a,b,c,d = map(float, cub.text.split(','))
                r = EquationEngine.solve_cubic(a,b,c,d)
                self.show_result('Cubic', f'Roots: {r}')
            except: self.show_result('Error', 'Invalid!')
        
        def solve_poly(instance):
            try:
                coeffs = list(map(float, poly.text.split(',')))
                r = EquationEngine.solve_polynomial(coeffs)
                self.show_result('Polynomial', f'Roots: {r}')
            except: self.show_result('Error', 'Invalid!')
        
        def do_matrix(instance):
            try:
                op = {'Add':'add','Multiply':'mul','Determinant':'det','Inverse':'inv'}[mat_op.text]
                r = EquationEngine.matrix_op(mat_a.text, mat_b.text, op)
                self.show_result('Matrix', str(r) if r else 'Error')
            except: self.show_result('Error', 'Invalid format!')
        
        btns = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(230))
        btns.add_widget(ColoredButton(text='Linear', on_press=solve_lin))
        btns.add_widget(ColoredButton(text='2-Var', on_press=solve_2var))
        btns.add_widget(ColoredButton(text='Quadratic', on_press=solve_quad))
        btns.add_widget(ColoredButton(text='Cubic', on_press=solve_cub))
        btns.add_widget(ColoredButton(text='Polynomial', on_press=solve_poly))
        btns.add_widget(ColoredButton(text='Matrix Op', on_press=do_matrix))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_geometry_tab(self):
        tab = TabbedPanelItem(text='Geometry')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        shapes = self.make_spinner(['Square','Rectangle','Circle','Triangle','Cube','Sphere','Cylinder','Cone'])
        layout.add_widget(self.make_label('Shape:'))
        layout.add_widget(shapes)
        
        layout.add_widget(self.make_label('Param 1:'))
        p1 = self.make_input('side/radius/length')
        layout.add_widget(p1)
        layout.add_widget(self.make_label('Param 2:'))
        p2 = self.make_input('width/height (optional)')
        layout.add_widget(p2)
        
        layout.add_widget(self.make_label('Pythagorean (a,b):'))
        pyth = self.make_input('a,b')
        layout.add_widget(pyth)
        
        layout.add_widget(self.make_label('Trig (sin/cos/tan in °):'))
        trig_expr = self.make_input('sin(30)')
        layout.add_widget(trig_expr)
        
        def calc_geo(instance):
            try:
                s = shapes.text; v1 = float(p1.text)
                v2 = float(p2.text) if p2.text else 0
                if s == 'Square': r = f'P={4*v1}, A={v1**2}'
                elif s == 'Rectangle': r = f'P={2*(v1+v2)}, A={v1*v2}'
                elif s == 'Circle': r = f'C={2*math.pi*v1:.2f}, A={math.pi*v1**2:.2f}'
                elif s == 'Triangle': r = f'P={3*v1}, A={math.sqrt(3)/4*v1**2:.2f}' if not v2 else f'P={v1+v2+math.sqrt(v1**2+v2**2):.2f}, A={0.5*v1*v2:.2f}'
                elif s == 'Cube': r = f'V={v1**3}'
                elif s == 'Sphere': r = f'V={4/3*math.pi*v1**3:.2f}'
                elif s == 'Cylinder': r = f'V={math.pi*v1**2*v2:.2f}'
                elif s == 'Cone': r = f'V={1/3*math.pi*v1**2*v2:.2f}'
                self.show_result('Geometry', r)
            except: self.show_result('Error', 'Invalid!')
        
        def calc_pyth(instance):
            try:
                a,b = map(float, pyth.text.split(','))
                self.show_result('Pythagorean', f'c = {math.sqrt(a**2+b**2):.2f}')
            except: self.show_result('Error', 'Invalid!')
        
        def calc_trig(instance):
            try:
                e = trig_expr.text
                r = eval(e, {"__builtins__": {}}, {'sin':lambda x: math.sin(math.radians(x)), 'cos':lambda x: math.cos(math.radians(x)), 'tan':lambda x: math.tan(math.radians(x)), 'pi':math.pi})
                self.show_result('Trig', f'{e} = {r}')
            except: self.show_result('Error', 'Use sin(x), cos(x), tan(x) in degrees')
        
        btns = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, height=dp(200))
        btns.add_widget(ColoredButton(text='Calculate Shape', on_press=calc_geo))
        btns.add_widget(ColoredButton(text='Pythagorean Theorem', on_press=calc_pyth))
        btns.add_widget(ColoredButton(text='Trigonometry', on_press=calc_trig))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_numbers_tab(self):
        tab = TabbedPanelItem(text='Numbers')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Prime Check:'))
        prime_in = self.make_input('number')
        layout.add_widget(prime_in)
        
        layout.add_widget(self.make_label('Primes up to N:'))
        primes_n = self.make_input('N')
        layout.add_widget(primes_n)
        
        layout.add_widget(self.make_label('GCD/LCM (a,b):'))
        gcd_in = self.make_input('a,b')
        layout.add_widget(gcd_in)
        
        layout.add_widget(self.make_label('Fibonacci N:'))
        fib_n = self.make_input('N terms')
        layout.add_widget(fib_n)
        
        layout.add_widget(self.make_label('Base (num,base):'))
        base_in = self.make_input('number,2|8|16')
        layout.add_widget(base_in)
        
        def check_prime(instance):
            try:
                n = int(prime_in.text)
                self.show_result('Prime', f'{n} is {"prime" if MathEngine.is_prime(n) else "not prime"}')
            except: self.show_result('Error', 'Invalid!')
        
        def list_primes(instance):
            try:
                n = int(primes_n.text)
                p = [i for i in range(2, n+1) if MathEngine.is_prime(i)]
                self.show_result(f'Primes up to {n}', f'{len(p)} primes: {p[:50]}...' if len(p)>50 else str(p))
            except: self.show_result('Error', 'Invalid!')
        
        def calc_gcd(instance):
            try:
                a,b = map(int, gcd_in.text.split(','))
                self.show_result('GCD/LCM', f'GCD({a},{b})={math.gcd(a,b)}\nLCM({a},{b})={MathEngine.lcm(a,b)}')
            except: self.show_result('Error', 'Invalid!')
        
        def calc_fib(instance):
            try:
                n = int(fib_n.text)
                a,b = 0,1
                seq = []
                for _ in range(min(n, 100)): seq.append(str(a)); a,b = b,a+b
                self.show_result('Fibonacci', ' '.join(seq))
            except: self.show_result('Error', 'Invalid!')
        
        def convert_base(instance):
            try:
                num, base = base_in.text.split(',')
                num, base = int(num), int(base)
                if base == 2: r = bin(num)
                elif base == 8: r = oct(num)
                elif base == 16: r = hex(num)
                else: r = 'Use 2, 8, or 16'
                self.show_result('Base', f'{num} = {r}')
            except: self.show_result('Error', 'Invalid!')
        
        btns = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, height=dp(320))
        btns.add_widget(ColoredButton(text='Check Prime', on_press=check_prime))
        btns.add_widget(ColoredButton(text='List Primes', on_press=list_primes))
        btns.add_widget(ColoredButton(text='GCD & LCM', on_press=calc_gcd))
        btns.add_widget(ColoredButton(text='Fibonacci Sequence', on_press=calc_fib))
        btns.add_widget(ColoredButton(text='Base Converter', on_press=convert_base))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_stats_tab(self):
        tab = TabbedPanelItem(text='Stats')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Data (comma):'))
        data_in = self.make_input('1,2,3,4,5')
        layout.add_widget(data_in)
        
        layout.add_widget(self.make_label('Distribution:'))
        dist_type = self.make_spinner(['uniform','normal','exponential','triangular'])
        layout.add_widget(dist_type)
        layout.add_widget(self.make_label('Params:'))
        dist_params = self.make_input('param1,param2')
        layout.add_widget(dist_params)
        
        def calc_stats(instance):
            try:
                data = list(map(float, data_in.text.split(',')))
                m = StatisticsEngine.mean(data)
                med = StatisticsEngine.median(data)
                mode = StatisticsEngine.mode(data)
                self.show_result('Statistics', f'Mean: {m}\nMedian: {med}\nMode: {mode}')
            except: self.show_result('Error', 'Invalid data!')
        
        def gen_random(instance):
            try:
                params = dist_params.text.split(',')
                r = StatisticsEngine.random_dist(dist_type.text, params)
                if r: self.show_result('Random', f'{dist_type.text}: {r}')
                else: self.show_result('Error', 'Invalid params!')
            except: self.show_result('Error', 'Error!')
        
        btns = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, height=dp(130))
        btns.add_widget(ColoredButton(text='Calculate Statistics', on_press=calc_stats))
        btns.add_widget(ColoredButton(text='Generate Random Number', on_press=gen_random))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_calculus_tab(self):
        tab = TabbedPanelItem(text='Calculus')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Function f(x):'))
        func = self.make_input('x**2 + sin(x)')
        layout.add_widget(func)
        
        layout.add_widget(self.make_label('Derivative at x:'))
        deriv_x = self.make_input('x value')
        layout.add_widget(deriv_x)
        
        layout.add_widget(self.make_label('Integral lower:'))
        int_a = self.make_input('a (lower bound)')
        layout.add_widget(int_a)
        layout.add_widget(self.make_label('Integral upper:'))
        int_b = self.make_input('b (upper bound)')
        layout.add_widget(int_b)
        
        def calc_deriv(instance):
            try:
                x = float(deriv_x.text)
                r = MathEngine.der(func.text, x)
                self.show_result('Derivative', f"f'({x}) = {r}")
            except: self.show_result('Error', 'Invalid! Use x as variable.')
        
        def calc_integ(instance):
            try:
                a, b = float(int_a.text), float(int_b.text)
                r = MathEngine.integral(func.text, a, b)
                self.show_result('Integral', f'∫[{a},{b}] f(x)dx = {r}')
            except: self.show_result('Error', 'Invalid! Use x as variable.')
        
        btns = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, height=dp(130))
        btns.add_widget(ColoredButton(text='Calculate Derivative', on_press=calc_deriv))
        btns.add_widget(ColoredButton(text='Calculate Integral', on_press=calc_integ))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_physics_tab(self):
        tab = TabbedPanelItem(text='Physics')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        all_forms = PhysicsEngine.get_all()
        cat_spin = self.make_spinner(list(all_forms.keys()))
        layout.add_widget(self.make_label('Category:'))
        layout.add_widget(cat_spin)
        
        form_spin = self.make_spinner(list(all_forms['Kinematics'].keys()))
        layout.add_widget(self.make_label('Formula:'))
        layout.add_widget(form_spin)
        
        def update_formulas(spinner, text):
            form_spin.values = list(all_forms[text].keys())
            form_spin.text = form_spin.values[0]
        cat_spin.bind(text=update_formulas)
        
        layout.add_widget(self.make_label('Params (comma):'))
        params_in = self.make_input('e.g. 0,9.8,3')
        layout.add_widget(params_in)
        
        def calc_physics(instance):
            try:
                cat = cat_spin.text
                form = form_spin.text
                fn = all_forms[cat][form]
                params = [float(x.strip()) for x in params_in.text.split(',') if x.strip()]
                r = fn(*params)
                self.show_result('Physics', f'{form}\nResult: {r}')
            except: self.show_result('Error', 'Check parameters!')
        
        const_spin = self.make_spinner(list(PhysicsEngine.CONSTANTS.keys()))
        layout.add_widget(self.make_label('Constant:'))
        layout.add_widget(const_spin)
        
        def show_const(instance):
            self.show_result('Constant', f'{const_spin.text} = {PhysicsEngine.get_constant(const_spin.text)}')
        
        btns = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, height=dp(130))
        btns.add_widget(ColoredButton(text='Calculate Formula', on_press=calc_physics))
        btns.add_widget(ColoredButton(text='Show Constant Value', on_press=show_const))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_chemistry_tab(self):
        tab = TabbedPanelItem(text='Chemistry')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Atomic # (1-118):'))
        at_num = self.make_input('e.g. 79 for Gold')
        layout.add_widget(at_num)
        
        layout.add_widget(self.make_label('Search:'))
        search_in = self.make_input('name or symbol')
        layout.add_widget(search_in)
        
        def lookup(instance):
            try:
                n = int(at_num.text)
                e = ChemistryEngine.get_element(n)
                if e:
                    self.show_result('Element', f'{e["name"]} ({e["symbol"]})\n\nAtomic: {n}\nMass: {e["mass"]} g/mol\nGroup: {e["group"]}\nPeriod: {e["period"]}\nConfig: {e["config"]}')
                else: self.show_result('Error', 'Element not found! (1-118)')
            except: self.show_result('Error', 'Enter a number 1-118')
        
        def search(instance):
            q = search_in.text.strip()
            if q:
                results = ChemistryEngine.search(q)
                if results:
                    txt = '\n'.join([f'#{k}: {v["name"]} ({v["symbol"]})' for k,v in list(results.items())[:30]])
                    self.show_result(f'Search: "{q}"', txt if txt else 'No results')
                else: self.show_result('Search', 'No results found')
        
        btns = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, height=dp(130))
        btns.add_widget(ColoredButton(text='Lookup Element', on_press=lookup))
        btns.add_widget(ColoredButton(text='Search Elements', on_press=search))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_convert_tab(self):
        tab = TabbedPanelItem(text='Convert')
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=dp(12), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Value:'))
        val_in = self.make_input('e.g. 100')
        layout.add_widget(val_in)
        
        layout.add_widget(self.make_label('From Unit:'))
        from_u = self.make_input('cm, C, g, kg...')
        layout.add_widget(from_u)
        layout.add_widget(self.make_label('To Unit:'))
        to_u = self.make_input('m, F, pound...')
        layout.add_widget(to_u)
        
        def do_convert(instance):
            length_map = {'cm':0.01, 'm':1, 'km':1000, 'inch':0.0254, 'foot':0.3048}
            try:
                v = float(val_in.text)
                f, t = from_u.text.strip(), to_u.text.strip()
                if f in length_map and t in length_map:
                    r = v * length_map[f] / length_map[t]
                elif f=='C' and t=='F': r = v*9/5+32
                elif f=='C' and t=='K': r = v+273.15
                elif f=='F' and t=='C': r = (v-32)*5/9
                elif f=='F' and t=='K': r = (v-32)*5/9+273.15
                elif f=='K' and t=='C': r = v-273.15
                elif f=='K' and t=='F': r = (v-273.15)*9/5+32
                elif f=='g' and t=='kg': r = v/1000
                elif f=='kg' and t=='g': r = v*1000
                elif f=='kg' and t=='pound': r = v*2.20462
                elif f=='pound' and t=='kg': r = v/2.20462
                else: r = 'Unsupported!'
                self.show_result('Convert', f'{v} {f} = {r} {t}')
            except: self.show_result('Error', 'Invalid!')
        
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(ColoredButton(text='Convert Unit', on_press=do_convert))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        
        help_text = Label(text='Length: cm, m, km, inch, foot\nTemperature: C, F, K\nWeight: g, kg, pound', color=(0.7,0.7,0.7,1), size_hint_y=None, height=dp(100), font_size=dp(16))
        layout.add_widget(help_text)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

if __name__ == '__main__':
    OmegaApp().run()