import ast
import os
import sys

import supervisely as sly
from supervisely.io.fs import mkdir
from dotenv import load_dotenv


if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

def str_to_list(data):
    data = ast.literal_eval(data)
    data = [n.strip() for n in data]
    return data


TASK_ID = os.environ["TASK_ID"]

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()

COCO_MODE = os.environ["modal.state.cocoDataset"]
META = sly.ProjectMeta()

OUTPUT_PROJECT_NAME = os.environ.get("modal.state.projectName", "")

CACHE_DIR = os.environ["DEBUG_CACHE_DIR"]
STORAGE_DIR = os.path.join(sly.app.get_data_dir(), "storage_dir")
mkdir(STORAGE_DIR)#, True)
COCO_BASE_DIR = os.path.join(STORAGE_DIR, "coco_base_dir")
mkdir(COCO_BASE_DIR)
SLY_BASE_DIR = os.path.join(STORAGE_DIR, "supervisely")
mkdir(SLY_BASE_DIR, True)

if COCO_MODE == "original":
    is_original = True
    original_ds = str_to_list(os.environ["modal.state.originalDataset"])
else:
    is_original = False
    custom_ds = os.environ["modal.state.customDataset"]

img_dir = None
ann_dir = None
src_img_dir = None
dst_img_dir = None

images_links = {
    "train2014": "http://images.cocodataset.org/zips/train2014.zip",
    "val2014": "http://images.cocodataset.org/zips/val2014.zip",
    "test2014": "http://images.cocodataset.org/zips/test2014.zip",
    "train2017": "http://images.cocodataset.org/zips/train2017.zip",
    "val2017": "http://images.cocodataset.org/zips/val2017.zip",
    "test2017": "http://images.cocodataset.org/zips/test2017.zip",
}

annotations_links = {
    "trainval2014": "http://images.cocodataset.org/annotations/annotations_trainval2014.zip",
    "trainval2017": "http://images.cocodataset.org/annotations/annotations_trainval2017.zip",
}