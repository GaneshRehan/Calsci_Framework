class SpreadsheetUploader:
    def __init__(self, disp_out, chrs, spreadsheet):
        self.disp_out = disp_out
        self.chrs = chrs
        self.sheet = spreadsheet
        self.visible_rows = 6
        self.visible_cols = 5  
        self.row_scroll = 0
        self.col_scroll = 0
        self.disp_out.clear_display()

    def refresh(self):
        self.disp_out.clear_display()


        rows = self.sheet.row_labels
        cols = self.sheet.col_labels

        cell_width = 24
        start_x = 8 

        self.disp_out.set_page_address(0)

        visible_cols = cols[self.col_scroll:self.col_scroll + self.visible_cols]
        for idx, col in enumerate(visible_cols):
            label = col  
            col_x = start_x + idx * cell_width

            label_pixel_width = len(label) * 6
            x_offset = max((cell_width - label_pixel_width) // 2, 0)

            self.disp_out.set_column_address(col_x + x_offset)

            for ch in label:
                for b in self.chrs.Chr2bytes(ch):
                    self.disp_out.write_data(b)
                self.disp_out.write_data(0x00)

            remaining_px = cell_width - (x_offset + label_pixel_width)
            for _ in range(remaining_px):
                self.disp_out.write_data(0x00)


                

        for col in cols[self.col_scroll:self.col_scroll + self.visible_cols]:
            col_str = " " * (2 - len(col)) + col if len(col) < 2 else col  
            for ch in col_str:
                bytes_ = self.chrs.Chr2bytes(ch)
                for b in bytes_:
                    self.disp_out.write_data(b)
                self.disp_out.write_data(0x00) 

        for i in range(self.visible_rows):
            row_idx = self.row_scroll + i
            if row_idx >= len(rows):
                break

            row_label = rows[row_idx]
            self.disp_out.set_page_address(i + 1)
            self.disp_out.set_column_address(0)

            # Draw row label (e.g. 'A')
            for b in self.chrs.Chr2bytes(row_label):
                self.disp_out.write_data(b)
            self.disp_out.write_data(0x00)

            self.disp_out.set_column_address(8)
            for j in range(self.visible_cols):
                col_idx = self.col_scroll + j
                if col_idx >= len(cols):
                    break

                cell_id = f"{row_label}{cols[col_idx]}"
                val = self.sheet.get_cell_value(cell_id).strip()

                if len(val) <= 3:
                    display_val = val + " " * (4 - len(val))
                else:
                    display_val = val[:2] + ". "

                for char in display_val:
                    if self.sheet.current_cell == cell_id:
                        data = self.chrs.invert_letter(char)
                    else:
                        data = self.chrs.Chr2bytes(char)
                    for b in data:
                        self.disp_out.write_data(b)
                    self.disp_out.write_data(0x00)

        self.disp_out.set_page_address(7)
        self.disp_out.set_column_address(0)

        label = f"{self.sheet.current_cell}: "

        if self.sheet.in_input_mode:
            content = self.sheet.temp_value
            full = label + content + "_"
        else:
            content = self.sheet.get_cell_value().strip()
            full = label + content

        for ch in full:
            bytes_ = self.chrs.Chr2bytes(ch)
            for b in bytes_:
                self.disp_out.write_data(b)
            self.disp_out.write_data(0x00)


    def update_scroll(self):
        cur_row = self.sheet.row_labels.index(self.sheet.current_cell[0])
        cur_col = self.sheet.col_labels.index(self.sheet.current_cell[1:])

        if cur_row < self.row_scroll:
            self.row_scroll = cur_row
        elif cur_row >= self.row_scroll + self.visible_rows:
            self.row_scroll = cur_row - self.visible_rows + 1

        if cur_col < self.col_scroll:
            self.col_scroll = cur_col
        elif cur_col >= self.col_scroll + self.visible_cols:
            self.col_scroll = cur_col - self.visible_cols + 1
