import argparse

from excel_loader import load_excel

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('excelfile', type=str, help='excel file to upload')
    parser.add_argument('-c', '--config', type=str, help="configuration file to map columns to attribute", default='excel_vizivault_configuration.json')
    parser.add_argument('-u', '--url', type=str, help="url of your vault", default='http://localhost:8083')
    parser.add_argument('-a', '--api_key', type=str, help="application identifier", default='12345')
    parser.add_argument('-e', '--encryption_key_file', type=str, help="encryption key file", default='./resources/encryption_key.txt')
    parser.add_argument('-d', '--decryption_key_file', type=str, help="decryption key file", default='./resources/decryption_key.txt')
    #parser.add_argument('--output', type=str, help="output file of results", default='output.txt')
    args = parser.parse_args()

    load_excel(file_path=args.excelfile,
                conf_path=args.config,
                url=args.url,
                api_key=args.api_key,
                encryption_key_file=args.encryption_key_file,
                decryption_key_file=args.decryption_key_file)





