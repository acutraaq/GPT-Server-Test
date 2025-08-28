import os
import sys
import importlib.util
from loguru import logger


def get_module_path(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return f"Module '{module_name}' not found."
    return spec.origin


def check_lmdeploy_lib():
    if os.path.exists(os.path.join(lmdeploy_path, "lib")):
        return True
    return False


# Example
module_name = "lmdeploy"
lmdeploy_path = os.path.dirname(get_module_path(module_name))
if not check_lmdeploy_lib():
    logger.warning("The lmdeploy lib file directory does not exist, the system will automatically download!")
    cmd = "pip install --force-reinstall lmdeploy==0.6.2 --no-deps"
    logger.info(f"Executing command: {cmd}")
    os.system(cmd)
    logger.info("Installation successful, please restart the service!")
    sys.exit()
else:
    pass
