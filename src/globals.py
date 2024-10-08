import ast
import os

import supervisely as sly
from supervisely.io.fs import mkdir
from dotenv import load_dotenv
from distutils.util import strtobool


if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()


def strtolist(data):
    data = ast.literal_eval(data)
    data = [n.strip() for n in data]
    return data


TASK_ID = os.environ["TASK_ID"]

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()

META = sly.ProjectMeta()
OUTPUT_PROJECT_NAME = os.environ.get("modal.state.projectName", "")

STORAGE_DIR = os.path.join(sly.app.get_data_dir(), "storage_dir")
mkdir(STORAGE_DIR, True)
COCO_BASE_DIR = os.path.join(STORAGE_DIR, "coco_base_dir")
mkdir(COCO_BASE_DIR)
SLY_BASE_DIR = os.path.join(STORAGE_DIR, "supervisely")
mkdir(SLY_BASE_DIR)

img_dir = None
ann_dir = None
src_img_dir = None
dst_img_dir = None

ds_mode = os.environ["modal.state.cocoDataset"]

original_ds = strtolist(os.environ["modal.state.originalDataset"])
custom_ds = os.environ["modal.state.customDataset"]
if custom_ds is "":
    raise ValueError("Please, input filepath to the custom dataset")

label_visibility = bool(strtobool(os.getenv("modal.state.labelVisibility")))
if label_visibility:
    label_visibility = [0, 1]
else:
    label_visibility = [0]

images_links = {
    "train2017": "http://images.cocodataset.org/zips/train2017.zip",
    "val2017": "http://images.cocodataset.org/zips/val2017.zip",
    "test2017": "http://images.cocodataset.org/zips/test2017.zip",
}

annotations_links = {
    "trainval2017": "http://images.cocodataset.org/annotations/annotations_trainval2017.zip",
}
