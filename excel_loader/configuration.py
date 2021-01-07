import json

class Configuration:

    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.configuration = self.__extract_configuration()

    def __extract_configuration(self):
        # TODO Handle file missing here.
        with open(self.conf_path) as conf_file:
            configuration_dict = json.load(conf_file)
            self.__validate_configuration(configuration_dict)
            return configuration_dict

    def __validate_configuration(self, configuration_dict: dict):
        for k, v in configuration_dict.items():
            if k == 'attributes':
                self.__validate_attributes(v)
                self.attributes = v
            elif k == 'user_id_column':
                self.user_id_column = v
            else:
                raise TypeError('Unexpected field in configuration: '+k)

    def __validate_attributes(self, attributes: list):
        for attribute in attributes:
            if 'name' not in attribute:
                raise TypeError('Attribute must have name')
            if 'schema' not in attribute:
                raise TypeError('Attribute %s has no schema' % attribute['name'])
            if 'columns' not in attribute:
                raise TypeError('Attribute %s has no column mapping specified' % attribute['name'])

            self.__validate_schema(attribute['schema'])

            for k, v in attribute.items():
                if k in {'name','key', 'hint', 'createdDate', 'modifiedDate'}:
                    if not isinstance(v, str):
                        raise TypeError("Expected string for %s (got %s instead)" % (k, str(v)))
                elif k in {'immutable', 'indexed', 'mandatory'}:
                    if not (isinstance(v, str) and v.capitalize() in ['TRUE', 'FALSE']):
                        raise TypeError("Expected boolean for %s (got %s instead)" % (k, str(v)))
                elif k in {'tags', 'regulations'}:
                    if not isinstance(v, list):
                        raise TypeError("Expected list for %s (got %s instead)" % (k, str(v)))
                elif k == 'columns':
                    self.__validate_columns(v, attribute['schema'])
                elif k != 'schema':
                    raise TypeError("Unexpected field in attribute: "+k)

    def __validate_schema(self, schema):
        if schema not in ['string', 'int', 'float', 'boolean', 'file']:
            if isinstance(schema, dict):
                for k, v in schema.items():
                    # TODO validate k also
                    self.__validate_schema(v)
            else:
                raise TypeError('Schema contains %s, which is neither a valid primitive schema nor a dict' % str(schema))

    def __validate_columns(self, columns, schema):
        if isinstance(columns, dict):
            for k, v in columns.items():
                if k not in schema:
                    raise TypeError('Column mapping reads from subattribute %s, which is not present in the corresponding schema')
                self.__validate_columns(v, schema[k])
        elif not isinstance(columns, str):
            raise TypeError('Column mapping contains %s, which is neither a string nor a dict' % str(schema))

