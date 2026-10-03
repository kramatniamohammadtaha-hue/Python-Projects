import ast
import json
import math
import operator
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


class SafeMath:
    OPS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod,
    }
    FUNCS = {
        "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
        "abs": abs, "floor": math.floor, "ceil": math.ceil,
        "exp": math.exp, "factorial": math.factorial,
    }

    def __init__(self, angle="DEG"):
        self.angle = angle

    def calc(self, text):
        text = text.replace("×", "*").replace("÷", "/").replace("^", "**")
        return self.visit(ast.parse(text, mode="eval").body)

    def visit(self, n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in self.OPS:
            a, b = self.visit(n.left), self.visit(n.right)
            if isinstance(n.op, ast.Pow) and abs(b) > 100:
                raise ValueError
            return self.OPS[type(n.op)](a, b)
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            return +self.visit(n.operand) if isinstance(n.op, ast.UAdd) else -self.visit(n.operand)
        if isinstance(n, ast.Name):
            if n.id == "pi": return math.pi
            if n.id == "e": return math.e
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            name = n.func.id
            if len(n.args) != 1: raise ValueError
            x = self.visit(n.args[0])
            if name in ("sin", "cos", "tan"):
                x = math.radians(x) if self.angle == "DEG" else x
                return getattr(math, name)(x)
            if name in ("asin", "acos", "atan"):
                r = getattr(math, name)(x)
                return math.degrees(r) if self.angle == "DEG" else r
            if name in self.FUNCS: return self.FUNCS[name](x)
        raise ValueError("Invalid expression")


class Calculator:
    DARK = {"bg":"#0b1120","card":"#111827","display":"#020617",
            "button":"#1e293b","hover":"#334155","text":"#f8fafc",
            "muted":"#94a3b8"}
    LIGHT = {"bg":"#f1f5f9","card":"#ffffff","display":"#e2e8f0",
             "button":"#e2e8f0","hover":"#cbd5e1","text":"#0f172a",
             "muted":"#475569"}

    def __init__(self, root):
        self.root = root
        self.root.title("ProCalc — Professional Calculator")
        self.root.geometry("1050x680")
        self.root.minsize(850, 580)

        self.file = Path(__file__).with_name("settings.json")
        self.settings = self.load()
        self.lang = self.settings.get("language", "en")
        self.theme = self.settings.get("theme", "dark")
        self.angle = self.settings.get("angle", "DEG")
        self.history = self.settings.get("history", [])
        self.memory = 0
        self.just_calculated = False
        self.expr = tk.StringVar()
        self.answer = tk.StringVar(value="0")
        self.status = tk.StringVar()

        self.words = {
            "en":{"title":"Professional Calculator","history":"History",
                  "clear":"Clear History","ready":"Ready","error":"Invalid expression",
                  "zero":"Cannot divide by zero","about":"ProCalc",
                  "about_text":"A modern scientific calculator built with Python and Tkinter.",
                  "copied":"Result copied","lang":"FA"},
            "fa":{"title":"ماشین حساب حرفه‌ای","history":"تاریخچه",
                  "clear":"پاک کردن تاریخچه","ready":"آماده","error":"عبارت نامعتبر است",
                  "zero":"تقسیم بر صفر امکان‌پذیر نیست","about":"ProCalc",
                  "about_text":"یک ماشین حساب علمی مدرن ساخته شده با Python و Tkinter.",
                  "copied":"نتیجه کپی شد","lang":"EN"}
        }
        self.engine = SafeMath(self.angle)
        self.build()
        self.apply_theme()
        self.apply_language()
        self.bind_keys()

    def load(self):
        try:
            return json.loads(self.file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def save(self):
        data = {"language":self.lang,"theme":self.theme,"angle":self.angle,
                "history":self.history[-50:]}
        try: self.file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError: pass

    def t(self, key):
        return self.words[self.lang][key]

    def build(self):
        self.root.configure(bg=self.DARK["bg"])
        self.main = tk.Frame(self.root); self.main.pack(fill="both", expand=True, padx=18, pady=18)

        head = tk.Frame(self.main); head.pack(fill="x", pady=(0,12))
        self.title = tk.Label(head, text="ProCalc", font=("Segoe UI",24,"bold"))
        self.title.pack(side="left")
        self.subtitle = tk.Label(head, font=("Segoe UI",10))
        self.subtitle.pack(side="left", padx=12, pady=10)

        tools = tk.Frame(head); tools.pack(side="right")
        self.lang_btn = self.small_btn(tools, "FA", self.toggle_lang); self.lang_btn.pack(side="left", padx=3)
        self.theme_btn = self.small_btn(tools, "☼", self.toggle_theme); self.theme_btn.pack(side="left", padx=3)
        self.angle_btn = self.small_btn(tools, "DEG", self.toggle_angle); self.angle_btn.pack(side="left", padx=3)
        self.about_btn = self.small_btn(tools, "?", self.about); self.about_btn.pack(side="left", padx=3)

        body = tk.Frame(self.main); body.pack(fill="both", expand=True)
        self.card = tk.Frame(body, highlightthickness=1); self.card.pack(side="left", fill="both", expand=True, padx=(0,10))
        self.side = tk.Frame(body, width=290, highlightthickness=1); self.side.pack(side="right", fill="y"); self.side.pack_propagate(False)

        self.display = tk.Frame(self.card); self.display.pack(fill="x", padx=14, pady=14)
        self.expr_label = tk.Label(self.display, textvariable=self.expr, font=("Consolas",14), anchor="e", pady=10)
        self.expr_label.pack(fill="x")
        self.answer_label = tk.Label(self.display, textvariable=self.answer, font=("Segoe UI",34,"bold"), anchor="e", pady=12)
        self.answer_label.pack(fill="x")

        self.status_label = tk.Label(self.card, textvariable=self.status, font=("Segoe UI",9), anchor="w")
        self.status_label.pack(fill="x", padx=18)

        self.grid = tk.Frame(self.card); self.grid.pack(fill="both", expand=True, padx=12, pady=12)
        for c in range(6): self.grid.columnconfigure(c, weight=1)
        for r in range(7): self.grid.rowconfigure(r, weight=1)

        buttons = [
            ("MC",self.mc),("MR",self.mr),("M+",self.mp),("M-",self.mm),("MS",self.ms),("⌫",self.back),
            ("(",lambda:self.add("(")),(")",lambda:self.add(")")),("%",self.percent),("AC",self.clear),("CE",self.clear),("÷",lambda:self.add("÷")),
            ("sin",lambda:self.add("sin(")),("cos",lambda:self.add("cos(")),("tan",lambda:self.add("tan(")),("√",lambda:self.add("sqrt(")),("x²",self.square),("×",lambda:self.add("×")),
            ("asin",lambda:self.add("asin(")),("acos",lambda:self.add("acos(")),("atan",lambda:self.add("atan(")),("log",lambda:self.add("log(")),("ln",lambda:self.add("ln(")),("−",lambda:self.add("-")),
            ("7",lambda:self.add("7")),("8",lambda:self.add("8")),("9",lambda:self.add("9")),("π",lambda:self.add("pi")),("e",lambda:self.add("e")),("+",lambda:self.add("+")),
            ("4",lambda:self.add("4")),("5",lambda:self.add("5")),("6",lambda:self.add("6")),("^",lambda:self.add("^")),("!",self.fact),("=",self.calculate),
            ("1",lambda:self.add("1")),("2",lambda:self.add("2")),("3",lambda:self.add("3")),(".",lambda:self.add(".")),("0",lambda:self.add("0")),("00",lambda:self.add("00"))
        ]
        self.buttons={}
        for i,(label,cmd) in enumerate(buttons):
            b=tk.Button(self.grid,text=label,command=cmd,font=("Segoe UI",11,"bold"),relief="flat",bd=0,cursor="hand2")
            b.grid(row=i//6,column=i%6,sticky="nsew",padx=4,pady=4)
            self.buttons[label]=b

        self.side_title=tk.Label(self.side,font=("Segoe UI",15,"bold")); self.side_title.pack(anchor="w",padx=16,pady=(18,8))
        self.list=tk.Listbox(self.side,font=("Consolas",10),borderwidth=0,highlightthickness=0,activestyle="none")
        self.list.pack(fill="both",expand=True,padx=12,pady=5)
        self.list.bind("<Double-Button-1>",self.use_history)
        self.clear_history=self.small_btn(self.side,"Clear",self.erase_history); self.clear_history.pack(pady=10)
        self.mem_label=tk.Label(self.side,font=("Consolas",10)); self.mem_label.pack(pady=(0,15))
        self.refresh_history()

    def small_btn(self,parent,text,cmd):
        return tk.Button(parent,text=text,command=cmd,font=("Segoe UI",10,"bold"),relief="flat",bd=0,cursor="hand2")

    def apply_theme(self):
        c=self.DARK if self.theme=="dark" else self.LIGHT
        for w in [self.root,self.main,self.grid]: w.configure(bg=c["bg"] if w!=self.grid else c["card"])
        self.card.configure(bg=c["card"],highlightbackground="#243244")
        self.side.configure(bg=c["card"],highlightbackground="#243244")
        self.display.configure(bg=c["display"])
        self.expr_label.configure(bg=c["display"],fg=c["muted"])
        self.answer_label.configure(bg=c["display"],fg=c["text"])
        self.title.configure(bg=c["bg"],fg=c["text"])
        self.subtitle.configure(bg=c["bg"],fg=c["muted"])
        self.status_label.configure(bg=c["card"],fg=c["muted"])
        self.side_title.configure(bg=c["card"],fg=c["text"])
        self.mem_label.configure(bg=c["card"],fg=c["muted"])
        self.list.configure(bg=c["display"],fg=c["text"],selectbackground="#0284c7")
        for b in [self.lang_btn,self.theme_btn,self.angle_btn,self.about_btn,self.clear_history]:
            b.configure(bg=c["button"],fg=c["text"],activebackground=c["hover"],activeforeground=c["text"])
        for label,b in self.buttons.items():
            if label=="=": bg,fg="#0284c7","white"
            elif label in ("AC","CE","⌫"): bg,fg=c["button"],"#ef4444"
            elif label in ("÷","×","−","+"): bg,fg=c["button"],"#38bdf8"
            elif label in ("MC","MR","M+","M-","MS"): bg,fg=c["button"],c["muted"]
            elif label in ("sin","cos","tan","asin","acos","atan","log","ln","√","x²","π","e","^","!"): bg,fg=c["button"],"#38bdf8"
            else: bg,fg=c["button"],c["text"]
            b.configure(bg=bg,fg=fg,activebackground=c["hover"],activeforeground=c["text"])

    def apply_language(self):
        self.subtitle.configure(text=self.t("title"))
        self.side_title.configure(text=self.t("history"))
        self.clear_history.configure(text=self.t("clear"))
        self.lang_btn.configure(text=self.t("lang"))
        self.angle_btn.configure(text=self.angle)
        self.status.set(self.t("ready"))
        self.refresh_history()

    def toggle_lang(self):
        self.lang="fa" if self.lang=="en" else "en"; self.save(); self.apply_language()

    def toggle_theme(self):
        self.theme="light" if self.theme=="dark" else "dark"; self.save(); self.apply_theme()

    def toggle_angle(self):
        self.angle="RAD" if self.angle=="DEG" else "DEG"
        self.engine.angle=self.angle; self.angle_btn.configure(text=self.angle); self.save()

    def add(self,x):
        if self.just_calculated and x not in "+-×÷^":
            self.expr.set("")
        self.just_calculated=False
        self.expr.set(self.expr.get()+x)
        self.answer.set("0")

    def clear(self):
        self.expr.set(""); self.answer.set("0"); self.just_calculated=False

    def back(self):
        self.expr.set(self.expr.get()[:-1])

    def calculate(self,event=None):
        s=self.expr.get().strip()
        if not s:return
        try:
            value=self.engine.calc(s)
            result=self.format(value)
            self.answer.set(result); self.just_calculated=True
            self.history.append([s,result]); self.history=self.history[-50:]
            self.refresh_history(); self.save()
        except ZeroDivisionError:
            self.answer.set("Error"); self.status.set(self.t("zero"))
        except Exception:
            self.answer.set("Error"); self.status.set(self.t("error"))

    def format(self,x):
        if isinstance(x,float) and x.is_integer(): return str(int(x))
        if abs(x)>=1e12 or (0<abs(x)<1e-8): return f"{x:.10e}"
        return f"{x:.12g}"

    def percent(self):
        try:
            x=self.engine.calc(self.expr.get())/100
            self.expr.set(self.format(x)); self.answer.set(self.format(x))
        except Exception:self.answer.set("Error")

    def square(self):
        if self.expr.get(): self.expr.set(f"({self.expr.get()})^2"); self.calculate()

    def fact(self):
        try:
            x=self.engine.calc(self.expr.get())
            if x<0 or x!=int(x) or x>170: raise ValueError
            r=math.factorial(int(x)); self.expr.set(f"factorial({int(x)})"); self.answer.set(self.format(r))
        except Exception:self.answer.set("Error")

    def value(self):
        try:return self.engine.calc(self.expr.get())
        except Exception:return None

    def mc(self): self.memory=0; self.mem_label.configure(text="M = 0")
    def mr(self): self.add(self.format(self.memory))
    def ms(self):
        x=self.value()
        if x is not None:self.memory=x; self.mem_label.configure(text=f"M = {self.format(x)}")
    def mp(self):
        x=self.value()
        if x is not None:self.memory+=x; self.mem_label.configure(text=f"M = {self.format(self.memory)}")
    def mm(self):
        x=self.value()
        if x is not None:self.memory-=x; self.mem_label.configure(text=f"M = {self.format(self.memory)}")

    def refresh_history(self):
        self.list.delete(0,tk.END)
        if not self.history:self.list.insert(tk.END,"No calculations yet"); return
        for e,r in reversed(self.history):self.list.insert(tk.END,f"{e} = {r}")

    def use_history(self,event=None):
        sel=self.list.curselection()
        if sel and self.history:
            e,r=list(reversed(self.history))[sel[0]]
            self.expr.set(e); self.answer.set(r); self.just_calculated=True

    def erase_history(self):
        self.history=[]; self.refresh_history(); self.save()

    def copy(self):
        if self.answer.get()!="Error":
            self.root.clipboard_clear(); self.root.clipboard_append(self.answer.get())
            self.status.set(self.t("copied"))

    def about(self):
        messagebox.showinfo(self.t("about"),self.t("about_text"))

    def bind_keys(self):
        self.root.bind("<Return>",self.calculate); self.root.bind("<KP_Enter>",self.calculate)
        self.root.bind("<BackSpace>",lambda e:self.back()); self.root.bind("<Escape>",lambda e:self.clear())
        self.root.bind("<Control-c>",lambda e:self.copy())
        for k in "0123456789.": self.root.bind(k,lambda e,x=k:self.add(x))
        self.root.bind("+",lambda e:self.add("+")); self.root.bind("-",lambda e:self.add("-"))
        self.root.bind("*",lambda e:self.add("×")); self.root.bind("/",lambda e:self.add("÷"))
        self.root.bind("^",lambda e:self.add("^"))


if __name__ == "__main__":
    root=tk.Tk()
    Calculator(root)
    root.mainloop()
