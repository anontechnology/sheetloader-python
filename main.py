import argparse

from excel_loader import load_excel

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('--xls', type=str, help='excel file to upload', default='vizivault_test.xlsx')
    parser.add_argument('--records', type=int, help="number of records")
    parser.add_argument('--conf', type=str, help="configuration file to map columns to attribute", default='excel_vizivault_configuration.json')
    parser.add_argument('--url', type=str, help="url of your vault", default='http://localhost:8083')
    parser.add_argument('--api_key', type=str, help="application identifier", default='12345')
    parser.add_argument('--encryption_key_file', type=str, help="encryption key file", default='./resources/test_encryption_key.txt')
    parser.add_argument('--decryption_key_file', type=str, help="decryption key file", default='./resources/test_decryption_key.txt')
    parser.add_argument('--output', type=str, help="output file of results", default='output.txt')
    args = parser.parse_args()

    load_excel(file_path=args.xls, records=args.records, conf_path=args.conf,
                url=args.url,
                api_key=args.api_key,
                encryption_key_file=args.encryption_key_file, decryption_key_file=args.decryption_key_file,
                output_path=args.output)





