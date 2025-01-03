# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

import pandas as pd
import json
import os

from unleash.data.utils import generate_logformat_regex, log_to_dataframe
from unleash.sampling.entropy_sampling import sampling as entropy_sampling
from unleash.sampling.lilac_sampling import sampling as lilac_sampling
from unleash.sampling.logppt_sampling import sampling as logppt_sampling

from config import benchmark, datasets

DOWNLOAD_URL = "https://zenodo.org/records/8275861/files/{}.zip"

def load_loghub_dataset(dataset_name="Apache", cache_dir=None, format="csv", log_format=None):
    """
    Load from cache if available, otherwise download, unzip and cache the dataset
    """
    dataset_url = DOWNLOAD_URL.format(dataset_name)
    print(dataset_url)
    # Check if the dataset is already downloaded
    if cache_dir is None:
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "unleash")
    dataset_dir = os.path.join(cache_dir, dataset_name)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        # Download the dataset
        dataset_zip = os.path.join(cache_dir, f"{dataset_name}.zip")
        os.system(f"wget {dataset_url} -O {dataset_zip}")
        # Unzip the dataset
        os.system(f"unzip {dataset_zip} -d {os.path.dirname(dataset_dir)}")
        # Remove the zip file
        os.remove(dataset_zip)
    # Load the dataset
    if format == "csv":
        log_df = pd.read_csv(f"{dataset_dir}/{dataset_name}_full.log_structured.csv")
    elif format == "text":
        headers, regex = generate_logformat_regex(log_format)
        log_df = log_to_dataframe(f"{dataset_dir}/{dataset_name}_full.log", regex, headers)
    return log_df



if __name__ == '__main__':

    dname = sys.argv[1:]
    data_dir = "../datasets/loghub-2.0"
    output_dir = "../datasets/loghub-2.0"
    for dataset in datasets:
        if dname != None and dataset not in dname:
            continue
        print(dataset)
        log_file = benchmark[dataset]['log_file']
        print(f"Loading {log_file}...")
        labelled_logs = load_loghub_dataset(dataset, data_dir)

        os.makedirs(f'{output_dir}/{dataset}/samples', exist_ok=True)
        # pd.read_csv(f'{data_dir}/{log_file}_structured.csv')
        print(f"Loaded {len(labelled_logs)} logs.")
        k_rate = 0.2
        length = int(k_rate * len(labelled_logs))
        labelled_logs = labelled_logs[:length]
        raw_logs = labelled_logs['Content'].tolist()
        labels = labelled_logs['EventTemplate'].tolist()
        with open(f'{output_dir}/{dataset}/validation.json', 'w') as f:
            for log, label in zip(raw_logs, labels):
                f.write(json.dumps({'log': log, 'template': label}) + '\n')
        shots = [8, 16, 32, 64, 128, 256]
        
        ## Entropy Sampling ###
        sample_candidates = entropy_sampling(raw_logs, labels, shots)
        for shot, samples in sample_candidates.items():
            with open(f'{output_dir}/{dataset}/samples/entropy_{shot}.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps({'log': sample[0], 'template': sample[1]}) + '\n')

        ## Hierichical Sampling from LILAC ###
        sample_candidates = lilac_sampling(raw_logs, labels, shots)
        for shot, samples in sample_candidates.items():
            with open(f'{output_dir}/{dataset}/samples/lilac_{shot}.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps({'log': sample[0], 'template': sample[1]}) + '\n')

        ## Adaptive Random Sampling from LogPPT ###
        sample_candidates = logppt_sampling(raw_logs, labels, shots)
        for shot, samples in sample_candidates.items():
            with open(f'{output_dir}/{dataset}/samples/logppt_{shot}.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps({'log': sample[0], 'template': sample[1]}) + '\n')
