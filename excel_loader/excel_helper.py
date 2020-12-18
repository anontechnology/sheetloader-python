import openpyxl

# Wraps one worksheet.
class ExcelHelper:

    def __init__(self, sheet, configuration):
        self.sheet = sheet
        self.configuration = configuration
        
        # Get first row of sheet, and populate headers with it
        self.header = [cell.value for cell in next(sheet.rows)]

    def validate_columns(self):

        # To Do: add configuration for a unique identifier
        if 'USERID' not in self.header:
            raise TypeError(
                'Need a user identifier'
            )

        missing_items = [item for item in self.configuration.extract_attribute_keys() if not item in self.header]
        if missing_items:
            raise TypeError("Attribute missing from excel file: "+ ", ".join(missing_items))

    def map_columns(self):

        attribute_names = self.configuration.extract_attribute_keys() + ['USERID']

        return {attribute_name : self.header.index(attribute_name) for attribute_name in attribute_names}

