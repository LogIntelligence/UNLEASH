# UNLEASH: SOTA Semantic-based Log Parser with Pre-trained Language Models

__UNLEASH__ is and end-to-end semantic-based log parsing framework. This repository includes artifacts for reuse and reproduction of experimental results presented in our ICSE'25 paper titled _"Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models"_.

__Table of Contents__
- [Repository Structure](#repository-structure)
- [Installation Instruction](#installation-instruction)
    - [Install Python 3.9](#install-python-39)
    - [Clone UNLEASH from GitHub](#clone-unleash-from-github)
    - [Create and activate a virtual environment](#create-and-activate-a-virtual-environment)
    - [Install UNLEASH from PyPI or Build from source](#install-unleash-from-pypi-or-build-from-source)
    - [Test the installation](#test-the-installation)
- [To run the code](#to-run-the-code)
- [Reproducibility](#reproducibility)
    - [RQ1 - Parsing Efficaicy](#rq1---parsing-efficaicy)
    - [RQ2 - Scalability and Generalization](#rq2---scalability-and-generalization)
    - [RQ3-5 - The Impact of Enhancement Mechanisms](#rq3---the-impact-of-enhancement-mechanisms)

- [Download Paper](#download-paper)
- [Citation](#citation)
- [Contact](#contact)

## Repository Structure

There are three main components in the repository:
1. `datasets`: Contains the log datasets used in the experiments.
2. `examples`: Contains the scripts to run the experiments.
3. `unleash`: Contains the implementation of UNLEASH.

<details>
<Summary>The main structure of the repository would look like this</Summary>

```
📦 UNLEASH
├─ LICENSE
├─ README.md
├─ datasets
│  └─ loghub-2.0
│     ├─ Apache
│     │  ├─ Apache_full.log
│     │  ├─ Apache_full.log_structured.csv
│     │  ├─ Apache_full.log_structured_corrected.csv
│     │  ├─ Apache_full.log_templates.csv
│     │  └─ Apache_full.log_templates_corrected.csv
│     ├─ ...
├─ docs
│  ├─ CL.png
│  ├─ Ob2_res.png
│  ├─ Ob3_res.png
│  ├─ RESULTS.md
│  └─ S_test_1.png
├─ environment.yml
├─ examples
│  ├─ 01_sampling.py
│  ├─ 02_run_unleash.py
│  ├─ 03_evaluation.py
│  ├─ benchmark.py
│  └─ config.py
├─ requirements.txt
├─ setup.py
├─ tests
│  └─ test.py
└─ unleash
   ├─ __init__.py
   ├─ arguments.py
   ├─ data
   │  ├─ __init__.py
   │  ├─ data_loader.py
   │  └─ utils.py
   ├─ evaluation
   │  ├─ settings.py
   │  └─ utils
   │     ├─ GA_calculator.py
   │     ├─ PA_calculator.py
   │     ├─ common.py
   │     ├─ evaluator_main.py
   │     ├─ oracle_template_correction.py
   │     ├─ post_process.py
   │     ├─ postprocess.py
   │     └─ template_level_analysis.py
   ├─ models
   │  ├─ __init__.py
   │  ├─ base.py
   │  ├─ deberta.py
   │  └─ roberta.py
   ├─ parsing_base.py
   ├─ parsing_cache.py
   ├─ postprocess.py
   ├─ sampling
   │  ├─ __init__.py
   │  ├─ entropy_sampling.py
   │  ├─ lilac_sampling.py
   │  ├─ logppt_sampling.py
   │  └─ utils.py
   └─ tuning
      ├─ __init__.py
      ├─ early_stopping.py
      ├─ trainer.py
      └─ utils.py
```
</details>


## Installation Instruction
The code is implemented in Python 3.9.

### Install Python 3.9
We recommend using Python 3.9+ to run the code.
```bash
sudo apt update
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
pip install unleash

# Build from source
pip install -e .
```

### Test the installation
```bash
pytest tests/test.py
```

<details>
<Summary>Expected output</Summary>

```bash
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-6.2.5, pluggy-1.0.0
rootdir: /home/username/UNLEASH
collected 1 item

tests/test.py .                                                         [100%]

============================== 1 passed in 0.01s ===============================
```
</details>

## To run the code
### Download the data
Download the log datasets from [Loghub](https://zenodo.org/records/8275861) and extract them in the `datasets/loghub-2.0` folder.

### 1. Run sampling for a specific dataset
Set the `data_dir` variable in the `01_sampling.py` file to the path of the loghub-2.0 folder and the `output_dir` variable to the path where you want to save the sampled data.
Then run the following command:

```bash
cd examples
python 01_sampling.py Apache
```

### 2. Run UNLEASH on a specific dataset
```bash
cd examples
export dataset=Apache
python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/entropy_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results --max_train_steps 1000
```
Set `parsing_num_processes` to the number of CPU cores you want to use for parsing. The results will be saved in the `results` folder.

### 3. Evaluate Unleash on a specific dataset
```bash
cd examples
export dataset=Apache
python 03_evaluation.py --output_dir ../results --dataset $dataset
```
