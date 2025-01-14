#!/bin/bash

for p in 1 4 8 16 32; do
    echo "========= Using $p processes ========="
    for dataset in Apache BGL Hadoop HDFS HealthApp HPC Linux Mac OpenSSH OpenStack Proxifier Spark Zookeeper Thunderbird; do
        python 01_sampling.py $dataset
        python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/entropy_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes $p --output_dir ../results/${p}_processes --max_train_steps 1000
    done
    python 03_evaluation.py --output_dir ../results/${p}_processes
done