"""
If using hf download:
pip install -U huggingface_hub hf_transfer

If using modelscope download:
pip install modelscope
"""


def model_download(model_id, local_dir="/data", hub_name="hf", repo_type="model"):
    import os

    # Configure hf mirror
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    if hub_name == "hf":
        cmd = f"huggingface-cli download --repo-type {repo_type} --resume-download {model_id} --local-dir {local_dir}/{model_id} --local-dir-use-symlinks False --token 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"
        # Start download
        os.system(cmd)
        print("Download completed!")
    elif hub_name == "modelscope":
        from modelscope.hub.snapshot_download import snapshot_download

        snapshot_download(model_id=model_id, cache_dir=local_dir)  # revision="v1.0.2"
        print("Download completed!")
    else:
        print("hub_name only supports hf and modelscope! Please reset")


if __name__ == "__main__":
    import os

    # Set save path
    local_dir = "/home/dev/model"
    # Repository type dataset / model
    repo_type = "model"

    data_model_id_list = [
        "Qwen/Qwen2.5-0.5B-Instruct-AWQ",
    ]

    for model_id in data_model_id_list:
        # Set repository id
        model_download(model_id, local_dir, hub_name="hf", repo_type=repo_type)
    print("All downloads completed!")
