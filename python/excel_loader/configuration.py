import json

class Configuration:

    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.configuration = self.__extract_configuration()


    def __extract_configuration(self):
        # TODO Handle file missing here.
        with open(self.conf_path) as conf_file:
            configuration_dict = json.load(conf_file)
            if not self.__validate_configuration(configuration_dict):
                raise TypeError(
                    'Configuration has an attribute with an illegal type'
                )
        return configuration_dict

    def __validate_configuration(self, configuration_dict: dict):
        for k, v in configuration_dict.items():
            if k in ['attributes'] and self.__validate_attributes(attributes=v):
                self.attributes = v
                continue
            else:
                return False
        return True

    def __validate_attributes(self, attributes: list):
        for attribute in attributes:
            for k, v in attribute.items():
                if k in ['name','key', 'hint', 'createdDate', 'modifiedDate'] and isinstance(v, str):
                    continue
                elif k in ['immutable', 'indexed', 'mandatory'] and isinstance(v, str) and v.capitalize() in ['TRUE', 'FALSE']:
                    continue
                elif k in ['tags', 'regulations'] and isinstance(v, list):
                    continue
                elif k in ['schema'] and self.__validate_schema(configuration_dict=v):
                    continue
                else:
                    return False
        return True

    def __validate_schema(self, configuration_dict: dict):
        for k, v in configuration_dict.items():
            if v in ['string', 'int', 'boolean', 'file']:
                continue
            elif isinstance(v, dict):
                self.__validate_configuration(configuration_dict)
            else:
                return False
        return True

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


