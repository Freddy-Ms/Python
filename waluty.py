from tkinter import *
import requests
from tkinter import ttk
from screeninfo import get_monitors
import random
currencies = []
users_width, users_height = get_monitors()[0].width, get_monitors()[0].height
width, height = 300,300
def isnumber(input):
        try:
            float(input)
            return True
        except ValueError:
            return False
def getcurrencies():
    global currencies
    url = f"https://api.frankfurter.app/currencies"
    response = requests.get(url)
    tmp_data = response.json()
    currencies = [(f"{value} - {key}") for key,value in tmp_data.items()]
def getvalue(curr,to):
    curr = curr[-3:]
    to = to[-3:]
    url= f"https://api.frankfurter.app/latest?to={to},{curr}"
    tmp_data = requests.get(url).json().get("rates",[])
    if curr != "EUR" and to != "EUR":
        curr = tmp_data[curr]
        to = tmp_data[to]
        return float(curr / to)
    else:
        if curr == "EUR":
            return float(tmp_data[to])
        else:
            return float(1 / tmp_data[curr])
def changecurrency():
    curr = from_currency.get()
    to = to_currency.get()
    amount = entry_label.get().replace(",",".")
    value = getvalue(curr,to)
    if isnumber(amount):
        amount = float(amount)
        result_label.config(text = f"{amount * value}")
    else:
        result_label.config(text = f"Enter a number")
         
window =Tk()
window.geometry(f"{width}x{height}+{(users_width-width)//2}+{(users_height - height)//2}") #center window
window.resizable(0,0)
window.configure(background="black")
window.title("Przelicznik walut")
getcurrencies()
main_frame = Frame(window, bg="black")
main_frame.pack()

info_box = Label(main_frame,font=("Arial",15), bg = "black", fg="green", text= "From this currency:")
info_box.pack(fill = BOTH)

selected_option = StringVar()
from_currency = ttk.Combobox(main_frame,values = currencies, state="readonly", background="black", textvariable= selected_option)
from_currency.pack(fill = BOTH)
selected_option.set(random.choice(currencies))

iinfo_box = Label(main_frame,font=("Arial",15), bg = "black", fg="green", text= "To this:")
iinfo_box.pack(fill =BOTH)


to_currency = ttk.Combobox(main_frame,values = currencies, state= "readonly",textvariable= selected_option)
to_currency.pack(fill= BOTH)

amount_label = Label(main_frame,font=("Arial",15), bg = "black", fg="green", text= "Enter amount:")
amount_label.pack()


entry_label = Entry(main_frame, bg="white", font=("Arial",15), fg= "green")
entry_label.pack(pady=(5,5))

sumbit_button = Button(main_frame, text="Convert", command= changecurrency)
sumbit_button.pack()

result_label = Label(main_frame,font=("Arial",15), bg = "black", fg="green", text= "Result:")
result_label.pack(pady = (5,0))
print(currencies)
window.mainloop()