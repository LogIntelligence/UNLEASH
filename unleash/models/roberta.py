from transformers import (
    RobertaForMaskedLM,
    AutoTokenizer,
)
from collections import Counter
from unleash.models.base import ModelBase
import re
import torch
from torch import nn
from unleash.postprocess import correct_single_template

delimiters = "([ |\(|\)|\[|\]|\{|\})])"

class Similarity(nn.Module):
    """
    Dot product or cosine similarity
    """

    def __init__(self, temp):
        super().__init__()
        self.temp = temp
        self.cos = nn.CosineSimilarity(dim=-1)

    def forward(self, x, y):
        return self.cos(x, y) / self.temp


class RobertaForLogParsing(ModelBase):
    def __init__(self, 
                 model_path, 
                 num_label_tokens: int = 1,
                 vtoken="virtual-param",
                 ct_loss_weight=0.1,
                 mode='train'
                 ):
        super().__init__(model_path, num_label_tokens)
        self.plm = RobertaForMaskedLM.from_pretrained(self.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.tokenizer.model_max_length = self.plm.config.max_position_embeddings - 2
        self.vtoken = vtoken
        if mode == 'train':
            self.add_label_token(self.num_label_tokens)
        self.sim = Similarity(0.05)
        self.ct_loss = nn.CrossEntropyLoss()
        self.ct_loss_weight = ct_loss_weight

    def forward(self, batch):
        vtoken_id = self.tokenizer.convert_tokens_to_ids(self.vtoken)
        outputs = self.plm(**batch, output_hidden_states=True)
        loss = outputs.loss
        y = batch['labels'] == vtoken_id
        vtoken_reprs = outputs.hidden_states[-1][y]
        if vtoken_reprs.size(0) % 2 == 1:
            vtoken_reprs = vtoken_reprs[:-1]
        if vtoken_reprs.size(0) == 0:
            return loss
        z1_embed = vtoken_reprs[:vtoken_reprs.size(0) // 2]
        z2_embed = vtoken_reprs[vtoken_reprs.size(0) // 2:]
        sim = self.sim(z1_embed.unsqueeze(1), z2_embed.unsqueeze(0))
        labels = torch.arange(sim.size(0)).long().to(sim.device)
        # print(sim.dtype, labels.dtype)
        # print(sim.shape, labels.shape)
        # print(batch['labels'].dtype)
        loss_ct = self.ct_loss(sim, labels)
        # print(f"Loss: {loss}, CT Loss: {loss_ct}")
        loss += loss_ct * self.ct_loss_weight
        return loss

    def add_label_token(self, num_tokens: int):
        crr_tokens, _ = self.plm.roberta.embeddings.word_embeddings.weight.shape
        self.plm.resize_token_embeddings(crr_tokens + num_tokens)

    def named_parameters(self):
        return self.plm.named_parameters()
    
    def eval(self):
        self.plm.eval()
    
    def parse(self, log_line, device="cpu", vtoken="virtual-param"):
        def tokenize(log_line, max_length=256):
            log_tokens = re.split(delimiters, log_line)
            log_tokens = [token for token in log_tokens if len(token) > 0]
            refined_tokens = []
            if log_tokens[0] != " ":
                refined_tokens.append(log_tokens[0])
            for i in range(1, len(log_tokens)):
                if log_tokens[i] == " ":
                    continue
                if log_tokens[i - 1] == " ":
                    refined_tokens.append(" " + log_tokens[i])
                else:
                    refined_tokens.append(log_tokens[i])
            token_ids = []
            for token in refined_tokens:
                ids = self.tokenizer.encode(token, add_special_tokens=False)
                token_ids.extend(ids)
            token_ids = token_ids[:max_length - 2]
            token_ids = [self.tokenizer.bos_token_id] + token_ids + [self.tokenizer.eos_token_id]
            return {
                'input_ids': torch.tensor([token_ids], dtype=torch.int64),
                'attention_mask': torch.tensor([[1] * len(token_ids)], dtype=torch.int64)
            }
        tokenized_input = tokenize(log_line)
        tokenized_input = {k: v.to(device) for k, v in tokenized_input.items()}
        with torch.no_grad():
            outputs = self.plm(**tokenized_input, output_hidden_states=True)
        logits = outputs.logits.argmax(dim=-1)
        # logits = accelerator.pad_across_processes(logits, dim=1, pad_index=-100)
        logits = logits.detach().cpu().clone().tolist()
        template = map_template(self.tokenizer, tokenized_input['input_ids'][0], logits[0], vtoken=vtoken)
        return correct_single_template(template)
    

def map_template(tokenizer, c, t, vtoken="virtual-param"):
    vtoken = tokenizer.convert_tokens_to_ids(vtoken)
    tokens = tokenizer.convert_ids_to_tokens(c)
    res = [" "]
    for i in range(1, len(c)):
        if c[i] == tokenizer.sep_token_id:
            break
        if t[i] < vtoken:
            res.append(tokens[i])
        else:
            if "Ġ" in tokens[i]:
                # if "<*>" not in res[-1]:
                res.append("Ġ<*>")
            elif "<*>" not in res[-1]:
                res.append("<*>")
    r = "".join(res)
    r = r.replace("Ġ", " ")
    return r.strip()
