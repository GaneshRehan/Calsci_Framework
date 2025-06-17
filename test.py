# # # # import urequests
# # # # import ujson
# # # # url = "https://jsonplaceholder.typicode.com/todos/1"
# # # # response = urequests.get("https://jsonplaceholder.typicode.com/todos/1")

# # # import urequests
# # # import ujson

# # # # URL to fetch data from
# # # url = "https://jsonplaceholder.typicode.com/todos/1"

# # # try:
# # #     # Send a GET request to the URL
# # #     response = urequests.get(url)
    
# # #     # Check if the request was successful (status code 200)
# # #     if response.status_code == 200:
# # #         # Parse the JSON response
# # #         data = ujson.loads(response.text)
# # #         print("Response JSON:", data)
# # #     else:
# # #         print("Failed to fetch data. Status code:", response.status_code)
    
# # #     # Close the response to free up resources
# # #     response.close()
# # # except Exception as e:
# # #     print("An error occurred:", e)

# # from tkinter import *
# # import math
# # import tkinter.messagebox

# # root = Tk()
# # root.title("Scientific Calculator")
# # root.configure(background = 'white')
# # root.resizable(width=False, height=False)
# # root.geometry("480x568+450+90")
# # calc = Frame(root)
# # calc.grid()

# # class Calc():
# # 	def __init__(self):
# # 		self.total=0
# # 		self.current=''
# # 		self.input_value=True
# # 		self.check_sum=False
# # 		self.op=''
# # 		self.result=False

# # 	def numberEnter(self, num):
# # 		self.result=False
# # 		firstnum=txtDisplay.get()
# # 		secondnum=str(num)
# # 		if self.input_value:
# # 			self.current = secondnum
# # 			self.input_value=False
# # 		else:
# # 			if secondnum == '.':
# # 				if secondnum in firstnum:
# # 					return
# # 			self.current = firstnum+secondnum
# # 		self.display(self.current)

# # 	def sum_of_total(self):
# # 		self.result=True
# # 		self.current=float(self.current)
# # 		if self.check_sum==True:
# # 			self.valid_function()
# # 		else:
# # 			self.total=float(txtDisplay.get())

# # 	def display(self, value):
# # 		txtDisplay.delete(0, END)
# # 		txtDisplay.insert(0, value)

# # 	def valid_function(self):
# # 		if self.op == "add":
# # 			self.total += self.current
# # 		if self.op == "sub":
# # 			self.total -= self.current
# # 		if self.op == "multi":
# # 			self.total *= self.current
# # 		if self.op == "divide":
# # 			self.total /= self.current
# # 		if self.op == "mod":
# # 			self.total %= self.current
# # 		self.input_value=True
# # 		self.check_sum=False
# # 		self.display(self.total)

# # 	def operation(self, op):
# # 		self.current = float(self.current)
# # 		if self.check_sum:
# # 			self.valid_function()
# # 		elif not self.result:
# # 			self.total=self.current
# # 			self.input_value=True
# # 		self.check_sum=True
# # 		self.op=op
# # 		self.result=False

# # 	def Clear_Entry(self):
# # 		self.result = False
# # 		self.current = "0"
# # 		self.display(0)
# # 		self.input_value=True

# # 	def All_Clear_Entry(self):
# # 		self.Clear_Entry()
# # 		self.total=0

# # 	def pi(self):
# # 		self.result = False
# # 		self.current = math.pi
# # 		self.display(self.current)

# # 	def tau(self):
# # 		self.result = False
# # 		self.current = math.tau
# # 		self.display(self.current)

# # 	def e(self):
# # 		self.result = False
# # 		self.current = math.e
# # 		self.display(self.current)

# # 	def mathPM(self):
# # 		self.result = False
# # 		self.current = -(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def squared(self):
# # 		self.result = False
# # 		self.current = math.sqrt(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def cos(self):
# # 		self.result = False
# # 		self.current = math.cos(math.radians(float(txtDisplay.get())))
# # 		self.display(self.current)

# # 	def cosh(self):
# # 		self.result = False
# # 		self.current = math.cosh(math.radians(float(txtDisplay.get())))
# # 		self.display(self.current)

# # 	def tan(self):
# # 		self.result = False
# # 		self.current = math.tan(math.radians(float(txtDisplay.get())))
# # 		self.display(self.current)

# # 	def tanh(self):
# # 		self.result = False
# # 		self.current = math.tanh(math.radians(float(txtDisplay.get())))
# # 		self.display(self.current)

# # 	def sin(self):
# # 		self.result = False
# # 		self.current = math.sin(math.radians(float(txtDisplay.get())))
# # 		self.display(self.current)

# # 	def sinh(self):
# # 		self.result = False
# # 		self.current = math.sinh(math.radians(float(txtDisplay.get())))
# # 		self.display(self.current)

# # 	def log(self):
# # 		self.result = False
# # 		self.current = math.log(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def exp(self):
# # 		self.result = False
# # 		self.current = math.exp(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def acosh(self):
# # 		self.result = False
# # 		self.current = math.acosh(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def asinh(self):
# # 		self.result = False
# # 		self.current = math.asinh(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def expm1(self):
# # 		self.result = False
# # 		self.current = math.expm1(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def lgamma(self):
# # 		self.result = False
# # 		self.current = math.lgamma(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def degrees(self):
# # 		self.result = False
# # 		self.current = math.degrees(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def log2(self):
# # 		self.result = False
# # 		self.current = math.log2(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def log10(self):
# # 		self.result = False
# # 		self.current = math.log10(float(txtDisplay.get()))
# # 		self.display(self.current)

# # 	def log1p(self):
# # 		self.result = False
# # 		self.current = math.log1p(float(txtDisplay.get()))
# # 		self.display(self.current)

# # added_value = Calc()

# # txtDisplay = Entry(calc, font=('Helvetica',20,'bold'),
# # 				bg='black',fg='white',
# # 				bd=30,width=28,justify=RIGHT)
# # txtDisplay.grid(row=0,column=0, columnspan=4, pady=1)
# # txtDisplay.insert(0,"0")

# # numberpad = "789456123"
# # i=0
# # btn = []
# # for j in range(2,5):
# # 	for k in range(3):
# # 		btn.append(Button(calc, width=6, height=2,
# # 						bg='black',fg='white',
# # 						font=('Helvetica',20,'bold'),
# # 						bd=4,text=numberpad[i]))
# # 		btn[i].grid(row=j, column= k, pady = 1)
# # 		btn[i]["command"]=lambda x=numberpad[i]:added_value.numberEnter(x)
# # 		i+=1
	
# # btnClear = Button(calc, text=chr(67),width=6,
# # 				height=2,bg='powder blue',
# # 				font=('Helvetica',20,'bold')
# # 				,bd=4, command=added_value.Clear_Entry
# # 				).grid(row=1, column= 0, pady = 1)

# # btnAllClear = Button(calc, text=chr(67)+chr(69),
# # 					width=6, height=2,
# # 					bg='powder blue', 
# # 					font=('Helvetica',20,'bold'),
# # 					bd=4,
# # 					command=added_value.All_Clear_Entry
# # 					).grid(row=1, column= 1, pady = 1)

# # btnsq = Button(calc, text="\u221A",width=6, height=2,
# # 			bg='powder blue', font=('Helvetica',
# # 									20,'bold'),
# # 			bd=4,command=added_value.squared
# # 			).grid(row=1, column= 2, pady = 1)

# # btnAdd = Button(calc, text="+",width=6, height=2,
# # 				bg='powder blue',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.operation("add")
# # 				).grid(row=1, column= 3, pady = 1)

# # btnSub = Button(calc, text="-",width=6,
# # 				height=2,bg='powder blue',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.operation("sub")
# # 				).grid(row=2, column= 3, pady = 1)

# # btnMul = Button(calc, text="x",width=6, 
# # 				height=2,bg='powder blue', 
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.operation("multi")
# # 				).grid(row=3, column= 3, pady = 1)

# # btnDiv = Button(calc, text="/",width=6, 
# # 				height=2,bg='powder blue',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.operation("divide")
# # 				).grid(row=4, column= 3, pady = 1)

# # btnZero = Button(calc, text="0",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.numberEnter(0)
# # 				).grid(row=5, column= 0, pady = 1)

# # btnDot = Button(calc, text=".",width=6,
# # 				height=2,bg='powder blue', 
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.numberEnter(".")
# # 				).grid(row=5, column= 1, pady = 1)
# # btnPM = Button(calc, text=chr(177),width=6, 
# # 			height=2,bg='powder blue', font=('Helvetica',20,'bold'),
# # 			bd=4,command=added_value.mathPM
# # 			).grid(row=5, column= 2, pady = 1)

# # btnEquals = Button(calc, text="=",width=6,
# # 				height=2,bg='powder blue',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.sum_of_total
# # 				).grid(row=5, column= 3, pady = 1)
# # # ROW 1 :
# # btnPi = Button(calc, text="pi",width=6,
# # 			height=2,bg='black',fg='white', 
# # 			font=('Helvetica',20,'bold'),
# # 			bd=4,command=added_value.pi
# # 			).grid(row=1, column= 4, pady = 1)

# # btnCos = Button(calc, text="Cos",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.cos
# # 			).grid(row=1, column= 5, pady = 1)

# # btntan = Button(calc, text="tan",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.tan
# # 			).grid(row=1, column= 6, pady = 1)

# # btnsin = Button(calc, text="sin",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.sin
# # 			).grid(row=1, column= 7, pady = 1)

# # # ROW 2 :
# # btn2Pi = Button(calc, text="2pi",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.tau
# # 			).grid(row=2, column= 4, pady = 1)

# # btnCosh = Button(calc, text="Cosh",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.cosh
# # 				).grid(row=2, column= 5, pady = 1)

# # btntanh = Button(calc, text="tanh",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.tanh
# # 				).grid(row=2, column= 6, pady = 1)

# # btnsinh = Button(calc, text="sinh",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.sinh
# # 				).grid(row=2, column= 7, pady = 1)

# # # ROW 3 :
# # btnlog = Button(calc, text="log",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.log
# # 			).grid(row=3, column= 4, pady = 1)

# # btnExp = Button(calc, text="exp",width=6, height=2,
# # 				bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.exp
# # 			).grid(row=3, column= 5, pady = 1)

# # btnMod = Button(calc, text="Mod",width=6,
# # 				height=2,bg='black',fg='white', 
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=lambda:added_value.operation("mod")
# # 				).grid(row=3, column= 6, pady = 1)

# # btnE = Button(calc, text="e",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.e
# # 			).grid(row=3, column= 7, pady = 1)

# # # ROW 4 :
# # btnlog10 = Button(calc, text="log10",width=6, 
# # 				height=2,bg='black',fg='white', 
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.log10
# # 				).grid(row=4, column= 4, pady = 1)

# # btncos = Button(calc, text="log1p",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.log1p
# # 				).grid(row=4, column= 5, pady = 1)

# # btnexpm1 = Button(calc, text="expm1",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd = 4,command=added_value.expm1
# # 				).grid(row=4, column= 6, pady = 1)

# # btngamma = Button(calc, text="gamma",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.lgamma
# # 				).grid(row=4, column= 7, pady = 1)
# # # ROW 5 :
# # btnlog2 = Button(calc, text="log2",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.log2
# # 				).grid(row=5, column= 4, pady = 1)

# # btndeg = Button(calc, text="deg",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.degrees
# # 			).grid(row=5, column= 5, pady = 1)

# # btnacosh = Button(calc, text="acosh",width=6,
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.acosh
# # 				).grid(row=5, column= 6, pady = 1)

# # btnasinh = Button(calc, text="asinh",width=6, 
# # 				height=2,bg='black',fg='white',
# # 				font=('Helvetica',20,'bold'),
# # 				bd=4,command=added_value.asinh
# # 				).grid(row=5, column= 7, pady = 1)

# # lblDisplay = Label(calc, text = "Scientific Calculator",
# # 				font=('Helvetica',30,'bold'),
# # 				bg='black',fg='white',justify=CENTER)

# # lblDisplay.grid(row=0, column= 4,columnspan=4)

# # def iExit():
# # 	iExit = tkinter.messagebox.askyesno("Scientific Calculator",
# # 										"Do you want to exit ?")
# # 	if iExit>0:
# # 		root.destroy()
# # 		return

# # def Scientific():
# # 	root.resizable(width=False, height=False)
# # 	root.geometry("944x568+0+0")


# # def Standard():
# # 	root.resizable(width=False, height=False)
# # 	root.geometry("480x568+0+0")

# # menubar = Menu(calc)

# # # ManuBar 1 :
# # filemenu = Menu(menubar, tearoff = 0)
# # menubar.add_cascade(label = 'File', menu = filemenu)
# # filemenu.add_command(label = "Standard", command = Standard)
# # filemenu.add_command(label = "Scientific", command = Scientific)
# # filemenu.add_separator()
# # filemenu.add_command(label = "Exit", command = iExit)

# # # ManuBar 2 :
# # editmenu = Menu(menubar, tearoff = 0)
# # menubar.add_cascade(label = 'Edit', menu = editmenu)
# # editmenu.add_command(label = "Cut")
# # editmenu.add_command(label = "Copy")
# # editmenu.add_separator()
# # editmenu.add_command(label = "Paste")

# # root.config(menu=menubar)

# # root.mainloop()

# import utime as time
# from math import *
# from data_modules.object_handler import display, text, nav, text_refresh, typer, keypad_state_manager, keypad_state_manager_reset, menu, menu_refresh
# from data_modules.object_handler import current_app

# class ScientificCalculator:
#     def __init__(self):
#         self.total = 0
#         self.current = ''
#         self.input_value = True
#         self.check_sum = False
#         self.op = ''
#         self.result = False

#     def numberEnter(self, num):
#         try:
#             self.result = False
#             firstnum = self.current
#             secondnum = str(num)
#             if self.input_value:
#                 self.current = secondnum
#                 self.input_value = False
#             else:
#                 if secondnum == '.' and '.' in firstnum:
#                     return
#                 self.current = firstnum + secondnum
#             self.display(self.current)
#             print(f"Number entered: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in numberEnter: {e}")

#     def sum_of_total(self):
#         try:
#             self.result = True
#             self.current = float(self.current)
#             if self.check_sum:
#                 self.valid_function()
#             else:
#                 self.total = self.current
#             self.display(str(self.total))
#             print(f"Result: {self.total}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in sum_of_total: {e}")

#     def display(self, value):
#         try:
#             text.all_clear()
#             text.update_buffer(str(value))
#             text_refresh.refresh(state=nav.current_state())
#             print(f"Displaying: {value}")
#         except Exception as e:
#             print(f"Error in display: {e}")

#     def valid_function(self):
#         try:
#             if self.op == "add":
#                 self.total += self.current
#             elif self.op == "sub":
#                 self.total -= self.current
#             elif self.op == "multi":
#                 self.total *= self.current
#             elif self.op == "divide":
#                 self.total /= self.current
#             elif self.op == "mod":
#                 self.total %= self.current
#             self.input_value = True
#             self.check_sum = False
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in valid_function: {e}")

#     def operation(self, op):
#         try:
#             self.current = float(self.current)
#             if self.check_sum:
#                 self.valid_function()
#             elif not self.result:
#                 self.total = self.current
#                 self.input_value = True
#             self.check_sum = True
#             self.op = op
#             self.result = False
#             self.current = ''
#             self.display(str(self.total) + " " + op)
#             print(f"Operation: {op}, Total: {self.total}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in operation: {e}")

#     def clear_entry(self):
#         try:
#             self.result = False
#             self.current = '0'
#             self.input_value = True
#             self.display('0')
#             print("Cleared entry")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in clear_entry: {e}")

#     def all_clear(self):
#         try:
#             self.clear_entry()
#             self.total = 0
#             print("All cleared")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in all_clear: {e}")

#     def mathPM(self):
#         try:
#             self.result = False
#             self.current = str(-float(self.current))
#             self.display(self.current)
#             print(f"Sign changed: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in mathPM: {e}")

#     def squared(self):
#         try:
#             self.result = False
#             self.current = str(sqrt(float(self.current)))
#             self.display(self.current)
#             print(f"Square root: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in squared: {e}")

#     def sin(self):
#         try:
#             self.result = False
#             self.current = str(sin(radians(float(self.current))))
#             self.display(self.current)
#             print(f"sin: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in sin: {e}")

#     def cos(self):
#         try:
#             self.result = False
#             self.current = str(cos(radians(float(self.current))))
#             self.display(self.current)
#             print(f"cos: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in cos: {e}")

#     def tan(self):
#         try:
#             self.result = False
#             self.current = str(tan(radians(float(self.current))))
#             self.display(self.current)
#             print(f"tan: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in tan: {e}")

#     def asin(self):
#         try:
#             self.result = False
#             self.current = str(degrees(asin(float(self.current))))
#             self.display(self.current)
#             print(f"asin: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in asin: {e}")

#     def acos(self):
#         try:
#             self.result = False
#             self.current = str(degrees(acos(float(self.current))))
#             self.display(self.current)
#             print(f"acos: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in acos: {e}")

#     def atan(self):
#         try:
#             self.result = False
#             self.current = str(degrees(atan(float(self.current))))
#             self.display(self.current)
#             print(f"atan: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in atan: {e}")

#     def log(self):
#         try:
#             self.result = False
#             self.current = str(log(float(self.current)))
#             self.display(self.current)
#             print(f"log: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in log: {e}")

#     def pi(self):
#         try:
#             self.result = False
#             self.current = str(pi)
#             self.display(self.current)
#             print(f"pi: {self.current}")
#         except Exception as e:
#             self.display("Error")
#             print(f"Error in pi: {e}")

# def calculate(db={}):
#     keypad_state_manager_reset()
#     calc = ScientificCalculator()
#     display.clear_display()
#     text.all_clear()
#     text_refresh.refresh()
#     print("Calculator initialized")
#     try:
#         while True:
#             x = typer.start_typing()
#             print(f"Key pressed: {x}")

#             if x == "back":
#                 current_app[0] = "home"
#                 print("Exiting to home")
#                 break

#             if x in ("ans", "exe"):
#                 if text.text_buffer[0] != "𖤓":
#                     calc.sum_of_total()

#             elif x in ("alpha", "beta"):
#                 keypad_state_manager(x=x)
#                 menu.update_buffer(x)
#                 menu_refresh.refresh(state=nav.current_state())
#                 time.sleep(0.2)
#                 temp_inp = typer.start_typing()
#                 print(f"Secondary key after {x}: {temp_inp}")
#                 if x == "alpha" and temp_inp == "on":
#                     import machine
#                     print("Entering deep sleep")
#                     machine.deepsleep()
#                 keypad_state_manager(x=x)
#                 text.update_buffer("")

#             elif x in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
#                 calc.numberEnter(x)

#             elif x == "AC":
#                 calc.all_clear()

#             elif x == "+":
#                 calc.operation("add")

#             elif x == "-":
#                 calc.operation("sub")

#             elif x == "*":
#                 calc.operation("multi")

#             elif x == "/":
#                 calc.operation("divide")

#             elif x == "%":
#                 calc.operation("mod")

#             elif x == "sin(":
#                 calc.sin()

#             elif x == "cos(":
#                 calc.cos()

#             elif x == "tan(":
#                 calc.tan()

#             elif x == "log(":
#                 calc.log()

#             elif x == "asin(":
#                 calc.asin()

#             elif x == "acos(":
#                 calc.acos()

#             elif x == "atan(":
#                 calc.atan()

#             elif x == "pi":
#                 calc.pi()

#             elif x == "&":
#                 calc.squared()

#             elif x == "'":
#                 calc.mathPM()

#             else:
#                 # Handle other valid keys by appending to buffer
#                 if x in ('"', "'", "(", ")", "pow("):
#                     text.update_buffer(x)
#                     print(f"Appended to buffer: {x}")

#             if text.text_buffer[0] == "𖤓":
#                 display.clear_display()
#                 text.all_clear()
#                 calc.all_clear()
#                 print("Buffer reset due to error state")

#             text_refresh.refresh(state=nav.current_state())
#             time.sleep(0.1)

#     except Exception as e:
#         print(f"Fatal error in calculate: {e}")
#         calc.display("Error")

# from process_modules.spreadsheet_buffer import SpreadsheetBuffer

# # Initialize the spreadsheet buffer
# spreadsheet = SpreadsheetBuffer(rows=10, cols=10, display_rows=7, display_cols=21)

# # Example: Update buffer with navigation or text input
# spreadsheet.update_buffer("nav_r")  # Move to the next column
# spreadsheet.update_buffer("123")    # Enter text in the current cell
# print(spreadsheet.buffer())        # View the current display buffer



import framebuf # type: ignore
from data_modules.object_handler import display
buffer1 = bytearray((128 * 64) // 8)



fb = framebuf.FrameBuffer(buffer1, 128, 64, framebuf.MONO_VLSB)
for y in range(0, 56, 8):
    fb.line(0, y, 127, y, 1)
for x in range(0, 128, 24):
    fb.line(x, 0, x, 48, 1)
display.clear_display()
display.graphics(buf=buffer1)