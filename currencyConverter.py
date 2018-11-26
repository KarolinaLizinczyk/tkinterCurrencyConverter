import requests
import Tkinter as tk
from xml.etree import ElementTree as ET



r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)

tree = ET.parse(r.raw)
rootXML = tree.getroot()

namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

currencyList = []

for cube in rootXML.findall('.//ex:Cube[@currency]', namespaces=namespaces):
    currencyList.append(cube.attrib['currency'])
    print(cube.attrib['currency'], cube.attrib['rate'])


class CurrencyConverter(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.geometry('550x300+800+400')
        self.resizable(width=False, height=False)
        self.initialize()

    def initialize(self):
        self.grid()

        # Title
        self.label = tk.Label(self, text="Currency Converter", fg='darkblue', font=("Helvetica", 16))
        self.label.grid(row=0, padx=15, pady=15)

        # Amount
        self.label = tk.Label(self, text="Convert this amount")
        self.label.grid(row=2, column=0, pady=5, padx=18, sticky=tk.E)
        self.var = tk.DoubleVar()
        self.E1 = tk.Entry(self, bd=2, textvariable=self.var, justify=tk.RIGHT)
        self.E1.grid(row=3, column=0, pady=5, padx=5, sticky=tk.E, ipady=2)

        #OptionMenu
        self.label = tk.Label(self, text="From this currency")
        self.label.grid(row=2, column=1, pady=10, padx=15, sticky=tk.W)
        self.variable1 = tk.StringVar(self)
        self.variable1.set(currencyList[0])
        self.E2 = tk.OptionMenu(self, self.variable1, *currencyList)
        self.E2.config(width=15)
        self.E2.grid(row=3, column=1, sticky=tk.E)

        #OptionMenu
        self.label = tk.Label(self, text="To this currency")
        self.label.grid(row=2, column=2, pady=10, padx=15, sticky=tk.W)
        self.variable2 = tk.StringVar(self)
        self.variable2.set(currencyList[0])
        self.E3 = tk.OptionMenu(self, self.variable2, *currencyList)
        self.E3.config(width=15)
        self.E3.grid(row=3, column=2, padx=10, sticky=tk.E)

        #Result
        self.label = tk.Label(self, text="Result", font=("Helvetica", 18))
        self.label.grid(row=4, column=0, pady=35, sticky=tk.E)
        self.variable3 = tk.DoubleVar()
        self.E4 = tk.Entry(self, bd=2, textvariable=self.variable3, justify=tk.RIGHT)
        self.E4.grid(row=4, column=1, ipady=3, padx=10, sticky=tk.E)

        #Buttons
        self.button = tk.Button(self, text='Convert', command=self.currencyCalculate, width=12, height=2)
        self.button.grid(row=5, column=1, padx=5, sticky=tk.E)
        self.button = tk.Button(self, text='Close', command=self.currencyCalculate,  width=12, height=2)
        self.button.grid(row=5, column=2, sticky=tk.W)


    def currencyCalculate(self):
        user_input = self.var.get()
        option_menu_input1 = self.variable1.get()
        option_menu_input2 = self.variable2.get()
        for cube in rootXML.findall('.//ex:Cube[@currency]', namespaces=namespaces):
            if cube.attrib['currency'] == option_menu_input1:
                to_dollars = float(user_input) / float(cube.attrib['rate'])

                for cube in rootXML.findall('.//ex:Cube[@currency]', namespaces=namespaces):
                    if cube.attrib['currency'] == option_menu_input2:
                        result = to_dollars * float(cube.attrib['rate'])
                        self.variable3.set(round(result, 2))
                        return result


if __name__ == "__main__":
    app = CurrencyConverter(None)
    app.title('My Currency Converter')
    app.mainloop()
