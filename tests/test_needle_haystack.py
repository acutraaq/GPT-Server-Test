"""Needle in a haystack evaluation"""

import os
from evalscope import TaskConfig, run_task

task_cfg = TaskConfig(
    model="qwen",
    api_url="http://localhost:8082/v1",
    api_key="123",
    eval_type="service",  # Use API model service
    datasets=["needle_haystack"],
    eval_batch_size=20,
    dataset_args={
        "needle_haystack": {
            "subset_list": ["chinese", "english"][:1],  # Optional, specify using Chinese or English subset
            # Supported configuration parameters
            "extra_params": {
                # Question
                "retrieval_question": "What is the best thing to do in San Francisco?",
                # Inserted text (can be set to multiple)
                "needles": [
                    "\nThe best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny day.\n"
                ],
                # Minimum corpus length
                "context_lengths_min": 1000,
                # Maximum corpus length
                "context_lengths_max": 64 * 1024,  # 64K
                # Number of corpus intervals
                "context_lengths_num_intervals": 20,
                # Minimum position for inserted text (percentage)
                "document_depth_percent_min": 0,
                # Maximum position for inserted text (percentage)
                "document_depth_percent_max": 100,
                # Number of intervals for inserted text position
                "document_depth_percent_intervals": 10,
                # Path to tokenizer (can specify modelscope id)
                "tokenizer_path": "/home/dev/model/Qwen/Qwen2___5-32B-Instruct-AWQ/",
                "show_score": True,  # Whether to display scores on heatmap
            },
        }
    },
    generation_config={
        "max_tokens": 512,  # Maximum number of generated tokens
    },
    judge_worker_num=5,
    judge_model_args={
        "model_id": "qwen",
        "api_url": "http://localhost:8082/v1",
        "api_key": "123",
    },
)
run_task(task_cfg=task_cfg)
