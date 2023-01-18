import os

import supervisely as sly
from pycocotools.coco import COCO
from supervisely.io.fs import dir_exists
from supervisely import logger

import coco_converter
import coco_downloader
import globals as g

def import_coco(api: sly.Api):
    project_name, coco_datasets = coco_downloader.start(logger)
    for dataset in coco_datasets:
        coco_dataset_dir = os.path.join(g.COCO_BASE_DIR, dataset)
        if not dir_exists(coco_dataset_dir):
            logger.info(
                f"File {coco_dataset_dir} has been skipped."
            )
            continue
        coco_ann_dir = os.path.join(coco_dataset_dir, "annotations")
        if not dir_exists(os.path.join(coco_dataset_dir, "images")):
            logger.warn(
                "Incorrect input data. Folder with images must be named 'images'. See 'README' for more information."
            )
            continue

        if coco_converter.check_dataset_for_annotation(
            dataset_name=dataset, ann_dir=coco_ann_dir
        ):
            coco_ann_path = coco_converter.get_ann_path(
                ann_dir=coco_ann_dir, dataset_name=dataset
            )

            coco = COCO(annotation_file=coco_ann_path)
            categories = coco.loadCats(ids=coco.getCatIds())
            coco_images = coco.imgs
            coco_anns = coco.imgToAnns

            sly_dataset_dir = coco_converter.create_sly_dataset_dir(
                dataset_name=dataset
            )
            g.img_dir = os.path.join(sly_dataset_dir, "img")
            g.ann_dir = os.path.join(sly_dataset_dir, "ann")
            meta = coco_converter.get_sly_meta_from_coco(
                coco_categories=categories, dataset_name=dataset
            )

            ds_progress = sly.Progress(
                message=f"Converting dataset: {dataset}",
                total_cnt=len(coco_images),
                min_report_percent=1,
            )

            for img_id, img_info in coco_images.items():
                img_ann = coco_anns[img_id]
                img_size = (img_info["height"], img_info["width"])
                ann = coco_converter.create_sly_ann_from_coco_annotation(
                    meta=meta,
                    coco_categories=categories,
                    coco_ann=img_ann,
                    image_size=img_size,
                )
                coco_converter.move_trainvalds_to_sly_dataset(
                    dataset=dataset, coco_image=img_info, ann=ann
                )
                ds_progress.iter_done_report()
        else:
            sly_dataset_dir = coco_converter.create_sly_dataset_dir(
                dataset_name=dataset
            )
            g.src_img_dir = os.path.join(g.COCO_BASE_DIR, dataset, "images")
            g.dst_img_dir = os.path.join(sly_dataset_dir, "img")
            g.ann_dir = os.path.join(sly_dataset_dir, "ann")
            coco_converter.move_testds_to_sly_dataset(dataset=dataset)

    sly.upload_project(
        dir=g.SLY_BASE_DIR,
        api=api,
        workspace_id=g.WORKSPACE_ID,
        project_name=project_name,
        log_progress=True,
    )


def main():
    import_coco(api=g.api)


if __name__ == "__main__":
    main()