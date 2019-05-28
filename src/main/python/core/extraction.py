# Author: Dahir Muhammad Dahir
# Date: 15th-05-2019 10:43 PM
# this module requires python3

from datetime import datetime, timedelta
from core.unique import Unique
from core.error import Error
import re


class Extract(Error, Unique):
    def __init__(self, filename=None, filenames=None):
        Unique.__init__(self)
        self.make_chain()
        self.filename = filename
        self.filenames = filenames
        self.time_start = re.compile(r"^Time of start of window")
        self.time_end = re.compile("^Time of {2}end {2}of window")
        self.data_point_begin = re.compile(r"^4-character ID")
        self.data_second_to_end = re.compile(r"^SMP\s*\d\s*")
        self.data_point_end = re.compile(r"^SUM\s*\d\s*")
        self.continued_line = re.compile(r"^\s{20,}")
        self.empty_line = re.compile("^\s*$")
        self.invalid_line = re.compile("^ \* or unknown elevation")
        self.invalid_line1 = re.compile(r"^\s*first epoch")
        self.data_date_format = "%Y %b %d  %H:%M:%S.%f"  # 2017 Jun 13  01:59:59.000
        self._1hour = timedelta(hours=1)
        self._1day = timedelta(hours=24)
        self.table = {"begin": 0, "end": 0}  # contain the indexes of the table
        self.extracted_table = []
        self.extracted_tables = []
        self.all_table_fields = {}
        self.final_table = []
        self.called = False

    def extract_table(self):
        try:
            with open(self.filename, "r") as f:
                file_lines = f.readlines()

            clean_lines = []
            for file_line in file_lines:
                clean_lines.append(file_line.strip("\n"))

            for line in clean_lines:
                if self.data_point_begin.match(line):
                    self.table["begin"] = clean_lines.index(line)
                if self.data_point_end.match(line):
                    self.table["end"] = clean_lines.index(line)
                    break

            self.fix_data(clean_lines)
            self.prepare_table_for_write()

        except FileNotFoundError as e:
            Error.error_handler(e)

        except Exception as e:
            Error.error_handler(e)

    def fix_data(self, data_lines):
        try:
            for valid_data_line in data_lines[self.table["begin"]: self.table["end"] + 1]:
                if self.invalid_line1.match(valid_data_line):
                    continue

                if self.time_start.match(valid_data_line):
                    time = valid_data_line[39:44]
                    begin_hour = datetime.strptime(time, "%H:%M")
                    end_hour = begin_hour + self._1hour
                    self.extracted_table.append("Hours : {} - {}".format(begin_hour.strftime("%H:%M"), end_hour.strftime("%H:%M")))

                if self.data_second_to_end.match(valid_data_line):
                    self.extracted_table.append("first epoch : {}".format(valid_data_line[:19]))
                    self.extracted_table.append("last epoch : {}".format(valid_data_line[19:35]))
                    self.extracted_table.append("mp12 : {}".format(valid_data_line[35:41]))
                    self.extracted_table.append("mp21 : {}".format(valid_data_line[41:47]))
                    self.extracted_table.append("mp15 : {}".format(valid_data_line[47:53]))
                    self.extracted_table.append("mp51 : {}".format(valid_data_line[53:59]))
                    self.extracted_table.append("mp16 : {}".format(valid_data_line[59:65]))
                    self.extracted_table.append("mp61 : {}".format(valid_data_line[65:71]))
                    self.extracted_table.append("mp17 : {}".format(valid_data_line[71:77]))
                    self.extracted_table.append("mp71 : {}".format(valid_data_line[77:83]))
                    self.extracted_table.append("mp18 : {}".format(valid_data_line[83:89]))
                    self.extracted_table.append("mp81 : {}".format(valid_data_line[89:95]))
                    continue

                if self.data_point_end.match(valid_data_line):
                    self.extracted_table.append("hrs : {}".format(valid_data_line[34:41]))
                    self.extracted_table.append("dt : {}".format(valid_data_line[42:45]))
                    self.extracted_table.append("#expt : {}".format(valid_data_line[45:52]))
                    self.extracted_table.append("#have : {}".format(valid_data_line[52:59]))
                    self.extracted_table.append("% : {}".format(valid_data_line[59:63]))
                    self.extracted_table.append("mp1 : {}".format(valid_data_line[63:69]))
                    self.extracted_table.append("mp2 : {}".format(valid_data_line[69:75]))
                    self.extracted_table.append("o/slps : {}".format(valid_data_line[75:82]))
                    continue

                if self.data_point_end.match(valid_data_line):
                    pass

                if self.invalid_line.match(valid_data_line):
                    continue

                if not self.empty_line.match(valid_data_line) and not self.continued_line.match(valid_data_line):
                    self.extracted_table.append(valid_data_line.strip(" "))
                    continue

                if self.continued_line.match(valid_data_line) and self.extracted_table:
                    self.extracted_table[-1] = self.extracted_table[-1] + "  " + valid_data_line.strip(" ")

        except Exception as e:
            Error.error_handler(e)

    def get_table_fields(self):
        try:
            fields = []
            if not self.extracted_table:  # this is in case extract table has been called b4 no need to do it again
                self.extract_table()

            if self.extracted_table:  # ensuring the table is not empty
                for line in self.extracted_table:
                    data = line.split(":", 1)[0].strip(" ")
                    fields.append(data)
                    self.add_table_field(data)

            return fields

        except Exception as e:
            Error.error_handler(e)

    def extract_tables(self):
        try:
            if self.filenames:
                temp_table = []
                for filename in self.filenames:
                    self.filename = filename
                    self.extracted_table = []
                    self.extract_table()
                    if self.extracted_table:
                        for line in self.extracted_table:
                            data = line.split(":", 1)
                            value = data[0].strip(" ")
                            key = data[1].strip(" ")
                            self.add_table_field(value)
                            temp_table.append([value, key])
                        self.extracted_tables.append(temp_table)
                        temp_table = []

                self.sort_tables()
                self.make_final_table()

        except Exception as e:
            Error.error_handler(e)

    def add_table_field(self, field):
        for dict_item in self.all_table_fields:
            if self.all_table_fields[dict_item] == field:
                return
        key = self.get_unique_key()
        self.all_table_fields[key] = field

    def prepare_table_for_write(self):
        try:
            table_fields = self.get_table_fields()
            if "Time of start of window" in table_fields and "Time of  end  of window" in table_fields:
                start_time_index = table_fields.index("Time of start of window")
                end_time_index = table_fields.index("Time of  end  of window")
                hours_index = table_fields.index("Hours")
                first_item = self.extracted_table[0]
                second_item = self.extracted_table[1]
                third_item = self.extracted_table[2]
                self.extracted_table[0] = self.extracted_table[hours_index]
                self.extracted_table[hours_index] = first_item
                self.extracted_table[1] = self.extracted_table[start_time_index]
                self.extracted_table[start_time_index] = second_item
                self.extracted_table[2] = self.extracted_table[end_time_index]
                self.extracted_table[end_time_index] = third_item
        except Exception as e:
            Error.error_handler(e)

    def make_final_table(self):
        self.final_table = []
        temp_table = {}
        for table in self.extracted_tables:
            for item in table:
                table_field = item[0]
                for field in self.all_table_fields:
                    if self.all_table_fields[field] == table_field:
                        temp_table[field] = item[1]
            self.final_table.append(temp_table)
            temp_table = {}
        self.extracted_tables = []

    def sort_tables(self):
        try:
            self.extracted_tables.sort(key=self.get_table_key)
        except Exception as e:
            Error.error_handler(e)

    def reorder_table_keys(self):
        dictionary = self.all_table_fields
        a_value = dictionary['A']
        b_value = dictionary['B']
        c_value = dictionary['C']
        d_value = dictionary['D']
        e_value = dictionary['E']
        f_value = dictionary['F']

        dictionary['A'] = d_value
        dictionary['B'] = e_value
        dictionary['C'] = f_value
        dictionary['D'] = a_value
        dictionary['E'] = b_value
        dictionary['F'] = c_value

        self.called = True

    def get_table_key(self, table):
        return datetime.strptime(table[1][1], self.data_date_format)
