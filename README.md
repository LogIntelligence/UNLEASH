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

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-7btt{border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
.tg .tg-zw5y{border-color:inherit;text-align:center;text-decoration:underline;vertical-align:top}
</style>
<table class="tg"><thead>
  <tr>
    <th class="tg-c3ow"></th>
    <th class="tg-7btt" colspan="4">UNLEASH</th>
    <th class="tg-7btt" colspan="4">Drain</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">GA</td>
    <td class="tg-c3ow">FGA</td>
    <td class="tg-c3ow">PA</td>
    <td class="tg-c3ow">FTA</td>
    <td class="tg-c3ow">GA</td>
    <td class="tg-c3ow">FGA</td>
    <td class="tg-c3ow">PA</td>
    <td class="tg-c3ow">FTA</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Apache</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.995</td>
    <td class="tg-c3ow">0.800</td>
    <td class="tg-c3ow">0.997</td>
    <td class="tg-c3ow">0.949</td>
    <td class="tg-c3ow">0.727</td>
    <td class="tg-c3ow">0.508</td>
  </tr>
  <tr>
    <td class="tg-c3ow">HDFS</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.968</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.925</td>
    <td class="tg-c3ow">0.999</td>
    <td class="tg-c3ow">0.935</td>
    <td class="tg-c3ow">0.57</td>
    <td class="tg-c3ow">0.522</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Hadoop</td>
    <td class="tg-c3ow">0.982</td>
    <td class="tg-c3ow">0.948</td>
    <td class="tg-c3ow">0.902</td>
    <td class="tg-c3ow">0.740</td>
    <td class="tg-c3ow">0.926</td>
    <td class="tg-c3ow">0.791</td>
    <td class="tg-c3ow">0.541</td>
    <td class="tg-c3ow">0.383</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Zookeeper</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.938</td>
    <td class="tg-c3ow">0.832</td>
    <td class="tg-c3ow">0.994</td>
    <td class="tg-c3ow">0.904</td>
    <td class="tg-c3ow">0.844</td>
    <td class="tg-c3ow">0.639</td>
  </tr>
  <tr>
    <td class="tg-c3ow">HealthApp</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.996</td>
    <td class="tg-c3ow">0.936</td>
    <td class="tg-c3ow">0.862</td>
    <td class="tg-c3ow">0.01</td>
    <td class="tg-c3ow">0.312</td>
    <td class="tg-c3ow">0.004</td>
  </tr>
  <tr>
    <td class="tg-c3ow">HPC</td>
    <td class="tg-c3ow">0.996</td>
    <td class="tg-c3ow">0.940</td>
    <td class="tg-c3ow">0.991</td>
    <td class="tg-c3ow">0.808</td>
    <td class="tg-c3ow">0.793</td>
    <td class="tg-c3ow">0.309</td>
    <td class="tg-c3ow">0.721</td>
    <td class="tg-c3ow">0.147</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Linux</td>
    <td class="tg-c3ow">0.922</td>
    <td class="tg-zw5y"><span style="font-style:italic">0.773</span></td>
    <td class="tg-c3ow">0.852</td>
    <td class="tg-c3ow">0.635</td>
    <td class="tg-c3ow">0.805</td>
    <td class="tg-c3ow"><span style="font-weight:bold">0.778</span></td>
    <td class="tg-c3ow">0.111</td>
    <td class="tg-c3ow">0.259</td>
  </tr>
  <tr>
    <td class="tg-c3ow">OpenSSH</td>
    <td class="tg-c3ow">0.748</td>
    <td class="tg-c3ow">0.877</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.904</td>
    <td class="tg-c3ow">0.707</td>
    <td class="tg-c3ow">0.872</td>
    <td class="tg-c3ow">0.586</td>
    <td class="tg-c3ow">0.487</td>
  </tr>
  <tr>
    <td class="tg-c3ow">OpenStack</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.979</td>
    <td class="tg-c3ow">0.752</td>
    <td class="tg-c3ow">0.007</td>
    <td class="tg-c3ow">0.029</td>
    <td class="tg-c3ow">0.002</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Proxifier</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">1.000</td>
    <td class="tg-c3ow">0.692</td>
    <td class="tg-c3ow">0.206</td>
    <td class="tg-c3ow">0.688</td>
    <td class="tg-c3ow">0.176</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Mac</td>
    <td class="tg-c3ow">0.913</td>
    <td class="tg-c3ow">0.767</td>
    <td class="tg-c3ow">0.747</td>
    <td class="tg-c3ow">0.503</td>
    <td class="tg-c3ow">0.761</td>
    <td class="tg-c3ow">0.229</td>
    <td class="tg-c3ow">0.357</td>
    <td class="tg-c3ow">0.069</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Spark</td>
    <td class="tg-c3ow">0.985</td>
    <td class="tg-c3ow">0.918</td>
    <td class="tg-c3ow">0.850</td>
    <td class="tg-c3ow">0.703</td>
    <td class="tg-c3ow">0.889</td>
    <td class="tg-c3ow">0.877</td>
    <td class="tg-c3ow">0.394</td>
    <td class="tg-c3ow">0.412</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Thunderbird</td>
    <td class="tg-c3ow">0.915</td>
    <td class="tg-c3ow">0.848</td>
    <td class="tg-c3ow">0.589</td>
    <td class="tg-c3ow">0.441</td>
    <td class="tg-c3ow">0.73</td>
    <td class="tg-c3ow">0.236</td>
    <td class="tg-c3ow">0.216</td>
    <td class="tg-c3ow">0.071</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BGL</td>
    <td class="tg-zw5y"><span style="font-style:italic">0.905</span></td>
    <td class="tg-c3ow">0.924</td>
    <td class="tg-c3ow">0.863</td>
    <td class="tg-c3ow">0.771</td>
    <td class="tg-c3ow"><span style="font-weight:bold">0.919</span></td>
    <td class="tg-c3ow">0.62</td>
    <td class="tg-c3ow">0.407</td>
    <td class="tg-c3ow">0.193</td>
  </tr>
  <tr>
    <td class="tg-c3ow">Average</td>
    <td class="tg-c3ow">0.955</td>
    <td class="tg-c3ow">0.926</td>
    <td class="tg-c3ow">0.909</td>
    <td class="tg-c3ow">0.784</td>
    <td class="tg-c3ow">0.845</td>
    <td class="tg-c3ow">0.552</td>
    <td class="tg-c3ow">0.465</td>
    <td class="tg-c3ow">0.277</td>
  </tr>
</tbody></table>
<!-- 
|             	| UNLEASH 	|         	|       	|       	|   Drain   	|           	|       	|       	|
|:-----------:	|:-------:	|:-------:	|:-----:	|:-----:	|:---------:	|:---------:	|:-----:	|:-----:	|
|             	|    GA   	|   FGA   	|   PA  	|  FTA  	|     GA    	|    FGA    	|   PA  	|  FTA  	|
|    Apache   	|  1.000  	|  1.000  	| 0.995 	| 0.800 	|   0.997   	|   0.949   	| 0.727 	| 0.508 	|
|     HDFS    	|  1.000  	|  0.968  	| 1.000 	| 0.925 	|   0.999   	|   0.935   	|  0.57 	| 0.522 	|
|    Hadoop   	|  0.982  	|  0.948  	| 0.902 	| 0.740 	|   0.926   	|   0.791   	| 0.541 	| 0.383 	|
|  Zookeeper  	|  1.000  	|  1.000  	| 0.938 	| 0.832 	|   0.994   	|   0.904   	| 0.844 	| 0.639 	|
|  HealthApp  	|  1.000  	|  1.000  	| 0.996 	| 0.936 	|   0.862   	|    0.01   	| 0.312 	| 0.004 	|
|     HPC     	|  0.996  	|  0.940  	| 0.991 	| 0.808 	|   0.793   	|   0.309   	| 0.721 	| 0.147 	|
|    Linux    	|  0.922  	| <u>_0.773_</u> 	| 0.852 	| 0.635 	|   0.805   	| **0.778** 	| 0.111 	| 0.259 	|
|   OpenSSH   	|  0.748  	|  0.877  	| 1.000 	| 0.904 	|   0.707   	|   0.872   	| 0.586 	| 0.487 	|
|  OpenStack  	|  1.000  	|  1.000  	| 1.000 	| 0.979 	|   0.752   	|   0.007   	| 0.029 	| 0.002 	|
|  Proxifier  	|  1.000  	|  1.000  	| 1.000 	| 1.000 	|   0.692   	|   0.206   	| 0.688 	| 0.176 	|
|     Mac     	|  0.913  	|  0.767  	| 0.747 	| 0.503 	|   0.761   	|   0.229   	| 0.357 	| 0.069 	|
|    Spark    	|  0.985  	|  0.918  	| 0.850 	| 0.703 	|   0.889   	|   0.877   	| 0.394 	| 0.412 	|
| Thunderbird 	|  0.915  	|  0.848  	| 0.589 	| 0.441 	|    0.73   	|   0.236   	| 0.216 	| 0.071 	|
|     BGL     	| <u>_0.905_</u>	|  0.924  	| 0.863 	| 0.771 	| **0.919** 	|    0.62   	| 0.407 	| 0.193 	|
|   Average   	|  0.955  	|  0.926  	| 0.909 	| 0.784 	|   0.845   	|   0.552   	| 0.465 	| 0.277 	| -->

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