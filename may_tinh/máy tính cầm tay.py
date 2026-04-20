import tkinter as tk
import math

# Hàm xử lý khi bấm phím số hoặc phép toán
def button_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

# Hàm xử lý khi bấm nút Clear (C)
def button_clear():
    global expression
    expression = ""
    input_text.set("")

# Hàm xử lý khi bấm nút xóa lùi (DEL)
def button_backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)

# Hàm xử lý đổi dấu (+/-)
def button_negate():
    global expression
    if expression.startswith('-'):
        expression = expression[1:]
    else:
        expression = '-' + expression
    input_text.set(expression)

# Hàm xử lý khi bấm dấu Bằng (=)
def button_equal():
    global expression
    try:
        calc_expr = expression.replace('÷', '/').replace('×', '*').replace('^', '**').replace('√', 'math.sqrt')
        result = str(eval(calc_expr))
        if result.endswith('.0'):
            result = result[:-2]
        input_text.set(result)
        expression = result 
    except ZeroDivisionError:
        input_text.set("Lỗi chia 0")
        expression = ""
    except Exception:
        input_text.set("Lỗi cú pháp")
        expression = ""

# Cửa sổ chính 
window = tk.Tk()
window.title("Máy Tính Pro")
window.geometry("340x480")
window.resizable(0, 0)

expression = ""
input_text = tk.StringVar()

# Khung hiển thị kết quả
input_frame = tk.Frame(window, width=340, height=50, bd=0, highlightbackground="gray", highlightthickness=1)
input_frame.pack(side=tk.TOP, pady=5)

input_field = tk.Entry(input_frame, font=('Arial', 20, 'bold'), textvariable=input_text, width=50, bd=0, justify=tk.RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=15)

# Khung chứa các nút bấm
btns_frame = tk.Frame(window, width=340, height=400)
btns_frame.pack()

# Thiết lập chung cho nút
btn_params = {'width': 6, 'height': 2, 'bd': 1, 'font': ('Arial', 14, 'bold'), 'cursor': 'hand2'}

# Danh sách các nút
buttons = [
    'C', 'DEL', '(', ')',
    '√', '^', '%', '÷',
    '7', '8', '9', '×',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '+/-', '0', '.', '='
]

row_val = 0
col_val = 0

for text in buttons:
    # Phân loại hàm chức năng
    if text == 'C':
        action = button_clear
    elif text == 'DEL':
        action = button_backspace
    elif text == '=':
        action = button_equal
    elif text == '+/-':
        action = button_negate
    elif text == '√':
        action = lambda: button_click('√(')
    else:
        action = lambda t=text: button_click(t)
        
    # Tạo nút và đưa lên lưới
    b = tk.Button(btns_frame, text=text, command=action, **btn_params)
    b.grid(row=row_val, column=col_val, padx=3, pady=3)
    
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

window.mainloop()