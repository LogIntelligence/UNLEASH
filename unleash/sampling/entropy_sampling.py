import numpy as np
import math
import calendar
from collections import Counter
import re
import heapq
import time
import json
import pandas as pd
from copy import deepcopy
from . import datasets, benchmark


def entropy(s):
    if isinstance(s, int):
        s = str(s)
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob]) / len(s)
    return entropy


def first_token(s):
    return s.split()[0] if s and " " in s else s


def entropy_sampling(logs, k=10, n_layers=5):
    # print(logs)
    entropy_and_token = [(idx, entropy(item), first_token(item))
                         for idx, item in enumerate(logs)]
    # print(entropy_and_token)
    entropy_and_token.sort(key=lambda x: x[1], reverse=True)
    layers = np.array_split(entropy_and_token, n_layers)
    selected_samples = set([])
    tokens_selected = set([])
    # can_select = True
    # while len(selected_samples) < k and can_select:
    #     can_select = True
    for layer in layers:
        for item in layer:
            if item[2] not in tokens_selected or len(tokens_selected) >= k:
                selected_samples.add(item[0])
                tokens_selected.add(item[2])
                # can_select = False
            if len(selected_samples) >= k:
                break
        if len(selected_samples) >= k:
            break

    ret = [int(idx) for idx in selected_samples]
    return ret, len(selected_samples)


class Vocab:
    def __init__(self, stopwords=["<*>"]):
        stopwords = [
            "a",
            "an",
            "and",
            "i",
            "ie",
            "so",
            "to",
            "the",

        ] + list(calendar.day_name) + list(calendar.day_abbr) \
          + list(calendar.month_name) + list(calendar.month_abbr)
        self.token_counter = Counter()
        self.stopwords = frozenset(set(stopwords))
        # print(self.__filter_stopwords(['LDAP', 'Built', 'with']))

    def build(self, sequences):
        print("Build vocab with examples: ", len(sequences))
        for sequence in sequences:
            sequence = self.__filter_stopwords(sequence)
            # print(sequence)
            self.update(sequence)

    def update(self, sequence):
        sequence = self.__filter_stopwords(sequence)
        self.token_counter.update(sequence)

    def topk_tokens(self, sequence, topk=3):
        sequence = self.__filter_stopwords(sequence)
        token_count = [(token, self.token_counter[token])
                       for token in set(sequence)]
        topk_tuples = heapq.nlargest(topk, token_count, key=lambda x: x[1])
        topk_keys = tuple([t[0] for t in topk_tuples])
        return topk_keys

    def __len__(self):
        return len(self.token_counter)

    def __filter_stopwords(self, sequence):
        return [
            token
            for token in sequence
            if (len(token) > 2) and (token not in self.stopwords)
        ]


def clean(s):
    s = s.lower().strip()
    log_format = re.sub(r'[0-9A-Za-z, ]+', '', s)
    unique_chars = list(set(log_format))
    sorted_string = ''.join(sorted(unique_chars))
    s = re.sub('\+|\_|\#|:|\(|\)|=|,|"|\{|\}|@|$|\[|\]|\||;|\.?!', ' ', s)
    s = " ".join([word for word in s.strip().split()
                 if not bool(re.search(r'\d', word))])
    # trantab = str.maketrans(dict.fromkeys(list(string.punctuation)))
    return s, sorted_string


def hierarchical_clustering(contents):
    vocab = Vocab()
    vocab.build([v[0].split() for v in contents.values()])

    # hierarchical clustering
    hierarchical_clusters = {}
    for k, v in contents.items():
        frequent_token = tuple(sorted(vocab.topk_tokens(v[0].split(), 3)))
        log_format = v[1]
        if frequent_token not in hierarchical_clusters:
            hierarchical_clusters[frequent_token] = {
                "size": 1, "cluster": {log_format: [k]}}
        else:
            hierarchical_clusters[frequent_token]["size"] = hierarchical_clusters[frequent_token]["size"] + 1
            if log_format not in hierarchical_clusters[frequent_token]["cluster"]:
                hierarchical_clusters[frequent_token]["cluster"][log_format] = [
                    k]
            else:
                hierarchical_clusters[frequent_token]["cluster"][log_format].append(
                    k)
    print("Number of coarse-grained clusters: ",
          len(hierarchical_clusters.keys()))
    total_fine_clusters = 0
    for k, v in hierarchical_clusters.items():
        total_fine_clusters += len(hierarchical_clusters[k]["cluster"])
    print("Number of fine-grained clusters: ", total_fine_clusters)
    return hierarchical_clusters


def hierarchical_distribute(hierarchical_clusters, shot, logs=[]):
    # hierarchical distribution
    candidate_samples = []
    coarse_clusters = hierarchical_clusters.keys()
    # coarse_clusters = shuffle(list(coarse_clusters))
    coarse_clusters = sorted(
        coarse_clusters, key=lambda x: hierarchical_clusters[x]["size"], reverse=True)
    corase_size = len(coarse_clusters)
    empty_clusters = []
    print("Shot: ", shot, "Coarse size: ", corase_size)
    # for coarse_key in coarse_clusters:
    #     print(coarse_key, hierarchical_clusters[coarse_key]["size"])
    while shot > 0:
        for coarse_id, coarse_key in enumerate(coarse_clusters):
            if coarse_key in empty_clusters:
                continue
            # + (coarse_id < shot % corase_size)
            coarse_quota = max(int(shot // corase_size), 1)
            if coarse_quota == 0:
                break

            fine_clusters = hierarchical_clusters[coarse_key]["cluster"].keys()
            fine_clusters = sorted(fine_clusters, key=lambda x: len(
                hierarchical_clusters[coarse_key]["cluster"][x]), reverse=True)
            fine_size = len(fine_clusters)
            cluster_size = 0
            for fine_id, fine_key in enumerate(fine_clusters):
                fine_quota = min(
                    shot, int(coarse_quota // fine_size) + (fine_id < coarse_quota % fine_size))
                fine_quota = min(fine_quota, len(
                    hierarchical_clusters[coarse_key]["cluster"][fine_key]))
                if fine_quota == 0:
                    continue
                # empty_cluster = False
                cluster_ids = hierarchical_clusters[coarse_key]["cluster"][fine_key]
                cluster_logs = [logs[i] for i in cluster_ids]
                # print(fine_quota, len(cluster_logs))
                # while fine_quota > 0 and len(cluster_logs) > 0:
                samples_ids, num_samples = entropy_sampling(
                    cluster_logs, fine_quota)
                samples = [cluster_ids[i] for i in samples_ids]
                candidate_samples.extend(samples)
                fine_quota -= num_samples
                shot -= num_samples
                for i in sorted(samples_ids, reverse=True):
                    cluster_ids.pop(i)
                    cluster_logs.pop(i)
                cluster_size += len(
                    hierarchical_clusters[coarse_key]["cluster"][fine_key])
            # print(coarse_key, cluster_size, shot)
            if cluster_size == 0:
                empty_clusters.append(coarse_key)
                corase_size -= 1

    return candidate_samples


def sampling(logs, labels=None, shots=[8]):
    # only keep unique logs with the corresponding labels
    logs, labels = zip(*list(set(zip(logs, labels))))
    contents = {}
    for i, x in enumerate(logs):
        x, fx = clean(x)
        if len(x.split()) > 0:
            contents[i] = (x, fx)
    # content = {i: clean(x) if len(x.split()) > 1 for i, x in enumerate(labelled_logs['Content'].tolist())}
    begin_time = time.time()
    hierarchical_clusters = hierarchical_clustering(contents)
    end_time = time.time()
    clustering_time = end_time - begin_time
    print("hierarchical clustering time: ", clustering_time)
    sample_candidates = {}
    for idx, shot in enumerate(shots):
        begin_time = time.time()
        sampled_ids = hierarchical_distribute(
            deepcopy(hierarchical_clusters), shot, logs)
        if labels is not None:
            samples = [(logs[i], labels[i]) for i in sampled_ids]
        else:
            samples = [(logs[i], logs[i]) for i in sampled_ids]
        sample_candidates[shot] = samples
        end_time = time.time()
        print(f"{shot}-shot sampling time: ", (end_time - begin_time))

    return sample_candidates


if __name__ == '__main__':
    data_dir = "./datasets/loghub-2k"
    for dataset in datasets:
        print(dataset)
        log_file = benchmark[dataset]['log_file']
        print(data_dir, log_file)
        labelled_logs = pd.read_csv(
            f'{data_dir}/{log_file}_structured_corrected.csv')
        k_rate = 0.2
        length = int(k_rate * len(labelled_logs))
        labelled_logs = labelled_logs[:length]
        raw_logs = labelled_logs['Content'].tolist()
        labels = labelled_logs['EventTemplate'].tolist()
        shots = [8, 16, 32, 64, 128, 256]
        sample_candidates = sampling(raw_logs, labels, shots)
        for shot, samples in sample_candidates.items():
            with open(f'{data_dir}/{dataset}/sampled_{shot}_v2.json', 'w') as f:
                for sample in samples:
                    f.write(json.dumps(
                        {'log': sample[0], 'template': sample[1]}) + '\n')
