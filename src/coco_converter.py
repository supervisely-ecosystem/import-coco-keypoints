import os
import shutil
import uuid

import numpy as np
import pycocotools.mask as mask_util
import supervisely as sly
from PIL import Image
from supervisely.io.fs import file_exists, mkdir
from supervisely.geometry.graph import Node, GraphNodes, KeypointsTemplate
from supervisely.geometry.rectangle import Rectangle

import globals as g


def create_orig_geometry_config():
    template = KeypointsTemplate()
    # add keypoints
    template.add_point(label="nose", row=635, col=427)
    template.add_point(label="left_eye", row=597, col=404)
    template.add_point(label="right_eye", row=685, col=401)
    template.add_point(label="left_ear", row=575, col=431)
    template.add_point(label="right_ear", row=723, col=425)
    template.add_point(label="left_shoulder", row=502, col=614)
    template.add_point(label="right_shoulder", row=794, col=621)
    template.add_point(label="left_elbow", row=456, col=867)
    template.add_point(label="right_elbow", row=837, col=874)
    template.add_point(label="left_wrist", row=446, col=1066)
    template.add_point(label="right_wrist", row=845, col=1073)
    template.add_point(label="left_hip", row=557, col=1035)
    template.add_point(label="right_hip", row=743, col=1043)
    template.add_point(label="left_knee", row=541, col=1406)
    template.add_point(label="right_knee", row=751, col=1421)
    template.add_point(label="left_ankle", row=501, col=1760)
    template.add_point(label="right_ankle", row=774, col=1765)
    # add connections
    template.add_edge(src="left_ankle", dst="left_knee")
    template.add_edge(src="left_knee", dst="left_hip")
    template.add_edge(src="right_ankle", dst="right_knee")
    template.add_edge(src="right_knee", dst="right_hip")
    template.add_edge(src="left_hip", dst="right_hip")
    template.add_edge(src="left_shoulder", dst="left_hip")
    template.add_edge(src="right_shoulder", dst="right_hip")
    template.add_edge(src="left_shoulder", dst="right_shoulder")
    template.add_edge(src="left_shoulder", dst="left_elbow")
    template.add_edge(src="right_shoulder", dst="right_elbow")
    template.add_edge(src="left_elbow", dst="left_wrist")
    template.add_edge(src="right_elbow", dst="right_wrist")
    template.add_edge(src="left_eye", dst="right_eye")
    template.add_edge(src="nose", dst="left_eye")
    template.add_edge(src="nose", dst="right_eye")
    template.add_edge(src="left_eye", dst="left_ear")
    template.add_edge(src="right_eye", dst="right_ear")
    template.add_edge(src="left_ear", dst="left_shoulder")
    template.add_edge(src="right_ear", dst="right_shoulder")
    return template


def create_custom_geometry_config(num_keypoints=None, cat_labels=None, cat_edges=None):
    template = KeypointsTemplate()

    if cat_labels is None:
        if num_keypoints is None:
            raise ValueError(
                "Number of keypoints can not be specified, please check your annotation (categories: num_keypoints)"
            )
        for p in list(range(num_keypoints)):
            template.add_point(label=str(p), row=0, col=0)
    else:
        for label in cat_labels:
            template.add_point(label=label, row=0, col=0)

    if cat_edges is not None and cat_labels is not None:
        for edge in cat_edges:
            template.add_edge(src=cat_labels[edge[0] - 1], dst=cat_labels[edge[1] - 1])
    else:
        sly.logger.info("Edges can not be mapped without skeleton, please check your annotation")
    return template


def create_sly_meta_from_coco_categories(coco_categories, coco_images=None, coco_anns=None):
    colors = []
    for category in coco_categories:
        if category["name"] in [obj_class.name for obj_class in g.META.obj_classes]:
            continue
        if f"{category['name']}_bbox" in [obj_class.name for obj_class in g.META.obj_classes]:
            continue

        geometry_config = None
        if g.ds_mode == "original":
            geometry_config = create_orig_geometry_config()
        elif g.ds_mode == "custom":
            cat_num_kp = None
            # look for labels
            cat_labels = category.get("keypoints", None)
            # look for edges
            cat_edges = category.get("skeleton", None)

            # find object with most keypoints of this category (num_keypoints)
            if cat_labels is None:
                cat_num_kp = []
                for img_id, img_info in coco_images.items():
                    ann_p = coco_anns[img_id]
                    for ann in ann_p:
                        if ann["category_id"] == category["id"]:
                            cat_num_kp.append(ann["num_keypoints"])
                cat_num_kp = max(cat_num_kp)

            geometry_config = create_custom_geometry_config(
                num_keypoints=cat_num_kp, cat_labels=cat_labels, cat_edges=cat_edges
            )

        new_color = sly.color.generate_rgb(colors)
        colors.append(new_color)
        obj_class = sly.ObjClass(
            name=category["name"],
            geometry_type=sly.GraphNodes,
            color=new_color,
            geometry_config=geometry_config,
        )
        bbox_obj_class = sly.ObjClass(
            name=f"{category['name']}_bbox", geometry_type=sly.Rectangle, color=new_color
        )

        g.META = g.META.add_obj_classes(new_obj_classes=[obj_class, bbox_obj_class])
    return g.META


def get_sly_meta_from_coco(coco_categories, coco_images=None, coco_anns=None):
    path_to_meta = os.path.join(g.SLY_BASE_DIR, "meta.json")
    g.META = dump_meta(coco_categories, path_to_meta, coco_images, coco_anns)
    return g.META


def dump_meta(coco_categories, path_to_meta, coco_images=None, coco_anns=None):
    g.META = create_sly_meta_from_coco_categories(coco_categories, coco_images, coco_anns)
    meta_json = g.META.to_json()
    sly.json.dump_json_file(meta_json, path_to_meta)
    return g.META


def get_coco_annotations_for_current_image(coco_image, coco_anns):
    image_id = coco_image["id"]
    return [coco_ann for coco_ann in coco_anns if image_id == coco_ann["image_id"]]


def coco_category_to_class_name(coco_categories):
    return {category["id"]: category for category in coco_categories}


def convert_polygon_vertices(coco_ann):
    for polygons in coco_ann["segmentation"]:
        exterior = polygons
        exterior = [exterior[i * 2 : (i + 1) * 2] for i in range((len(exterior) + 2 - 1) // 2)]
        exterior = [sly.PointLocation(height, width) for width, height in exterior]
        return sly.Polygon(exterior, [])


def convert_rle_mask_to_polygon(coco_ann):
    rle_obj = mask_util.frPyObjects(
        coco_ann["segmentation"],
        coco_ann["segmentation"]["size"][0],
        coco_ann["segmentation"]["size"][1],
    )
    mask = mask_util.decode(rle_obj)
    mask = np.array(mask, dtype=bool)
    return sly.Bitmap(mask).to_contours()


def get_coords(keypoints):
    for i in range(0, len(keypoints), 3):
        yield keypoints[i : i + 3]


def create_sly_ann_from_coco_annotation(meta, coco_categories, coco_ann, image_size):
    labels = []
    for object in coco_ann:
        obj_category_id = object["category_id"]
        # keypoint
        cat_id_map = coco_category_to_class_name(coco_categories)
        obj_class_name = cat_id_map[obj_category_id].get("name")
        obj_class = meta.get_obj_class(obj_class_name)
        if obj_class_name is None or obj_class is None:
            sly.logger.warn(f"Object class {obj_class_name} not found in COCO categories.")
            continue

        keypoints = list(get_coords(object["keypoints"]))


        keypoint_names = cat_id_map[obj_category_id].get("keypoints")
        if keypoint_names is None:
            sly.logger.warn(f"Keypoints field not found in {obj_class_name} COCO category.")
            continue

        nodes = []
        for coords, keypoint_name in zip(keypoints, keypoint_names):
            col, row, visibility = coords
            # v = False
            if visibility in g.label_visibility:
                # col, row = None, None
                # v = True
                continue

            node = Node(label=keypoint_name, row=row, col=col)  # , disabled=v)
            nodes.append(node)

        if len(nodes) != 0:
            key = uuid.uuid4().hex

            # bbox
            obj_class_bbox_name = f"{obj_class_name}_bbox"
            obj_class_bbox = meta.get_obj_class(obj_class_bbox_name)
            bbox = object.get("bbox")
            if bbox is None or len(bbox) == 0:
                label_graph = sly.Label(GraphNodes(nodes), obj_class)
                labels.append(label_graph)
                continue
            label_graph = sly.Label(GraphNodes(nodes), obj_class, binding_key=key)
            xmin = bbox[0]
            ymin = bbox[1]
            xmax = xmin + bbox[2]
            ymax = ymin + bbox[3]
            label_bbox = sly.Label(
                sly.Rectangle(top=ymin, left=xmin, bottom=ymax, right=xmax),
                obj_class_bbox,
                binding_key=key,
            )
            labels.append(label_bbox)
            labels.append(label_graph) # to keep correct group name and objects order
    return sly.Annotation(img_size=image_size, labels=labels)


def create_sly_dataset_dir(dataset_name):
    dataset_dir = os.path.join(g.SLY_BASE_DIR, dataset_name)
    mkdir(dataset_dir)
    img_dir = os.path.join(dataset_dir, "img")
    mkdir(img_dir)
    ann_dir = os.path.join(dataset_dir, "ann")
    mkdir(ann_dir)
    return dataset_dir


def move_trainvalds_to_sly_dataset(dataset, coco_image, ann):
    image_name = coco_image["file_name"]
    ann_json = ann.to_json()
    sly.json.dump_json_file(ann_json, os.path.join(g.ann_dir, f"{image_name}.json"))
    coco_img_path = os.path.join(g.COCO_BASE_DIR, dataset, "images", image_name)
    sly_img_path = os.path.join(g.img_dir, image_name)
    if file_exists(os.path.join(coco_img_path)):
        shutil.move(coco_img_path, sly_img_path)


def move_testds_to_sly_dataset(dataset):
    ds_progress = sly.Progress(
        f"Converting dataset: {dataset}",
        len(os.listdir(g.src_img_dir)),
        min_report_percent=1,
    )
    for image in os.listdir(g.src_img_dir):
        src_image_path = os.path.join(g.src_img_dir, image)
        dst_image_path = os.path.join(g.dst_img_dir, image)
        shutil.move(src_image_path, dst_image_path)
        im = Image.open(dst_image_path)
        width, height = im.size
        img_size = (height, width)
        ann = sly.Annotation(img_size)
        ann_json = ann.to_json()
        sly.json.dump_json_file(ann_json, os.path.join(g.ann_dir, f"{image}.json"))
        ds_progress.iter_done_report()


def check_dataset_for_annotation(dataset_name, ann_dir):
    if g.ds_mode == "original":
        ann_path = os.path.join(ann_dir, f"person_keypoints_{dataset_name}.json")
    elif g.ds_mode == "custom":
        ann_path = os.listdir(ann_dir)
        if len(ann_path) == 0:
            raise ValueError(f"Annotation file not found in {ann_dir}")
        elif ann_path[0].endswith(".json"):
            ann_path = os.path.join(ann_dir, ann_path[0])
        else:
            raise ValueError(f"Annotation file must be in '.json' format: {ann_path[0]}")
    return bool(os.path.exists(ann_path) and os.path.isfile(ann_path))


def get_ann_path(ann_dir, dataset_name):
    if g.ds_mode == "original":
        return os.path.join(ann_dir, f"person_keypoints_{dataset_name}.json")
    elif g.ds_mode == "custom":
        return os.path.join(ann_dir, os.listdir(ann_dir)[0])
