import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def run_sql(query, params=()):
    conn = sqlite3.connect('university.db') # 1. Kết nối 
    cur = conn.cursor()                     # 2. Tạo con trỏ 
    cur.execute(query, params)              # 3. Thực thi 
    res = cur.fetchall()                    # Lấy dữ liệu 
    conn.commit()                           # 4. Lưu 
    conn.close()                            # 5. Đóng 
    return res

run_sql("CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, major TEXT, gpa REAL)")

# CÁC HÀM CHỨC NĂNG
def load_data(q="SELECT * FROM students"):
    tree.delete(*tree.get_children()) 
    for row in run_sql(q): tree.insert("", tk.END, values=row)

def add_student():
    try:
        run_sql("INSERT INTO students (id, name, major, gpa) VALUES (?, ?, ?, ?)", 
                (e_id.get(), e_name.get(), e_major.get(), float(e_gpa.get())))
        load_data()
        for e in (e_id, e_name, e_major, e_gpa): e.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Lỗi", "Mã sinh viên này đã tồn tại!")
    except: 
        messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin và GPA phải là số!")

def update_gpa_only():
    try:
        selected_id = tree.item(tree.selection())['values'][0]
        # UPDATE cho cột gpa 
        new_gpa = float(e_gpa.get())
        run_sql("UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, selected_id))
        
        load_data()
        messagebox.showinfo("Thành công", f"Đã cập nhật GPA mới cho SV: {selected_id}")
    except: 
        messagebox.showwarning("Lỗi", "Hãy chọn 1 sinh viên bên dưới và nhập điểm GPA mới vào ô trống!")

def delete_low_gpa():
    if messagebox.askyesno("Xác nhận", "Xóa tất cả sinh viên có GPA < 2.0?"):
        run_sql("DELETE FROM students WHERE gpa < 2.0") 
        load_data()

def on_select(event):
    if tree.selection(): 
        values = tree.item(tree.selection())['values'] 
        for entry, val in zip((e_id, e_name, e_major, e_gpa), values):
            entry.delete(0, tk.END)
            entry.insert(0, val)

# GIAO DIỆN CHÍNH
root = tk.Tk()
root.title("Quản Lý Sinh Viên SQLite")
root.geometry("650x550") 

frame_input = tk.Frame(root, pady=15)
frame_input.pack()

# Các ô nhập liệu theo cột dọc
fields = [("Mã sinh viên:", "e_id"), ("Tên sinh viên:", "e_name"), 
          ("Chuyên ngành:", "e_major"), ("Điểm GPA:", "e_gpa")]
entries = {}

for i, (label_text, var_name) in enumerate(fields):
    tk.Label(frame_input, text=label_text, font=("Arial", 10)).grid(row=i, column=0, sticky="e", pady=5)
    ent = tk.Entry(frame_input, width=35, font=("Arial", 10))
    ent.grid(row=i, column=1, pady=5, padx=10)
    entries[var_name] = ent

e_id, e_name, e_major, e_gpa = entries["e_id"], entries["e_name"], entries["e_major"], entries["e_gpa"]

# Khu vực nút bấm
frame_btns = tk.Frame(root, pady=10)
frame_btns.pack()
buttons = [
    ("Thêm Sinh Viên", add_student, "lightblue"), 
    ("Cập nhật GPA", update_gpa_only, "lightgreen"),
    ("Xóa SV (GPA < 2.0)", delete_low_gpa, "salmon"),
    ("Lọc SV (GPA > 3.0)", lambda: load_data("SELECT * FROM students WHERE gpa > 3.0"), "white"),
    ("Tất cả", load_data, "white")
]
for text, cmd, bg in buttons:
    tk.Button(frame_btns, text=text, command=cmd, bg=bg, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)

# Bảng hiển thị
tree = ttk.Treeview(root, columns=("1", "2", "3", "4"), show="headings", height=12)
cols = [("1", 80, "Mã SV"), ("2", 160, "Tên sinh viên"), ("3", 160, "Chuyên ngành"), ("4", 100, "GPA")]
for col_id, width, text in cols:
    tree.heading(col_id, text=text)
    tree.column(col_id, width=width, anchor=tk.CENTER if col_id in ("1","4") else tk.W)
tree.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

tree.bind('<<TreeviewSelect>>', on_select)
load_data()
root.mainloop()