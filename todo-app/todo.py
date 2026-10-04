import customtkinter as ctk
import json
import uuid
from datetime import datetime, date
from pathlib import Path

class TodoApp(ctk.CTk):
    DATA = Path(__file__).with_name("tasks.json")
    SETTINGS = Path(__file__).with_name("settings.json")

    T = {
        "en": {"title":"TaskFlow","sub":"Professional Task Manager","add":"Add Task","search":"Search tasks...",
               "all":"All","active":"Active","done":"Completed","overdue":"Overdue","today":"Today",
               "clear":"Clear completed","lang":"فارسی","light":"Light","dark":"Dark","save":"Save Task",
               "cancel":"Cancel","edit":"Edit","delete":"Delete","yes":"Delete","no":"Cancel",
               "required":"Task title is required.","stats":"Total: {t}  •  Done: {d}  •  Remaining: {r}",
               "empty":"No tasks found","priority":"Priority","category":"Category","due":"Due date",
               "description":"Description","low":"Low","medium":"Medium","high":"High",
               "work":"Work","study":"Study","personal":"Personal","shopping":"Shopping","other":"Other",
               "newest":"Newest","oldest":"Oldest","priority_sort":"Priority","due_sort":"Due date",
               "deleted":"Task deleted","added":"Task added","updated":"Task updated"},
        "fa": {"title":"تسک‌فلو","sub":"مدیریت حرفه‌ای وظایف","add":"افزودن وظیفه","search":"جستجوی وظایف...",
               "all":"همه","active":"در حال انجام","done":"تکمیل‌شده","overdue":"عقب‌افتاده","today":"امروز",
               "clear":"پاک‌کردن تکمیل‌شده‌ها","lang":"English","light":"روشن","dark":"تیره","save":"ذخیره وظیفه",
               "cancel":"لغو","edit":"ویرایش","delete":"حذف","yes":"حذف","no":"لغو",
               "required":"عنوان وظیفه الزامی است.","stats":"کل: {t}  •  انجام‌شده: {d}  •  باقی‌مانده: {r}",
               "empty":"وظیفه‌ای پیدا نشد","priority":"اولویت","category":"دسته‌بندی","due":"تاریخ سررسید",
               "description":"توضیحات","low":"کم","medium":"متوسط","high":"زیاد",
               "work":"کار","study":"تحصیل","personal":"شخصی","shopping":"خرید","other":"سایر",
               "newest":"جدیدترین","oldest":"قدیمی‌ترین","priority_sort":"اولویت","due_sort":"سررسید",
               "deleted":"وظیفه حذف شد","added":"وظیفه اضافه شد","updated":"وظیفه ویرایش شد"}
    }

    def __init__(self):
        super().__init__()
        s = self.load(self.SETTINGS, {})
        self.lang = s.get("language", "en")
        self.theme = s.get("theme", "dark")
        self.sort = s.get("sort", "newest")
        self.tasks = self.load(self.DATA, [])
        self.filter = "all"
        self.query = ""
        self.edit_id = None
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode(self.theme)
        self.title("TaskFlow")
        self.geometry("1180x760")
        self.minsize(900, 620)
        self.build()
        self.apply_language()
        self.refresh()

    @property
    def t(self): return self.T[self.lang]

    @property
    def c(self):
        return {"window":"#0b1120","panel":"#101827","card":"#111a2d","input":"#0e1728",
                "border":"#293750","text":"#f5f7fb","muted":"#8b98ad","secondary":"#263247",
                "hover":"#34425a","accent":"#3b82f6","danger":"#ef4444","success":"#22c55e",
                "warning":"#f59e0b"} if self.theme=="dark" else                {"window":"#eef3f8","panel":"#ffffff","card":"#ffffff","input":"#f8fafc",
                "border":"#cbd5e1","text":"#172033","muted":"#64748b","secondary":"#dbe4ef",
                "hover":"#cbd8e6","accent":"#2563eb","danger":"#dc2626","success":"#16a34a",
                "warning":"#d97706"}

    def load(self,p,default):
        try: return json.loads(p.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError): return default

    def save(self,p,data):
        try: p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
        except OSError: pass

    def save_state(self):
        self.save(self.SETTINGS,{"language":self.lang,"theme":self.theme,"sort":self.sort})

    def build(self):
        c=self.c
        self.grid_columnconfigure(0,weight=0); self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(0,weight=1)
        self.side=ctk.CTkFrame(self,width=255,corner_radius=0,fg_color=c["panel"]); self.side.grid(row=0,column=0,sticky="nsew"); self.side.grid_propagate(False)
        self.logo=ctk.CTkLabel(self.side,text="✓  TaskFlow",font=ctk.CTkFont(size=25,weight="bold"),text_color=c["text"]); self.logo.pack(anchor="w",padx=24,pady=(28,3))
        self.sub=ctk.CTkLabel(self.side,text="",text_color=c["muted"]); self.sub.pack(anchor="w",padx=26,pady=(0,25))
        self.nav={}
        for k in ["all","active","done","overdue","today"]:
            b=ctk.CTkButton(self.side,text="",height=42,corner_radius=10,anchor="w",fg_color="transparent",hover_color=c["secondary"],text_color=c["text"],command=lambda x=k:self.set_filter(x))
            b.pack(fill="x",padx=16,pady=3); self.nav[k]=b
        self.side_space=ctk.CTkFrame(self.side,fg_color="transparent"); self.side_space.pack(fill="both",expand=True)
        self.prog_text=ctk.CTkLabel(self.side,text="",text_color=c["muted"]); self.prog_text.pack(anchor="w",padx=24,pady=(0,6))
        self.prog=ctk.CTkProgressBar(self.side,height=8,progress_color=c["accent"],fg_color=c["secondary"]); self.prog.pack(fill="x",padx=24,pady=(0,20)); self.prog.set(0)
        self.lang_btn=ctk.CTkButton(self.side,text="",height=40,fg_color=c["secondary"],hover_color=c["hover"],text_color=c["text"],command=self.toggle_language); self.lang_btn.pack(fill="x",padx=20,pady=4)
        self.theme_btn=ctk.CTkButton(self.side,text="",height=40,fg_color=c["secondary"],hover_color=c["hover"],text_color=c["text"],command=self.toggle_theme); self.theme_btn.pack(fill="x",padx=20,pady=(4,20))

        self.main=ctk.CTkFrame(self,corner_radius=0,fg_color=c["window"]); self.main.grid(row=0,column=1,sticky="nsew")
        self.main.grid_columnconfigure(0,weight=1); self.main.grid_rowconfigure(2,weight=1)
        head=ctk.CTkFrame(self.main,fg_color="transparent"); head.grid(row=0,column=0,sticky="ew",padx=30,pady=(28,12)); head.grid_columnconfigure(0,weight=1)
        self.title_lbl=ctk.CTkLabel(head,text="",font=ctk.CTkFont(size=28,weight="bold"),text_color=c["text"]); self.title_lbl.grid(row=0,column=0,sticky="w")
        self.stats=ctk.CTkLabel(head,text="",text_color=c["muted"]); self.stats.grid(row=1,column=0,sticky="w")
        self.add=ctk.CTkButton(head,text="",width=145,height=42,fg_color=c["accent"],command=self.editor); self.add.grid(row=0,column=1,rowspan=2,padx=(15,0))
        self.toolbar=ctk.CTkFrame(self.main,fg_color=c["card"],corner_radius=14,border_width=1,border_color=c["border"]); self.toolbar.grid(row=1,column=0,sticky="ew",padx=30,pady=8); self.toolbar.grid_columnconfigure(0,weight=1)
        self.search=ctk.CTkEntry(self.toolbar,height=40,fg_color=c["input"],border_color=c["border"],text_color=c["text"]); self.search.grid(row=0,column=0,sticky="ew",padx=12,pady=12); self.search.bind("<KeyRelease>",lambda e:self.search_changed())
        self.sort_menu=ctk.CTkOptionMenu(self.toolbar,width=135,height=40,fg_color=c["secondary"],button_color=c["secondary"],button_hover_color=c["hover"],command=self.change_sort,values=["Newest"]); self.sort_menu.grid(row=0,column=1,padx=8,pady=12)
        self.clear=ctk.CTkButton(self.toolbar,text="",width=130,height=40,fg_color=c["secondary"],hover_color=c["hover"],text_color=c["text"],command=self.clear_done); self.clear.grid(row=0,column=2,padx=(0,12),pady=12)
        self.list=ctk.CTkScrollableFrame(self.main,fg_color="transparent"); self.list.grid(row=2,column=0,sticky="nsew",padx=30,pady=(8,24)); self.list.grid_columnconfigure(0,weight=1)

    def apply_language(self):
        t=self.t
        self.sub.configure(text=t["sub"]); self.title_lbl.configure(text=t["title"]); self.add.configure(text="+  "+t["add"])
        self.search.configure(placeholder_text=t["search"]); self.clear.configure(text=t["clear"]); self.lang_btn.configure(text=t["lang"])
        self.theme_btn.configure(text=t["light"] if self.theme=="dark" else t["dark"])
        for k,icon in zip(self.nav,["▦","○","✓","⚠","◷"]): self.nav[k].configure(text=f"{icon}  {t[k]}")
        vals=[t["newest"],t["oldest"],t["priority_sort"],t["due_sort"]]; self.sort_menu.configure(values=vals)
        self.sort_menu.set(dict(newest=t["newest"],oldest=t["oldest"],priority=t["priority_sort"],due=t["due_sort"]).get(self.sort,t["newest"]))
        self.save_state(); self.refresh()

    def toggle_language(self):
        self.lang="fa" if self.lang=="en" else "en"; self.apply_language()

    def toggle_theme(self):
        self.theme="light" if self.theme=="dark" else "dark"; ctk.set_appearance_mode(self.theme); self.retheme(); self.apply_language()

    def retheme(self):
        c=self.c
        self.configure(fg_color=c["window"]); self.side.configure(fg_color=c["panel"]); self.main.configure(fg_color=c["window"])
        for w in [self.logo,self.title_lbl]: w.configure(text_color=c["text"])
        for w in [self.sub,self.stats,self.prog_text]: w.configure(text_color=c["muted"])
        for b in self.nav.values(): b.configure(text_color=c["text"],hover_color=c["secondary"])
        for b in [self.lang_btn,self.theme_btn,self.clear]: b.configure(fg_color=c["secondary"],hover_color=c["hover"],text_color=c["text"])
        self.prog.configure(progress_color=c["accent"],fg_color=c["secondary"]); self.toolbar.configure(fg_color=c["card"],border_color=c["border"])
        self.search.configure(fg_color=c["input"],border_color=c["border"],text_color=c["text"])
        self.sort_menu.configure(fg_color=c["secondary"],button_color=c["secondary"],button_hover_color=c["hover"])
        self.refresh()

    def search_changed(self):
        self.query=self.search.get().strip().lower(); self.refresh()

    def set_filter(self,k): self.filter=k; self.refresh()

    def change_sort(self,value):
        self.sort={self.t["newest"]:"newest",self.t["oldest"]:"oldest",self.t["priority_sort"]:"priority",self.t["due_sort"]:"due"}.get(value,"newest"); self.save_state(); self.refresh()

    def normalize(self,v,keys):
        for k in keys:
            if v in (self.T["en"][k],self.T["fa"][k]): return k
        return v

    def editor(self,task=None):
        self.edit_id=task["id"] if task else None
        d=ctk.CTkToplevel(self); d.title(self.t["edit"] if task else self.t["add"]); d.geometry("530x600"); d.resizable(False,False); d.transient(self); d.grab_set(); d.configure(fg_color=self.c["window"])
        d.grid_columnconfigure(0,weight=1)
        c= self.c
        ctk.CTkLabel(d,text=self.t["edit"] if task else self.t["add"],font=ctk.CTkFont(size=24,weight="bold"),text_color=c["text"]).grid(row=0,column=0,sticky="w",padx=28,pady=(25,15))
        title=ctk.CTkEntry(d,height=44,placeholder_text=("New task title..." if self.lang=="en" else "عنوان وظیفه جدید..."),fg_color=c["input"],border_color=c["border"]); title.grid(row=1,column=0,sticky="ew",padx=28,pady=7)
        desc=ctk.CTkTextbox(d,height=100,fg_color=c["input"],border_color=c["border"],border_width=1); desc.grid(row=2,column=0,sticky="ew",padx=28,pady=7)
        priority=ctk.CTkOptionMenu(d,values=[self.t["low"],self.t["medium"],self.t["high"]],fg_color=c["secondary"],button_color=c["secondary"],button_hover_color=c["hover"]); priority.grid(row=3,column=0,sticky="ew",padx=28,pady=7)
        category=ctk.CTkOptionMenu(d,values=[self.t[x] for x in ["work","study","personal","shopping","other"]],fg_color=c["secondary"],button_color=c["secondary"],button_hover_color=c["hover"]); category.grid(row=4,column=0,sticky="ew",padx=28,pady=7)
        due=ctk.CTkEntry(d,height=42,placeholder_text="YYYY-MM-DD",fg_color=c["input"],border_color=c["border"]); due.grid(row=5,column=0,sticky="ew",padx=28,pady=7)
        if task:
            title.insert(0,task["title"]); desc.insert("1.0",task.get("description","")); priority.set(self.t[task.get("priority","medium")]); category.set(self.t[task.get("category","other")]); due.insert(0,task.get("due_date",""))
        box=ctk.CTkFrame(d,fg_color="transparent"); box.grid(row=6,column=0,sticky="ew",padx=28,pady=18); box.grid_columnconfigure((0,1),weight=1)
        ctk.CTkButton(box,text=self.t["cancel"],fg_color=c["secondary"],hover_color=c["hover"],text_color=c["text"],command=d.destroy).grid(row=0,column=0,sticky="ew",padx=4)
        ctk.CTkButton(box,text=self.t["save"],fg_color=c["accent"],command=lambda:self.save_editor(d,title,desc,priority,category,due)).grid(row=0,column=1,sticky="ew",padx=4)

    def save_editor(self,d,title,desc,priority,category,due):
        title=title.get().strip(); due=due.get().strip()
        if not title: self.toast(self.t["required"],True); return
        if due:
            try: datetime.strptime(due,"%Y-%m-%d")
            except ValueError: self.toast("Use YYYY-MM-DD",True); return
        p=self.normalize(priority.get(),["low","medium","high"]); cat=self.normalize(category.get(),["work","study","personal","shopping","other"])
        if self.edit_id:
            task=next(x for x in self.tasks if x["id"]==self.edit_id); task.update(title=title,description=desc.get("1.0","end").strip(),priority=p,category=cat,due_date=due,updated_at=datetime.now().isoformat(timespec="seconds")); msg=self.t["updated"]
        else:
            self.tasks.append({"id":uuid.uuid4().hex,"title":title,"description":desc.get("1.0","end").strip(),"priority":p,"category":cat,"due_date":due,"completed":False,"created_at":datetime.now().isoformat(timespec="seconds"),"updated_at":datetime.now().isoformat(timespec="seconds")}); msg=self.t["added"]
        self.save(self.DATA,self.tasks); d.destroy(); self.refresh(); self.toast(msg)

    def filtered(self):
        today=date.today().isoformat(); r=[]
        for x in self.tasks:
            text=(x.get("title","")+" "+x.get("description","")).lower()
            if self.query and self.query not in text: continue
            due=x.get("due_date",""); done=x.get("completed",False)
            if self.filter=="active" and done: continue
            if self.filter=="done" and not done: continue
            if self.filter=="overdue" and (done or not due or due>=today): continue
            if self.filter=="today" and due!=today: continue
            r.append(x)
        rank={"high":0,"medium":1,"low":2}
        if self.sort=="oldest": r.sort(key=lambda x:x.get("created_at",""))
        elif self.sort=="priority": r.sort(key=lambda x:rank.get(x.get("priority"),9))
        elif self.sort=="due": r.sort(key=lambda x:x.get("due_date") or "9999-12-31")
        else: r.sort(key=lambda x:x.get("created_at",""),reverse=True)
        return r

    def refresh(self):
        if not hasattr(self,"list"): return
        for w in self.list.winfo_children(): w.destroy()
        total=len(self.tasks); done=sum(x.get("completed",False) for x in self.tasks); remaining=total-done
        self.stats.configure(text=self.t["stats"].format(t=total,d=done,r=remaining)); self.prog.set(done/total if total else 0)
        self.prog_text.configure(text=f"{self.t['done']}: {round(done/total*100) if total else 0}%")
        for k,b in self.nav.items(): b.configure(fg_color=self.c["accent"] if k==self.filter else "transparent")
        tasks=self.filtered()
        if not tasks:
            ctk.CTkLabel(self.list,text=self.t["empty"],font=ctk.CTkFont(size=17),text_color=self.c["muted"]).grid(row=0,column=0,pady=100); return
        for i,x in enumerate(tasks): self.card(x,i)

    def card(self,x,row):
        c=self.c
        f=ctk.CTkFrame(self.list,fg_color=c["card"],corner_radius=14,border_width=1,border_color=c["border"]); f.grid(row=row,column=0,sticky="ew",pady=6); f.grid_columnconfigure(1,weight=1)
        chk=ctk.CTkCheckBox(f,text="",width=28,command=lambda:self.toggle(x["id"])); chk.grid(row=0,column=0,rowspan=2,padx=(16,8),pady=15)
        if x.get("completed"): chk.select()
        title=ctk.CTkLabel(f,text=x["title"],font=ctk.CTkFont(size=16,weight="bold"),text_color=c["muted"] if x.get("completed") else c["text"],anchor="w"); title.grid(row=0,column=1,sticky="ew",padx=4,pady=(14,2))
        meta=[self.t[x.get("priority","medium")],self.t[x.get("category","other")]]
        if x.get("due_date"): meta.append(f"{self.t['due']}: {x['due_date']}")
        ctk.CTkLabel(f,text=" • ".join(meta),text_color=c["muted"],font=ctk.CTkFont(size=11),anchor="w").grid(row=1,column=1,sticky="ew",padx=4,pady=(0,14))
        pc={"high":c["danger"],"medium":c["warning"],"low":c["success"]}.get(x.get("priority"),c["accent"])
        ctk.CTkLabel(f,text=self.t[x.get("priority","medium")],width=70,height=25,corner_radius=8,fg_color=pc,text_color="white").grid(row=0,column=2,padx=5,pady=12)
        ctk.CTkButton(f,text="✎",width=38,height=32,fg_color=c["secondary"],hover_color=c["hover"],text_color=c["text"],command=lambda:self.editor(x)).grid(row=0,column=3,padx=3)
        ctk.CTkButton(f,text="×",width=38,height=32,fg_color=c["secondary"],hover_color=c["danger"],command=lambda:self.delete(x["id"])).grid(row=0,column=4,padx=(3,12))
        if x.get("description"): ctk.CTkLabel(f,text=x["description"],text_color=c["muted"],font=ctk.CTkFont(size=11),anchor="w").grid(row=2,column=1,columnspan=4,sticky="ew",padx=4,pady=(0,12))

    def toggle(self,i):
        for x in self.tasks:
            if x["id"]==i: x["completed"]=not x.get("completed",False); x["updated_at"]=datetime.now().isoformat(timespec="seconds")
        self.save(self.DATA,self.tasks); self.refresh()

    def delete(self,i):
        self.tasks=[x for x in self.tasks if x["id"]!=i]; self.save(self.DATA,self.tasks); self.refresh(); self.toast(self.t["deleted"])

    def clear_done(self):
        self.tasks=[x for x in self.tasks if not x.get("completed")]; self.save(self.DATA,self.tasks); self.refresh()

    def toast(self,msg,error=False):
        w=ctk.CTkLabel(self,text=msg,corner_radius=10,fg_color=self.c["danger"] if error else self.c["success"],text_color="white",padx=18,pady=9); w.place(relx=.98,rely=.96,anchor="se"); self.after(2200,w.destroy)

if __name__=="__main__":
    TodoApp().mainloop()
