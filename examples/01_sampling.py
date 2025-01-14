# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

import json
import os

from unleash.data.utils import load_loghub_dataset
from unleash.sampling.entropy_sampling import sampling as entropy_sampling
from unleash.sampling.lilac_sampling import sampling as lilac_sampling
from unleash.sampling.logppt_sampling import sampling as logppt_sampling

from config import benchmark, datasets


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
