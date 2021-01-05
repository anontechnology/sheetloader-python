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
                elif k == 'schema':
                    self.__validate_schema(v)
                elif k == 'columns':
                    self.__validate_columns(v)
                else:
                    raise TypeError("Unexpected field in attribute: "+k)

    def __validate_schema(self, schema):
        if schema not in ['string', 'int', 'float', 'boolean', 'file']:
            if isinstance(schema, dict):
                for k, v in schema.items():
                    # TODO validate k also
                    self.__validate_schema(v)
            else:
                raise TypeError('Schema contains %s, which is neither a valid primitive schema nor a dict' % str(schema))

    def __validate_columns(self, schema):
        if isinstance(schema, dict):
            for k, v in schema.items():
                # TODO validate k also
                self.__validate_columns(v)
        elif not isinstance(schema, str):
            raise TypeError('Column mapping contains %s, which is neither a string nor a dict' % str(schema))

    def extract_attribute_keys(self):
        keys = []
        for attribute in self.configuration['attributes']:
           # TODO: Need just a unified way to just handle this
            if 'schema' in attribute:
                for schema_key, schema_type in attribute['schema'].items():
                    keys.append(attribute['name'] + '/' + schema_key.upper())
            else:
                keys.append(attribute['name'])
        return keys


