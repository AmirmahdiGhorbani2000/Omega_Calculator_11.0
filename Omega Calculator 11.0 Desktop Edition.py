# Omega Calculator 11.0 - main_desktop.py (Desktop Edition)
# Author: Amirmahdi Ghorbani
# Optimized for computers: 1024x768, compact layout, mouse-friendly

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
Window.size = (1024, 768)

class ColoredButton(Button):
    def __init__(self, color=(0.2, 0.6, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = color
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = dp(32)
        self.font_size = dp(11)

class ResultPopup(Popup):
    def __init__(self, title, content, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.title_size = dp(14)
        self.size_hint = (0.5, 0.5)
        self.separator_height = dp(1)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(6))
        scroll = ScrollView()
        self.label = Label(text=str(content), size_hint_y=None, halign='left', valign='top', color=(1, 1, 1, 1), font_size=dp(11))
        self.label.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))
        self.label.text_size = (dp(480), None)
        scroll.add_widget(self.label)
        layout.add_widget(scroll)
        layout.add_widget(Button(text='Close', size_hint_y=None, height=dp(28), font_size=dp(11), on_press=self.dismiss))
        self.content = layout

class OmegaApp(App):
    def build(self):
        self.title = 'Omega Calculator 11.0'
        main = BoxLayout(orientation='vertical')
        header = Label(text='[b]Omega Calculator 11.0[/b]', markup=True, size_hint_y=None, height=dp(36), color=(1, 0.8, 0.2, 1), font_size=dp(18))
        main.add_widget(header)
        self.tabs = TabbedPanel(do_default_tab=False, tab_width=dp(90), tab_height=dp(30))
        self.add_all_tabs()
        self.tabs.default_tab = self.tabs.tab_list[0]
        main.add_widget(self.tabs)
        footer = Label(text='By Amirmahdi Ghorbani | v11.0 Desktop Edition', size_hint_y=None, height=dp(18), color=(0.5, 0.5, 0.5, 1), font_size=dp(9))
        main.add_widget(footer)
        return main

    def show_result(self, title, result):
        ResultPopup(title=title, content=str(result)).open()

    def make_label(self, text):
        return Label(text=text, color=(1,1,1,1), size_hint_y=None, height=dp(24), font_size=dp(11))

    def make_input(self, hint=''):
        return TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(28), font_size=dp(11), padding=[dp(8), dp(4)])

    def make_spinner(self, values):
        return Spinner(text=values[0], values=values, size_hint_y=None, height=dp(28), font_size=dp(11))

    def add_all_tabs(self):
        self.add_basic_tab()
        self.add_algebra_tab()
        self.add_geometry_tab()
        self.add_numbers_tab()
        self.add_stats_tab()
        self.add_calculus_tab()
        self.add_physics_tab()
        self.add_chemistry_tab()
        self.add_convert_tab()

    def add_basic_tab(self):
        tab = TabbedPanelItem(text='Basic')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Expression:'))
        expr_input = self.make_input('e.g. 2+3*4')
        layout.add_widget(expr_input)
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        
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
        layout.add_widget(self.make_label('Absolute x:'))
        abs_input = self.make_input('x')
        layout.add_widget(abs_input)
        
        btns = GridLayout(cols=5, spacing=dp(3), size_hint_y=None, height=dp(36))
        
        def calc_expr(i):
            try:
                e=expr_input.text.replace('×','*').replace('÷','/')
                r=eval(e,{"__builtins__":{}},{'sin':math.sin,'cos':math.cos,'tan':math.tan,'sqrt':math.sqrt,'log':math.log,'pi':math.pi,'e':math.e})
                self.show_result('Result',f'{expr_input.text} = {r}')
            except: self.show_result('Error','Invalid expression')
        def calc_pow(i):
            try: self.show_result('Power',f'{power_base.text}^{power_exp.text} = {float(power_base.text)**float(power_exp.text)}')
            except: self.show_result('Error','Invalid')
        def calc_rt(i):
            try: self.show_result('Root',f'{root_n.text}√{root_num.text} = {float(root_num.text)**(1/float(root_n.text))}')
            except: self.show_result('Error','Invalid')
        def calc_fact(i):
            try:
                n=int(fact_input.text)
                if n<0: raise ValueError
                self.show_result('Factorial',f'{n}! = {math.factorial(n)}')
            except: self.show_result('Error','Invalid')
        def calc_abs(i):
            try: self.show_result('Absolute',f'|{abs_input.text}| = {abs(float(abs_input.text))}')
            except: self.show_result('Error','Invalid')
        
        btns.add_widget(ColoredButton(text='Calculate', on_press=calc_expr))
        btns.add_widget(ColoredButton(text='Power', on_press=calc_pow))
        btns.add_widget(ColoredButton(text='Root', on_press=calc_rt))
        btns.add_widget(ColoredButton(text='n!', on_press=calc_fact))
        btns.add_widget(ColoredButton(text='|x|', on_press=calc_abs))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(5)))
        layout.add_widget(Label(size_hint_y=None, height=dp(5)))
        layout.add_widget(Label(size_hint_y=None, height=dp(5)))
        layout.add_widget(Label(size_hint_y=None, height=dp(5)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_algebra_tab(self):
        tab = TabbedPanelItem(text='Algebra')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Linear (a,b,c,d):'))
        lin = self.make_input('ax+b=cx+d')
        layout.add_widget(lin)
        layout.add_widget(self.make_label('2-Var Sys: a1,b1,c1,a2,b2,c2'))
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
        layout.add_widget(self.make_label('Matrix B (opt):'))
        mat_b = self.make_input('for add/mul')
        layout.add_widget(mat_b)
        
        mat_op = self.make_spinner(['Add','Multiply','Determinant','Inverse'])
        layout.add_widget(self.make_label('Matrix Op:'))
        layout.add_widget(mat_op)
        
        btns = GridLayout(cols=3, spacing=dp(3), size_hint_y=None, height=dp(60))
        
        def sl(i):
            try:
                a,b,c,d=map(float,lin.text.split(','))
                self.show_result('Linear Eq',f'x = {(d-b)/(a-c)}' if a!=c else 'No unique solution')
            except: self.show_result('Error','Invalid')
        def s2(i):
            try:
                v=list(map(float,var2.text.split(',')))
                r=EquationEngine.solve_linear_2var(*v)
                self.show_result('2-Var System',f'x={r[0]}, y={r[1]}' if r else 'No solution')
            except: self.show_result('Error','Invalid')
        def sq(i):
            try:
                a,b,c=map(float,quad.text.split(','))
                r=EquationEngine.solve_quadratic(a,b,c)
                if not r: self.show_result('Error','a cannot be 0')
                elif r[0]=='complex': self.show_result('Quadratic',f'Complex: {r[1]}+{r[2]}i, {r[1]}-{r[2]}i')
                elif r[0]=='double': self.show_result('Quadratic',f'Double root: x={r[1]}')
                else: self.show_result('Quadratic',f'x1={r[1]}, x2={r[2]}')
            except: self.show_result('Error','Invalid')
        def sc(i):
            try:
                a,b,c,d=map(float,cub.text.split(','))
                self.show_result('Cubic',str(EquationEngine.solve_cubic(a,b,c,d)))
            except: self.show_result('Error','Invalid')
        def sp(i):
            try:
                c=list(map(float,poly.text.split(',')))
                self.show_result('Polynomial',str(EquationEngine.solve_polynomial(c)))
            except: self.show_result('Error','Invalid')
        def dm(i):
            try:
                op={'Add':'add','Multiply':'mul','Determinant':'det','Inverse':'inv'}[mat_op.text]
                r=EquationEngine.matrix_op(mat_a.text,mat_b.text,op)
                self.show_result('Matrix',str(r) if r else 'Error in operation')
            except: self.show_result('Error','Invalid format')
        
        btns.add_widget(ColoredButton(text='Linear', on_press=sl))
        btns.add_widget(ColoredButton(text='2-Var', on_press=s2))
        btns.add_widget(ColoredButton(text='Quadratic', on_press=sq))
        btns.add_widget(ColoredButton(text='Cubic', on_press=sc))
        btns.add_widget(ColoredButton(text='Polynomial', on_press=sp))
        btns.add_widget(ColoredButton(text='Matrix Op', on_press=dm))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_geometry_tab(self):
        tab = TabbedPanelItem(text='Geometry')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        shapes = self.make_spinner(['Square','Rectangle','Circle','Triangle','Cube','Sphere','Cylinder','Cone'])
        layout.add_widget(self.make_label('Shape:'))
        layout.add_widget(shapes)
        layout.add_widget(self.make_label('Param 1:'))
        p1 = self.make_input('side/r/length')
        layout.add_widget(p1)
        layout.add_widget(self.make_label('Param 2 (opt):'))
        p2 = self.make_input('width/height')
        layout.add_widget(p2)
        
        layout.add_widget(self.make_label('Pythagorean (a,b):'))
        pyth = self.make_input('a,b')
        layout.add_widget(pyth)
        layout.add_widget(self.make_label('Trigonometry:'))
        trig_expr = self.make_input('sin(30)')
        layout.add_widget(trig_expr)
        
        btns = GridLayout(cols=3, spacing=dp(3), size_hint_y=None, height=dp(36))
        
        def cg(i):
            try:
                s=shapes.text;v1=float(p1.text);v2=float(p2.text) if p2.text else 0
                if s=='Square': r=f'P={4*v1}, A={v1**2}'
                elif s=='Rectangle': r=f'P={2*(v1+v2)}, A={v1*v2}'
                elif s=='Circle': r=f'C={2*math.pi*v1:.2f}, A={math.pi*v1**2:.2f}'
                elif s=='Triangle': r=f'P={3*v1}, A={math.sqrt(3)/4*v1**2:.2f}' if not v2 else f'P={v1+v2+math.sqrt(v1**2+v2**2):.2f}, A={0.5*v1*v2:.2f}'
                elif s=='Cube': r=f'V={v1**3}'
                elif s=='Sphere': r=f'V={4/3*math.pi*v1**3:.2f}'
                elif s=='Cylinder': r=f'V={math.pi*v1**2*v2:.2f}'
                elif s=='Cone': r=f'V={1/3*math.pi*v1**2*v2:.2f}'
                self.show_result('Geometry',r)
            except: self.show_result('Error','Invalid')
        def cp(i):
            try:
                a,b=map(float,pyth.text.split(','))
                self.show_result('Pythagorean',f'c = {math.sqrt(a**2+b**2):.2f}')
            except: self.show_result('Error','Invalid')
        def ct(i):
            try:
                e=trig_expr.text
                r=eval(e,{"__builtins__":{}},{'sin':lambda x:math.sin(math.radians(x)),'cos':lambda x:math.cos(math.radians(x)),'tan':lambda x:math.tan(math.radians(x)),'pi':math.pi})
                self.show_result('Trig',f'{e} = {r}')
            except: self.show_result('Error','Use sin(x)/cos(x)/tan(x) in degrees')
        
        btns.add_widget(ColoredButton(text='Calculate Shape', on_press=cg))
        btns.add_widget(ColoredButton(text='Pythagorean', on_press=cp))
        btns.add_widget(ColoredButton(text='Trig', on_press=ct))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_numbers_tab(self):
        tab = TabbedPanelItem(text='Numbers')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Prime Check n:'))
        prime_in = self.make_input('number')
        layout.add_widget(prime_in)
        layout.add_widget(self.make_label('Primes up to N:'))
        primes_n = self.make_input('N')
        layout.add_widget(primes_n)
        
        layout.add_widget(self.make_label('GCD/LCM (a,b):'))
        gcd_in = self.make_input('a,b')
        layout.add_widget(gcd_in)
        layout.add_widget(self.make_label('Fibonacci N terms:'))
        fib_n = self.make_input('N')
        layout.add_widget(fib_n)
        
        layout.add_widget(self.make_label('Base Conv (n,base):'))
        base_in = self.make_input('number,2|8|16')
        layout.add_widget(base_in)
        
        btns = GridLayout(cols=5, spacing=dp(3), size_hint_y=None, height=dp(36))
        
        def chp(i):
            try: self.show_result('Prime Check',f'{prime_in.text} is {"prime" if MathEngine.is_prime(int(prime_in.text)) else "not prime"}')
            except: self.show_result('Error','Invalid')
        def lp(i):
            try:
                n=int(primes_n.text)
                p=[i for i in range(2,n+1) if MathEngine.is_prime(i)]
                self.show_result(f'Primes up to {n}',f'{len(p)} primes found')
            except: self.show_result('Error','Invalid')
        def cg(i):
            try:
                a,b=map(int,gcd_in.text.split(','))
                self.show_result('GCD & LCM',f'GCD({a},{b}) = {math.gcd(a,b)}\nLCM({a},{b}) = {MathEngine.lcm(a,b)}')
            except: self.show_result('Error','Invalid')
        def cf(i):
            try:
                n=int(fib_n.text);a,b=0,1;seq=[]
                for _ in range(min(n,80)):seq.append(str(a));a,b=b,a+b
                self.show_result('Fibonacci',f'First {n} terms:\n{" ".join(seq)}')
            except: self.show_result('Error','Invalid')
        def cb(i):
            try:
                n,b=base_in.text.split(',');n,b=int(n),int(b)
                r=bin(n) if b==2 else oct(n) if b==8 else hex(n) if b==16 else 'Use 2, 8, or 16'
                self.show_result('Base Conversion',f'{n} (base 10) = {r} (base {b})')
            except: self.show_result('Error','Invalid')
        
        btns.add_widget(ColoredButton(text='Check Prime', on_press=chp))
        btns.add_widget(ColoredButton(text='List Primes', on_press=lp))
        btns.add_widget(ColoredButton(text='GCD/LCM', on_press=cg))
        btns.add_widget(ColoredButton(text='Fibonacci', on_press=cf))
        btns.add_widget(ColoredButton(text='Base Conv', on_press=cb))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_stats_tab(self):
        tab = TabbedPanelItem(text='Stats')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Data (comma):'))
        data_in = self.make_input('1,2,3,4,5')
        layout.add_widget(data_in)
        layout.add_widget(self.make_label('Distribution:'))
        dist_type = self.make_spinner(['uniform','normal','exponential','triangular'])
        layout.add_widget(dist_type)
        layout.add_widget(self.make_label('Dist Params:'))
        dist_params = self.make_input('param1,param2')
        layout.add_widget(dist_params)
        
        btns = GridLayout(cols=2, spacing=dp(3), size_hint_y=None, height=dp(32))
        
        def cs(i):
            try:
                d=list(map(float,data_in.text.split(',')))
                self.show_result('Statistics',f'Mean: {StatisticsEngine.mean(d)}\nMedian: {StatisticsEngine.median(d)}\nMode: {StatisticsEngine.mode(d)}')
            except: self.show_result('Error','Invalid data')
        def gr(i):
            try:
                p=dist_params.text.split(',')
                r=StatisticsEngine.random_dist(dist_type.text,p)
                self.show_result('Random',f'{dist_type.text}: {r}' if r else 'Error generating')
            except: self.show_result('Error','Invalid params')
        
        btns.add_widget(ColoredButton(text='Calculate Statistics', on_press=cs))
        btns.add_widget(ColoredButton(text='Generate Random', on_press=gr))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_calculus_tab(self):
        tab = TabbedPanelItem(text='Calculus')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('f(x) ='))
        func = self.make_input('x**2 + sin(x)')
        layout.add_widget(func)
        layout.add_widget(self.make_label('Derivative at x:'))
        deriv_x = self.make_input('x value')
        layout.add_widget(deriv_x)
        layout.add_widget(self.make_label('Integral [a]:'))
        int_a = self.make_input('lower bound')
        layout.add_widget(int_a)
        layout.add_widget(self.make_label('Integral [b]:'))
        int_b = self.make_input('upper bound')
        layout.add_widget(int_b)
        
        btns = GridLayout(cols=2, spacing=dp(3), size_hint_y=None, height=dp(32))
        
        def cd(i):
            try: self.show_result('Derivative',f"f'({deriv_x.text}) = {MathEngine.der(func.text,float(deriv_x.text))}")
            except: self.show_result('Error','Invalid function or x value')
        def ci(i):
            try:
                a,b=float(int_a.text),float(int_b.text)
                self.show_result('Definite Integral',f'∫[{a},{b}] f(x)dx = {MathEngine.integral(func.text,a,b)}')
            except: self.show_result('Error','Invalid function or bounds')
        
        btns.add_widget(ColoredButton(text='Derivative', on_press=cd))
        btns.add_widget(ColoredButton(text='Integral', on_press=ci))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_physics_tab(self):
        tab = TabbedPanelItem(text='Physics')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        all_forms = PhysicsEngine.get_all()
        cat_spin = self.make_spinner(list(all_forms.keys()))
        layout.add_widget(self.make_label('Category:'))
        layout.add_widget(cat_spin)
        form_spin = self.make_spinner(list(all_forms['Kinematics'].keys()))
        layout.add_widget(self.make_label('Formula:'))
        layout.add_widget(form_spin)
        def uf(s,t): form_spin.values=list(all_forms[t].keys());form_spin.text=form_spin.values[0]
        cat_spin.bind(text=uf)
        
        layout.add_widget(self.make_label('Parameters:'))
        params_in = self.make_input('comma separated')
        layout.add_widget(params_in)
        const_spin = self.make_spinner(list(PhysicsEngine.CONSTANTS.keys()))
        layout.add_widget(self.make_label('Constant:'))
        layout.add_widget(const_spin)
        
        btns = GridLayout(cols=2, spacing=dp(3), size_hint_y=None, height=dp(32))
        
        def cp(i):
            try:
                fn=all_forms[cat_spin.text][form_spin.text]
                p=[float(x.strip()) for x in params_in.text.split(',') if x.strip()]
                self.show_result('Physics Result',f'{form_spin.text}\n= {fn(*p)}')
            except: self.show_result('Error','Check formula parameters')
        def sc(i): self.show_result('Physical Constant',f'{const_spin.text} = {PhysicsEngine.get_constant(const_spin.text)}')
        
        btns.add_widget(ColoredButton(text='Calculate', on_press=cp))
        btns.add_widget(ColoredButton(text='Show Constant', on_press=sc))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_chemistry_tab(self):
        tab = TabbedPanelItem(text='Chemistry')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Atomic Number:'))
        at_num = self.make_input('1-118 (e.g. 79)')
        layout.add_widget(at_num)
        layout.add_widget(self.make_label('Search Element:'))
        search_in = self.make_input('name or symbol')
        layout.add_widget(search_in)
        
        btns = GridLayout(cols=2, spacing=dp(3), size_hint_y=None, height=dp(32))
        
        def lu(i):
            try:
                n=int(at_num.text)
                e=ChemistryEngine.get_element(n)
                if e: self.show_result(f'Element #{n}',f'{e["name"]} ({e["symbol"]})\nAtomic Mass: {e["mass"]} g/mol\nGroup: {e["group"]} | Period: {e["period"]}\nElectron Config: {e["config"]}')
                else: self.show_result('Error','Element not found (1-118)')
            except: self.show_result('Error','Enter a valid atomic number')
        def se(i):
            q=search_in.text.strip()
            if q:
                r=ChemistryEngine.search(q)
                if r: self.show_result(f'Search: {q}','\n'.join([f'#{k}: {v["name"]} ({v["symbol"]})' for k,v in list(r.items())[:25]]))
                else: self.show_result('Not Found',f'No elements match "{q}"')
        
        btns.add_widget(ColoredButton(text='Lookup Element', on_press=lu))
        btns.add_widget(ColoredButton(text='Search', on_press=se))
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(btns)
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

    def add_convert_tab(self):
        tab = TabbedPanelItem(text='Convert')
        scroll = ScrollView()
        layout = GridLayout(cols=4, spacing=dp(4), padding=dp(6), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(self.make_label('Value:'))
        val_in = self.make_input('e.g. 100')
        layout.add_widget(val_in)
        layout.add_widget(self.make_label('From Unit:'))
        from_u = self.make_input('cm, C, g, kg')
        layout.add_widget(from_u)
        layout.add_widget(self.make_label('To Unit:'))
        to_u = self.make_input('m, F, pound')
        layout.add_widget(to_u)
        
        def dc(i):
            lm={'cm':0.01,'m':1,'km':1000,'inch':0.0254,'foot':0.3048}
            try:
                v,f,t=float(val_in.text),from_u.text.strip(),to_u.text.strip()
                if f in lm and t in lm: r=v*lm[f]/lm[t]
                elif f=='C' and t=='F': r=v*9/5+32
                elif f=='C' and t=='K': r=v+273.15
                elif f=='F' and t=='C': r=(v-32)*5/9
                elif f=='F' and t=='K': r=(v-32)*5/9+273.15
                elif f=='K' and t=='C': r=v-273.15
                elif f=='K' and t=='F': r=(v-273.15)*9/5+32
                elif f=='g' and t=='kg': r=v/1000
                elif f=='kg' and t=='g': r=v*1000
                elif f=='kg' and t=='pound': r=v*2.20462
                elif f=='pound' and t=='kg': r=v/2.20462
                else: r='Unsupported conversion'
                self.show_result('Unit Conversion',f'{v} {f} = {r} {t}')
            except: self.show_result('Error','Invalid input')
        
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(ColoredButton(text='Convert Unit', on_press=dc))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(size_hint_y=None, height=dp(3)))
        layout.add_widget(Label(text='Length: cm,m,km,in,ft | Temp: C,F,K | Weight: g,kg,lb',color=(0.7,0.7,0.7,1),size_hint_y=None,height=dp(20),font_size=dp(10)))
        
        scroll.add_widget(layout)
        tab.content = scroll
        self.tabs.add_widget(tab)

if __name__ == '__main__':
    OmegaApp().run()