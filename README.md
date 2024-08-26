# UNLEASH
Submission #1161: Unleashing the True Potential of Semantic-based Log Parsing with Pre-trained Language Models


## Introduction
In this paper, we show that semantic-based log parsers with small PLMs can actually achieve better or comparable performance to state-of-the- art LLM-based log parsing models while being more efficient and cost-effective. We propose UNLEASH, a novel semantic-based log parsing approach, which incorporates three enhancement methods to boost the performance of PLMs for log parsing, including (1) an entropy-based ranking method to select the most informative log samples; (2) a contrastive learning method to enhance the fine-tuning process; and (3) an inference optimization method to improve the log parsing performance. We evaluate UNLEASH on a set of large-scale, public log datasets and the experimental results show that UNLEASH is effective and efficient compared to state-of-the-art log parsers.

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

## Addtional Experimental Results

### Comparison with Traditional Log Parsing Methods

#### Accuracy

<!-- <style>
table, th, td {
  border: 1px solid black;
}
</style> -->
<table><thead>
  <tr>
    <th></th>
    <th colspan="4">UNLEASH</th>
    <th colspan="4">Drain</th>
    <th colspan="4">AEL</th>
  </tr></thead>
<tbody>
  <tr>
    <td></td>
    <td>GA</td>
    <td>FGA</td>
    <td>PA</td>
    <td>FTA</td>
    <td>GA</td>
    <td>FGA</td>
    <td>PA</td>
    <td>FTA</td>
    <td>GA</td>
    <td>FGA</td>
    <td>PA</td>
    <td>FTA</td>
  </tr>
  <tr>
    <td>Apache</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>0.995</td>
    <td>0.800</td>
    <td>0.997</td>
    <td>0.949</td>
    <td>0.727</td>
    <td>0.508</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>0.727</td>
    <td>0.517</td>
  </tr>
  <tr>
    <td>HDFS</td>
    <td>1.000</td>
    <td>0.968</td>
    <td>1.000</td>
    <td>0.925</td>
    <td>0.999</td>
    <td>0.935</td>
    <td>0.57</td>
    <td>0.522</td>
    <td>0.999</td>
    <td>0.764</td>
    <td>0.621</td>
    <td>0.562</td>
  </tr>
  <tr>
    <td>Hadoop</td>
    <td>0.982</td>
    <td>0.948</td>
    <td>0.902</td>
    <td>0.740</td>
    <td>0.926</td>
    <td>0.791</td>
    <td>0.541</td>
    <td>0.383</td>
    <td>0.823</td>
    <td>0.117</td>
    <td>0.535</td>
    <td>0.058</td>
  </tr>
  <tr>
    <td>Zookeeper</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>0.938</td>
    <td>0.832</td>
    <td>0.994</td>
    <td>0.904</td>
    <td>0.844</td>
    <td>0.639</td>
    <td>0.996</td>
    <td>0.788</td>
    <td>0.742</td>
    <td>0.465</td>
  </tr>
  <tr>
    <td>HealthApp</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>0.996</td>
    <td>0.936</td>
    <td>0.862</td>
    <td>0.01</td>
    <td>0.312</td>
    <td>0.004</td>
    <td>0.725</td>
    <td>0.008</td>
    <td>0.311</td>
    <td>0.003</td>
  </tr>
  <tr>
    <td>HPC</td>
    <td>0.996</td>
    <td>0.940</td>
    <td>0.991</td>
    <td>0.808</td>
    <td>0.793</td>
    <td>0.309</td>
    <td>0.721</td>
    <td>0.147</td>
    <td>0.748</td>
    <td>0.201</td>
    <td>0.741</td>
    <td>0.136</td>
  </tr>
  <tr>
    <td>Linux</td>
    <td>0.922</td>
    <td><u>0.773</u></td>
    <td>0.852</td>
    <td>0.635</td>
    <td>0.805</td>
    <td><b>0.778</b></td>
    <td>0.111</td>
    <td>0.259</td>
    <td>0.916</td>
    <td><b>0.806</b></td>
    <td>0.082</td>
    <td>0.217</td>
  </tr>
  <tr>
    <td>OpenSSH</td>
    <td>0.748</td>
    <td>0.877</td>
    <td>1.000</td>
    <td>0.904</td>
    <td>0.707</td>
    <td>0.872</td>
    <td>0.586</td>
    <td>0.487</td>
    <td>0.705</td>
    <td>0.689</td>
    <td>0.364</td>
    <td>0.333</td>
  </tr>
  <tr>
    <td>OpenStack</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>0.979</td>
    <td>0.752</td>
    <td>0.007</td>
    <td>0.029</td>
    <td>0.002</td>
    <td>0.743</td>
    <td>0.682</td>
    <td>0.029</td>
    <td>0.165</td>
  </tr>
  <tr>
    <td>Proxifier</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>1.000</td>
    <td>0.692</td>
    <td>0.206</td>
    <td>0.688</td>
    <td>0.176</td>
    <td>0.974</td>
    <td>0.667</td>
    <td>0.677</td>
    <td>0.417</td>
  </tr>
  <tr>
    <td>Mac</td>
    <td>0.913</td>
    <td>0.767</td>
    <td>0.747</td>
    <td>0.503</td>
    <td>0.761</td>
    <td>0.229</td>
    <td>0.357</td>
    <td>0.069</td>
    <td>0.797</td>
    <td>0.793</td>
    <td>0.245</td>
    <td>0.205</td>
  </tr>
  <tr>
    <td>Spark</td>
    <td>0.985</td>
    <td>0.918</td>
    <td>0.850</td>
    <td>0.703</td>
    <td>0.889</td>
    <td>0.877</td>
    <td>0.394</td>
    <td>0.412</td>
    <td>___</td>
    <td>___</td>
    <td>___</td>
    <td>___</td>
  </tr>
  <tr>
    <td>Thunderbird</td>
    <td>0.915</td>
    <td>0.848</td>
    <td>0.589</td>
    <td>0.441</td>
    <td>0.73</td>
    <td>0.236</td>
    <td>0.216</td>
    <td>0.071</td>
    <td>0.786</td>
    <td>0.116</td>
    <td>0.163</td>
    <td>0.035</td>
  </tr>
  <tr>
    <td>BGL</td>
    <td><u>0.905</u></td>
    <td>0.924</td>
    <td>0.863</td>
    <td>0.771</td>
    <td><b>0.919</b></td>
    <td>0.62</td>
    <td>0.407</td>
    <td>0.193</td>
    <td><b>0.915</b></td>
    <td>0.587</td>
    <td>0.406</td>
    <td>0.165</td>
  </tr>
  <tr>
    <td>Average</td>
    <td>0.955</td>
    <td>0.926</td>
    <td>0.909</td>
    <td>0.784</td>
    <td>0.845</td>
    <td>0.552</td>
    <td>0.465</td>
    <td>0.277</td>
    <td>0.856</td>
    <td>0.555</td>
    <td>0.442</td>
    <td>0.252</td>
  </tr>
</tbody></table>


#### Efficiency
<table><thead>
  <tr>
    <th></th>
    <th>UNLEASH (1 core)</th>
    <th>UNLEASH (4 cores)</th>
    <th>Drain</th>
    <th>AEL</th>
  </tr></thead>
<tbody>
  <tr>
    <td>Apache</td>
    <td>2.5</td>
    <td>2.5</td>
    <td>4.2</td>
    <td>2.7</td>
  </tr>
  <tr>
    <td>HDFS</td>
    <td>775.1</td>
    <td>190.1</td>
    <td>1,130.4</td>
    <td>1403.0</td>
  </tr>
  <tr>
    <td>Hadoop</td>
    <td>13.2</td>
    <td>14.0</td>
    <td>18.8</td>
    <td>83.1</td>
  </tr>
  <tr>
    <td>Zookeeper</td>
    <td>1.8</td>
    <td>1.7</td>
    <td>9.6</td>
    <td>2.8</td>
  </tr>
  <tr>
    <td>HealthApp</td>
    <td>5.7</td>
    <td>5.0</td>
    <td>15.3</td>
    <td>349.5</td>
  </tr>
  <tr>
    <td>HPC</td>
    <td>5.5</td>
    <td>5.9</td>
    <td>32.7</td>
    <td>344.1</td>
  </tr>
  <tr>
    <td>Linux</td>
    <td>4.0</td>
    <td>4.0</td>
    <td>9.8</td>
    <td>3.9</td>
  </tr>
  <tr>
    <td>OpenSSH</td>
    <td>28.2</td>
    <td>12.0</td>
    <td>61.8</td>
    <td>344.1</td>
  </tr>
  <tr>
    <td>OpenStack</td>
    <td>14.9</td>
    <td>14.9</td>
    <td>73.0</td>
    <td>25.7</td>
  </tr>
  <tr>
    <td>Proxifier</td>
    <td>1.6</td>
    <td>1.6</td>
    <td>2.8</td>
    <td>2.8</td>
  </tr>
  <tr>
    <td>Mac</td>
    <td>52.2</td>
    <td>60.6</td>
    <td>17.6</td>
    <td>8.6</td>
  </tr>
  <tr>
    <td>Spark</td>
    <td>758.0</td>
    <td>247.6</td>
    <td>1,737.9</td>
    <td>___</td>
  </tr>
  <tr>
    <td>Thunderbird</td>
    <td>8,561.7</td>
    <td>1,189.6</td>
    <td>2,071.3</td>
    <td>11807.5</td>
  </tr>
  <tr>
    <td>BGL</td>
    <td>325.5</td>
    <td>128.3</td>
    <td>424.6</td>
    <td>9269.8</td>
  </tr>
  <tr>
    <td>Average</td>
    <td>753.6</td>
    <td><b>34.1</b></td>
    <td>400.7</td>
    <td>1793.6</td>
  </tr>
</tbody></table>