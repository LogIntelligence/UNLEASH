# UNLEASH: SOTA Semantic-based Log Parser with Pre-trained Language Models

__UNLEASH__ is and end-to-end semantic-based log parsing framework. This repository includes artifacts for reuse and reproduction of experimental results presented in our ICSE'25 paper titled _"Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models"_.

__Table of Contents__
- [Repository Structure](#repository-structure)
- [Requirements and Setup](#requirements-and-setup)
- [To run the code](#to-run-the-code)

## Repository Structure
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
├─ dev.env
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


## Requirements and Setup
The code is implemented in Python 3.9. To install the required packages, run the following command:
```
pip install -r requirements.txt
```
or import the environment.yml file to create a conda environment:
```
conda env create -f environment.yml
```

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
