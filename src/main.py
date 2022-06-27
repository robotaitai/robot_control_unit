import argparse
import logging

from hydra import compose, initialize
from omegaconf import OmegaConf

from robot_control import RobotControl

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    logger.addHandler(logging.StreamHandler())
    logger.info("starting state manager node")

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml", default="../../menteebot_light/configs/default.yaml", help="Configuration file")

    args, unknown = parser.parse_known_args()

    # Configuring hydra
    yaml_path_split = args.yaml.split("/")
    config_path = "/".join(yaml_path_split[:-1])
    config_name = yaml_path_split[-1][:-5]
    with initialize(config_path=config_path, job_name="mentor_app"):
        yaml_conf = compose(config_name=config_name, overrides=["hydra.run.dir=/tmp"])
        # Struct to normal :)
        yaml_conf = OmegaConf.to_container(yaml_conf)
        yaml_conf = OmegaConf.create(yaml_conf)

    cfg = yaml_conf.hardware

    RobotControl(cfg).run()
