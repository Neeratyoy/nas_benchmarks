import os
import json
import argparse

from tabular_benchmarks.wrn_cifar10_3h import WRNCIFAR103HBenchmark
from tabular_benchmarks.fcnet_year_prediction import FCNetYearPredictionBenchmark
from tabular_benchmarks.fcnet_benchmark import FCNetBenchmark

parser = argparse.ArgumentParser()
parser.add_argument('--run_id', default=0, type=int, nargs='?', help='unique number to identify this run')
parser.add_argument('--benchmark', default="wrn_cifar10", type=str, nargs='?', help='specifies the benchmark')
parser.add_argument('--n_iters', default=100, type=int, nargs='?', help='number of iterations for optimization method')
parser.add_argument('--output_path', default="./", type=str, nargs='?',
                    help='specifies the path where the results will be saved')
parser.add_argument('--data_dir', default="./", type=str, nargs='?', help='specifies the path to the tabular data')

args = parser.parse_args()

if args.benchmark == "wrn_cifar10":
    b = WRNCIFAR103HBenchmark(data_dir=args.data_dir)

elif args.benchmark == "fcnet_regression":
    b = FCNetYearPredictionBenchmark(data_dir=args.data_dir)

elif args.benchmark == "protein_structure":
    b = FCNetBenchmark(dataset=args.data_dir)

elif args.benchmark == "slice_localization":
    b = FCNetBenchmark(dataset=args.data_dir)

output_path = os.path.join(args.output_path, "random_search")
os.makedirs(os.path.join(output_path), exist_ok=True)

cs = b.get_configuration_space()

runtime = []
regret = []
curr_incumbent = None
curr_inc_value = None

rt = 0
X = []
for i in range(args.n_iters):
    config = cs.sample_configuration()

    b.objective_function(config)

res = b.get_results()

fh = open(os.path.join(output_path, 'run_%d.json' % args.run_id), 'w')
json.dump(res, fh)
fh.close()
