import os
import pandas as pd
from nltk.metrics.distance import edit_distance
from sklearn.metrics import accuracy_score
import numpy as np
from tqdm import tqdm


def calculate_avg(numbers, round_num = 4):
    avg = sum(numbers) / len(numbers)
    numbers.append(avg)
    numbers = [round(num, round_num) for num in numbers]
    return numbers


def evaluate_all_datasets(output_dir, datasets = [], data_tpye = 'full'):
    
    table_data = {
        'dataset': [],
        'GA': [],
        'PA': [],
        'ED': []
    }

    metrics = {}

    file_name = output_dir.split('/')[-1]

    result_table_path = f'outputs/results/result_table_{file_name}.csv'
    ga, pa, ed,n_ed = [], [], [], []
    for dataset in datasets:
        metrics[dataset] = {
            'GA': [],
            'PA': [],
            'ED': []
        }
        table_data['dataset'].append(dataset)
        output_file = f'{output_dir}/{dataset}_{data_tpye}.log_structured.csv'

        a, b, c, d = evaluate(output_file=output_file, groundtruth_file=f'../datasets/loghub-2.0/{dataset}/{dataset}_{data_tpye}.log_structured.csv', dataset=dataset, debug = True)
        ga.append(a)
        pa.append(b)
        ed.append(c)
        n_ed.append(d)

    table_data['dataset'].append('avg')
    table_data['GA'] = calculate_avg(ga)
    table_data['PA'] = calculate_avg(pa)
    table_data['ED'] = calculate_avg(ed)
    table_data['N_ED'] = calculate_avg(n_ed,5)

    df = pd.DataFrame(table_data)
    df.to_csv(result_table_path, index=False)


def evaluate(output_file, groundtruth_file, dataset, mismatch=False,  debug = False):

    if debug:
        print(f'loading {dataset}....')

    df1 = pd.read_csv(output_file)
    df2 = pd.read_csv(groundtruth_file)
    length_logs = len(df1['EventTemplate'].values)


    # Remove invalid groundtruth event Ids
    null_logids = df2[~df2['EventTemplate'].isnull()].index
    df1 = df1.loc[null_logids]
    df2 = df2.loc[null_logids]

    # MLA
    iterable = zip(df1['EventTemplate'].values, df2['EventTemplate'].values)
    if debug:
        print('Calculating Message-Level Accuracy....')
        iterable = tqdm(iterable, total=length_logs)
    # accuracy_MLA = accuracy_score(np.array(df1['EventTemplate'].values, dtype='str'),np.array(df2['EventTemplate'], dtype='str'))
    count_MLA = 0
    for i, j in iterable:
        if i == j:
            count_MLA += 1
    accuracy_MLA = count_MLA / length_logs
    # print(accuracy_MLA)

    # Ouput Mismatch Logs
    if mismatch:
        head,_,_ = output_file.rpartition('/')
        os.makedirs(f'{head}/mismatch', exist_ok=True)
        df_mismatch = df1[df1.EventTemplate != df2.EventTemplate]
        df_mismatch[['Content', 'EventTemplate']].to_csv(
            f'{head}/mismatch/{dataset}.csv', index=False)

    # # ED and NED
    # edit_distance_result = []
    # normalized_ed_result = []

    # iterable = zip(df1['Template'].values, df2['EventTemplate'].values)
    # if debug:
    #     print('Calculating Edit Distance....')
    #     iterable = tqdm(iterable, total=length_logs)

    # for i, j in iterable:
    #     if i != j:
    #         ed = edit_distance(i, j)
    #         normalized_ed = 1 - ed / max(len(i), len(j))
    #         edit_distance_result.append(ed)
    #         normalized_ed_result.append(normalized_ed)

    # length_logs = len(df1['Template'].values)
    # accuracy_ED = sum(edit_distance_result) / length_logs
    # accuracy_NED = (sum(normalized_ed_result) + length_logs - len(normalized_ed_result)) / length_logs

    accuracy_ED = 0
    accuracy_NED = 0

    
    # GA
    accuracy_GA = get_accuracy_GA(df1['EventTemplate'],df2['EventTemplate'], debug)

    dataset = ' ' * (12 - len(dataset)) + dataset 
    print('%s: Group Accuracy: %.4f, Message-Level Accuracy: %.4f, Edit Distance: %.4f, Normalized Edit Distance: %.4f' % (dataset, accuracy_GA, accuracy_MLA, accuracy_ED, accuracy_NED))
    return accuracy_GA, accuracy_MLA, accuracy_ED, accuracy_NED



def get_accuracy_GA(series_groundtruth, series_parsedlog, debug):

    series_parsedlog_valuecounts = series_parsedlog.value_counts()
    accurate_events = 0  # determine how many lines are correctly parsed

    iterable = series_parsedlog_valuecounts.index
    if debug:
        print('Calculating Group Accuracy....')
        iterable = tqdm(iterable, total=len(series_parsedlog_valuecounts.index))

    for parsed_eventId in iterable:
        logIds = series_parsedlog[series_parsedlog == parsed_eventId].index
        series_groundtruth_logId_valuecounts = series_groundtruth[logIds].value_counts()
        if series_groundtruth_logId_valuecounts.size == 1:
            groundtruth_eventId = series_groundtruth_logId_valuecounts.index[0]
            if logIds.size == series_groundtruth[series_groundtruth == groundtruth_eventId].size:
                accurate_events += logIds.size
        
    accuracy_GA = float(accurate_events) / series_groundtruth.size
    return accuracy_GA


# evaluate_all_datasets("outputs/results/logppt_32_100", ["OpenSSH"])