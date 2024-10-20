import argparse

from embeddings import embeddings

risk = ['low', 'medium', 'high']
observation = ['ppe', 'documentation', 'equipment']
hazard = ['traffic', 'fire', 'electrical', 'fall']

parser = argparse.ArgumentParser()
parser.add_argument('--risk', '-r', action='store_true')
parser.add_argument('--observation', '-o', action='store_true')
parser.add_argument('--hazard', '-h', action='store_true')
parser.add_argument('--all', '-a', action='store_true')
parser.add_argument('--count', '-n', type=int, default=-1)
args = parser.parse_args()

assert args.count != 0 and args.count >= -1, 'invalid count'

if not any([args.all, args.risk, args.observation, args.hazard]):
    args.all = True

print(f'\nconducting analysis on {'all' if args.count == -1 else args.count} records...\n')

if args.all or args.risk:
    print('\nanalyzing risk...\n')
    embeddings.analyze(risk, args.count)

if args.all or args.observation:
    print('\nanalyzing observation...\n')
    embeddings.analyze(observation, args.count)

if args.all or args.hazard:
    print('\nanalyzing hazard...\n')
    embeddings.analyze(hazard, args.count)