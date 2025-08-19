import argparse
import tkinter as tk
from ui_login import LoginApp
from logger import Logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Logger utility")
    parser.add_argument("--generate-csv-report", action="store_true", help="Export logs to CSV report")
    args = parser.parse_args()
    
    if args.generate_csv_report:
        logger = Logger()
        logger.export_to_csv()
        print(f"CSV report generated at: {logger.csv_path}")
    else:
        root = tk.Tk()
        app = LoginApp(root)
        root.mainloop()
        