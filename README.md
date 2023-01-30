
<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/215463770-427a0fc2-f715-49e0-9562-c7cd726f6079.png"/>

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

- Import full original COCO 2017 dataset
- Supports only keypoint detection and object detection (bounding boxes) from COCO format
- All information about dataset, licenses and images from COCO annotation file **will be lost**

# How to Use

**Step 1.** Run app from the `Ecosystem`:

<div align="center" markdown>
  <img src=""/>
</div>

**Step 2.** Select import mode:

- Your can download selected datasets from [COCO](https://cocodataset.org/#download).  

<div align="center" markdown>
  <img src="" width="700px"/>
</div>

**Step 3.** After pressing the `Run` button you will be redirected to the `Tasks` page.

# Results

Result project will be saved in your current `Workspace` with name `Original COCO` if you haven't specified project name in the modal window.

<div align="center" markdown>
<img src=""/>
</div>
