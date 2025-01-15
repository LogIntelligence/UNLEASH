from abc import ABC, abstractmethod
from datasets import load_dataset
import copy
import re
from torch.utils.data import DataLoader
from unleash.data.utils import CustomDataCollator

filter_list = ["and", "or", "the", "a", "of", "to", "at"]
delimiters = r"([ |\(|\)|\[|\]|\{|\})])"


def align_with_null_values(log, template):
    """
    Align the null values
    """

    pattern_parts = template.split("<*>")
    pattern_parts_escaped = [re.escape(part) for part in pattern_parts]
    regex_pattern = "(.*?)".join(pattern_parts_escaped)
    regex = "^" + regex_pattern + "$"
    matches = re.search(regex, log)

    if matches is None:
        return template

    parts = []
    for index, part in enumerate(template.split("<*>")):
        parts.append(part)
        if index < len(matches.groups()):
            if matches.groups()[index] == '':
                parts.append('')
            else:
                parts.append('<*>')
    return ''.join(parts)


def get_template_regex(template):
    """
    :param template: template regex with <*> indicates parameters
    :return: regex pattern
    """
    # template_regex = re.sub(r"<.{1,5}>", "<*>", template_regex)
    if "<*>" not in template:
        return None
    template_regex = re.sub(r'([^A-Za-z0-9])', r'\\\1', template)
    template_regex = re.sub(r'\\ +', r'\\s+', template_regex)
    template_regex = "^" + template_regex.replace(r"\<\*\>", "(.*?)") + "$"
    return template_regex


class BaseDataLoader(ABC):
    def __init__(self, config) -> None:
        self.config = config
        self.vtoken = "<*>"

    def size(self):
        return len(self.raw_datasets['train'])

    def get_train_dataloader(self):
        """
        Returns the training dataloader
        """
        return self.train_loader

    def get_val_dataloader(self):
        """
        Returns the validation dataloader
        """
        return self.val_loader

    def get_test_dataloader(self):
        """
        Returns the test dataloader
        """
        return self.val_loader

    def load_data(self):
        """
        Load data from file
        """
        # Get the datasets: the data file are JSON files
        data_files = {}
        if self.config.train_file is not None:
            data_files["train"] = [self.config.train_file]
        if self.config.validation_file is not None:
            data_files["validation"] = self.config.validation_file
        if self.config.dev_file is not None:
            data_files["dev"] = self.config.dev_file

        self.raw_datasets = load_dataset("json", data_files=data_files)

        if self.raw_datasets["train"] is not None:
            column_names = self.raw_datasets["train"].column_names
        else:
            column_names = self.raw_datasets["validation"].column_names

        if self.config.text_column_name is not None:
            text_column_name = self.config.text_column_name
        else:
            text_column_name = column_names[0]

        if self.config.label_column_name is not None:
            label_column_name = self.config.label_column_name
        else:
            label_column_name = column_names[1]
        self.text_column_name = text_column_name
        self.label_column_name = label_column_name

    @abstractmethod
    def initialize(self, tokenizer):
        pass

    @abstractmethod
    def tokenize(self):
        pass

    @abstractmethod
    def build_dataloaders(self):
        pass


class DataLoaderForPromptTuning(BaseDataLoader):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.load_data()

    def initialize(self, tokenizer):
        self.tokenizer = tokenizer
        self.ori_label_token_map = {
            self.vtoken: []
        }

        sorted_add_tokens = sorted(
            list(self.ori_label_token_map.keys()), key=lambda x: len(x), reverse=True)
        self.tokenizer.add_tokens(sorted_add_tokens)

        self.label_list = list(self.ori_label_token_map.keys())
        self.label_list += 'o'
        self.label_to_id = {'o': 0}
        for label in self.label_list:
            if label != 'o':
                self.label_to_id[label] = len(self.label_to_id)

        new_label_to_id = copy.deepcopy(self.label_to_id)
        self.label_to_id = new_label_to_id
        self.id_to_label = {id: label for label,
                            id in self.label_to_id.items()}
        self.label_token_map = {
            item: item for item in self.ori_label_token_map}
        self.label_token_to_id = {label: tokenizer.convert_tokens_to_ids(label_token) for label, label_token in
                                  self.label_token_map.items()}
        self.label_token_id_to_label = {
            idx: label for label, idx in self.label_token_to_id.items()}

        return self.tokenizer

    def tokenize(self):
        label_words = []
        keywords = []

        def tokenize_and_align_labels(examples):
            target_tokens = []
            tag_labels = []
            input_ids = []
            attention_masks = []
            for i, (log, label) in enumerate(zip(examples[self.text_column_name], examples[self.label_column_name])):
                log = " ".join(log.strip().split())
                label = " ".join(label.strip().split())
                template_regex = get_template_regex(label)
                # print(template_regex, log)
                if template_regex is None:
                    input_tokens, label_tokens = [log], ['o']
                else:
                    match = next(re.finditer(template_regex, log))
                    input_tokens = []
                    label_tokens = []
                    cur_position = 0
                    for idx in range(match.lastindex):
                        start, end = match.span(idx + 1)
                        if start > cur_position:
                            input_tokens.append(
                                log[cur_position:start].rstrip())
                            label_tokens.append("o")
                        input_tokens.append(log[start:end])
                        if start > 0 and log[start - 1] == " ":
                            input_tokens[-1] = " " + input_tokens[-1]
                        label_tokens.append(self.vtoken)
                        cur_position = end
                    # return input_tokens, label_tokens
                    if cur_position < len(log):
                        input_tokens.append(
                            log[cur_position:len(log)].rstrip())
                        label_tokens.append('o')
                # print(input_tokens)
                # print(label_tokens)
                refined_tokens = []
                refined_labels = []
                for (t, l) in zip(input_tokens, label_tokens):
                    if len(t) == 0:
                        continue
                    t = re.split(delimiters, t)
                    t = [x for x in t if len(x) > 0]
                    sub_tokens = []
                    if t[0] != " ":
                        sub_tokens.append(t[0])
                    for i in range(1, len(t)):
                        if t[i] == " ":
                            continue
                        if t[i - 1] == " ":
                            sub_tokens.append(" " + t[i])
                        else:
                            sub_tokens.append(t[i])
                    refined_tokens.extend(sub_tokens)
                    refined_labels.extend([l] * len(sub_tokens))
                # print(refined_tokens)
                # print(refined_labels)
                # print("=" * 30)
                input_id = []
                labels = []
                target_token = []
                # print(i, input_tokens, label_tokens)
                for (input_token, label_token) in zip(refined_tokens, refined_labels):
                    token_ids = self.tokenizer.encode(
                        input_token, add_special_tokens=False)
                    input_id.extend(token_ids)
                    if label_token != self.vtoken:
                        target_token.extend(token_ids)
                        keywords.extend(token_ids)
                    else:
                        target_token.extend(
                            [self.label_token_to_id[label_token]] * len(token_ids))
                        label_words.extend(token_ids)
                        # print(input_token)
                    labels.extend([self.label_to_id[label_token]]
                                  * len(token_ids))
                input_id = [self.tokenizer.cls_token_id] + \
                    input_id + [self.tokenizer.sep_token_id]
                target_token = [self.tokenizer.bos_token_id] + \
                    target_token + [self.tokenizer.eos_token_id]
                labels = [-100] + labels + [-100]
                attention_mask = [1] * len(input_id)
                input_ids.append(input_id)
                target_tokens.append(target_token)
                tag_labels.append(labels)
                attention_masks.append(attention_mask)
            # print(len(input_ids), len(target_tokens),
            #       len(tag_labels), len(attention_masks))
            return {
                "input_ids": input_ids,
                "labels": target_tokens,
                "ori_labels": tag_labels,
                "attention_mask": attention_masks
            }

        self.processed_raw_datasets = {}
        self.processed_raw_datasets['train'] = self.raw_datasets['train'].map(
            tokenize_and_align_labels,
            batched=True,
            remove_columns=self.raw_datasets["train"].column_names,
            desc="Running tokenizer on train dataset"
        )

        # pdb.set_trace()

        self.keywords = list(set(keywords))
        self.label_words = list(set(label_words))
        self.label_words = [x for x in label_words if x not in self.keywords]

        if 'validation' in self.raw_datasets:
            self.processed_raw_datasets['validation'] = self.raw_datasets['validation'].map(
                tokenize_and_align_labels,
                batched=True,
                remove_columns=self.raw_datasets["validation"].column_names,
                desc="Running tokenizer on test dataset",
                num_proc=4
            )

    def build_dataloaders(self, per_device_train_batch_size, per_device_eval_batch_size):
        data_collator = CustomDataCollator(
            tokenizer=self.tokenizer, pad_to_multiple_of=None)
        self.train_loader = DataLoader(
            self.processed_raw_datasets['train'],
            shuffle=True,
            collate_fn=data_collator,
            batch_size=per_device_train_batch_size
        )
        if 'validation' in self.processed_raw_datasets:
            self.val_loader = DataLoader(
                self.processed_raw_datasets['validation'],
                collate_fn=data_collator,
                batch_size=per_device_eval_batch_size
            )
        else:
            self.val_loader = None
