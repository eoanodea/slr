import csv
import sys
import os

RIS_MAP = {
    'Title': 'TI',
    'Author': 'AU',
    'Publication Title': 'JO',
    'Year': 'PY',
    'Date': 'DA',
    'DOI': 'DO',
    'Abstract': 'AB',
    'Url': 'UR',
    'ISSN': 'SN',
    'ISBN': 'SN',
    'Publisher': 'PB',
    'Keywords': 'KW',
    'Author Keywords': 'KW',
    'Source title': 'JO',
}

def csv_to_ris(csv_file):
    ris_file = os.path.splitext(csv_file)[0] + '.ris'
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(ris_file, 'w', encoding='utf-8') as risfile:
            for row in reader:
                risfile.write('TY  - JOUR\n')
                for csv_key, value in row.items():
                    if value:
                        ris_tag = RIS_MAP.get(csv_key)
                        if ris_tag:
                            # Handle multiple authors/keywords
                            if ris_tag in ['AU', 'KW']:
                                for v in value.split(';'):
                                    v = v.strip()
                                    if v:
                                        risfile.write(f'{ris_tag}  - {v}\n')
                            else:
                                risfile.write(f'{ris_tag}  - {value}\n')
                risfile.write('ER  - \n\n')
    print(f'Converted {csv_file} to {ris_file}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 csv2ris.py path_to_file.csv")
        sys.exit(1)
    csv_to_ris(sys.argv[1])