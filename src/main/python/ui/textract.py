# Author: Dahir Muhammad Dahir
# Date: 20th-05-2019 04:49 PM

from core.extraction import Extract
from core.writing import WriteExcel
from ui.main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os


class TextractGui(QMainWindow, Ui_MainWindow, Extract):
    def __init__(self):
        super(TextractGui, self).__init__()
        Extract.__init__(self)

        # set up the the user interface
        self.setupUi(self)

        # extract criteria daily, monthly, yearly
        self.extract_criteria = self.extractComboBox.currentText()

        # make excel icon
        self.excel_icon = QIcon()
        self.excel_icon.addPixmap(QPixmap(":/base/excel.png"), QIcon.Normal, QIcon.Off)

        # make txt icon
        self.txt_icon = QIcon()
        self.txt_icon.addPixmap(QPixmap(":/base/txt.png"), QIcon.Normal, QIcon.Off)

        # make file icon
        self.file_icon = QIcon()
        self.file_icon.addPixmap(QPixmap(":/base/file.png"), QIcon.Normal, QIcon.Off)

        # callback for button click
        self.openProjectButton.clicked.connect(self.choose_project_dir)

        # callback for text change
        self.openProjectLineEdit.textChanged.connect(self.show_project_dir_files)

        # callback check all button in project selection
        self.selectProjectCheckButton.clicked.connect(self.check_all_project_files)

        # callback 4 uncheck all button in project selection
        self.selectProjectUncheckButton.clicked.connect(self.uncheck_all_project_files)

        # callback 4 any item being selected
        self.selectProjectListWidget.clicked.connect(self.show_table_fields)

        # callback 4 table field buttons
        self.selectTableCheckButton.clicked.connect(self.check_all_table_field)
        self.selectTableUncheckButton.clicked.connect(self.uncheck_all_table_field)

        # callback if you know what i mean
        self.outputBrowseButton.clicked.connect(self.choose_output_dir)
        self.outputLineEdit.textChanged.connect(self.show_output_dir_files)
        self.outputListWidget.clicked.connect(self.show_output_dir_files)

        self.extractComboBox.currentIndexChanged.connect(self.extract_combo_changed)
        self.extractButton.clicked.connect(self.extract)

        self.statusbar.showMessage("Ready")

    def choose_project_dir(self):
        try:
            dir_dialog = QFileDialog(self)
            dir_dialog.setWindowTitle("Select Project Directory")
            dir_dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dir_dialog.setFileMode(QFileDialog.Directory)
            dir_dialog.setOption(QFileDialog.ShowDirsOnly)
            dir_dialog.open()
            if dir_dialog.exec():
                self.openProjectLineEdit.setText(dir_dialog.selectedFiles()[0])
        except Exception as e:
            self.error_handler(e)

    def choose_output_dir(self):
        try:
            output_dialog = QFileDialog(self)
            output_dialog.setWindowTitle("Select Output Directory")
            output_dialog.setAcceptMode(QFileDialog.AcceptOpen)
            output_dialog.setFileMode(QFileDialog.Directory)
            output_dialog.setOption(QFileDialog.ShowDirsOnly)
            output_dialog.open()
            if output_dialog.exec():
                self.outputLineEdit.setText(output_dialog.selectedFiles()[0])
        except Exception as e:
            self.error_handler(e)

    def show_project_dir_files(self):
        try:
            # clear any existing item b4 we populate the list
            self.clear_list_widget_items(self.selectProjectListWidget)

            # Get the user specified directory and extract the files
            project_dir = self.openProjectLineEdit.text()
            dir_items = os.listdir(project_dir)
            for item in dir_items:
                full_path = "{}/{}".format(project_dir, item)
                if os.path.isfile(full_path):
                    if item.endswith("txt"):
                        project_file = QListWidgetItem()
                        project_file.setIcon(self.txt_icon)
                        project_file.setCheckState(Qt.Unchecked)
                        project_file.setText(item)
                        self.selectProjectListWidget.addItem(project_file)
        except Exception as e:
            self.error_handler(e)

    def show_output_dir_files(self):
        try:
            # clear any existing item b4 we populate the list
            self.clear_list_widget_items(self.outputListWidget)

            # Get the user specified directory and extract the files
            output_dir = self.outputLineEdit.text()
            dir_items = os.listdir(output_dir)
            for item in dir_items:
                full_path = "{}/{}".format(output_dir, item)
                if os.path.isfile(full_path):
                    if item.endswith("xlsx") or item.endswith("xls") or item.endswith("csv"):
                        output_file = QListWidgetItem()
                        output_file.setIcon(self.excel_icon)
                        output_file.setCheckState(Qt.Unchecked)
                        output_file.setText(item)
                        self.outputListWidget.addItem(output_file)

        except Exception as e:
            self.error_handler(e)

    def check_all_project_files(self):
        self.check_all(self.selectProjectListWidget)

    def uncheck_all_project_files(self):
        self.uncheck_all(self.selectProjectListWidget)

    def check_all_table_field(self):
        self.check_all(self.selectTableListWidget)

    def uncheck_all_table_field(self):
        self.uncheck_all(self.selectTableListWidget)

    def check_all(self, widget_name):
        try:
            widget = widget_name
            item_count = widget.count()

            for item_num in range(item_count):
                widget_item = widget.item(item_num)
                widget_item.setCheckState(Qt.Checked)
        except Exception as e:
            self.error_handler(e)

    def uncheck_all(self, widget_name):
        try:
            widget = widget_name
            item_count = widget.count()

            for item_num in range(item_count):
                widget_item = widget.item(item_num)
                widget_item.setCheckState(Qt.Unchecked)
        except Exception as e:
            self.error_handler(e)

    def show_table_fields(self):
        try:
            project_dir = self.openProjectLineEdit.text()  # select project folder path here
            widget = self.selectProjectListWidget
            item_count = widget.count()

            # clear widget b4 we add items
            self.clear_list_widget_items(self.selectTableListWidget)

            for item_num in range(item_count):
                current_item = widget.item(item_num)
                if current_item.checkState() == Qt.Checked:
                    self.filename = "{}/{}".format(project_dir, current_item.text())  # full file path: project_dir + file
                    self.extracted_table = []
                    fields = self.get_table_fields()

                    for field in fields:
                        table_field = QListWidgetItem()
                        table_field.setCheckState(Qt.Unchecked)
                        table_field.setText(field)
                        self.selectTableListWidget.addItem(table_field)
                    break
        except Exception as e:
            self.error_handler(e)

    def clear_list_widget_items(self, widget_name):
        try:
            widget = widget_name
            item_count = widget.count()

            for item_num in range(item_count):
                item = widget.takeItem(0)
                del item  # manually deleting because Qt won't help us here
        except Exception as e:
            self.error_handler(e)

    def extract_combo_changed(self):
        try:
            self.extract_criteria = self.extractComboBox.currentText()
        except Exception as e:
            self.error_handler(e)

    def extract(self):
        try:
            if not self.called:
                self.reorder_table_keys()
            criteria_dict = {"All In One Table": "All", "Daily Table": "Daily", "Monthly Table": "Monthly", "Yearly Table": "Yearly"}
            criteria = criteria_dict[self.extract_criteria]
            project_dir = self.openProjectLineEdit.text()
            output_dir = self.outputLineEdit.text()
            selected_files = []
            # table_fields = self.get_checked_item_text(self.selectTableListWidget)
            table_fields = self.all_table_fields
            user_selected_fields = self.get_checked_item_text(self.selectTableListWidget)

            items_to_remove = []

            for field in table_fields:
                if not table_fields[field] in user_selected_fields:
                    items_to_remove.append(field)

            for i in range(len(items_to_remove)):
                table_fields.pop(items_to_remove[i])

            for table in self.final_table:
                for i in range(len(items_to_remove)):
                    if items_to_remove[i] in table:
                        table.pop(items_to_remove[i])

            for item in self.get_checked_item_text(self.selectProjectListWidget):
                selected_files.append("{}/{}".format(project_dir, item))

            writer = WriteExcel()

            writer.output_filename = "{}/{}.xlsx".format(output_dir, criteria)

            if project_dir and output_dir and selected_files and table_fields:
                self.filenames = selected_files
                self.extract_tables()
                writer.tables = self.final_table
                writer.table_fields = table_fields

                if criteria == "All":
                    writer.write_all()

                if criteria == "Daily":
                    writer.write_daily()

                if criteria == "Monthly":
                    writer.write_monthly()

                if criteria == "Yearly":
                    pass

            else:
                self.error_handler("something went wrong")
            self.show_output_dir_files()
        except Exception as e:
            self.error_handler(e)

    def get_checked_item_text(self, list_widget):
        try:
            selected = []
            widget = list_widget
            count = widget.count()

            for item_num in range(count):
                item = widget.item(item_num)
                if item.checkState() == Qt.Checked:
                    selected.append(item.text())

            return selected
        except Exception as e:
            self.error_handler(e)

    def error_handler(self, error):
        self.statusbar.showMessage(str(error))
