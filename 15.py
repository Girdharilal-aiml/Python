"""
Age Calculator - Modern UI
Calculate exact age with detailed breakdown
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
from datetime import datetime, date

class AgeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Calculator")
        self.root.geometry("550x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.result_font = tkfont.Font(family='Arial', size=48, weight='bold')

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🎂",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Age Calculator",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Input card
        input_card = tk.Frame(main_frame, bg='#161b22')
        input_card.pack(fill=tk.X, pady=10)

        # Birth date section
        birth_frame = tk.Frame(input_card, bg='#161b22')
        birth_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            birth_frame,
            text="Birth Date:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', pady=(0, 10))

        date_inputs = tk.Frame(birth_frame, bg='#161b22')
        date_inputs.pack(fill=tk.X)

        # Day
        day_frame = tk.Frame(date_inputs, bg='#161b22')
        day_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Label(day_frame, text="Day", font=('Arial', 9), bg='#161b22', fg='#8b949e').pack(anchor='w')
        self.day_var = tk.StringVar()
        day_spin = tk.Spinbox(
            day_frame,
            from_=1,
            to=31,
            textvariable=self.day_var,
            font=('Arial', 16),
            bg='#0d1117',
            fg='#c9d1d9',
            buttonbackground='#21262d',
            relief=tk.FLAT,
            bd=0,
            width=8
        )
        day_spin.pack(fill=tk.X, ipady=8)

        # Month
        month_frame = tk.Frame(date_inputs, bg='#161b22')
        month_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(month_frame, text="Month", font=('Arial', 9), bg='#161b22', fg='#8b949e').pack(anchor='w')
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"],
            state='readonly',
            font=('Arial', 12),
            width=10
        )
        month_combo.pack(fill=tk.X, ipady=6)
        month_combo.current(0)

        # Year
        year_frame = tk.Frame(date_inputs, bg='#161b22')
        year_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        tk.Label(year_frame, text="Year", font=('Arial', 9), bg='#161b22', fg='#8b949e').pack(anchor='w')
        self.year_var = tk.StringVar()
        year_spin = tk.Spinbox(
            year_frame,
            from_=1900,
            to=datetime.now().year,
            textvariable=self.year_var,
            font=('Arial', 16),
            bg='#0d1117',
            fg='#c9d1d9',
            buttonbackground='#21262d',
            relief=tk.FLAT,
            bd=0,
            width=10
        )
        year_spin.pack(fill=tk.X, ipady=8)

        # Calculate button
        calc_btn = tk.Button(
            main_frame,
            text="Calculate Age",
            command=self.calculate_age,
            bg='#238636',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            activebackground='#2ea043',
            activeforeground='white'
        )
        calc_btn.pack(pady=25, ipadx=40, ipady=12)

        # Result card
        result_card = tk.Frame(main_frame, bg='#161b22')
        result_card.pack(fill=tk.BOTH, expand=True, pady=10)

        # Main age display
        self.age_label = tk.Label(
            result_card,
            text="--",
            font=self.result_font,
            bg='#161b22',
            fg='#8b949e'
        )
        self.age_label.pack(pady=(30, 5))

        tk.Label(
            result_card,
            text="Years Old",
            font=('Arial', 14),
            bg='#161b22',
            fg='#8b949e'
        ).pack()

        # Detailed breakdown
        detail_frame = tk.Frame(result_card, bg='#161b22')
        detail_frame.pack(pady=20, padx=30)

        self.details_label = tk.Label(
            detail_frame,
            text="",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e',
            justify='left'
        )
        self.details_label.pack()

        # Fun facts
        self.facts_label = tk.Label(
            result_card,
            text="Enter your birth date to calculate age",
            font=('Arial', 11),
            bg='#161b22',
            fg='#8b949e',
            wraplength=450,
            justify='center'
        )
        self.facts_label.pack(pady=(10, 30))

    def calculate_age(self):
        try:
            # Get birth date
            day = int(self.day_var.get())
            month_name = self.month_var.get()
            year = int(self.year_var.get())

            # Convert month name to number
            months = ["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"]
            month = months.index(month_name) + 1

            birth_date = date(year, month, day)
            today = date.today()

            # Check if birth date is in future
            if birth_date > today:
                self.show_error("Birth date cannot be in the future!")
                return

            # Calculate age
            age_years = today.year - birth_date.year
            age_months = today.month - birth_date.month
            age_days = today.day - birth_date.day

            # Adjust if current month/day is before birth month/day
            if age_days < 0:
                age_months -= 1
                # Get days in previous month
                if today.month == 1:
                    prev_month_days = 31
                else:
                    prev_month = today.month - 1
                    if prev_month in [1, 3, 5, 7, 8, 10, 12]:
                        prev_month_days = 31
                    elif prev_month in [4, 6, 9, 11]:
                        prev_month_days = 30
                    else:  # February
                        if today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0):
                            prev_month_days = 29
                        else:
                            prev_month_days = 28
                age_days += prev_month_days

            if age_months < 0:
                age_years -= 1
                age_months += 12

            # Display main age
            self.age_label.config(text=str(age_years), fg='#58a6ff')

            # Calculate total time lived
            total_days = (today - birth_date).days
            total_weeks = total_days // 7
            total_months = age_years * 12 + age_months
            total_hours = total_days * 24
            total_minutes = total_hours * 60

            # Detailed breakdown
            details = f"📅 {age_years} years, {age_months} months, {age_days} days\n\n"
            details += f"📊 Total:\n"
            details += f"   • {total_months:,} months\n"
            details += f"   • {total_weeks:,} weeks\n"
            details += f"   • {total_days:,} days\n"
            details += f"   • {total_hours:,} hours\n"
            details += f"   • {total_minutes:,} minutes"

            self.details_label.config(text=details, fg='#c9d1d9')

            # Calculate next birthday
            next_birthday = date(today.year, birth_date.month, birth_date.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
            days_to_birthday = (next_birthday - today).days

            # Fun facts
            facts = f"🎉 Next birthday in {days_to_birthday} days!\n"
            
            if age_years < 1:
                facts += "You're still a baby! 👶"
            elif age_years < 13:
                facts += "You're a kid! Enjoy your childhood! 🎈"
            elif age_years < 20:
                facts += "You're a teenager! 🌟"
            elif age_years < 30:
                facts += "You're in your twenties! 🚀"
            elif age_years < 50:
                facts += "You're in your prime! 💪"
            elif age_years < 65:
                facts += "You've got great experience! 🎯"
            else:
                facts += "Wisdom comes with age! 👑"

            self.facts_label.config(text=facts, fg='#8b949e')

        except ValueError:
            self.show_error("Please enter a valid date!")

    def show_error(self, message):
        self.age_label.config(text="Error", fg='#f85149')
        self.details_label.config(text="", fg='#8b949e')
        self.facts_label.config(text=message, fg='#f85149')

def main():
    root = tk.Tk()
    app = AgeCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()