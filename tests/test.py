# -*- coding: utf-8 -*-
from unleash.data.utils import load_loghub_dataset
from unleash.sampling.entropy_sampling import sampling as entropy_sampling
from unleash.sampling.lilac_sampling import sampling as lilac_sampling
from unleash.sampling.logppt_sampling import sampling as logppt_sampling
from unleash.models.roberta import RobertaForLogParsing
from unleash.models.deberta import DebertaForLogParsing


def test_load_loghub_dataset():
    """Test the load_loghub_dataset function"""
    log_df = load_loghub_dataset(dataset_name="Apache")
    assert len(log_df) > 0, "Expected more than 0 logs in the Apache dataset"


def test_sampling():
    labelled_logs = load_loghub_dataset("Apache")
    k_rate = 0.2
    length = int(k_rate * len(labelled_logs))
    labelled_logs = labelled_logs[:length]
    raw_logs = labelled_logs['Content'].tolist()
    labels = labelled_logs['EventTemplate'].tolist()
    shots = [32]
    
    ## Entropy Sampling ###
    sample_candidates = entropy_sampling(raw_logs, labels, shots)
    assert len(sample_candidates[32]) == 32, "Expected 32 samples from entropy sampling"

    ## Hierichical Sampling from LILAC ###
    sample_candidates = lilac_sampling(raw_logs, labels, shots)
    assert len(sample_candidates[32]) == 32, "Expected 32 samples from LILAC sampling"

    ## Adaptive Random Sampling from LogPPT ###
    sample_candidates = logppt_sampling(raw_logs, labels, shots)
    assert len(sample_candidates[32]) == 32, "Expected 32 samples from LogPPT sampling"

def test_model():
    import torch
    p_model = RobertaForLogParsing('roberta-base', ct_loss_weight=0.1)
    p_model.tokenizer.add_tokens(['<*>'])
    log = "mod_jk child init 1 -2"
    template = "mod_jk child init <*> <*><*>"
    batch = p_model.tokenizer([log], padding=True, truncation=True, return_tensors="pt")
    label_tokens = p_model.tokenizer.tokenize(template)
    label_tokens = ["<s>"] + [x for x in label_tokens if x != 'Ġ'] + ["</s>"]
    label_ids = p_model.tokenizer.convert_tokens_to_ids(label_tokens)
    batch['labels'] = torch.tensor(label_ids).unsqueeze(0)
    p_model.train()
    loss = p_model(batch)
    assert loss is not None, "Expected a loss from the model"
    loss.backward()
    p_model.eval()
    extracted_template = p_model.parse(log)
    assert type(extracted_template) == str, "Expected a string template from the model"
