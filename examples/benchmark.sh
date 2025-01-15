#!/bin/bash

# We repeat the experiment 5 times

## Iteration 1

echo "==================== Iteration 1 ===================="

for dataset in Apache BGL Hadoop HDFS HealthApp HPC Linux Mac OpenSSH OpenStack Proxifier Spark Zookeeper Thunderbird; do
    python 01_sampling.py --dataset $dataset --sampling_method unleash
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results/iteration_01 --max_train_steps 1000
done

python 03_evaluation.py --output_dir ../results/iteration_01

## Iteration 2

echo "==================== Iteration 2 ===================="

for dataset in Apache BGL Hadoop HDFS HealthApp HPC Linux Mac OpenSSH OpenStack Proxifier Spark Zookeeper Thunderbird; do
    python 01_sampling.py --dataset $dataset --sampling_method unleash
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results/iteration_02 --max_train_steps 1000
done

python 03_evaluation.py --output_dir ../results/iteration_02

## Iteration 3

echo "==================== Iteration 3 ===================="

for dataset in Apache BGL Hadoop HDFS HealthApp HPC Linux Mac OpenSSH OpenStack Proxifier Spark Zookeeper Thunderbird; do
    python 01_sampling.py --dataset $dataset --sampling_method unleash
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results/iteration_03 --max_train_steps 1000
done

python 03_evaluation.py --output_dir ../results/iteration_03

## Iteration 4

echo "==================== Iteration 4 ===================="

for dataset in Apache BGL Hadoop HDFS HealthApp HPC Linux Mac OpenSSH OpenStack Proxifier Spark Zookeeper Thunderbird; do
    python 01_sampling.py --dataset $dataset --sampling_method unleash
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results/iteration_04 --max_train_steps 1000
done

python 03_evaluation.py --output_dir ../results/iteration_04

## Iteration 5

echo "==================== Iteration 5 ===================="

for dataset in Apache BGL Hadoop HDFS HealthApp HPC Linux Mac OpenSSH OpenStack Proxifier Spark Zookeeper Thunderbird; do
    python 01_sampling.py --dataset $dataset --sampling_method unleash
    python 02_run_unleash.py --log_file ../datasets/loghub-2.0/$dataset/${dataset}_full.log_structured.csv --model_name_or_path roberta-base --train_file ../datasets/loghub-2.0/$dataset/samples/unleash_32.json --validation_file ../datasets/loghub-2.0/$dataset/validation.json --dataset_name $dataset --parsing_num_processes 1 --output_dir ../results/iteration_05 --max_train_steps 1000
done

python 03_evaluation.py --output_dir ../results/iteration_05