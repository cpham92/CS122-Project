import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import your polymorphic classes
from models.reports import TaskCompletionReport, UserCompletionReport

class ReportWindow(tk.Toplevel):
    def __init__(self, parent, history_manager, user_id):
        super().__init__(parent)
        self.title("Productivity Analytics")
        self.geometry("800x600")
        
        self.history_manager = history_manager
        self.user_id = user_id
        
        # Fetch the history data immediately
        # This is the list of History objects that the reports will analyze
        self.history_data = self.history_manager.get_history_for_user(self.user_id)
        
        self._setup_ui()

    def _setup_ui(self):
        # --- Top Section: Controls ---
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side='top', fill='x')
        
        ttk.Label(control_frame, text="Select Report Type:", font=("Arial", 12)).pack(side='left', padx=5)
        
        # The Dropdown to switch reports
        self.report_type = tk.StringVar()
        self.combo = ttk.Combobox(control_frame, textvariable=self.report_type, state="readonly")
        self.combo['values'] = ("Task Completion", "User Breakdown")
        self.combo.current(0) # Default to first option
        self.combo.pack(side='left', padx=5)
        
        # When user changes selection, run refresh_report
        self.combo.bind("<<ComboboxSelected>>", self.refresh_report)
        
        # --- Bottom Section: Split View (Text vs Graph) ---
        split_frame = ttk.Frame(self, padding=10)
        split_frame.pack(fill='both', expand=True)
        
        # Left Side: Text Summary
        text_frame = ttk.LabelFrame(split_frame, text="Summary", padding=5)
        text_frame.pack(side='left', fill='y', padx=(0, 10))
        
        self.text_area = tk.Text(text_frame, width=30, height=20, font=("Consolas", 10))
        self.text_area.pack(fill='both', expand=True)
        
        # Right Side: Graph Area
        self.graph_frame = ttk.LabelFrame(split_frame, text="Visuals", padding=5)
        self.graph_frame.pack(side='right', fill='both', expand=True)

        # Draw the initial report
        self.refresh_report(None)

    def refresh_report(self, event):
        """
        The Master Controller for the window.
        It uses POLYMORPHISM to handle different report types identically.
        """
        # 1. Clear previous graph widgets to prevent overlapping
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # 2. Polymorphic Factory: Pick the class based on dropdown
        selection = self.combo.get()
        report_engine = None

        if selection == "Task Completion":
            report_engine = TaskCompletionReport(self.history_data)
        elif selection == "User Breakdown":
            report_engine = UserCompletionReport(self.history_data)

        if not report_engine:
            return

        # 3. Update Text (The Report object knows how to generate its own text)
        text_summary = report_engine.generate_text()
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", text_summary)

        # 4. Update Graph (The Report object knows how to format its own data)
        chart_data = report_engine.get_chart_data()
        self._draw_graph(chart_data, title=selection)

    def _draw_graph(self, data, title):
        """
        Draws a Matplotlib bar chart into the Tkinter window.
        """
        if not data:
            self.text_area.insert(tk.END, "\n[No data for graph]")
            return

        # Create a Figure (the blank canvas)
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Extract data for plotting
        labels = list(data.keys())
        values = list(data.values())

        # Draw the bar chart
        bars = ax.bar(labels, values, color='#4CAF50')
        
        # Styling
        ax.set_title(title)
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45) # Rotate labels if they are long
        
        # Fix layout to prevent labels being cut off
        fig.tight_layout()

        # Render onto Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)