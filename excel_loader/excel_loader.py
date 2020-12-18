from .configuration import Configuration
from . import excel_helper
import vizivault
import openpyxl

def load_excel(file_path: str, records: int, conf_path: str,
                url: str,
                api_key: str,
                encryption_key_file: str,
                decryption_key_file: str,
                output_path: str):
                
    configuration = Configuration(conf_path)

    with open(encryption_key_file, 'r') as encryption_file:
        encryption_key = encryption_file.read()
    with open(decryption_key_file, 'r') as decryption_file:
        decryption_key = decryption_file.read()

    vault = vizivault.ViziVault(base_url=url, api_key=api_key, encryption_key=encryption_key,
                                        decryption_key=decryption_key)

    for attribute in configuration.attributes:
        attribute_def = vizivault.AttributeDefinition(**attribute)
        vault.store_attribute_definition(attribute_definition=attribute_def)

    #TODO Load in parallel and validate data types. Mostly the existance of a valid users.

    workbook = openpyxl.load_workbook(file_path)
    for sheet in workbook.worksheets:

        attribute_map = excel_helper.map_columns(sheet, configuration)
        for row_cells in sheet.iter_rows()[1:]:
        #TODO Need to validate users exist and if it's an update or an insertion
            new_user = vizivault.User(str(row_cells[attribute_map['USERID']].value))

            for attribute in configuration.attributes:
                if 'schema' in attribute:
                    #TODO  handle inserting a schema value here. Probably need to separate out schema from flat attributes
                    print("Found schema value")
                else:
                    new_user.add_attribute(attribute=attribute['name'], value=str(row_cells[attribute_map[attribute['name']]].value))
            vault.save(new_user)

    #TODO Export the result of the upload as a lo file and STDIO. Export shoudl be inserts/updates and errors or warnings.





