import argparse
import tkinter as tk
from ui_login import LoginApp
from logger import Logger
from offline_cache import load_offline_cache

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MiniAuth utility")
    parser.add_argument("--generate-csv-report", action="store_true", help="Export logs to CSV report")
    parser.add_argument("--show-offline-cache", action="store_true", help="Outputs the current offline cache content")
    args = parser.parse_args()
    
    
    if args.generate_csv_report:
        logger = Logger()
        logger.export_to_csv()
        print(f"CSV report generated at: {logger.csv_path}")
    elif args.show_offline_cache:
        offline_cache = load_offline_cache()
        print(f"Offline Cache Content: {offline_cache}")
    else:
        root = tk.Tk()
        app = LoginApp(root)
        root.mainloop()
        