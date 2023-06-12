#!/usr/bin/env python3

import argparse
import json
import datetime

def program(patient_records, verbose):
    today = datetime.date.today()
    disease_records = {}
    for record in patient_records:
        disease = record['disease']
        if disease not in disease_records:
            disease_records[disease] = {}
        date = datetime.datetime.strptime(record['date'], '%Y-%m-%d').date()
        if date > today:
            continue
        if date not in disease_records[disease]:
            disease_records[disease][date] = []
        disease_records[disease][date].append(record['evolution'])
    for disease, records in disease_records.items():
        sorted_dates = sorted(list(records.keys()))
        print(disease)
        for date in sorted_dates:
            print('    Date:', date)
            for evolution in records[date]:
                if verbose:
                    print('        Evolution:', evolution)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Patient records by disease and date.')
    parser.add_argument('patient_records', metavar='N', type=str, nargs='+', help='Patient records by disease, date, and evolution.')
    parser.add_argument('--verbose', help='Increase output verbosity', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    program(json.loads(args.patient_records[0]), args.verbose)
