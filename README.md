# UNLEASH: Semantic-based Log Parser with Pre-trained Language Models
[![pypi package](https://img.shields.io/pypi/v/icse-unleash.svg)](https://pypi.org/project/icse-unleash/)
[![Build and test](https://github.com/LogIntelligence/UNLEASH/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/LogIntelligence/UNLEASH/actions/workflows/build-and-test.yml)
[![Upload Python Package](https://github.com/LogIntelligence/UNLEASH/actions/workflows/python-publish.yml/badge.svg)](https://github.com/LogIntelligence/UNLEASH/actions/workflows/python-publish.yml)
[![Archived](https://archive.softwareheritage.org/badge/origin/https://github.com/LogIntelligence/UNLEASH)](https://archive.softwareheritage.org/browse/origin/https://github.com/LogIntelligence/UNLEASH/)

__UNLEASH__ is a semantic-based log parsing framework. This repository includes artifacts for reuse and reproduction of experimental results presented in our ICSE'25 paper titled _"Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models"_.

__Table of Contents__
- [Purpose](#repository-structure)
- [Provenacne](#provenance)
- [Data](#data)
- [Setup](#setup)
    - [Install Python 3.9](#install-python-39)
    - [Clone UNLEASH from GitHub](#clone-unleash-from-github)
    - [Create and activate a virtual environment](#create-and-activate-a-virtual-environment)
    - [Install UNLEASH from PyPI or Build from source](#install-unleash-from-pypi-or-build-from-source)
- [Usage](#to-run-the-code)
    - [Test the installation](#test-the-installation)
    - [Basic usage](#basic-usage)
        - [Run sampling for a specific dataset](#1-run-sampling-for-a-specific-dataset)
        - [Run UNLEASH on a specific dataset](#2-run-unleash-on-a-specific-dataset)
        - [Evaluate Unleash on a specific dataset](#3-evaluate-unleash-on-a-specific-dataset)
    - [Reproducibility](#reproducibility)
        - [Parsing Performance](#parsing-performance)
        - [Scalability and Generalization](#scalability-and-generalization)
        - [Other Settings](#other-settings)
- [Download Paper](#download-paper)
- [Citation](#citation)
- [Contact](#contact)

## Purpose

The artifacts in this repository provides the UNLEASH tool along with the neccessary benchmarks and scripts, facilitating its reuse and enabling the replication of the associated study.

## Provenance

Our artifacts are available via public archival repositories, including:
- A copy of the paper is available at: [docs/paper/ICSE_25__Unleash.pdf](docs/paper/ICSE_25___Unleash.pdf).
- The archival repository is available at: https://archive.softwareheritage.org/browse/origin/https://github.com/LogIntelligence/UNLEASH/.
- The datasets are adopted from existing works, which are publicly available at: https://zenodo.org/record/8275861.

## Data

The datasets used in the study are publicly available at: https://zenodo.org/record/8275861. The storage requirements for the datasets are approximately 966 MB (compressed) and 13 GB (uncompressed) for 14 datasets.

During the operation of UNLEASH, the datasets will be automatically downloaded and extracted to the `datasets` folder by default. You can also download the datasets manually and extract them in the `datasets` folder. The datasets should be organized as follows:
```
📦 UNLEASH
├─ datasets
│  └─ loghub-2.0
│     ├─ Apache
│     │  ├─ Apache_full.log
│     │  ├─ Apache_full.log_structured.csv
│     │  ├─ Apache_full.log_structured_corrected.csv
│     │  ├─ Apache_full.log_templates.csv
│     │  └─ Apache_full.log_templates_corrected.csv
│     ├─ ...
```


## Setup
The code is implemented in Python 3.9. We recommend using machines equipped with at least an 4-cores CPU, an 8GB **GPU**, 16GB RAM, and ~50GB available disk space with **Ubuntu 20.04** or **Ubuntu 22.04** to stably reproduce the experimental results in our paper. The full requirements to run the code can be found at [REQUIREMENTS.md](REQUIREMENTS.md).

### Install Python 3.9
We recommend using Python 3.9+ to run the code.
```bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 python3.9-venv python3.9-dev
```

### Clone UNLEASH from GitHub

```bash
git clone https://github.com/LogIntelligence/UNLEASH.git && cd UNLEASH
```

### Create and activate a virtual environment
We recommend creating a virtual environment to run the code.
```bash
python3.9 -m venv env
source env/bin/activate
```

### Install UNLEASH from PyPI or Build from source
You can install UNLEASH from PyPI or build from source.
```bash
# Install from PyPI
pip install icse-unleash

# Build from source
pip install -e .
```

## Usage

### Test the installation
```bash
pytest tests/test.py
```

<details>
<Summary>Expected output</Summary>

```bash
============================== test session starts ===============================
platform linux -- Python 3.9.21, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/ubuntu/Documents/UNLEASH
collected 3 items                                                                

tests/test.py ...                                                          [100%]

=============================== 3 passed in 3.93s ================================
```
</details>


### Basic usage

To perform log parsing on a specific dataset, you need to set the `dataset` parameter and set the working directory to the `examples` folder.
```bash
export dataset=Apache
cd examples
```

#### 1. Run sampling for a specific dataset
```bash
python 01_sampling.py --dataset $dataset --sampling_method unleash
```

<details>
<Summary>Expected output</Summary>

```bash
Apache
Loading Apache/Apache_full.log...
https://zenodo.org/records/8275861/files/Apache.zip
--2025-01-15 10:06:19--  https://zenodo.org/records/8275861/files/Apache.zip
Resolving zenodo.org (zenodo.org)... 188.185.45.92, 188.185.48.194, 188.185.43.25, ...
Connecting to zenodo.org (zenodo.org)|188.185.45.92|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 578629 (565K) [application/octet-stream]
Saving to: ‘../datasets/loghub-2.0/Apache.zip’

../datasets/loghub-2.0/Apache 100%[==============================================>] 565.07K   276KB/s    in 2.0s    

2025-01-15 10:06:22 (276 KB/s) - ‘../datasets/loghub-2.0/Apache.zip’ saved [578629/578629]

Archive:  ../datasets/loghub-2.0/Apache.zip
  inflating: ../datasets/loghub-2.0/Apache/Apache_full.log  
  inflating: ../datasets/loghub-2.0/Apache/Apache_full.log_structured.csv  
  inflating: ../datasets/loghub-2.0/Apache/Apache_full.log_templates.csv  
Loaded 51978 logs.
Build vocab with examples:  4125
Number of coarse-grained clusters:  25
Number of fine-grained clusters:  31
hierarchical clustering time:  0.018030643463134766
Shot:  8 Coarse size:  25
8-shot sampling time:  0.03555607795715332
Shot:  16 Coarse size:  25
16-shot sampling time:  0.027220964431762695
Shot:  32 Coarse size:  25
32-shot sampling time:  0.053362369537353516
Shot:  64 Coarse size:  25
64-shot sampling time:  0.13954639434814453
Shot:  128 Coarse size:  25
128-shot sampling time:  0.2863941192626953
Shot:  256 Coarse size:  25
256-shot sampling time:  0.6433525085449219
```
</details>


#### 2. Run UNLEASH on a specific dataset
```bash
python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results --max_train_steps 1000
```

<details>
<Summary>Expected output</Summary>

```bash
Generating train split: 32 examples [00:00, 28220.72 examples/s]
Generating validation split: 10395 examples [00:00, 4274908.33 examples/s]
2025-01-15 10:07:14,564 | unleash | DEBUG | Apache loaded with 32 train samples
2025-01-15 10:07:14,564 | unleash | DEBUG | Text column name: log - Label column name: template
Running tokenizer on train dataset: 100%|███████████████████████████████████| 32/32 [00:00<00:00, 2985.34 examples/s]
Running tokenizer on test dataset (num_proc=4): 100%|████████████████| 10395/10395 [00:00<00:00, 20829.57 examples/s]
2025-01-15 10:07:15,135 | unleash | DEBUG | {'train': Dataset({
    features: ['input_ids', 'labels', 'ori_labels', 'attention_mask'],
    num_rows: 32
}), 'validation': Dataset({
    features: ['input_ids', 'labels', 'ori_labels', 'attention_mask'],
    num_rows: 10395
})}
2025-01-15 10:07:15,135 | unleash | DEBUG | Train dataloader: <torch.utils.data.dataloader.DataLoader object at 0x7907fc1e2790>
2025-01-15 10:07:15,135 | unleash | DEBUG | Validation dataloader: <torch.utils.data.dataloader.DataLoader object at 0x7907fc1e2550>
2025-01-15 10:07:15,136 | unleash | INFO | Initialized Trainer
2025-01-15 10:07:15,136 | unleash | INFO | ***** Running training *****
2025-01-15 10:07:15,136 | unleash | INFO |   Num examples = 32
2025-01-15 10:07:15,136 | unleash | INFO |   Num Epochs = 500
2025-01-15 10:07:15,136 | unleash | INFO |   Instantaneous batch size per device = 16
2025-01-15 10:07:15,136 | unleash | INFO |   Total train batch size (w. parallel, distributed & accumulation) = 16
2025-01-15 10:07:15,136 | unleash | INFO |   Gradient Accumulation steps = 1
2025-01-15 10:07:15,136 | unleash | INFO |   Total optimization steps = 1000
Loss: 0.004792781546711922: 100%|████████████████████████████████████████████████| 1000/1000 [01:05<00:00, 15.16it/s]
2025-01-15 10:08:21,103 | unleash | INFO | Starting template extraction
Parsing: 100%|██████████████████████████████████████████████████████████████| 51978/51978 [00:00<00:00, 62204.15it/s]
2025-01-15 10:08:21,939 | unleash | INFO | Total time taken: 0.20595479011535645
2025-01-15 10:08:21,939 | unleash | INFO | No of model invocations: 29
2025-01-15 10:08:21,939 | unleash | INFO | Total time taken by model: 0.11258220672607422
```
</details>

#### 3. Evaluate Unleash on a specific dataset
```bash
python 03_evaluation.py --output_dir ../results --dataset $dataset
```
<details>
<Summary>Expected output</Summary>

```bash
=== Evaluation on Apache ===
../results/logs/Apache_full.log_structured.csv
Start to align with null values
100%|████████████████████████████████████████████████████| 51978/51978 [00:00<00:00, 220944.35it/s]
100%|████████████████████████████████████████████████████| 51978/51978 [00:00<00:00, 220116.95it/s]
Start compute grouping accuracy
100%|████████████████████████████████████████████████████████████| 30/30 [00:00<00:00, 1057.17it/s]
Grouping_Accuracy (GA): 1.0000, FGA: 1.0000,
Grouping Accuracy calculation done. [Time taken: 0.039]
Parsing_Accuracy (PA): 0.9953
Parsing Accuracy calculation done. [Time taken: 0.002]
100%|███████████████████████████████████████████████████████████| 30/30 [00:00<00:00, 14847.09it/s]
PTA: 0.8000, RTA: 0.8000 FTA: 0.8000
Identify : 30, Groundtruth : 30
Template-level accuracy calculation done. [Time taken: 0.010]
```
</details>

### Reproducibility

#### Parsing Performance

To reproduce the parsing performance, you can run the following command:
```bash
cd examples
bash benchmark.sh
```
**Notes:**
- The parsing accuracy (`parsing_accuracy.csv`) and parsing time (`time_cost.json`) will be saved in the corresponding folders in the `../results` directory (e.g., `../results/iteration_01/logs`).
- According to our experience, `benchmark.sh` may take up to 15 hours to complete five iterations.
- The results can differ from our paper due to the randomness of the training process as we report the average results over five iterations.

#### Scalability and Generalization

- Scalability: The scalability of UNLEASH is reflected in the parsing time and accuracy with different numbers of parsing processes. To run UNLEASH with different numbers of parsing processes, you can set the `parsing_num_processes` parameter in the `02_run_unleash.py` script and run [Step 2](#2-run-unleash-on-a-specific-dataset) again:
```bash
export num_processes=4

python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes $num_processes --output_dir ../results --max_train_steps 1000
```

- Generalization: The generalization of UNLEASH is reflected in the parsing accuracy on different pre-trained language models and numbers of training examples.

    - To run UNLEASH with different pre-trained language models, you can set the `model_name_or_path` parameter in the `02_run_unleash.py` script and run [Step 2](#2-run-unleash-on-a-specific-dataset) again:

    ```bash
    export model_name="roberta-base" # currently, we support roberta-base, microsoft/deberta-base, microsoft/codebert-base, and huggingface/CodeBERTa-small-v1
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path $model_name --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results --max_train_steps 1000
    ```

    - To run UNLEASH with different numbers of training examples, you can set the `train_file` parameter in the `02_run_unleash.py` script and run [Step 2](#2-run-unleash-on-a-specific-dataset) again:

    ```bash
    export shot=64 # can be [32, 64, 128, 256]
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_$shot.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results --max_train_steps 1000
    ```

#### Other Settings

UNLEASH provides various settings to customize the parsing process. You can set the following **main parameters**:
- For sampling (Step 1 - `01_sampling.py`):
    - `sampling_method`: The sampling method to use for selecting training examples. Currently, we support `unleash`, `lilac`, and `logppt`. To sample using all methods, set `sampling_method` to `all`.
- For parsing (Step 2 - `02_run_unleash.py`):
    - `model_name_or_path`: The pre-trained language model to use for parsing. Currently, we support `roberta-base`, `microsoft/deberta-base`, `microsoft/codebert-base`, and `huggingface/CodeBERTa-small-v1`.
    - `train_file`: The path to the training examples.
    - `max_train_steps`: The maximum number of training steps.
    - `save_model`: Whether to save the trained model.
    - `parsing_num_processes`: The number of parsing processes to use for parsing.
- To view all available parameters, you can run:
```bash
python 02_run_unleash.py --help
```


## Download Paper

The paper is available at [ICSE_25___Unleash.pdf](https://github.com/LogIntelligence/UNLEASH/blob/master/docs/paper/ICSE_25___Unleash.pdf).

## Citation

```
@inproceedings{le2025unleash,
  title={Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models},
  author={Le, Van-Hoang and Xiao, Yi and Zhang, Hongyu},
  booktitle={Proceedings of the 47th International Conference on Software Engineering},
  year={2025}
}
```

## Contact

For any questions, please contact [Van-Hoang Le](mailto:levanhoang.psa@gmail.com).
