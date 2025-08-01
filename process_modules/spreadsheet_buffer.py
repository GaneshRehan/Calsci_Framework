import json
import os

class SpreadsheetBuffer:
    def __init__(self, rows=26, cols=44):
        self.row_labels = [chr(i) for i in range(65, 65 + rows)]  # ['A', 'B', ..., 'Z']
        self.col_labels = [str(i) for i in range(1, cols + 1)]    # ['1', '2', ..., '44']
        self.buffer = {f"{r}{c}": "" for r in self.row_labels for c in self.col_labels}
        self.current_cell = "A1"
        self.in_input_mode = False
        self.temp_value = ""
        self.data_file = "database/spreadsheet_data.json"
        self.load_from_file()  # Load saved data on startup

    def save_to_file(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.buffer, f)
        except Exception as e:
            print("Error saving spreadsheet data:", e)

    def load_from_file(self):
        try:
            with open(self.data_file, 'r') as f:
                self.buffer.update(json.load(f))
        except OSError:
            # File not found, skip loading
            pass
        except Exception as e:
            print("Error loading spreadsheet data:", e)


    def move(self, direction):
        row_idx = self.row_labels.index(self.current_cell[0])
        col_idx = self.col_labels.index(self.current_cell[1:])

        if direction == "up":
            row_idx = (row_idx - 1) % len(self.row_labels)
        elif direction == "down":
            row_idx = (row_idx + 1) % len(self.row_labels)
        elif direction == "left":
            col_idx = (col_idx - 1) % len(self.col_labels)
        elif direction == "right":
            col_idx = (col_idx + 1) % len(self.col_labels)

        self.current_cell = f"{self.row_labels[row_idx]}{self.col_labels[col_idx]}"


    def update_cell(self, value):
        self.buffer[self.current_cell] = value
        self.save_to_file()

        
    def get_cell_value(self, cell=None):
        cell = cell or self.current_cell
        # if self.in_input_mode and cell == self.current_cell:
        #     return self.temp_value
        return self.buffer.get(cell, "")






    def display(self):
        print("    " + " | ".join(self.col_labels) + " |")
        print("-" * (5 + len(self.col_labels) * 4))
        for r in self.row_labels:
            row = [self.buffer[f"{r}{c}"] or " " for c in self.col_labels]
            row_display = " | ".join(f"{val:2}" for val in row) + " |"
            pointer = "->" if self.current_cell.startswith(r) else "  "
            print(f"{pointer}{r} | {row_display}")

def test_spreadsheet():
    sheet = SpreadsheetBuffer()

    print("\nSpreadsheet Navigation: nav_u, nav_d, nav_l, nav_r")
    print("To enter a value, just type it.")
    print("To quit, type `exit`.\n")

    while True:
        sheet.display()
        print(f"\nCurrent Cell: {sheet.current_cell} | Value: '{sheet.get_cell_value()}'")
        cmd = input("Enter command/value: ").strip()

        if cmd.lower() == "exit":
            print("Exiting...")
            break
        elif cmd in ["nav_u", "nav_d", "nav_l", "nav_r"]:
            directions = {
                "nav_u": "up",
                "nav_d": "down",
                "nav_l": "left",
                "nav_r": "right"
            }
            sheet.move(directions[cmd])
        elif cmd:
            sheet.update_cell(cmd)

        print("\n" + "=" * 60 + "\n")


# test_spreadsheet()