from .configuration import Configuration
import vizivault
import openpyxl

def validate_columns(headers, column_config):
    if type(column_config) is str:
        if column_config not in headers:
            raise TypeError("Attempting to read from nonexistent column", column_config)
    else:
        for key, value in column_config.items():
            validate_columns(headers, value)

def validate_all_columns(headers, attributes):
    for attribute in attributes:
        validate_columns(headers, attribute['columns'])

def get_primitive(attribute_schema, value):
    if attribute_schema == "int":
        return int(value)
    elif attribute_schema == 'boolean':
        return bool(value)
    elif attribute_schema == 'float':
        return float(value)
    return str(value)

def assemble_value(attribute_columns, attribute_schema, header_map, cells):
    if type(attribute_columns) is str:
        return get_primitive(attribute_schema, cells[header_map[attribute_columns]].value)
    else:
        return {column : assemble_value(attribute_columns[column], attribute_schema[column], header_map, cells) for column in attribute_columns}

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

    vault = vizivault.ViziVault(base_url=url, api_key=api_key, encryption_key=encryption_key, decryption_key=decryption_key)


    for attribute in configuration.attributes:
        attribute_def = vizivault.AttributeDefinition(**{k:v for k, v in attribute.items() if k not in {'columns'}})
        vault.store_attribute_definition(attribute_definition=attribute_def)

    #TODO Load in parallel and validate data types based on primitive schemas.
    # Could potentially also check if user exists (update) or will be created (insertion)

    workbook = openpyxl.load_workbook(file_path)
    for sheet in workbook.worksheets:

        # use next(sheet.rows) to get the first row of the spreadsheet
        header_map = {cell.value : i for i, cell in enumerate(next(sheet.rows))}
        validate_all_columns(header_map.keys(), configuration.attributes)

        for row_cells in sheet.iter_rows(min_row=2):
            userid = row_cells[header_map[configuration.user_id_column]].value
            if userid is None:
                break

            new_user = vizivault.User(str(userid))

            for attribute in configuration.attributes:
                new_user.add_attribute(attribute=attribute['name'], value=assemble_value(attribute['columns'], attribute['schema'], header_map, row_cells))
            vault.save(new_user)

    #TODO Export the result of the upload as a log file and STDIO. Export shoudl be inserts/updates and errors or warnings.





