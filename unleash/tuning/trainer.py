import logging
import math

import torch

from tqdm import tqdm
from transformers import get_scheduler
from typing import Any, Optional


logger = logging.getLogger("unleash")


class TrainingArguments:
    def __init__(
        self,
        output_dir: str = "output",
        overwrite_output_dir: bool = False,
        do_train: bool = True,
        do_eval: bool = True,
        do_predict: bool = True,
        evaluation_strategy: str = "steps",
        per_device_train_batch_size: int = 8,
        per_device_eval_batch_size: int = 8,
        learning_rate: float = 5e-5,
        weight_decay: float = 0.0,
        num_train_epochs: int = 3,
        max_train_steps: int = -1,
        gradient_accumulation_steps: int = 1,
        lr_scheduler_type: str = "polynomial",
        num_warmup_steps: int = 0,
        seed: int = 42,
    ):
        self.output_dir = output_dir
        self.overwrite_output_dir = overwrite_output_dir
        self.do_train = do_train
        self.do_eval = do_eval
        self.do_predict = do_predict
        self.evaluation_strategy = evaluation_strategy
        self.per_device_train_batch_size = per_device_train_batch_size
        self.per_device_eval_batch_size = per_device_eval_batch_size
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.num_train_epochs = num_train_epochs
        self.max_train_steps = max_train_steps
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.lr_scheduler_type = lr_scheduler_type
        self.num_warmup_steps = num_warmup_steps
        self.seed = seed


class Trainer:
    def __init__(
        self,
        model: Any = None,
        args: TrainingArguments = None,
        train_loader: Optional[Any] = None,
        eval_loader: Optional[Any] = None,
        # tokenizer: Any = None,
        compute_metrics: Any = None,
        no_train_samples: int = 0,
        device: str = "cuda",
        callback: Any = None
    ):
        self.model = model
        self.args = args
        self.train_loader = train_loader
        self.eval_loader = eval_loader
        self.compute_metrics = compute_metrics
        self.no_train_samples = no_train_samples
        self.device = device
        self.initialize()

    def initialize(self):
        if self.args.max_train_steps > 0:
            if self.args.per_device_train_batch_size > self.no_train_samples:
                self.args.gradient_accumulation_steps = self.args.per_device_train_batch_size // self.no_train_samples
                self.args.per_device_train_batch_size = self.no_train_samples
                self.args.num_train_epochs = self.args.max_train_steps * \
                    self.args.gradient_accumulation_steps
            else:
                self.args.num_train_epochs = math.ceil(
                    self.args.max_train_steps /
                    (self.no_train_samples // (self.args.per_device_train_batch_size *
                     self.args.gradient_accumulation_steps))
                )
            self.args.num_warmup_steps = self.args.max_train_steps // 10
        else:
            self.args.max_train_steps = self.args.num_train_epochs * \
                (self.no_train_samples // (self.args.per_device_train_batch_size *
                 self.args.gradient_accumulation_steps))
            self.args.num_warmup_steps = self.args.max_train_steps // 10
        self.args.evaluation_strategy = "steps"
        self.args.eval_steps = 500
        self.args.logging_steps = 100
        self.args.save_steps = 500
        self.args.logging_dir = "logs"
        self.args.save_total_limit = 5
        self.args.eval_accumulation_steps = 1
        # Optimizer
        # Split weights in two groups, one with weight decay and the other not.
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in self.model.named_parameters() if not any(nd in n for nd in no_decay)],
                "weight_decay": self.args.weight_decay,
            },
            {
                "params": [p for n, p in self.model.named_parameters() if any(nd in n for nd in no_decay)],
                "weight_decay": 0.0,
            },
        ]

        self.optimizer = torch.optim.AdamW(
            optimizer_grouped_parameters,
            lr=self.args.learning_rate,
            betas=(0.9, 0.999),
            eps=1e-8,
        )

        self.lr_scheduler = get_scheduler(
            name=self.args.lr_scheduler_type,
            optimizer=self.optimizer,
            num_warmup_steps=self.args.num_warmup_steps,
            num_training_steps=self.args.max_train_steps,
        )

        logger.info("Initialized Trainer")

    def train(self):
        total_batch_size = self.args.per_device_train_batch_size * \
            self.args.gradient_accumulation_steps

        logger.info("***** Running training *****")
        logger.info(f"  Num examples = {self.no_train_samples}")
        logger.info(f"  Num Epochs = {self.args.num_train_epochs}")
        logger.info(
            f"  Instantaneous batch size per device = {self.args.per_device_train_batch_size}")
        logger.info(
            f"  Total train batch size (w. parallel, distributed & accumulation) = {total_batch_size}")
        logger.info(
            f"  Gradient Accumulation steps = {self.args.gradient_accumulation_steps}")
        logger.info(
            f"  Total optimization steps = {self.args.max_train_steps}")
        # Only show the progress bar once on each machine.
        progress_bar = tqdm(range(self.args.max_train_steps))
        completed_steps = 0

        self.model.to(self.device)
        # self.model, self.optimizer, self.train_loader, self.eval_loader = self.accelerator.prepare(
        #     self.model, self.optimizer, self.train_loader, self.eval_loader
        # )

        self.model.train()

        for epoch in range(self.args.num_train_epochs):
            # logger.info(f"Epoch {epoch}")
            total_loss = []
            for step, batch in enumerate(self.train_loader):
                batch.pop('ori_labels', 'not found ner_labels')
                batch = {k: v.to(self.device) for k, v in batch.items()}
                loss = self.model(batch)
                # loss = outputs.loss
                total_loss.append(float(loss))
                loss = loss / self.args.gradient_accumulation_steps
                # self.accelerator.backward(loss)
                loss.backward()
                if step % self.args.gradient_accumulation_steps == 0 or step == len(self.train_loader) - 1:
                    self.optimizer.step()
                    self.lr_scheduler.step()
                    self.optimizer.zero_grad()
                    progress_bar.update(1)
                    progress_bar.set_description(f"Loss: {float(loss)}")
                    completed_steps += 1

                if completed_steps >= self.args.max_train_steps:
                    break

            if completed_steps >= self.args.max_train_steps:
                break

        return self.model

    def save_pretrained(self, output_dir):
        self.model.save_pretrained(output_dir)
        logger.info("Model saved")
