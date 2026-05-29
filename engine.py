# Omega Calculator 11.0 - engine.py (Complete)
# Author: Amirmahdi Ghorbani
import math, cmath, random

class MathEngine:
    @staticmethod
    def make_function(expr):
        ns = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'sqrt': math.sqrt,
              'log': math.log, 'log10': math.log10, 'exp': math.exp, 'abs': abs,
              'pi': math.pi, 'e': math.e, '**': pow}
        e = expr.strip()
        return eval(e if e.startswith('lambda') else f"lambda x: {e}", {"__builtins__": {}}, ns)

    @staticmethod
    def der(expr, x, h=1e-6):
        f = MathEngine.make_function(expr)
        return (f(x + h) - f(x - h)) / (2 * h)

    @staticmethod
    def integral(expr, a, b, n=1000):
        f = MathEngine.make_function(expr)
        if n % 2: n += 1
        h = (b - a) / n
        total = f(a) + f(b)
        for i in range(1, n, 2): total += 4 * f(a + i * h)
        for i in range(2, n - 1, 2): total += 2 * f(a + i * h)
        return (h / 3) * total

    @staticmethod
    def is_prime(n):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0: return False
        return True

    @staticmethod
    def lcm(a, b): return abs(a * b) // math.gcd(int(a), int(b))
    @staticmethod
    def cot(x): return math.cos(x) / math.sin(x)


class EquationEngine:
    @staticmethod
    def solve_quadratic(a, b, c):
        if abs(a) < 1e-12: return None
        delta = b*b - 4*a*c
        if delta < 0: return ("complex", -b/(2*a), math.sqrt(abs(delta))/(2*a))
        if delta == 0: return ("double", -b/(2*a))
        return ("real", (-b+math.sqrt(delta))/(2*a), (-b-math.sqrt(delta))/(2*a))

    @staticmethod
    def solve_cubic(a, b, c, d):
        if abs(a) < 1e-12: return EquationEngine.solve_quadratic(b, c, d)
        p = (3*a*c - b*b) / (3*a*a)
        q = (2*b**3 - 9*a*b*c + 27*a*a*d) / (27*a**3)
        delta = (q/2)**2 + (p/3)**3
        if abs(delta) < 1e-12: delta = 0
        shift = -b/(3*a)
        if delta > 0:
            u = (-q/2 + cmath.sqrt(delta))**(1/3)
            v = (-q/2 - cmath.sqrt(delta))**(1/3)
            w = complex(-0.5, math.sqrt(3)/2)
            w2 = complex(-0.5, -math.sqrt(3)/2)
            return [u+v+shift, w*u+w2*v+shift, w2*u+w*v+shift]
        elif delta < 0:
            r = math.sqrt(-p/3)
            phi = math.acos(3*q/(2*p*r))
            return [2*r*math.cos(phi/3)+shift, 2*r*math.cos((phi+2*math.pi)/3)+shift, 2*r*math.cos((phi+4*math.pi)/3)+shift]
        else:
            y1 = 2*(-q/2)**(1/3); y2 = -(-q/2)**(1/3)
            return [y1+shift, y2+shift, y2+shift]

    @staticmethod
    def solve_polynomial(coeffs):
        degree = len(coeffs) - 1
        def f(x): return sum(c * (x**(degree-i)) for i, c in enumerate(coeffs))
        def df(x): return sum(c*(degree-i)*(x**(degree-i-1)) for i, c in enumerate(coeffs[:-1]))
        roots, bound = [], max(1, sum(abs(c) for c in coeffs)/abs(coeffs[0])) + 1
        for start in range(-int(bound*2), int(bound*2)):
            x = start * 0.5
            for _ in range(50):
                fx, dfx = f(x), df(x)
                if abs(dfx) < 1e-12: break
                x_new = x - fx/dfx
                if abs(x_new-x) < 1e-10:
                    x = round(x_new, 8)
                    if x not in roots and abs(f(x)) < 1e-6: roots.append(x)
                    break
                x = x_new
        return sorted(set(round(r, 4) for r in roots))

    @staticmethod
    def solve_linear_2var(a1, b1, c1, a2, b2, c2):
        det = a1*b2 - a2*b1
        if abs(det) < 1e-12: return None
        return ((c1*b2 - c2*b1)/det, (a1*c2 - a2*c1)/det)

    @staticmethod
    def matrix_op(a, b, op):
        try:
            A = [[float(x) for x in row.split(",")] for row in a.strip().split(";")]
            if op == "det":
                n = len(A)
                if n == 1: return A[0][0]
                if n == 2: return A[0][0]*A[1][1] - A[0][1]*A[1][0]
                if n == 3: return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1]) - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0]) + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
            B = [[float(x) for x in row.split(",")] for row in b.strip().split(";")]
            if op == "add": return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
            if op == "mul": return [[sum(A[i][k]*B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))] for i in range(len(A))]
            if op == "inv":
                det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
                if det == 0: return None
                return [[A[1][1]/det, -A[0][1]/det], [-A[1][0]/det, A[0][0]/det]]
        except: return None


class PhysicsEngine:
    CONSTANTS = {"g": 9.8, "G": 6.674e-11, "c": 3e8, "h": 6.626e-34, "hbar": 1.054e-34, "kB": 1.38e-23, "e": 1.6e-19, "eps0": 8.85e-12, "mu0": 4*math.pi*1e-7, "me": 9.11e-31, "mp": 1.67e-27, "NA": 6.022e23, "R": 8.314, "sigma": 5.67e-8, "Rydberg": 1.097e7, "muB": 9.274e-24, "a0": 5.29e-11}
    KINEMATICS = {"v = v0 + at": lambda v0,a,t: v0+a*t, "x = x0 + v0t + 0.5at^2": lambda x0,v0,a,t: x0+v0*t+0.5*a*t*t, "v^2 = v0^2 + 2ad": lambda v0,a,d: math.sqrt(v0*v0+2*a*d), "v_avg = d / t": lambda d,t: d/t, "Free fall v = gt": lambda t,g=9.8: g*t, "Free fall h = 0.5gt^2": lambda t,g=9.8: 0.5*g*t*t, "Projectile Range": lambda v0,th,g=9.8: v0*v0*math.sin(2*math.radians(th))/g, "Projectile Max H": lambda v0,th,g=9.8: v0*v0*(math.sin(math.radians(th))**2)/(2*g), "Projectile Time": lambda v0,th,g=9.8: 2*v0*math.sin(math.radians(th))/g}
    DYNAMICS = {"F = ma": lambda m,a: m*a, "w = mg": lambda m,g=9.8: m*g, "N on incline": lambda m,ang,g=9.8: m*g*math.cos(math.radians(ang)), "Friction kinetic": lambda mu,N: mu*N, "Friction static max": lambda mu,N: mu*N, "Momentum p = mv": lambda m,v: m*v, "Impulse J = Ft": lambda F,t: F*t, "Hooke F = -kx": lambda k,x: -k*x}
    ENERGY = {"Work W = Fd cos(a)": lambda F,d,a=0: F*d*math.cos(math.radians(a)), "Kinetic Energy": lambda m,v: 0.5*m*v*v, "Gravitational PE": lambda m,h,g=9.8: m*g*h, "Spring PE": lambda k,x: 0.5*k*x*x, "Power avg": lambda W,t: W/t, "Power inst": lambda F,v,a=0: F*v*math.cos(math.radians(a)), "Efficiency": lambda wo,wi: (wo/wi)*100}
    FLUIDS = {"Density": lambda m,V: m/V, "Pressure": lambda F,A: F/A, "Pressure depth": lambda P0,rho,h,g=9.8: P0+rho*g*h, "Buoyant force": lambda rho,V,g=9.8: rho*V*g, "Continuity": lambda A1,v1,A2: A1*v1/A2}
    ELECTRICITY = {"V = IR": lambda I,R: I*R, "I = V/R": lambda V,R: V/R, "R = V/I": lambda V,I: V/I, "P = VI": lambda V,I: V*I, "P = I^2R": lambda I,R: I*I*R, "P = V^2/R": lambda V,R: V*V/R, "Series R": lambda *a: sum(a), "Parallel R": lambda *a: 1/sum(1/r for r in a), "Coulomb": lambda q1,q2,r,k=8.99e9: k*q1*q2/(r*r)}
    HEAT = {"Q = mcT": lambda m,c,dT: m*c*dT, "Q fusion": lambda m,Lf: m*Lf, "Q vapor": lambda m,Lv: m*Lv, "Linear expansion": lambda L0,a,dT: a*L0*dT, "Ideal gas P": lambda n,R,T,V: n*R*T/V, "Ideal gas V": lambda n,R,T,P: n*R*T/P, "First law": lambda Q,W: Q-W, "Engine eff": lambda Qh,Qc: 1-(Qc/Qh)}
    OPTICS = {"Wave speed": lambda f,w: f*w, "Refractive index": lambda c,v: c/v, "Snell angle2": lambda n1,t1,n2: math.degrees(math.asin(n1*math.sin(math.radians(t1))/n2)), "Lens 1/f": lambda p,q: 1/(1/p+1/q), "Magnification": lambda p,q: -q/p, "Critical angle": lambda n1,n2: math.degrees(math.asin(n2/n1))}
    MODERN = {"E = mc^2": lambda m,c=3e8: m*c*c, "Photon E = hf": lambda f,h=6.626e-34: h*f, "Photon E = hc/w": lambda w,h=6.626e-34,c=3e8: h*c/w, "De Broglie": lambda m,v,h=6.626e-34: h/(m*v), "Lorentz": lambda v,c=3e8: 1/math.sqrt(1-v*v/(c*c)), "Time dilation": lambda t0,v,c=3e8: t0/math.sqrt(1-v*v/(c*c)), "Length contraction": lambda L0,v,c=3e8: L0*math.sqrt(1-v*v/(c*c))}

    @classmethod
    def get_all(cls):
        return {"Kinematics": cls.KINEMATICS, "Dynamics": cls.DYNAMICS, "Work & Energy": cls.ENERGY, "Fluids": cls.FLUIDS, "Electricity": cls.ELECTRICITY, "Heat & Thermo": cls.HEAT, "Optics": cls.OPTICS, "Modern Physics": cls.MODERN}

    @classmethod
    def get_constant(cls, name): return cls.CONSTANTS.get(name)


class ChemistryEngine:
    ELEMENTS = {
        1: {"name":"Hydrogen","symbol":"H","mass":1.008,"group":1,"period":1,"config":"1s1"},
        2: {"name":"Helium","symbol":"He","mass":4.0026,"group":18,"period":1,"config":"1s2"},
        3: {"name":"Lithium","symbol":"Li","mass":6.94,"group":1,"period":2,"config":"[He]2s1"},
        4: {"name":"Beryllium","symbol":"Be","mass":9.012,"group":2,"period":2,"config":"[He]2s2"},
        5: {"name":"Boron","symbol":"B","mass":10.81,"group":13,"period":2,"config":"[He]2s2 2p1"},
        6: {"name":"Carbon","symbol":"C","mass":12.011,"group":14,"period":2,"config":"[He]2s2 2p2"},
        7: {"name":"Nitrogen","symbol":"N","mass":14.007,"group":15,"period":2,"config":"[He]2s2 2p3"},
        8: {"name":"Oxygen","symbol":"O","mass":15.999,"group":16,"period":2,"config":"[He]2s2 2p4"},
        9: {"name":"Fluorine","symbol":"F","mass":18.998,"group":17,"period":2,"config":"[He]2s2 2p5"},
        10: {"name":"Neon","symbol":"Ne","mass":20.18,"group":18,"period":2,"config":"[He]2s2 2p6"},
        11: {"name":"Sodium","symbol":"Na","mass":22.99,"group":1,"period":3,"config":"[Ne]3s1"},
        12: {"name":"Magnesium","symbol":"Mg","mass":24.305,"group":2,"period":3,"config":"[Ne]3s2"},
        13: {"name":"Aluminium","symbol":"Al","mass":26.982,"group":13,"period":3,"config":"[Ne]3s2 3p1"},
        14: {"name":"Silicon","symbol":"Si","mass":28.086,"group":14,"period":3,"config":"[Ne]3s2 3p2"},
        15: {"name":"Phosphorus","symbol":"P","mass":30.974,"group":15,"period":3,"config":"[Ne]3s2 3p3"},
        16: {"name":"Sulfur","symbol":"S","mass":32.06,"group":16,"period":3,"config":"[Ne]3s2 3p4"},
        17: {"name":"Chlorine","symbol":"Cl","mass":35.45,"group":17,"period":3,"config":"[Ne]3s2 3p5"},
        18: {"name":"Argon","symbol":"Ar","mass":39.95,"group":18,"period":3,"config":"[Ne]3s2 3p6"},
        19: {"name":"Potassium","symbol":"K","mass":39.098,"group":1,"period":4,"config":"[Ar]4s1"},
        20: {"name":"Calcium","symbol":"Ca","mass":40.078,"group":2,"period":4,"config":"[Ar]4s2"},
        21: {"name":"Scandium","symbol":"Sc","mass":44.956,"group":3,"period":4,"config":"[Ar]3d1 4s2"},
        22: {"name":"Titanium","symbol":"Ti","mass":47.867,"group":4,"period":4,"config":"[Ar]3d2 4s2"},
        23: {"name":"Vanadium","symbol":"V","mass":50.942,"group":5,"period":4,"config":"[Ar]3d3 4s2"},
        24: {"name":"Chromium","symbol":"Cr","mass":51.996,"group":6,"period":4,"config":"[Ar]3d5 4s1"},
        25: {"name":"Manganese","symbol":"Mn","mass":54.938,"group":7,"period":4,"config":"[Ar]3d5 4s2"},
        26: {"name":"Iron","symbol":"Fe","mass":55.845,"group":8,"period":4,"config":"[Ar]3d6 4s2"},
        27: {"name":"Cobalt","symbol":"Co","mass":58.933,"group":9,"period":4,"config":"[Ar]3d7 4s2"},
        28: {"name":"Nickel","symbol":"Ni","mass":58.693,"group":10,"period":4,"config":"[Ar]3d8 4s2"},
        29: {"name":"Copper","symbol":"Cu","mass":63.546,"group":11,"period":4,"config":"[Ar]3d10 4s1"},
        30: {"name":"Zinc","symbol":"Zn","mass":65.38,"group":12,"period":4,"config":"[Ar]3d10 4s2"},
        31: {"name":"Gallium","symbol":"Ga","mass":69.723,"group":13,"period":4,"config":"[Ar]3d10 4s2 4p1"},
        32: {"name":"Germanium","symbol":"Ge","mass":72.63,"group":14,"period":4,"config":"[Ar]3d10 4s2 4p2"},
        33: {"name":"Arsenic","symbol":"As","mass":74.922,"group":15,"period":4,"config":"[Ar]3d10 4s2 4p3"},
        34: {"name":"Selenium","symbol":"Se","mass":78.96,"group":16,"period":4,"config":"[Ar]3d10 4s2 4p4"},
        35: {"name":"Bromine","symbol":"Br","mass":79.904,"group":17,"period":4,"config":"[Ar]3d10 4s2 4p5"},
        36: {"name":"Krypton","symbol":"Kr","mass":83.798,"group":18,"period":4,"config":"[Ar]3d10 4s2 4p6"},
        37: {"name":"Rubidium","symbol":"Rb","mass":85.468,"group":1,"period":5,"config":"[Kr]5s1"},
        38: {"name":"Strontium","symbol":"Sr","mass":87.62,"group":2,"period":5,"config":"[Kr]5s2"},
        39: {"name":"Yttrium","symbol":"Y","mass":88.906,"group":3,"period":5,"config":"[Kr]4d1 5s2"},
        40: {"name":"Zirconium","symbol":"Zr","mass":91.224,"group":4,"period":5,"config":"[Kr]4d2 5s2"},
        41: {"name":"Niobium","symbol":"Nb","mass":92.906,"group":5,"period":5,"config":"[Kr]4d4 5s1"},
        42: {"name":"Molybdenum","symbol":"Mo","mass":95.95,"group":6,"period":5,"config":"[Kr]4d5 5s1"},
        43: {"name":"Technetium","symbol":"Tc","mass":98,"group":7,"period":5,"config":"[Kr]4d5 5s2"},
        44: {"name":"Ruthenium","symbol":"Ru","mass":101.07,"group":8,"period":5,"config":"[Kr]4d7 5s1"},
        45: {"name":"Rhodium","symbol":"Rh","mass":102.91,"group":9,"period":5,"config":"[Kr]4d8 5s1"},
        46: {"name":"Palladium","symbol":"Pd","mass":106.42,"group":10,"period":5,"config":"[Kr]4d10"},
        47: {"name":"Silver","symbol":"Ag","mass":107.87,"group":11,"period":5,"config":"[Kr]4d10 5s1"},
        48: {"name":"Cadmium","symbol":"Cd","mass":112.41,"group":12,"period":5,"config":"[Kr]4d10 5s2"},
        49: {"name":"Indium","symbol":"In","mass":114.82,"group":13,"period":5,"config":"[Kr]4d10 5s2 5p1"},
        50: {"name":"Tin","symbol":"Sn","mass":118.71,"group":14,"period":5,"config":"[Kr]4d10 5s2 5p2"},
        51: {"name":"Antimony","symbol":"Sb","mass":121.76,"group":15,"period":5,"config":"[Kr]4d10 5s2 5p3"},
        52: {"name":"Tellurium","symbol":"Te","mass":127.6,"group":16,"period":5,"config":"[Kr]4d10 5s2 5p4"},
        53: {"name":"Iodine","symbol":"I","mass":126.9,"group":17,"period":5,"config":"[Kr]4d10 5s2 5p5"},
        54: {"name":"Xenon","symbol":"Xe","mass":131.29,"group":18,"period":5,"config":"[Kr]4d10 5s2 5p6"},
        55: {"name":"Caesium","symbol":"Cs","mass":132.91,"group":1,"period":6,"config":"[Xe]6s1"},
        56: {"name":"Barium","symbol":"Ba","mass":137.33,"group":2,"period":6,"config":"[Xe]6s2"},
        57: {"name":"Lanthanum","symbol":"La","mass":138.91,"group":3,"period":6,"config":"[Xe]5d1 6s2"},
        58: {"name":"Cerium","symbol":"Ce","mass":140.12,"group":3,"period":6,"config":"[Xe]4f1 5d1 6s2"},
        59: {"name":"Praseodymium","symbol":"Pr","mass":140.91,"group":3,"period":6,"config":"[Xe]4f3 6s2"},
        60: {"name":"Neodymium","symbol":"Nd","mass":144.24,"group":3,"period":6,"config":"[Xe]4f4 6s2"},
        61: {"name":"Promethium","symbol":"Pm","mass":145,"group":3,"period":6,"config":"[Xe]4f5 6s2"},
        62: {"name":"Samarium","symbol":"Sm","mass":150.36,"group":3,"period":6,"config":"[Xe]4f6 6s2"},
        63: {"name":"Europium","symbol":"Eu","mass":151.96,"group":3,"period":6,"config":"[Xe]4f7 6s2"},
        64: {"name":"Gadolinium","symbol":"Gd","mass":157.25,"group":3,"period":6,"config":"[Xe]4f7 5d1 6s2"},
        65: {"name":"Terbium","symbol":"Tb","mass":158.93,"group":3,"period":6,"config":"[Xe]4f9 6s2"},
        66: {"name":"Dysprosium","symbol":"Dy","mass":162.5,"group":3,"period":6,"config":"[Xe]4f10 6s2"},
        67: {"name":"Holmium","symbol":"Ho","mass":164.93,"group":3,"period":6,"config":"[Xe]4f11 6s2"},
        68: {"name":"Erbium","symbol":"Er","mass":167.26,"group":3,"period":6,"config":"[Xe]4f12 6s2"},
        69: {"name":"Thulium","symbol":"Tm","mass":168.93,"group":3,"period":6,"config":"[Xe]4f13 6s2"},
        70: {"name":"Ytterbium","symbol":"Yb","mass":173.04,"group":3,"period":6,"config":"[Xe]4f14 6s2"},
        71: {"name":"Lutetium","symbol":"Lu","mass":174.97,"group":3,"period":6,"config":"[Xe]4f14 5d1 6s2"},
        72: {"name":"Hafnium","symbol":"Hf","mass":178.49,"group":4,"period":6,"config":"[Xe]4f14 5d2 6s2"},
        73: {"name":"Tantalum","symbol":"Ta","mass":180.95,"group":5,"period":6,"config":"[Xe]4f14 5d3 6s2"},
        74: {"name":"Tungsten","symbol":"W","mass":183.84,"group":6,"period":6,"config":"[Xe]4f14 5d4 6s2"},
        75: {"name":"Rhenium","symbol":"Re","mass":186.21,"group":7,"period":6,"config":"[Xe]4f14 5d5 6s2"},
        76: {"name":"Osmium","symbol":"Os","mass":190.23,"group":8,"period":6,"config":"[Xe]4f14 5d6 6s2"},
        77: {"name":"Iridium","symbol":"Ir","mass":192.22,"group":9,"period":6,"config":"[Xe]4f14 5d7 6s2"},
        78: {"name":"Platinum","symbol":"Pt","mass":195.08,"group":10,"period":6,"config":"[Xe]4f14 5d9 6s1"},
        79: {"name":"Gold","symbol":"Au","mass":196.97,"group":11,"period":6,"config":"[Xe]4f14 5d10 6s1"},
        80: {"name":"Mercury","symbol":"Hg","mass":200.59,"group":12,"period":6,"config":"[Xe]4f14 5d10 6s2"},
        81: {"name":"Thallium","symbol":"Tl","mass":204.38,"group":13,"period":6,"config":"[Xe]4f14 5d10 6s2 6p1"},
        82: {"name":"Lead","symbol":"Pb","mass":207.2,"group":14,"period":6,"config":"[Xe]4f14 5d10 6s2 6p2"},
        83: {"name":"Bismuth","symbol":"Bi","mass":208.98,"group":15,"period":6,"config":"[Xe]4f14 5d10 6s2 6p3"},
        84: {"name":"Polonium","symbol":"Po","mass":209,"group":16,"period":6,"config":"[Xe]4f14 5d10 6s2 6p4"},
        85: {"name":"Astatine","symbol":"At","mass":210,"group":17,"period":6,"config":"[Xe]4f14 5d10 6s2 6p5"},
        86: {"name":"Radon","symbol":"Rn","mass":222,"group":18,"period":6,"config":"[Xe]4f14 5d10 6s2 6p6"},
        87: {"name":"Francium","symbol":"Fr","mass":223,"group":1,"period":7,"config":"[Rn]7s1"},
        88: {"name":"Radium","symbol":"Ra","mass":226,"group":2,"period":7,"config":"[Rn]7s2"},
        89: {"name":"Actinium","symbol":"Ac","mass":227,"group":3,"period":7,"config":"[Rn]6d1 7s2"},
        90: {"name":"Thorium","symbol":"Th","mass":232.04,"group":3,"period":7,"config":"[Rn]6d2 7s2"},
        91: {"name":"Protactinium","symbol":"Pa","mass":231.04,"group":3,"period":7,"config":"[Rn]5f2 6d1 7s2"},
        92: {"name":"Uranium","symbol":"U","mass":238.03,"group":3,"period":7,"config":"[Rn]5f3 6d1 7s2"},
        93: {"name":"Neptunium","symbol":"Np","mass":237,"group":3,"period":7,"config":"[Rn]5f4 6d1 7s2"},
        94: {"name":"Plutonium","symbol":"Pu","mass":244,"group":3,"period":7,"config":"[Rn]5f6 7s2"},
        95: {"name":"Americium","symbol":"Am","mass":243,"group":3,"period":7,"config":"[Rn]5f7 7s2"},
        96: {"name":"Curium","symbol":"Cm","mass":247,"group":3,"period":7,"config":"[Rn]5f7 6d1 7s2"},
        97: {"name":"Berkelium","symbol":"Bk","mass":247,"group":3,"period":7,"config":"[Rn]5f9 7s2"},
        98: {"name":"Californium","symbol":"Cf","mass":251,"group":3,"period":7,"config":"[Rn]5f10 7s2"},
        99: {"name":"Einsteinium","symbol":"Es","mass":252,"group":3,"period":7,"config":"[Rn]5f11 7s2"},
        100: {"name":"Fermium","symbol":"Fm","mass":257,"group":3,"period":7,"config":"[Rn]5f12 7s2"},
        101: {"name":"Mendelevium","symbol":"Md","mass":258,"group":3,"period":7,"config":"[Rn]5f13 7s2"},
        102: {"name":"Nobelium","symbol":"No","mass":259,"group":3,"period":7,"config":"[Rn]5f14 7s2"},
        103: {"name":"Lawrencium","symbol":"Lr","mass":262,"group":3,"period":7,"config":"[Rn]5f14 7s2 7p1"},
        104: {"name":"Rutherfordium","symbol":"Rf","mass":267,"group":4,"period":7,"config":"[Rn]5f14 6d2 7s2"},
        105: {"name":"Dubnium","symbol":"Db","mass":268,"group":5,"period":7,"config":"[Rn]5f14 6d3 7s2"},
        106: {"name":"Seaborgium","symbol":"Sg","mass":269,"group":6,"period":7,"config":"[Rn]5f14 6d4 7s2"},
        107: {"name":"Bohrium","symbol":"Bh","mass":270,"group":7,"period":7,"config":"[Rn]5f14 6d5 7s2"},
        108: {"name":"Hassium","symbol":"Hs","mass":277,"group":8,"period":7,"config":"[Rn]5f14 6d6 7s2"},
        109: {"name":"Meitnerium","symbol":"Mt","mass":278,"group":9,"period":7,"config":"[Rn]5f14 6d7 7s2"},
        110: {"name":"Darmstadtium","symbol":"Ds","mass":281,"group":10,"period":7,"config":"[Rn]5f14 6d8 7s2"},
        111: {"name":"Roentgenium","symbol":"Rg","mass":282,"group":11,"period":7,"config":"[Rn]5f14 6d9 7s2"},
        112: {"name":"Copernicium","symbol":"Cn","mass":285,"group":12,"period":7,"config":"[Rn]5f14 6d10 7s2"},
        113: {"name":"Nihonium","symbol":"Nh","mass":286,"group":13,"period":7,"config":"[Rn]5f14 6d10 7s2 7p1"},
        114: {"name":"Flerovium","symbol":"Fl","mass":289,"group":14,"period":7,"config":"[Rn]5f14 6d10 7s2 7p2"},
        115: {"name":"Moscovium","symbol":"Mc","mass":290,"group":15,"period":7,"config":"[Rn]5f14 6d10 7s2 7p3"},
        116: {"name":"Livermorium","symbol":"Lv","mass":293,"group":16,"period":7,"config":"[Rn]5f14 6d10 7s2 7p4"},
        117: {"name":"Tennessine","symbol":"Ts","mass":294,"group":17,"period":7,"config":"[Rn]5f14 6d10 7s2 7p5"},
        118: {"name":"Oganesson","symbol":"Og","mass":294,"group":18,"period":7,"config":"[Rn]5f14 6d10 7s2 7p6"},
    }

    @classmethod
    def get_element(cls, num): return cls.ELEMENTS.get(num)

    @classmethod
    def search(cls, query):
        q = query.lower()
        return {k:v for k,v in cls.ELEMENTS.items() if q in v["name"].lower() or q in v["symbol"].lower()}


class StatisticsEngine:
    @staticmethod
    def mean(data): return sum(data)/len(data) if data else 0
    @staticmethod
    def median(data):
        s = sorted(data); n = len(s)
        if n == 0: return 0
        return s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2
    @staticmethod
    def mode(data):
        freq = {}
        for d in data: freq[d] = freq.get(d, 0) + 1
        mx = max(freq.values())
        return [k for k,v in freq.items() if v == mx]
    @staticmethod
    def random_dist(dist_type, params):
        try:
            if dist_type == "uniform": return random.uniform(float(params[0]), float(params[1]))
            if dist_type == "normal": return random.gauss(float(params[0]), float(params[1]))
            if dist_type == "exponential": return random.expovariate(float(params[0]))
            if dist_type == "triangular": return random.triangular(float(params[0]), float(params[1]), float(params[2]))
        except: return None