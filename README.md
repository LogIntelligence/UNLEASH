# UNLEASH: SOTA Semantic-based Log Parser with Pre-trained Language Models

__UNLEASH__ is and end-to-end semantic-based log parsing framework. This repository includes artifacts for reuse and reproduction of experimental results presented in our ICSE'25 paper titled _"Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models"_.

__Table of Contents__
- [Requirements and Setup](#requirements-and-setup)
- [Repository Structure](#repository-structure)
- [To run the code](#to-run-the-code)

## Requirements and Setup
The code is implemented in Python 3.9. To install the required packages, run the following command:
```
pip install -r requirements.txt
```
or import the environment.yml file to create a conda environment:
```
conda env create -f environment.yml
```

## Repository Structure
```
├── datasets
│   └── loghub-2.0
│       ├── Apache
│       │   ├── Apache_full.log_structured.csv
│       │   ├── Apache_full.log_templates.csv
│       │   ├── samples
│       │   │   ├── entropy_32.json
│       │   │   ├── lilac_32.json
│       │   │   ├── logppt_32.json
|       |   |   ├── ...
│       │   └── validation.json
│       ├── ...
├── evaluation
│   ├── utils
│   ├── settings.py
│   ├── unleash_eval.py
├── examples
│   ├── 01_sampling.py
│   ├── 02_run_unleash.py
│   ├── benchmark.py
├── unleash
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── utils.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── roberta.py
│   |   ├── deberta.py
│   ├── sampling
│   │   ├── __init__.py
│   │   ├── entropy_sampling.py
│   │   ├── lilac_sampling.py
│   │   ├── logppt_sampling.py
│   |   ├── utils.py
│   ├── tuning
│   │   ├── __init__.py
│   │   ├── early_stopping.py
│   │   ├── trainer.py
│   │   ├── utils.py
│   ├── parsing_base.py
│   ├── parsing_cache.py
│   ├── postprocessing.py
```

## To run the code
### Download the data
Download the log datasets from [Loghub](https://zenodo.org/records/8275861) and extract them in the `datasets/loghub-2.0` folder.

### 1. Run sampling
Set the `data_dir` variable in the `01_sampling.py` file to the path of the loghub-2.0 folder and the `output_dir` variable to the path where you want to save the sampled data.
Then run the following command:

```bash
cd examples
python 01_sampling.py
```

### 2. Run UNLEASH on a specific dataset
```bash
cd examples
export dataset=Apache
python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/entropy_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results/models/$dataset --task_output_dir ../results/logs/$dataset --parsing_num_processes 1
```
Set `parsing_num_processes` to the number of CPU cores you want to use for parsing. The results will be saved in the `results` folder.

### 3. To benchmark on all datasets
```bash
cd examples
python benchmark.py
```
