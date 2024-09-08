# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

import pandas as pd
import json
import os

from unleash.sampling.entropy_sampling import sampling as entropy_sampling
from unleash.sampling.lilac_sampling import sampling as lilac_sampling
from unleash.sampling.logppt_sampling import sampling as logppt_sampling


datasets = [
    "Apache"
]

benchmark = {
    'Apache': {
        'log_file': 'Apache/Apache_2k.log',
        'log_format': '\[<Time>\] \[<Level>\] <Content>',
    },
}




if __name__ == '__main__':
    data_dir = "../datasets/loghub-2k"
    output_dir = "../datasets/loghub-2k"
    for dataset in datasets:
        print(dataset)
        os.makedirs(f'{output_dir}/{dataset}/samples', exist_ok=True)
        log_file = benchmark[dataset]['log_file']
        print(f"Loading {log_file}...")
        labelled_logs = pd.read_csv(f'{data_dir}/{log_file}_structured.csv')
        print(f"Loaded {len(labelled_logs)} logs.")
        k_rate = 0.2
        length = int(k_rate * len(labelled_logs))
        labelled_logs = labelled_logs[:length]
        raw_logs = labelled_logs['Content'].tolist()
        labels = labelled_logs['EventTemplate'].tolist()
        with open(f'{output_dir}/{dataset}/validation.json', 'w') as f:
            for log, label in zip(raw_logs, labels):
                f.write(json.dumps({'log': log, 'template': label}) + '\n')
        shots = [32]
        
        ## Entropy Sampling ###
        sample_candidates = entropy_sampling(raw_logs, labels, shots)
        assert len(sample_candidates[32]) == 32, f"Expected 32 samples from entropy sampling, got {len(sample_candidates[32])}"

        for shot, samples in sample_candidates.items():
            with open(f'{output_dir}/{dataset}/samples/entropy_{shot}.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps({'log': sample[0], 'template': sample[1]}) + '\n')

        ## Hierichical Sampling from LILAC ###
        sample_candidates = lilac_sampling(raw_logs, labels, shots)
        assert len(sample_candidates[32]) == 32, f"Expected 32 samples from lilac sampling, got {len(sample_candidates[32])}"

        for shot, samples in sample_candidates.items():
            with open(f'{output_dir}/{dataset}/samples/lilac_{shot}.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps({'log': sample[0], 'template': sample[1]}) + '\n')

        ## Adaptive Random Sampling from LogPPT ###
        sample_candidates = logppt_sampling(raw_logs, labels, shots)
        assert len(sample_candidates[32]) == 32, f"Expected 32 samples from logppt sampling, got {len(sample_candidates[32])}"

        for shot, samples in sample_candidates.items():
            with open(f'{output_dir}/{dataset}/samples/logppt_{shot}.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps({'log': sample[0], 'template': sample[1]}) + '\n')
