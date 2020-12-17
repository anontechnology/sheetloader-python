import openpyxl


class ExcelHelper:

    def __init__(self, file_path, configuration):
        self.excel_file_path = file_path
        self.configuration = configuration

        # TODO Handle file missing here.
        self.workbook = openpyxl.load_workbook(file_path)

    def get_header(self, sheet):
        headers = []
        for rows in sheet.rows:
            for cell in rows:
                headers.append(cell.value)
            break
        return headers

    def validate_columns(self):
        # TODO : use argument to specify sheets to evaluate
        for sheet in self.workbook.worksheets:

            header = self.get_header(sheet)

            # To Do: add configuration for a unique identifier
            if 'USERID' not in header:
                raise TypeError(
                    'Need a user identifier'
                )

            if not all(item in header for item in self.configuration.extract_attribute_keys()):
                # TODO: Need to note which attribute is missing in the excel file because that's more clear.
                raise TypeError(
                    "Attribute missing from excel file"
                )

    def map_columns(self, sheet):

        header_map = {}
        header = self.get_header(sheet)

        attribute_names = self.configuration.extract_attribute_keys() + ['USERID']

        for attribute_name in attribute_names:
            header_map[attribute_name] = header.index(attribute_name)

        return header_map

