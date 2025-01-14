"""
This file is part of TA-Eval-Rep.
Copyright (C) 2022 University of Luxembourg
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import os

# sys.path.append('../')

from unleash.evaluation.settings import benchmark_settings
from unleash.evaluation.utils.common import common_args
from unleash.evaluation.utils.evaluator_main import evaluator, prepare_results
from unleash.evaluation.utils.postprocess import post_average


datasets_full = [
    "Proxifier",
    "Apache",
    "OpenSSH",
    "HDFS",
    "OpenStack",
    "HPC",
    "Zookeeper",
    "HealthApp",
    "Hadoop",
    "Spark",
    "BGL",
    "Linux",
    "Mac",
    "Thunderbird",
]


if __name__ == "__main__":
    args = common_args()
    
    # initialize by data type
    if args.data_type == "full":
        datasets = datasets_full
        data_type = "full"
        input_dir = "../datasets/loghub-2.0/"
        output_dir = f"{args.output_dir}/logs"
        if not os.path.exists(output_dir):
            raise FileNotFoundError(f"Output directory {output_dir} does not exist.")
    elif args.data_type == "2k":
        raise NotImplementedError

    # prepare results file
    result_file = prepare_results(output_dir=output_dir)
    if args.dataset != "null":
        datasets = [args.dataset]

    for dataset in datasets:
        setting = benchmark_settings[dataset]
        log_file = setting['log_file'].replace("_2k", f"_{data_type}")
        if os.path.exists(os.path.join(output_dir, f"{dataset}.log_structured.csv")):
            raise FileExistsError(f"parsing result of dataset {dataset} not exist.")
        
        # run evaluator for a dataset
        # The file is only for evalutation, so we remove the parameter "LogParser"
        evaluator(
            dataset=dataset,
            input_dir=input_dir,
            output_dir=output_dir,
            log_file=log_file,
            result_file=result_file,
        )  # it internally saves the results into a summary file
    metric_file = os.path.join(output_dir, result_file)
    
    if args.dataset == "null":
        post_average(metric_file)
    
