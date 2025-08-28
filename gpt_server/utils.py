import socket
from typing import List, Optional
import os
import sys
import json
from multiprocessing import Process
import subprocess
from loguru import logger
import torch
import psutil
from rich import print
import signal
from pathlib import Path

ENV = os.environ
logger.add("logs/gpt_server.log", rotation="100 MB", level="INFO")
root_dir = Path(__file__).parent
STATIC_DIR = root_dir / "static"


def kill_child_processes(parent_pid, including_parent=False):
    "Kill child processes/zombie processes"
    try:
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                print(f"Terminating child process {child.pid}...")
                os.kill(child.pid, signal.SIGTERM)  # Graceful termination
                child.wait(5)  # Wait for child process for up to 5 seconds
            except psutil.NoSuchProcess:
                pass
            except psutil.TimeoutExpired():
                print(f"Terminating child process {child.pid} timeout! Force termination...")
                os.kill(child.pid, signal.SIGKILL)  # Force termination
        if including_parent:
            print(f"Terminating parent process {parent_pid}...")
            os.kill(parent_pid, signal.SIGTERM)
    except psutil.NoSuchProcess:
        print(f"Parent process {parent_pid} does not exist!")


# Record parent process PID
parent_pid = os.getpid()


def signal_handler(signum, frame):
    print("\nCtrl-C detected! Cleaning up...")
    # kill_child_processes(parent_pid, including_parent=False)
    stop_server()
    exit(0)  # Normal program exit


signal.signal(signal.SIGINT, signal_handler)


def run_cmd(cmd: str, *args, **kwargs):
    logger.info(f"Executing command as follows:\n{cmd}\n")
    # subprocess.run(cmd, shell=True)
    process = subprocess.Popen(cmd, shell=True)
    # Wait for command execution to complete
    process.wait()
    return process.pid


def start_controller(controller_host, controller_port, dispatch_method):
    """Start fastchat controller"""
    cmd = f"python -m gpt_server.serving.controller --host {controller_host} --port {controller_port} --dispatch-method {dispatch_method} "
    cmd += "> /dev/null 2>&1"  # Completely silent (Linux/macOS)
    controller_process = Process(target=run_cmd, args=(cmd,))
    controller_process.start()


def start_openai_server(host, port, controller_address, api_keys=None):
    """Start OpenAI API service"""
    os.environ["FASTCHAT_WORKER_API_EMBEDDING_BATCH_SIZE"] = "100000"

    cmd = f"python -m gpt_server.serving.openai_api_server --host {host} --port {port} --controller-address {controller_address}"
    if api_keys:
        cmd += f" --api-keys {api_keys}"
    openai_server_process = Process(target=run_cmd, args=(cmd,))
    openai_server_process.start()


def start_api_server(config: dict):
    server_enable = config["serve_args"].get("enable", True)
    host = config["serve_args"]["host"]
    port = config["serve_args"]["port"]
    controller_address = config["serve_args"]["controller_address"]
    api_keys = config["serve_args"].get("api_keys", None)

    controller_enable = config["controller_args"].get("enable", True)
    controller_host = config["controller_args"]["host"]
    controller_port = config["controller_args"]["port"]
    dispatch_method = config["controller_args"].get("dispatch_method", "shortest_queue")
    # -----------------------------------------------------------------------
    # Check if ports are in use
    used_ports = []
    if is_port_in_use(controller_port):
        used_ports.append(controller_port)
    if is_port_in_use(port):
        used_ports.append(port)
    if len(used_ports) > 0:
        logger.warning(
            f"Ports: {used_ports} are already in use! For normal system operation, please ensure they are occupied by the already started gpt_server service."
        )
    if controller_port not in used_ports and controller_enable:
        # Start controller
        start_controller(controller_host, controller_port, dispatch_method)
    if port not in used_ports and server_enable:
        # Start OpenAI API service
        start_openai_server(host, port, controller_address, api_keys)
    # -----------------------------------------------------------------------


def get_model_types():
    model_types = []
    model_worker_path = root_dir / "model_worker"
    # Traverse directory and subdirectories
    for root, dirs, files in os.walk(model_worker_path):
        for file in files:
            # Check if file ends with .py
            if file.endswith(".py") and file != "__init__.py":
                # Output complete file path
                model_type = file[:-3]
                model_types.append(model_type)
    return model_types


model_types = get_model_types() + ["embedding"]
embedding_backend_type = ["vllm", "infinity", "sentence_transformers"]


def start_model_worker(config: dict):
    process = []
    try:
        host = config["model_worker_args"]["host"]
        controller_address = config["model_worker_args"]["controller_address"]
        log_level = config["model_worker_args"].get("log_level", "WARNING")
        limit_worker_concurrency = config["model_worker_args"].get(
            "limit_worker_concurrency", 1024
        )
    except KeyError as e:
        error_msg = f"Please refer to https://github.com/shell-nlp/gpt_server/blob/main/gpt_server/script/config.yaml to set the correct model_worker_args"
        logger.error(error_msg)
        raise KeyError(error_msg)
    exist_model_names = []  # Record existing model_name
    for model_config_ in config["models"]:
        for model_name, model_config in model_config_.items():
            # Enabled models
            if model_config["enable"]:
                # pprint(model_config)
                print()
                engine_config = model_config.get("model_config", None)
                # TODO -------------- Forward compatibility --------------
                if engine_config:
                    # New version
                    # Model path
                    model_name_or_path = engine_config["model_name_or_path"]
                    enable_prefix_caching = engine_config.get(
                        "enable_prefix_caching", "False"
                    )
                    dtype = engine_config.get("dtype", "auto")
                    lora = engine_config.get("lora", None)
                    max_model_len = engine_config.get("max_model_len", None)
                    gpu_memory_utilization = engine_config.get(
                        "gpu_memory_utilization", 0.8
                    )
                    kv_cache_quant_policy = engine_config.get(
                        "kv_cache_quant_policy", 0
                    )
                    vad_model = engine_config.get("vad_model", "")
                    punc_model = engine_config.get("punc_model", "")
                    task_type = engine_config.get("task_type", "auto")

                else:
                    logger.error(
                        f"""Model: {model_name}'s model_name_or_path,model_name_or_path parameter configuration must be modified under model_config! For example:
- minicpmv:
    alias: null
    enable: false
    model_type: minicpmv
    model_config:
      model_name_or_path: /home/dev/model/OpenBMB/MiniCPM-V-2_6/
      enable_prefix_caching: false
      dtype: auto
    work_mode: lmdeploy-turbomind
    device: gpu
    workers:
    - gpus:
      - 3
  """
                    )
                    sys.exit()

                # -------------- Forward compatibility --------------
                # Model type
                model_type = model_config["model_type"]
                # Validate model type
                if model_type not in model_types:
                    logger.error(
                        f"Unsupported model_type: {model_type}, only supports one of {model_types} models!"
                    )
                    sys.exit()

                model_names = model_name
                if model_config["alias"]:
                    model_names = model_name + "," + model_config["alias"]
                    if lora:  # If using lora, add lora name to model_names
                        lora_names = list(lora.keys())
                        model_names += "," + ",".join(lora_names)
                intersection = list(
                    set(exist_model_names) & set(model_names.split(","))
                )  # Get intersection
                if intersection:  # If there is intersection return True
                    logger.error(
                        f"Duplicate model names or aliases exist: {intersection}, please check config.yaml file"
                    )
                    sys.exit()
                exist_model_names.extend(model_names.split(","))
                # Get worker count and resources for each worker
                workers = model_config["workers"]

                # process = []
                for worker in workers:
                    gpus = worker["gpus"]
                    # Convert gpus int ---> str
                    gpus = [str(i) for i in gpus]
                    gpus_str = ",".join(gpus)
                    num_gpus = len(gpus)
                    run_mode = "python "
                    CUDA_VISIBLE_DEVICES = ""
                    if (
                        torch.cuda.is_available()
                        and model_config["device"].lower() == "gpu"
                    ):
                        CUDA_VISIBLE_DEVICES = f"CUDA_VISIBLE_DEVICES={gpus_str} "
                    elif model_config["device"].lower() == "cpu":
                        CUDA_VISIBLE_DEVICES = ""
                    else:
                        raise Exception("Currently only supports CPU/GPU devices!")
                    backend = model_config["work_mode"]
                    if model_type == "embedding":
                        assert backend in embedding_backend_type
                        model_type = f"embedding_{backend}"

                    py_path = f"-m gpt_server.model_worker.{model_type}"
                    cmd = (
                        CUDA_VISIBLE_DEVICES
                        + run_mode
                        + py_path
                        + f" --num_gpus {num_gpus}"
                        + f" --model_name_or_path {model_name_or_path}"
                        + f" --model_names {model_names}"
                        + f" --backend {backend}"
                        + f" --host {host}"
                        + f" --controller_address {controller_address}"
                        + f" --dtype {dtype}"
                        + f" --enable_prefix_caching {enable_prefix_caching}"  # Whether to enable prefix cache
                        + f" --gpu_memory_utilization {gpu_memory_utilization}"  # GPU memory utilization ratio
                        + f" --kv_cache_quant_policy {kv_cache_quant_policy}"  # KV cache quantization policy
                        + f" --log_level {log_level}"  # Log level
                        + f" --task_type {task_type}"  # Task type
                        + f" --limit_worker_concurrency {limit_worker_concurrency}"  # Limit worker concurrency
                    )
                    # 处理为 None的情况
                    if lora:
                        cmd += f" --lora '{json.dumps(lora)}'"
                    if max_model_len:
                        cmd += f" --max_model_len '{max_model_len}'"
                    if vad_model:
                        cmd += f" --vad_model '{vad_model}'"
                    if punc_model:
                        cmd += f" --vad_model '{punc_model}'"
                    p = Process(target=run_cmd, args=(cmd,))
                    # p.start()
                    process.append(p)
    for p in process:
        p.start()
    for p in process:
        p.join()


def start_server(
    host: str = "0.0.0.0",
    port: int = 8081,
    controller_address: str = "http://localhost:21001",
    api_keys: Optional[List[str]] = None,
    controller_host: str = "localhost",
    controller_port: int = 21001,
    dispatch_method: str = "shortest_queue",
):
    """Start service"""
    # Check if ports are in use
    used_ports = []
    if is_port_in_use(controller_port):
        used_ports.append(controller_port)
    if is_port_in_use(port):
        used_ports.append(port)
    if len(used_ports) > 0:
        logger.warning(
            f"Ports: {used_ports} are already in use! For normal system operation, please ensure they are occupied by the already started gpt_server service."
        )
    if controller_port not in used_ports:
        # Start controller
        start_controller(controller_host, controller_port, dispatch_method)
    if port not in used_ports:
        # Start OpenAI API service
        start_openai_server(host, port, controller_address, api_keys)


def stop_controller():
    cmd = "ps -ef | grep fastchat.serve | awk '{print $2}' |xargs -I{} kill -9 {}"
    run_cmd(cmd=cmd)


def stop_openai_server():
    cmd = "ps -ef | grep gpt_server |grep serving | awk '{print $2}' |xargs -I{} kill -9 {}"
    run_cmd(cmd=cmd)


def stop_all_model_worker():
    cmd = "ps -ef | grep gpt_server |grep model_worker | awk '{print $2}' |xargs -I{} kill -9 {}"
    run_cmd(cmd=cmd)


def stop_server():
    """Stop service"""
    stop_all_model_worker()
    stop_controller()
    stop_openai_server()

    logger.info("Service stopped successfully!")


def delete_log():
    logs_path = os.environ.get("LOGDIR")
    logger.debug(f"logs_path: {logs_path}")
    # Create directory if it doesn't exist
    if not os.path.exists(logs_path):
        os.makedirs(logs_path, exist_ok=True)

    logs_path_datanames = os.listdir(logs_path)  # Find all files in this directory
    datanames = logs_path_datanames
    for dataname in datanames:
        if dataname.endswith(".log"):
            os.remove(os.path.join(logs_path, f"{dataname}"))


def get_free_tcp_port():
    """Get available port"""
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return False
        except:
            return True


def get_physical_ip():
    import socket

    local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    return local_ip


try:
    local_ip = get_physical_ip()
except Exception as e:
    local_ip = ENV.get("local_ip", "127.0.0.1")

model_type_mapping = {
    "yi": "yi",
    "qwen": "qwen",
    "glm4": "chatglm",
    "chatglm3": "chatglm",
    "internvl2-internlm2": "internvl2",
    "internlm2": "internlm",
    "internlm": "internlm",
    "baichuan2": "baichuan",
    "llama3": "llama",
    "mistral": "mistral",
    "deepseek": "deepseek",
}


if __name__ == "__main__":
    # /home/dev/model/KirillR/QwQ-32B-Preview-AWQ
    # get_model_types()
    from lmdeploy.serve.async_engine import get_names_from_model
    from lmdeploy.archs import get_model_arch
    from lmdeploy.cli.utils import get_chat_template

    print(local_ip)
    ckpt = "/home/dev/model/Qwen/Qwen3-32B/"  # internlm2
    chat_template = get_chat_template(ckpt)
    model_type = get_names_from_model(ckpt)
    arch = get_model_arch(ckpt)

    print(chat_template)
    # print(arch)
    print(model_type)
    print(model_type[1] == "base")
