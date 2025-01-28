import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF

# Function to generate the PDF
def generate_pdf():
    patient_name = name_var.get()
    age = age_var.get()
    if not patient_name or not age:
        messagebox.showerror("Error", "Please fill out all fields.")
        return
    
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return
    
    if not test_results:
        messagebox.showerror("Error", "Please add at least one test result.")
        return

    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, "Medical Laboratory Report", ln=True, align="C")
    pdf.ln(10)
    
    # Patient Details
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(100, 10, f"Age: {age}", ln=True)
    pdf.ln(10)
    
    # Test Results Table
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(100, 10, "Test", border=1)
    pdf.cell(40, 10, "Result", border=1, ln=True)
    pdf.set_font("Arial", size=12)
    for test, result in test_results.items():
        pdf.cell(100, 10, test, border=1)
        pdf.cell(40, 10, str(result), border=1, ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Thank you for choosing our lab!", ln=True, align="C")
    
    # Save the PDF
    filename = f"{patient_name.replace(' ', '_')}_Lab_Report.pdf"
    pdf.output(filename)
    messagebox.showinfo("Success", f"Report saved as {filename}")

# Function to add test results
def add_test_result():
    test_name = test_name_var.get()
    test_result = test_result_var.get()
    if not test_name or not test_result:
        messagebox.showerror("Error", "Please enter both test name and result.")
        return
    
    test_results[test_name] = test_result
    results_list.insert("", "end", values=(test_name, test_result))
    test_name_var.set("")
    test_result_var.set("")

# GUI Setup
root = tk.Tk()
root.title("Medical Lab Report Generator")
root.geometry("500x600")

# Patient Info Frame
patient_frame = ttk.LabelFrame(root, text="Patient Information")
patient_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(patient_frame, text="Patient Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_var = tk.StringVar()
ttk.Entry(patient_frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(patient_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
age_var = tk.StringVar()
ttk.Entry(patient_frame, textvariable=age_var, width=30).grid(row=1, column=1, padx=5, pady=5)

# Test Results Frame
test_frame = ttk.LabelFrame(root, text="Test Results")
test_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(test_frame, text="Test Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
test_name_var = tk.StringVar()
ttk.Entry(test_frame, textvariable=test_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(test_frame, text="Test Result:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
test_result_var = tk.StringVar()
ttk.Entry(test_frame, textvariable=test_result_var, width=30).grid(row=1, column=1, padx=5, pady=5)

ttk.Button(test_frame, text="Add Result", command=add_test_result).grid(row=2, column=0, columnspan=2, pady=5)

# Results Table
columns = ("Test Name", "Result")
results_list = ttk.Treeview(root, columns=columns, show="headings", height=10)
results_list.heading("Test Name", text="Test Name")
results_list.heading("Result", text="Result")
results_list.pack(pady=10, padx=10, fill="both")

# Generate Report Button
ttk.Button(root, text="Generate PDF Report", command=generate_pdf).pack(pady=20)

# Data Storage for Test Results
test_results = {}

# Run the GUI
root.mainloop()
