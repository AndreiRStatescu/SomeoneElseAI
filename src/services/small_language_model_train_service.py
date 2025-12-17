import tiktoken
import numpy as np
import logging
from tqdm.auto import tqdm
from datasets import load_dataset
from itertools import islice

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(processName)s - %(levelname)s - %(message)s",
)


class SmallLanguageModelTrainService:

    def __init__(self):
        self.enc = tiktoken.get_encoding("gpt2")
        self.process_count = 0

    def prepare_dataset(self):
        print("Starting dataset preparation...")
        ds = load_dataset("roneneldan/TinyStories")
        print(f"Dataset loaded: {ds}")

        print("Starting tokenization...")
        tokenized = ds.map(
            self.process,
            remove_columns=["text"],
            num_proc=8
        )
        print(f"Process function was called {self.process_count} times")
        print("Tokenization complete!")
        # concatenate all the ids in each dataset into one large file we can use for training
        for split, dset in reversed(tokenized.items()):
            arr_len = np.sum(dset["len"], dtype=np.uint64)
            filename = f"data/temp/{split}.bin"
            dtype = np.uint16  # (can do since enc.max_token_value == 50256 is < 2**16)
            arr = np.memmap(filename, dtype=dtype, mode="w+", shape=(arr_len,))
            total_batches = 1024

            idx = 0
            for batch_idx in tqdm(range(total_batches), desc=f"writing {filename}"):
                # Batch together samples for faster write
                batch = dset.shard(
                    num_shards=total_batches, index=batch_idx, contiguous=True
                ).with_format("numpy")
                arr_batch = np.concatenate(batch["ids"])
                # Write into mmap
                arr[idx : idx + len(arr_batch)] = arr_batch
                idx += len(arr_batch)
            arr.flush()

    def prepare_dataset_optimised(self):
        ds = load_dataset("roneneldan/TinyStories")

        tokenized = ds.map(
            self.process,
            remove_columns=["text"],
            desc="tokenizing the splits",
            num_proc=None,
        )
        for split, dset in reversed(tokenized.items()):
            arr_len = np.sum(dset["len"], dtype=np.uint64)
            filename = f"data/temp/{split}.bin"
            dtype = np.uint16
            arr = np.memmap(filename, dtype=dtype, mode="w+", shape=(arr_len,))

            batch_size = max(1, len(dset) // 100)

            idx = 0
            dset_iter = iter(dset.with_format("numpy"))

            with tqdm(
                total=len(dset), desc=f"writing {filename}", unit="samples"
            ) as pbar:
                while True:
                    batch_samples = list(islice(dset_iter, batch_size))
                    if not batch_samples:
                        break

                    batch_ids = [sample["ids"] for sample in batch_samples]
                    arr_batch = np.concatenate(batch_ids)

                    arr[idx : idx + len(arr_batch)] = arr_batch
                    idx += len(arr_batch)
                    pbar.update(len(batch_samples))

            arr.flush()

    def process(self, example):
        self.process_count += 1
        ids = self.enc.encode_ordinary(example["text"])
        out = {"ids": ids, "len": len(ids)}
        return out
