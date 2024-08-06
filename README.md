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
<table>
<thead>
  <tr>
    <th></th>
    <th colspan="4">UNLEASH</th>
    <th colspan="4">Drain</th>
  </tr>
</thead>
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
  </tr>
</tbody></table>


#### Efficiency

|             	| **UNLEASH (1 core)** 	| **UNLEASH (4 cores)** 	| **Drain** 	|
|:-----------:	|:--------------------:	|:---------------------:	|:---------:	|
|    Apache   	|         2.45         	|          2.46         	|    4.24   	|
|     HDFS    	|        775.12        	|         190.10        	|  1,130.40 	|
|    Hadoop   	|         13.24        	|         14.03         	|   18.83   	|
|  Zookeeper  	|         1.80         	|          1.74         	|    9.63   	|
|  HealthApp  	|         5.65         	|          4.99         	|   15.27   	|
|     HPC     	|         5.48         	|          5.92         	|   32.66   	|
|    Linux    	|         3.98         	|          4.04         	|    9.78   	|
|   OpenSSH   	|         28.21        	|         12.00         	|   61.82   	|
|  OpenStack  	|         14.94        	|         14.87         	|   73.01   	|
|  Proxifier  	|         1.63         	|          1.61         	|    2.75   	|
|     Mac     	|         52.15        	|         60.61         	|   17.58   	|
|    Spark    	|        758.01        	|         247.63        	|  1,737.89 	|
| Thunderbird 	|       8,561.71       	|        1,189.58       	|  2,071.28 	|
|     BGL     	|        325.45        	|         128.28        	|   424.58  	|
|   Average   	|        753.56        	|       **134.13**      	|   400.69  	|