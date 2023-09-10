import os
import shutil

import requests
from supervisely.io.fs import download, file_exists, mkdir, silent_remove, dir_exists

import dl_progress
import globals as g
import supervisely as sly


def download_file_from_link(link, file_name, archive_path, progress_message, app_logger):
    response = requests.head(link, allow_redirects=True)
    sizeb = int(response.headers.get("content-length", 0))
    progress_cb = dl_progress.get_progress_cb(
        g.api, g.TASK_ID, progress_message, sizeb, is_size=True
    )
    if not file_exists(archive_path):
        # @TODO: download CACHE dir
        download(link, archive_path, progress=progress_cb)
        dl_progress.reset_progress(g.api, g.TASK_ID)
        app_logger.info(f"{file_name} has been successfully downloaded")


def download_coco_images(dataset, archive_path, save_path, app_logger):
    link = g.images_links[dataset]
    file_name = f"{dataset}.zip"
    download_file_from_link(link, file_name, archive_path, f"Download {file_name}", app_logger)
    shutil.unpack_archive(archive_path, save_path, format="zip")
    os.rename(os.path.join(save_path, dataset), os.path.join(save_path, "images"))
    silent_remove(archive_path)


def download_coco_annotations(dataset, archive_path, save_path, app_logger):
    link = None
    file_name = None
    ann_dir = os.path.join(save_path, "annotations")
    if dataset in ["train2017", "val2017"]:
        if os.path.exists(ann_dir):
            return
        link = g.annotations_links["trainval2017"]
        file_name = "trainval2017.zip"
    download_file_from_link(link, file_name, archive_path, f"Download {file_name}", app_logger)
    shutil.unpack_archive(archive_path, save_path, format="zip")
    for file in os.listdir(ann_dir):
        if file != f"person_keypoints_{dataset}.json":
            silent_remove(os.path.join(ann_dir, file))
    silent_remove(archive_path)


def download_original_coco_dataset(datasets, app_logger):
    for dataset in datasets:
        dataset_dir = os.path.join(g.COCO_BASE_DIR, dataset)
        mkdir(dataset_dir)
        archive_path = f"{dataset_dir}.zip"
        download_coco_images(dataset, archive_path, dataset_dir, app_logger)
        if not dataset.startswith("test"):
            download_coco_annotations(dataset, archive_path, dataset_dir, app_logger)
    return datasets


def download_dir_from_supervisely(path_to_remote_dir, dir_path, progress_message, app_logger):
    dir_size = g.api.file.get_directory_size(g.TEAM_ID, path_to_remote_dir)
    if not dir_exists(dir_path):
        progress_upload_cb = dl_progress.get_progress_cb(
            g.api, g.TASK_ID, progress_message, total=dir_size, is_size=True
        )
        g.api.file.download_directory(
            g.TEAM_ID, path_to_remote_dir, dir_path, progress_cb=progress_upload_cb
        )

        app_logger.info(f'Directory "{path_to_remote_dir}" has been successfully downloaded')


def download_file_from_supervisely(
    path_to_remote_dataset, archive_path, archive_name, progress_message, app_logger
):
    file_size = g.api.file.get_info_by_path(g.TEAM_ID, path_to_remote_dataset).sizeb
    if not file_exists(archive_path):
        progress_upload_cb = dl_progress.get_progress_cb(
            g.api, g.TASK_ID, progress_message, total=file_size, is_size=True
        )
        g.api.file.download(
            g.TEAM_ID,
            path_to_remote_dataset,
            archive_path,
            progress_cb=progress_upload_cb,
        )
        app_logger.info(f'"{archive_name}" has been successfully downloaded')


def download_custom_coco_dataset(path_to_remote_dataset, app_logger):
    if g.api.file.exists(g.TEAM_ID, path_to_remote_dataset):
        archive_name = os.path.basename(os.path.normpath(path_to_remote_dataset))
        archive_path = os.path.join(g.COCO_BASE_DIR, archive_name)
        # extract_path =
        download_file_from_supervisely(
            path_to_remote_dataset,
            archive_path,
            archive_name,
            f'Download "{archive_name}"',
            app_logger,
        )
        app_logger.info("Unpacking archive...")
        sly.fs.unpack_archive(archive_path, g.COCO_BASE_DIR)
        silent_remove(archive_path)
        app_logger.info("Archive has been unpacked.")
    elif g.api.file.dir_exists(g.TEAM_ID, path_to_remote_dataset):
        dir_name = os.path.basename(os.path.normpath(path_to_remote_dataset))
        dir_path = os.path.join(g.COCO_BASE_DIR, dir_name)
        download_dir_from_supervisely(
            path_to_remote_dataset,
            dir_path,
            f'Download "{dir_name}"',
            app_logger,
        )
        sly.fs.remove_junk_from_dir(dir_path)
    else:
        raise ValueError(f"File or directory {path_to_remote_dataset} not found in Team Files.")

    def check_function(path):
        images_dir = os.path.join(path, "images")
        annotations_dir = os.path.join(path, "annotations")
        return os.path.isdir(images_dir) and os.path.isdir(annotations_dir)

    datasets = [ds for ds in sly.fs.dirs_filter(g.COCO_BASE_DIR, check_function)]
    path_components = [os.path.normpath(path).split(os.path.sep) for path in datasets]
    g.COCO_BASE_DIR = os.path.sep.join(os.path.commonprefix(path_components))
    return [os.path.basename(os.path.normpath(path)) for path in datasets]


def start(app_logger):
    project_name = g.OUTPUT_PROJECT_NAME
    if g.ds_mode == "original":
        coco_datasets = download_original_coco_dataset(g.original_ds, app_logger)
        if project_name is None or project_name == "":
            project_name = "Original COCO Keypoints"
    elif g.ds_mode == "custom":
        coco_datasets = download_custom_coco_dataset(g.custom_ds, app_logger)
        if project_name is None or project_name == "":
            project_name = "Custom COCO Keypoints"
    return project_name, coco_datasets
