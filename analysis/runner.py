import argparse

from embeddings import embeddings

severity = ['low', 'medium', 'high']
general = ['ppe', 'documentation', 'equipment']
particular = ['traffic', 'fire', 'electrical', 'fall']

parser = argparse.ArgumentParser()
parser.add_argument('--severity', '-s', action='store_true')
parser.add_argument('--general', '-g', action='store_true')
parser.add_argument('--particular', '-p', action='store_true')
parser.add_argument('--all', '-a', action='store_true')
parser.add_argument('--count', '-n', type=int, default=-1)
args = parser.parse_args()

assert args.count != 0 and args.count >= -1, 'invalid count'

if not any([args.all, args.severity, args.general, args.particular]):
    args.all = True

print(f'\nconducting analysis on {'all' if args.count == -1 else args.count} records...\n')

if args.all or args.severity:
    print('\nanalyzing severity...\n')
    embeddings.analyze(severity, args.count)

if args.all or args.general:
    print('\nanalyzing general...\n')
    embeddings.analyze(general, args.count)

if args.all or args.particular:
    print('\nanalyzing particular...\n')
    embeddings.analyze(particular, args.count)