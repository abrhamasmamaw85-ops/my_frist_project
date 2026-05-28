import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import json
import os

# --- DISEASE DATABASE ---
DISEASE_DATABASE = {
    'Malaria': {
        'symptoms': ['fever', 'chills', 'headache', 'nausea', 'sweating', 'fatigue', 'muscle_pain'],
        'severity': 'High',
        'meds': [{'name': 'Artemether/Lumefantrine', 'dosage': '1 tab twice daily', 'purpose': 'Antimalarial'}],
        'advice': 'Sleep under a mosquito net and complete full course of medication.'
    },
    'Influenza (Flu)': {
        'symptoms': ['fever', 'dry_cough', 'headache', 'joint_pain', 'fatigue', 'sore_throat', 'runny_nose'],
        'severity': 'Moderate',
        'meds': [{'name': 'Oseltamivir', 'dosage': '75mg once daily', 'purpose': 'Antiviral'}],
        'advice': 'Rest, stay hydrated, and avoid contact with others.'
    },
    'COVID-19': {
        'symptoms': ['fever', 'dry_cough', 'shortness_breath', 'fatigue', 'loss_taste_smell', 'sore_throat', 'headache'],
        'severity': 'High',
        'meds': [{'name': 'Paxlovid', 'dosage': '300mg twice daily', 'purpose': 'Antiviral'}],
        'advice': 'Isolate immediately, monitor oxygen levels, seek medical attention if breathing worsens.'
    },
    'Common Cold': {
        'symptoms': ['runny_nose', 'sore_throat', 'dry_cough', 'headache', 'fatigue'],
        'severity': 'Low',
        'meds': [{'name': 'Paracetamol', 'dosage': '500mg every 6 hours', 'purpose': 'Fever and pain relief'}],
        'advice': 'Rest, drink warm fluids, and use saline nasal spray.'
    },
    'Pneumonia': {
        'symptoms': ['fever', 'dry_cough', 'shortness_breath', 'chest_pain', 'fatigue', 'sweating', 'chills'],
        'severity': 'High',
        'meds': [{'name': 'Amoxicillin', 'dosage': '500mg three times daily', 'purpose': 'Antibiotic'}],
        'advice': 'Seek immediate medical attention, complete full antibiotic course, get chest X-ray.'
    },
    'Bronchitis': {
        'symptoms': ['dry_cough', 'shortness_breath', 'fatigue', 'chest_pain', 'headache'],
        'severity': 'Moderate',
        'meds': [{'name': 'Dextromethorphan', 'dosage': '20mg every 4 hours', 'purpose': 'Cough suppressant'}],
        'advice': 'Use humidifier, avoid smoke, drink warm tea with honey.'
    },
    'Dengue Fever': {
        'symptoms': ['fever', 'headache', 'joint_pain', 'nausea', 'fatigue', 'muscle_pain', 'rash'],
        'severity': 'High',
        'meds': [{'name': 'Paracetamol', 'dosage': '500mg every 6 hours', 'purpose': 'Fever and pain relief'}],
        'advice': 'Avoid NSAIDs like ibuprofen, increase fluid intake, monitor for bleeding signs.'
    },
    'Allergies': {
        'symptoms': ['runny_nose', 'sore_throat', 'headache', 'fatigue'],
        'severity': 'Low',
        'meds': [{'name': 'Cetirizine', 'dosage': '10mg once daily', 'purpose': 'Antihistamine'}],
        'advice': 'Avoid allergens, use air purifier, keep windows closed.'
    },
    'Tuberculosis': {
        'symptoms': ['dry_cough', 'fever', 'sweating', 'fatigue', 'chest_pain'],
        'severity': 'High',
        'meds': [{'name': 'Rifampicin', 'dosage': '600mg daily', 'purpose': 'Antibiotic'}],
        'advice': 'Complete 6-month treatment course, isolate until non-infectious, wear mask.'
    }
}

SYMPTOM_QUESTIONS = [
    {'id': 'fever', 'text': 'Do you have a high fever (above 101°F/38.3°C)?'},
    {'id': 'chills', 'text': 'Are you experiencing chills or shivering?'},
    {'id': 'chest_pain', 'text': 'Do you have sharp chest pain?'},
    {'id': 'dry_cough', 'text': 'Do you have a dry cough?'},
    {'id': 'shortness_breath', 'text': 'Is it difficult to breathe or shortness of breath?'},
    {'id': 'headache', 'text': 'Do you have a severe headache?'},
    {'id': 'nausea', 'text': 'Do you feel nauseous or vomiting?'},
    {'id': 'joint_pain', 'text': 'Do you have joint or muscle pain?'},
    {'id': 'fatigue', 'text': 'Are you experiencing extreme fatigue or tiredness?'},
    {'id': 'sweating', 'text': 'Do you have night sweats or excessive sweating?'},
    {'id': 'sore_throat', 'text': 'Do you have a sore throat?'},
    {'id': 'runny_nose', 'text': 'Do you have a runny or stuffy nose?'},
    {'id': 'loss_taste_smell', 'text': 'Have you lost your sense of taste or smell?'},
    {'id': 'rash', 'text': 'Do you have any skin rash or spots?'},
    {'id': 'muscle_pain', 'text': 'Do you have generalized muscle aches?'}
]

class AdvancedMedicalAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Medical Suite v3.0")
        self.root.geometry("1300x750")
        
        self.current_patient = None
        self.current_patient_id = None
        self.current_address = None
        self.current_phone = None
        self.answers = {}
        self.history_data = []
        self.symptom_widgets = {}
        self.top_diag = "None"
        self.top_score = 0
        self.top_severity = "Unknown"
        self.top_meds = []
        self.top_advice = ""
        
        # Load saved history from file
        self.load_history_from_file()
        self.setup_ui()
        self.refresh_history_display()

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#1a73e8', height=80)
        header.pack(fill='x')
        tk.Label(header, text="AI MEDICAL SUITE: DIAGNOSIS & HISTORY", 
                 fg="white", bg='#1a73e8', font=('Segoe UI', 22, 'bold')).pack(side='left', padx=30)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        self.tab_reg = ttk.Frame(self.notebook)
        self.tab_check = ttk.Frame(self.notebook)
        self.tab_result = ttk.Frame(self.notebook)
        self.tab_meds = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_reg, text="1. Registration")
        self.notebook.add(self.tab_check, text="2. Symptom Checker")
        self.notebook.add(self.tab_result, text="3. Diagnosis Report")
        self.notebook.add(self.tab_meds, text="4. Treatment & Medication")
        self.notebook.add(self.tab_history, text="5. History Records")

        self.init_reg_tab()
        self.init_check_tab()
        self.init_result_tab()
        self.init_meds_tab()
        self.init_history_tab()

    def init_reg_tab(self):
        main_frame = tk.Frame(self.tab_reg)
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        center = tk.Frame(scrollable_frame, bg='white', padx=30, pady=20, relief='groove', borderwidth=2)
        center.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(center, text="PATIENT REGISTRATION FORM", font=('Segoe UI', 16, 'bold'), bg='white', fg='#1a73e8').pack(pady=(0, 15))
        
        # Patient ID
        tk.Label(center, text="Patient ID:", font=('Segoe UI', 11), bg='white', anchor='w').pack(fill='x', pady=(5, 0))
        self.id_entry = ttk.Entry(center, font=('Segoe UI', 12), width=40)
        self.id_entry.pack(fill='x', pady=2)
        
        id_btn_frame = tk.Frame(center, bg='white')
        id_btn_frame.pack(fill='x', pady=(2, 8))
        ttk.Button(id_btn_frame, text="Generate Auto ID", command=self.generate_auto_id).pack(side='left')
        tk.Label(id_btn_frame, text="(Leave empty for auto-generation)", font=('Segoe UI', 8), bg='white', fg='gray').pack(side='left', padx=10)
        
        # Full Name
        tk.Label(center, text="Full Name (*Required):", font=('Segoe UI', 11), bg='white', anchor='w').pack(fill='x', pady=(5, 0))
        self.name_entry = ttk.Entry(center, font=('Segoe UI', 12), width=40)
        self.name_entry.pack(fill='x', pady=2)
        
        # Address
        tk.Label(center, text="Address (*Required):", font=('Segoe UI', 11), bg='white', anchor='w').pack(fill='x', pady=(5, 0))
        self.address_entry = tk.Text(center, font=('Segoe UI', 11), height=2, width=40, wrap=tk.WORD)
        self.address_entry.pack(fill='x', pady=2)
        
        # Phone Number
        tk.Label(center, text="Phone Number (*Required):", font=('Segoe UI', 11), bg='white', anchor='w').pack(fill='x', pady=(5, 0))
        self.phone_entry = ttk.Entry(center, font=('Segoe UI', 12), width=40)
        self.phone_entry.pack(fill='x', pady=2)
        
        button_frame = tk.Frame(center, bg='white')
        button_frame.pack(fill='x', pady=(15, 5))
        ttk.Button(button_frame, text="Load Demo Data", command=self.load_demo_data).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_registration_form).pack(side='left', padx=5)
        
        register_btn = tk.Button(center, text="✓ REGISTER PATIENT", font=('Segoe UI', 14, 'bold'), bg='#4CAF50', fg='white', padx=30, pady=10, command=self.register)
        register_btn.pack(pady=(10, 5))
        
        info_label = tk.Label(center, text="After registration, go to Symptom Checker tab", font=('Segoe UI', 9), fg='gray', bg='white')
        info_label.pack(pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def clear_registration_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete('1.0', tk.END)
        self.phone_entry.delete(0, tk.END)
        messagebox.showinfo("Form Cleared", "Registration form has been cleared.")

    def generate_auto_id(self):
        auto_id = f"PAT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, auto_id)
        messagebox.showinfo("Auto ID Generated", f"Patient ID generated: {auto_id}")

    def load_demo_data(self):
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, "PAT20241215001")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, "John Michael Smith")
        self.address_entry.delete('1.0', tk.END)
        self.address_entry.insert('1.0', "123 Main Street, Apartment 4B\nNew York, NY 10001")
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, "+1 (555) 123-4567")
        messagebox.showinfo("Demo Data Loaded", "Demo patient data has been loaded.\n\nClick 'REGISTER PATIENT' to continue.")

    def init_check_tab(self):
        self.status_lbl = tk.Label(self.tab_check, text="⚠️ Please register a patient first", font=('Segoe UI', 12), fg='red', pady=10)
        self.status_lbl.pack()
        
        self.patient_info_frame = tk.Frame(self.tab_check, bg='#f0f0f0', relief='ridge', borderwidth=1)
        self.patient_info_frame.pack(fill='x', padx=20, pady=10)
        self.patient_info_label = tk.Label(self.patient_info_frame, text="", font=('Segoe UI', 10), bg='#f0f0f0')
        self.patient_info_label.pack(pady=5)
        
        instructions = tk.Label(self.tab_check, text="Answer the following questions about the patient's symptoms:", font=('Segoe UI', 11, 'bold'))
        instructions.pack(pady=10)
        
        canvas_frame = tk.Frame(self.tab_check)
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for s in SYMPTOM_QUESTIONS:
            row = tk.Frame(scrollable_frame, pady=5)
            row.pack(fill='x', padx=20)
            tk.Label(row, text=s['text'], font=('Segoe UI', 10), width=45, anchor='w').pack(side='left')
            y = tk.Button(row, text="Yes", width=8, bg="#e6f4ea", command=lambda sid=s['id']: self.set_ans(sid, 'yes'))
            y.pack(side='left', padx=5)
            n = tk.Button(row, text="No", width=8, bg="#fce8e6", command=lambda sid=s['id']: self.set_ans(sid, 'no'))
            n.pack(side='left', padx=5)
            self.symptom_widgets[s['id']] = {'y': y, 'n': n}
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ===== VISIBLE BUTTONS SECTION =====
        action_frame = tk.Frame(self.tab_check, bg='#f8f9fa', relief='ridge', bd=2)
        action_frame.pack(fill='x', pady=15, padx=20)
        
        # Reset button
        reset_btn = tk.Button(action_frame, text="🔄 Reset All Answers", font=('Segoe UI', 11, 'bold'), 
                              bg='#e74c3c', fg='white', padx=15, pady=8, 
                              command=self.reset_answers)
        reset_btn.pack(side='left', padx=20, pady=10)
        
        # CHECK DIAGNOSIS Button - Large, green, and very visible
        check_btn = tk.Button(action_frame, text="🔍 CHECK DIAGNOSIS", font=('Segoe UI', 14, 'bold'), 
                              bg='#27ae60', fg='white', padx=40, pady=12, 
                              command=self.check_and_view_report)
        check_btn.pack(side='left', padx=20, pady=10, expand=True, fill='x')
        
        # Instruction banner
        instruction_banner = tk.Frame(self.tab_check, bg='#e8f0fe', height=40)
        instruction_banner.pack(fill='x', padx=20, pady=(0, 10))
        
        instruction_label = tk.Label(instruction_banner, 
                                      text="💡 TIP: After selecting symptoms above, click the GREEN 'CHECK DIAGNOSIS' button to analyze and view results", 
                                      font=('Segoe UI', 10, 'bold'), 
                                      fg='#1a73e8', bg='#e8f0fe', pady=8)
        instruction_label.pack()

    def check_and_view_report(self):
        """Run analysis and automatically switch to Diagnosis Report tab"""
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please register a patient first!")
            self.notebook.select(self.tab_reg)
            return
        
        # Check if any symptoms have been answered
        yes_count = len([v for v in self.answers.values() if v == 'yes'])
        
        if yes_count == 0:
            messagebox.showwarning("No Symptoms", "Please answer at least one symptom question first!")
            return
        
        # Run the analysis
        self.run_analysis()
        
        # Show confirmation message
        messagebox.showinfo("Analysis Complete", f"✅ Diagnosis analysis completed!\n\n📊 {yes_count} symptoms reported\n🏥 Top diagnosis: {self.top_diag}\n📈 Confidence: {self.top_score:.1f}%")
        
        # Automatically switch to Diagnosis Report tab
        self.notebook.select(self.tab_result)

    def init_result_tab(self):
        main_frame = tk.Frame(self.tab_result)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.diag_display = scrolledtext.ScrolledText(main_frame, font=('Consolas', 11), height=25)
        self.diag_display.pack(fill='both', expand=True)
        
        # Button frame for result tab actions
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        view_treatment_btn = tk.Button(button_frame, text="💊 View Treatment Plan", font=('Segoe UI', 10, 'bold'),
                                       bg='#27ae60', fg='white', padx=15, pady=5,
                                       command=lambda: self.notebook.select(self.tab_meds))
        view_treatment_btn.pack(side='left', padx=5)
        
        save_history_btn = tk.Button(button_frame, text="💾 Save to History", font=('Segoe UI', 10, 'bold'),
                                     bg='#f39c12', fg='white', padx=15, pady=5,
                                     command=self.save_to_history)
        save_history_btn.pack(side='left', padx=5)
        
        info_label = tk.Label(main_frame, text="📋 Diagnosis Report - Click 'View Treatment Plan' for medications or 'Save to History' to store record", 
                              font=('Segoe UI', 9), fg='blue', pady=5)
        info_label.pack()

    def init_meds_tab(self):
        main_frame = tk.Frame(self.tab_meds)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.meds_display = scrolledtext.ScrolledText(main_frame, font=('Consolas', 11), height=20)
        self.meds_display.pack(fill='both', expand=True)
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.save_button_meds = tk.Button(button_frame, text="💾 SAVE TREATMENT TO HISTORY", font=('Segoe UI', 12, 'bold'), 
                                          bg='#4CAF50', fg='white', padx=20, pady=10, 
                                          command=self.save_to_history)
        self.save_button_meds.pack()
        
        back_to_diagnosis_btn = tk.Button(button_frame, text="🔍 Back to Diagnosis", font=('Segoe UI', 10),
                                          bg='#3498db', fg='white', padx=15, pady=5,
                                          command=lambda: self.notebook.select(self.tab_result))
        back_to_diagnosis_btn.pack(pady=5)
        
        instruction = tk.Label(button_frame, text="Click the button above to save this treatment plan to history", font=('Segoe UI', 9), fg='gray')
        instruction.pack(pady=5)

    def init_history_tab(self):
        main_frame = tk.Frame(self.tab_history)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        title = tk.Label(main_frame, text="PATIENT HISTORY RECORDS", font=('Segoe UI', 14, 'bold'))
        title.pack(pady=10)
        
        columns = ('date', 'id', 'name', 'diagnosis', 'confidence', 'severity')
        self.history_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        self.history_tree.heading('date', text='Date/Time')
        self.history_tree.heading('id', text='Patient ID')
        self.history_tree.heading('name', text='Patient Name')
        self.history_tree.heading('diagnosis', text='Diagnosis')
        self.history_tree.heading('confidence', text='Confidence')
        self.history_tree.heading('severity', text='Severity')
        
        self.history_tree.column('date', width=140)
        self.history_tree.column('id', width=120)
        self.history_tree.column('name', width=160)
        self.history_tree.column('diagnosis', width=160)
        self.history_tree.column('confidence', width=80)
        self.history_tree.column('severity', width=80)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="🔄 Refresh", command=self.refresh_history_display).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ Clear All", command=self.clear_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📋 View Details", command=self.view_selected_record).pack(side='left', padx=5)
        
        self.history_status = tk.Label(main_frame, text="", font=('Segoe UI', 9))
        self.history_status.pack(pady=5)
        
        # Bind double-click event
        self.history_tree.bind('<Double-Button-1>', lambda event: self.view_selected_record())

    def register(self):
        patient_id = self.id_entry.get().strip()
        if not patient_id:
            patient_id = f"PAT{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.id_entry.insert(0, patient_id)
        
        name = self.name_entry.get().strip()
        address = self.address_entry.get('1.0', tk.END).strip()
        phone = self.phone_entry.get().strip()
        
        if not name:
            messagebox.showerror("Validation Error", "Please enter patient's full name!")
            return
        if not address:
            messagebox.showerror("Validation Error", "Please enter patient's address!")
            return
        if not phone:
            messagebox.showerror("Validation Error", "Please enter patient's phone number!")
            return
        
        self.current_patient = name
        self.current_patient_id = patient_id
        self.current_address = address
        self.current_phone = phone
        
        self.answers = {}
        self.top_diag = "None"
        self.top_score = 0
        self.top_severity = "Unknown"
        self.top_meds = []
        self.top_advice = ""
        
        for sw in self.symptom_widgets.values():
            sw['y'].config(bg="#e6f4ea", fg="black")
            sw['n'].config(bg="#fce8e6", fg="black")
        
        self.diag_display.delete('1.0', tk.END)
        self.meds_display.delete('1.0', tk.END)
        self.status_lbl.config(text=f"✅ Active Patient: {name} (ID: {patient_id})", fg='green')
        self.patient_info_label.config(text=f"👤 {name} | 🆔 {patient_id} | 📞 {phone}", font=('Segoe UI', 10, 'bold'))
        
        msg = f"✅ PATIENT REGISTERED SUCCESSFULLY!\n\n🆔 ID: {patient_id}\n👤 Name: {name}\n📍 Address: {address}\n📞 Phone: {phone}\n\nClick OK to go to Symptom Checker."
        messagebox.showinfo("Registration Successful", msg)
        self.notebook.select(self.tab_check)

    def reset_answers(self):
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please register a patient first!")
            return
        self.answers = {}
        for sw in self.symptom_widgets.values():
            sw['y'].config(bg="#e6f4ea", fg="black")
            sw['n'].config(bg="#fce8e6", fg="black")
        self.run_analysis()
        messagebox.showinfo("Reset", "All symptom answers have been reset.")

    def set_ans(self, sid, val):
        if not self.current_patient:
            messagebox.showwarning("No Patient", "Please register a patient first!")
            self.notebook.select(self.tab_reg)
            return
        self.answers[sid] = val
        if val == 'yes':
            self.symptom_widgets[sid]['y'].config(bg="#34a853", fg="white")
            self.symptom_widgets[sid]['n'].config(bg="#fce8e6", fg="black")
        else:
            self.symptom_widgets[sid]['n'].config(bg="#d93025", fg="white")
            self.symptom_widgets[sid]['y'].config(bg="#e6f4ea", fg="black")
        self.run_analysis()

    def run_analysis(self):
        if not self.current_patient:
            return
        self.diag_display.delete('1.0', tk.END)
        self.meds_display.delete('1.0', tk.END)
        
        yes_list = [sid for sid, v in self.answers.items() if v == 'yes']
        self.top_diag = "None"
        self.top_score = 0
        self.top_severity = "Unknown"
        self.top_meds = []
        self.top_advice = ""
        
        self.diag_display.insert(tk.END, "="*60 + "\nDIAGNOSIS REPORT\n" + "="*60 + "\n\n")
        self.diag_display.insert(tk.END, f"🆔 ID: {self.current_patient_id}\n👤 Patient: {self.current_patient}\n📍 Address: {self.current_address}\n📞 Phone: {self.current_phone}\n")
        self.diag_display.insert(tk.END, f"📊 Symptoms: {len(yes_list)} reported\n" + "="*60 + "\n\n")
        
        self.meds_display.insert(tk.END, "="*60 + "\nTREATMENT & MEDICATION PLAN\n" + "="*60 + "\n\n")
        self.meds_display.insert(tk.END, f"🆔 ID: {self.current_patient_id}\n👤 Patient: {self.current_patient}\n" + "="*60 + "\n\n")
        
        diagnoses_scores = []
        for name, data in DISEASE_DATABASE.items():
            match = set(yes_list) & set(data['symptoms'])
            if match:
                score = (len(match) / len(data['symptoms'])) * 100
                diagnoses_scores.append((name, score, data))
                self.diag_display.insert(tk.END, f"🏥 {name}\n   Confidence: {score:.1f}%\n   Severity: {data['severity']}\n" + "-"*40 + "\n\n")
                if score > self.top_score:
                    self.top_score = score
                    self.top_diag = name
                    self.top_severity = data['severity']
                    self.top_meds = data['meds']
                    self.top_advice = data['advice']
        
        if self.top_score == 0:
            self.diag_display.insert(tk.END, "❌ No matching conditions found.\n")
            self.meds_display.insert(tk.END, "❌ No specific treatment plan available.\n")
        else:
            diagnoses_scores.sort(key=lambda x: x[1], reverse=True)
            top_name, top_score, top_data = diagnoses_scores[0]
            self.meds_display.insert(tk.END, f"🏥 PRIMARY DIAGNOSIS: {top_name}\n📊 Confidence: {top_score:.1f}%\n⚠️ Severity: {top_data['severity']}\n\n")
            self.meds_display.insert(tk.END, "💊 MEDICATIONS:\n" + "-"*40 + "\n")
            for med in top_data['meds']:
                self.meds_display.insert(tk.END, f"• {med['name']}\n  Dosage: {med['dosage']}\n\n")
            self.meds_display.insert(tk.END, "📋 ADVICE:\n" + "-"*40 + f"\n• {top_data['advice']}\n")

    def save_to_history(self):
        """Save current diagnosis and treatment to history with confirmation"""
        if not self.current_patient:
            messagebox.showerror("Error", "No patient registered! Please register a patient first.")
            return
        
        if self.top_score == 0:
            if not messagebox.askyesno("No Diagnosis", "No diagnosis has been made yet. Do you want to save anyway?"):
                return
        
        # Create record
        record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'patient_id': self.current_patient_id,
            'patient': self.current_patient,
            'address': self.current_address,
            'phone': self.current_phone,
            'diagnosis': self.top_diag,
            'confidence': f"{self.top_score:.1f}%",
            'severity': self.top_severity,
            'medications': self.top_meds,
            'advice': self.top_advice,
            'symptoms': self.answers.copy()
        }
        
        # Add to history
        self.history_data.insert(0, record)
        
        # Save to file
        self.save_history_to_file()
        
        # Refresh display
        self.refresh_history_display()
        
        # Show success message
        success_msg = f"✅ RECORD SAVED SUCCESSFULLY!\n\n"
        success_msg += f"📅 Date & Time: {record['date']}\n"
        success_msg += f"🆔 Patient ID: {self.current_patient_id}\n"
        success_msg += f"👤 Patient Name: {self.current_patient}\n"
        success_msg += f"🏥 Diagnosis: {self.top_diag}\n"
        success_msg += f"📊 Confidence: {self.top_score:.1f}%\n"
        success_msg += f"⚠️ Severity: {self.top_severity}\n\n"
        success_msg += f"💾 Total records in history: {len(self.history_data)}"
        
        messagebox.showinfo("✅ SUCCESS", success_msg)
        
        # Ask if user wants to view history
        if messagebox.askyesno("View History", "Record saved successfully!\n\nWould you like to view the history records now?"):
            self.notebook.select(self.tab_history)

    def refresh_history_display(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if len(self.history_data) == 0:
            self.history_status.config(text="No records found. Save a diagnosis to see it here.", fg='orange')
        else:
            for record in self.history_data:
                self.history_tree.insert('', 'end', values=(
                    record['date'],
                    record['patient_id'],
                    record['patient'],
                    record['diagnosis'],
                    record['confidence'],
                    record['severity']
                ))
            self.history_status.config(text=f"Showing {len(self.history_data)} record(s)", fg='green')

    def view_selected_record(self):
        selection = self.history_tree.selection()
        
        if not selection:
            messagebox.showinfo("No Selection", "Please select a record first by clicking on it.")
            return
        
        selected_item = selection[0]
        values = self.history_tree.item(selected_item, 'values')
        
        if not values:
            messagebox.showwarning("Error", "Could not retrieve record details.")
            return
        
        selected_date = values[0]
        selected_patient_id = values[1]
        
        found_record = None
        for record in self.history_data:
            if record['date'] == selected_date and str(record['patient_id']) == str(selected_patient_id):
                found_record = record
                break
        
        if found_record:
            self.show_record_details(found_record)
        else:
            messagebox.showerror("Error", "Record details not found.")

    def show_record_details(self, record):
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Medical Record - {record['patient']}")
        detail_window.geometry("700x600")
        detail_window.configure(bg='white')
        
        text_frame = tk.Frame(detail_window, bg='white')
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        details_text = scrolledtext.ScrolledText(text_frame, font=('Consolas', 11), wrap=tk.WORD, height=30)
        details_text.pack(fill='both', expand=True)
        
        details_text.insert(tk.END, "="*60 + "\n")
        details_text.insert(tk.END, "COMPLETE MEDICAL RECORD\n")
        details_text.insert(tk.END, "="*60 + "\n\n")
        
        details_text.insert(tk.END, f"📅 Date & Time: {record['date']}\n")
        details_text.insert(tk.END, f"🆔 Patient ID: {record['patient_id']}\n")
        details_text.insert(tk.END, f"👤 Patient Name: {record['patient']}\n")
        details_text.insert(tk.END, f"📍 Address: {record['address']}\n")
        details_text.insert(tk.END, f"📞 Phone: {record['phone']}\n")
        details_text.insert(tk.END, f"🏥 Diagnosis: {record['diagnosis']}\n")
        details_text.insert(tk.END, f"📊 Confidence: {record['confidence']}\n")
        details_text.insert(tk.END, f"⚠️ Severity: {record['severity']}\n\n")
        
        details_text.insert(tk.END, "📋 SYMPTOMS REPORTED:\n")
        details_text.insert(tk.END, "-"*40 + "\n")
        symptom_count = 0
        for symptom, value in record.get('symptoms', {}).items():
            if value == 'yes':
                symptom_count += 1
                symptom_name = symptom.replace('_', ' ').title()
                details_text.insert(tk.END, f"  ✓ {symptom_name}\n")
        if symptom_count == 0:
            details_text.insert(tk.END, "  No symptoms recorded\n")
        details_text.insert(tk.END, "\n")
        
        if record.get('medications'):
            details_text.insert(tk.END, "💊 PRESCRIBED MEDICATIONS:\n")
            details_text.insert(tk.END, "-"*40 + "\n")
            for med in record['medications']:
                details_text.insert(tk.END, f"  • {med['name']}\n")
                details_text.insert(tk.END, f"    Dosage: {med['dosage']}\n")
                details_text.insert(tk.END, f"    Purpose: {med['purpose']}\n\n")
        
        if record.get('advice'):
            details_text.insert(tk.END, "📋 MEDICAL ADVICE:\n")
            details_text.insert(tk.END, "-"*40 + "\n")
            details_text.insert(tk.END, f"  • {record['advice']}\n\n")
        
        details_text.insert(tk.END, "="*60 + "\n")
        details_text.insert(tk.END, "END OF RECORD\n")
        details_text.insert(tk.END, "="*60)
        
        details_text.config(state='disabled')
        
        close_btn = tk.Button(detail_window, text="Close", font=('Segoe UI', 10), 
                             command=detail_window.destroy, bg='#1a73e8', fg='white', 
                             padx=20, pady=5)
        close_btn.pack(pady=10)

    def save_history_to_file(self):
        try:
            with open('medical_history.json', 'w') as f:
                json.dump(self.history_data, f, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")

    def load_history_from_file(self):
        try:
            if os.path.exists('medical_history.json'):
                with open('medical_history.json', 'r') as f:
                    self.history_data = json.load(f)
            else:
                self.history_data = []
        except Exception as e:
            print(f"Error loading: {e}")
            self.history_data = []

    def clear_history(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear ALL history records?\n\nThis action cannot be undone!"):
            self.history_data = []
            self.save_history_to_file()
            self.refresh_history_display()
            messagebox.showinfo("Success", "All history records have been cleared!")

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedMedicalAI(root)
    root.mainloop()
