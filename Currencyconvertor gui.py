import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def getting_API(user_currency, currency_to_be_converted):
    access_key = 'f33d3b1d06b56e0f4770e138'

    url = f'https://v6.exchangerate-api.com/v6/{access_key}/latest/{user_currency}'

    r = requests.get(url)

    if r.status_code != 200:
        print("\nError:", r.text)
        return None

    data = r.json()

    conversion_rates = data.get('conversion_rates', {})
    if currency_to_be_converted not in conversion_rates:
        print(f"\nError: Conversion rates for {currency_to_be_converted} not found.")
        return None
    if user_currency not in conversion_rates:
        print(f"\nError: Conversion rates for {user_currency} not found.")
        return None

    return data

def convert_currency():
    user_currency = user_currency_var.get()
    currency_to_be_converted = currency_to_be_converted_var.get()
    user_amount = user_amount_entry.get()

    if not user_amount:
        messagebox.showerror("Error", "Please enter an amount to convert.")
        return

    if not user_amount.isdigit():
        messagebox.showerror("Error", "Please enter a valid amount (only digits).")
        return

    user_amount = float(user_amount)

    dict_data = getting_API(user_currency, currency_to_be_converted)
    if dict_data:
        conversion_rates = dict_data.get('conversion_rates')

        initial_currency_rate = float(conversion_rates.get(currency_to_be_converted))
        ans = round((user_amount * initial_currency_rate), 3)

        # If result_label already exists, destroy it
        global result_label
        if 'result_label' in globals():
            result_label.destroy()

        # Create and display new result label
        result_label = tk.Label(window, text=f'1 {user_currency} = {initial_currency_rate} {currency_to_be_converted}\n{user_amount} {user_currency} = {ans} {currency_to_be_converted}', font='Calibri 10 ', bg='grey', fg='white', padx=8, relief='ridge', borderwidth=4)
        result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Create tkinter window
window = tk.Tk()
window.title("Currency Converter")
window.geometry('400x210')
window.resizable(False, False)
window.iconbitmap('icon.ico')

# Load and resize background image to fit window
img = Image.open('pic3.jpg')
background_img = ImageTk.PhotoImage(img)

# Keep a reference to the background image to prevent garbage collection
window.background_img = background_img

# Create label for background image
back_label = tk.Label(window, image=background_img)
back_label.place(relwidth=1, relheight=1)

# Create labels
user_currency_label = tk.Label(window, text="Select your currency:" , font='Calibri 13 italic' , bg='grey' , fg='white' , relief='raised')
user_currency_label.grid(row=0, column=0, padx=10, pady=5 , sticky='w')

currency_to_be_converted_label = tk.Label(window, text="Select currency to convert to:" , font='Calibri 13 italic' , bg='grey' , fg='white' , relief='raised')
currency_to_be_converted_label.grid(row=1, column=0, padx=10, pady=5  , sticky='w')

user_amount_label = tk.Label(window, text="Enter amount:" , font='Calibri 13 italic' , bg='grey' , fg='white' , relief='raised')
user_amount_label.grid(row=2, column=0, padx=10, pady=5 , sticky='w')

# Create dropdowns for selecting currencies
currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'PKR']

style = ttk.Style()
style.configure('TCombobox', background='grey', foreground='black', bordercolor='blue' )

user_currency_var = tk.StringVar(window)
user_currency_dropdown = ttk.Combobox(window, textvariable=user_currency_var, values=currencies, style='TCombobox')
user_currency_dropdown.grid(row=0, column=1, padx=10, pady=5)
user_currency_dropdown.current(0)

currency_to_be_converted_var = tk.StringVar(window)
currency_to_be_converted_dropdown = ttk.Combobox(window, textvariable=currency_to_be_converted_var, values=currencies, style='TCombobox')
currency_to_be_converted_dropdown.grid(row=1, column=1, padx=10, pady=5)
currency_to_be_converted_dropdown.current(1)

# Create entry for entering amount
user_amount_entry = tk.Entry(window)
user_amount_entry.grid(row=2, column=1, padx=10, pady=5 , sticky='ew')
user_amount_entry.config(font=('Calibri', 10), relief='raised', borderwidth=2)

# Create button to convert currency
convert_button = tk.Button(window, text="Convert", font='Calibri 10 bold', bg='black' , fg='White' , relief='ridge' , padx=5, borderwidth=3, command=convert_currency)
convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5 )

# Run the tkinter event loop
window.mainloop()
