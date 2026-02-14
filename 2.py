"""
To-Do List App
Lightweight GUI app using tkinter

FEATURES:
- Add, delete, and mark tasks as complete
- Tasks save automatically to a file
- Priority levels (High, Medium, Low)
- Search/filter tasks
- Clean, simple interface
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # File to save tasks
        self.data_file = "tasks.json"
        self.tasks = []
        
        # Load existing tasks
        self.load_tasks()
        
        # Title
        title_label = tk.Label(
            root, 
            text="📝 My To-Do List", 
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(root, bg='#f0f0f0')
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.task_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=30
        )
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority dropdown
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = tk.OptionMenu(
            input_frame,
            self.priority_var,
            "High",
            "Medium",
            "Low"
        )
        priority_menu.config(width=8)
        priority_menu.pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2'
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(root, bg='#f0f0f0')
        search_frame.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Label(search_frame, text="🔍 Search:", bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_tasks())
        
        clear_search_btn = tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            font=('Arial', 8)
        )
        clear_search_btn.pack(side=tk.LEFT, padx=5)
        
        # Task list frame with scrollbar
        list_frame = tk.Frame(root, bg='white')
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            bg='white',
            height=15
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Buttons frame
        button_frame = tk.Frame(root, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        complete_btn = tk.Button(
            button_frame,
            text="✓ Mark Complete",
            command=self.mark_complete,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            width=15
        )
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            button_frame,
            text="🗑 Delete",
            command=self.delete_task,
            bg='#f44336',
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            width=15
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        clear_all_btn = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            bg='#FF9800',
            fg='white',
            font=('Arial', 10),
            cursor='hand2',
            width=15
        )
        clear_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats label
        self.stats_label = tk.Label(
            root,
            text="",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#666'
        )
        self.stats_label.pack(pady=5)
        
        # Initial display
        self.display_tasks()
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task!")
            return
        
        task = {
            'text': task_text,
            'priority': self.priority_var.get(),
            'completed': False,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.display_tasks()
        
        # Clear entry
        self.task_entry.delete(0, tk.END)
        self.task_entry.focus()
        
    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            
            # Get actual task index (accounting for filtering)
            display_text = self.task_listbox.get(selected_index)
            
            # Find task in original list
            for task in self.tasks:
                if task['text'] in display_text and not task['completed']:
                    task['completed'] = True
                    self.save_tasks()
                    self.display_tasks()
                    break
                    
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to mark as complete!")
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            display_text = self.task_listbox.get(selected_index)
            
            # Find and remove task
            for i, task in enumerate(self.tasks):
                if task['text'] in display_text:
                    if messagebox.askyesno("Delete Task", f"Delete: {task['text']}?"):
                        self.tasks.pop(i)
                        self.save_tasks()
                        self.display_tasks()
                    break
                    
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete!")
    
    def clear_all(self):
        if self.tasks and messagebox.askyesno("Clear All", "Delete all tasks?"):
            self.tasks.clear()
            self.save_tasks()
            self.display_tasks()
    
    def filter_tasks(self):
        search_term = self.search_entry.get().lower()
        
        self.task_listbox.delete(0, tk.END)
        
        for task in self.tasks:
            if search_term in task['text'].lower():
                self.add_task_to_listbox(task)
        
        self.update_stats()
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.display_tasks()
    
    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        
        # Sort by priority and completion
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        sorted_tasks = sorted(
            self.tasks,
            key=lambda x: (x['completed'], priority_order[x['priority']])
        )
        
        for task in sorted_tasks:
            self.add_task_to_listbox(task)
        
        self.update_stats()
    
    def add_task_to_listbox(self, task):
        # Color coding
        if task['completed']:
            prefix = "✓ [DONE]"
            color = '#888888'
        elif task['priority'] == 'High':
            prefix = "🔴 [HIGH]"
            color = '#d32f2f'
        elif task['priority'] == 'Medium':
            prefix = "🟡 [MED]"
            color = '#f57c00'
        else:
            prefix = "🟢 [LOW]"
            color = '#388e3c'
        
        display_text = f"{prefix} {task['text']}"
        
        self.task_listbox.insert(tk.END, display_text)
        
        # Set color
        index = self.task_listbox.size() - 1
        self.task_listbox.itemconfig(index, fg=color)
        
        if task['completed']:
            self.task_listbox.itemconfig(index, fg='#888888')
    
    def update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        self.stats_label.config(
            text=f"Total: {total} | Completed: {completed} | Pending: {pending}"
        )
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save tasks: {e}")
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()