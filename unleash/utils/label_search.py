"""Automatic label search helpers."""

import itertools
from collections import Counter

import torch
import tqdm
import multiprocessing
import numpy as np
import scipy.spatial as spatial
import scipy.special as special
import scipy.stats as stats

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def get_initial_label_words(model, loader, val_label=1):
    initial_label_words = []
    for step, batch in enumerate(loader):
        label = batch.pop('ori_labels')
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'])
        logits = torch.topk(outputs.logits.log_softmax(dim=-1), k=5).indices
        for i in range(label.shape[0]):
            for j in range(len(label[i])):
                if label[i][j] != val_label:
                    continue
                initial_label_words.extend(logits[i][j].detach().cpu().clone().tolist())

    return list(set(initial_label_words))


def find_labels(model, train, eval, keywords, val_label=1):
    # Get top indices based on conditional likelihood using the LM.
    model.to(device)
    model.eval()
    initial_label_words = get_initial_label_words(model, train, val_label)
    label_words_freq = {}
    for batch in eval:
        for inp in batch['input_ids'].detach().clone().tolist():
            for i in inp:
                if i in initial_label_words and i not in keywords:
                    if i not in label_words_freq.keys():
                        label_words_freq[i] = 0
                    label_words_freq[i] += 1
                    
    label_words_freq = {x[0]: x[1] for x in sorted(label_words_freq.items(), key=lambda k: k[1], reverse=True)}
    return label_words_freq