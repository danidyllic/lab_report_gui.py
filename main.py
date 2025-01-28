import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fpdf import FPDF
import os

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

    # Ask user for save location
    save_path = filedialog.askdirectory()
    if not save_path:
        return

    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add logo and header
    logo_path = "lab_logo.png"  # Replace with your lab's logo file
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=30)
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, "Medical Laboratory Report", ln=True, align="C")
    pdf.ln(20)
    
    # Patient Details
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(100, 10, f"Age: {age}", ln=True)
    pdf.ln(10)
    
    # Test Results Table
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(100, 10, "Test", border=1)
    pdf.cell(40, 10, "Result", border=1)
    pdf.cell(50, 10, "Normal Range", border=1, ln=True)
    pdf.set_font("Arial", size=12)
    for test, result in test_results.items():
        pdf.cell(100, 10, test, border=1)
        pdf.cell(40, 10, str(result), border=1)
        pdf.cell(50, 10, test_ranges.get(test, "N/A"), border=1, ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Thank you for choosing our lab!", ln=True, align="C")
    
    # Save the PDF
    filename = f"{patient_name.replace(' ', '_')}_Lab_Report.pdf"
    pdf.output(os.path.join(save_path, filename))
    messagebox.showinfo("Success", f"Report saved as {os.path.join(save_path, filename)}")

# Function to add test results
def add_test_result():
    test_name = test_name_var.get()
    test_result = test_result_var.get()
    if not test_name or not test_result:
        messagebox.showerror("Error", "Please enter both test name and result.")
        return
    
    test_results[test_name] = test_result
    results_list.insert("", "end", values=(test_name, test_result, test_ranges.get(test_name, "N/A")))
    test_name_var.set("")
    test_result_var.set("")

# Function to clear the table
def clear_table():
    results_list.delete(*results_list.get_children())
    test_results.clear()

# GUI Setup
root = tk.Tk()
root.title("Enhanced Medical Lab Report Generator")
root.geometry("600x700")

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
columns = ("Test Name", "Result", "Normal Range")
results_list = ttk.Treeview(root, columns=columns, show="headings", height=10)
results_list.heading("Test Name", text="Test Name")
results_list.heading("Result", text="Result")
results_list.heading("Normal Range", text="Normal Range")
results_list.pack(pady=10, padx=10, fill="both")

# Clear Table and Generate Report Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Clear Table", command=clear_table).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Generate PDF Report", command=generate_pdf).grid(row=0, column=1, padx=10)

# Data Storage
test_results = {}
test_ranges = {
    "Blood Sugar": "70-110 mg/dL",
    "Cholesterol": "<200 mg/dL",
    "Hemoglobin": "12-16 g/dL",
    "Blood Pressure": "120/80 mmHg",
}

# Run the GUI
root.mainloop()
