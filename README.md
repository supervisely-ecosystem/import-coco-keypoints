
<div align="center" markdown>
<img src=""/>

# Import COCO Keypoints

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-coco-keypoints)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-coco-keypoints)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-coco-keypoints&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-coco-keypoints&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-coco-keypoints&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview

App converts [COCO format](https://cocodataset.org/#home) datasets to [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi)

Application key points:  
- Import full original COCO 2017 & COCO 2014 datasets
- Supports custom coco datasets
- Supports only instance segmentation(polygons) and object detection(bounding boxes) from COCO format
- All information about dataset, licenses and images from COCO annotation file **will be lost**
- Backward compatible with [Export to COCO](https://github.com/supervisely-ecosystem/export-to-coco)

Custom project structure:
```
.
COCO_BASE_DIRECTORY
├── coco_dataset_1        # With annotations
│   ├── annotations
│   │   └── instances.json
│   └── images
│       ├── IMG_3861.jpeg
│       ├── IMG_4451.jpeg
│       └── IMG_8144.jpeg
├── coco_dataset_2        # Dataset with empty annotations dir will be treated like dataset without annotations
│   ├── annotations
│   └── images
│       ├── IMG_0748.jpeg
│       ├── IMG_1836.jpeg
│       └── IMG_2084.jpeg
└── coco_dataset_3        # Without annotations
    └── images
        ├── IMG_0428.jpeg
        ├── IMG_1885.jpeg
        └── IMG_2994.jpeg
```

# How to Use

**Step 1.** Run app from the `Plugins & Apps` chapter:

<div align="center" markdown>
  <img src="https://i.imgur.com/2luJyn4.png"/>
</div>

**Step 2.** Select import mode:

- Your can download selected datasets from [COCO](https://cocodataset.org/#download).  
- Use your custom dataset in COCO format by path to your archive in `Team Files`.

<div align="center" markdown>
  <img src="https://user-images.githubusercontent.com/48913536/183898478-05fc7314-3d28-408e-bbe5-90e6522f0102.png" width="700px"/>
</div>

**Step 3.** After pressing the `Run` button you will be redirected to the `Tasks` page.

# Results

Result project will be saved in your current `Workspace` with name `Original COCO` for original datasets and `Custom COCO` for custom datasets

<div align="center" markdown>
<img src="https://i.imgur.com/BJuGxtL.png"/>
</div>
