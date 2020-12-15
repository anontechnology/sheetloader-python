from excel_loader.configuration import Configuration
from excel_loader.excel_helper import ExcelHelper
import vizivault
import openpyxl

class ExcelLoader:

    def __init__(self, file_path: str, records: int, conf_path: str,
                 url: str,
                 api_key: str,
                 encryption_key_file: str,
                 decryption_key_file: str,
                 output_path: str):
        self.file_path = file_path
        self.records = records
        self.conf = conf_path
        self.output = output_path
        self.configuration = Configuration(conf_path)

        with open(encryption_key_file, 'r') as encryption_file:
            encryption_key = encryption_file.read()
        with open(decryption_key_file, 'r') as decryption_file:
            decryption_key = decryption_file.read()

        self.vault = vizivault.ViziVault(base_url=url, api_key=api_key, encryption_key=encryption_key,
                                         decryption_key=decryption_key)
        self.spreadsheet = ExcelHelper(self.file_path, self.configuration)
        self.instantiate_variables()
        self.load_data()

    def instantiate_variables(self):
        self.spreadsheet.validate_columns()

        for attribute in self.configuration.attributes:
            attribute_def = vizivault.AttributeDefinition(**attribute)
            self.vault.store_attribute_definition(attribute_definition=attribute_def)

    def load_data(self):
        #TODO Load in parallel and validate data types. Mostly the existance of a valid users.

        workbook = openpyxl.load_workbook(self.file_path)
        for sheet in workbook.worksheets:
            attribute_map = self.spreadsheet.map_columns(sheet)
            for i, row_cells in enumerate(sheet.iter_rows()):
                # Annoying hack to skip the first row. Shoudl burry this into excel helper
                if i == 0:
                    continue
        #TODO Need to validate users exist and if it's an update or an insertion
                new_user = vizivault.User(str(row_cells[attribute_map['USERID']].value))

                for attribute in self.configuration.attributes:
                    if 'schema' in attribute:
                        #TODO  handle inserting a schema value here. Probably need to separate out schema from flat attributes
                        print("Found schema value")
                    else:
                        new_user.add_attribute(attribute=attribute['name'], value=str(row_cells[attribute_map[attribute['name']]].value))
                self.vault.save(new_user)

        #TODO Export the result of the upload as a lo file and STDIO. Export shoudl be inserts/updates and errors or warnings.





