import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
import os

class FineTuneService:

    def run(self):
        model_name = "Qwen/Qwen3-4B-Instruct-2507"
        # model_name = "Qwen/Qwen2.5-3B-Instruct"
        # model_name = "Qwen/Qwen2.5-0.5B-Instruct"

        # Select device: Apple Silicon → "mps", otherwise CPU fallback
        device = 0 if torch.backends.mps.is_available() else -1

        ask_llm = pipeline(model=model_name, device=device)

        # print(ask_llm("who is Jolaku Marf?")[0]["generated_text"])
        print(ask_llm("who is Mariya Sha?")[0]["generated_text"])

        raw_data = load_dataset("json", data_files="data/mariya.json")
        print(raw_data)

        breakpoint()

        print(raw_data["train"][0])

        breakpoint()

        tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map = device,
            torch_dtype = torch.float16
        )

        lora_config = LoraConfig(
            task_type = TaskType.CAUSAL_LM,
            target_modules = ["q_proj", "k_proj", "v_proj"]
        )

        model = get_peft_model(model, lora_config)

        breakpoint()

        os.environ["WANDB_DISABLED"] = "true"

        training_args = TrainingArguments(
            num_train_epochs=10,
            learning_rate=0.001,
            logging_steps=25,
            report_to="none"
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=data["train"]
        )

        trainer.train()

    def preprocess(sample):
        sample = sample["prompt"] + "\n" + sample["completion"]

        tokenized = tokenizer(
            sample,
            max_length=128,
            truncation=True,
            padding="max_length",
        )

        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized