import subprocess
import argparse
# from evaluator import evaluate_all_datasets

datasets = [
    "Apache",
    "BGL",
    "Hadoop",
    "HDFS",
    "HealthApp",
    "HPC",
    "Linux",
    "Mac",
    "OpenSSH",
    "OpenStack",
    "Proxifier",
    "Spark",
    "Zookeeper",
    "Thunderbird"
]

def parse_single_dataset(dataset_name, args):
    script_path = "02_run_unleash.py"
    args_ftandlp = [
        "--model_name_or_path", args.model,
        "--dataset_name", f"{dataset_name}",
        "--max_train_steps", f"{args.max_train_steps}",
        "--output_dir",f"outputs/models/{dataset_name}/{args.config}", # model output dir
        "--task_output_dir",f"outputs/logs/{args.config}", # result output dir
        "--log_file", f"../datasets/loghub-2.0/{dataset_name}/{dataset_name}_full.log_structured.csv", # TODO add log file end with .log
        "--train_file", f"../datasets/loghub-2.0/{dataset_name}/samples/{args.sampling_method}_{args.shot}.json",
        "--parsing_num_processes", f"{args.num_process}",
    ]
    
    subprocess.run(["python", script_path] + args_ftandlp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="roberta-base")
    parser.add_argument("--sampling_method", type=str, default="entropy")
    parser.add_argument("--shot", type=int, default=32)
    parser.add_argument("--max_train_steps", type=int, default=1000)
    parser.add_argument("--num_process", type=int, default=1)
    
    parser.add_argument("--dataset", type=str, default='null') # for testing
    args = parser.parse_args()
    args.config = f"{args.model.split('/')[-1].split('-')[0]}_{args.sampling_method}_{args.shot}_{args.max_train_steps}_P{args.num_process}"
    if args.dataset != 'null':
        if args.dataset in datasets:
            datasets = [args.dataset]
        else:
            raise ValueError(f"Dataset {args.dataset} not found in the list of datasets.")
    for dataset in datasets:
        parse_single_dataset(dataset, args)


    if args.dataset != 'null':
        subprocess.run(["python", "../evaluation/unleash_eval.py"] + [
            "--dataset", args.dataset,
            "--config", args.config
        ])
    else:
        subprocess.run(["python", "../evaluation/unleash_eval.py"] + [
            "--config", args.config
        ])
    # To evaluate: run unleash_eval.py in dir evaluation.
    # evaluate_all_datasets(output_dir = f"outputs/results/{args.sampling_method}_{args.shot}_{args.epochs}", datasets = datasets, data_tpye = "full")