
def map_columns(sheet, configuration):
    
    # Get first row of sheet, and populate headers with it
    header = [cell.value for cell in next(sheet.rows)]

    # TODO: add configuration for a unique identifier
    if 'USERID' not in header:
        raise TypeError(
            'Need a user identifier'
        )

    missing_items = [item for item in configuration.extract_attribute_keys() if not item in header]
    if missing_items:
        raise TypeError("Attribute missing from excel file: "+ ", ".join(missing_items))

    attribute_names = configuration.extract_attribute_keys() + ['USERID']

    return {attribute_name : header.index(attribute_name) for attribute_name in attribute_names}

