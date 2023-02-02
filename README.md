
<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/215463770-427a0fc2-f715-49e0-9562-c7cd726f6079.png"/>

# Import COCO Keypoints

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-coco-keypoints)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-coco-keypoints?include_prereleases)
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

COCO Keypoint detection annotation format have visibility flags:

- 0 Keypoint not in the image.
- 1 Keypoint is in the image, but not visible, namely maybe behind of an object.
- 2 Keypoint looks clearly, not hidden.

All keypoints with 0 visibility are ignored and will not be presented in the project.
As for other 2: you can specify label preferences in the modal window whether you want to include key points that are labeled, but not visible or import only clearly visible keypoints.

|                                                              Visibility = 1                                                               |                                                              Visibility = 2                                                               |
| :---------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://user-images.githubusercontent.com/48913536/215511152-c6d181be-9bb8-4b39-a43e-0b6ba9cdb3d6.png" style="max-width:100%;"> | <img src="https://user-images.githubusercontent.com/48913536/215511138-d909dd0e-bf2d-4686-80c8-586ade92c271.png" style="max-width:100%;"> |

# How to Run

**Step 1.** Run app from the `Ecosystem`

<div align="center" markdown>
  <img src="https://user-images.githubusercontent.com/48913536/215512527-02d3f25d-0f5e-4796-be45-a054716f3683.png"/>
</div>

**Step 2.** Select options in the modal window and run the app

<div align="center" markdown>
  <img src="https://user-images.githubusercontent.com/48913536/215732921-068a78ac-8e2b-4a2f-8307-dff21ffb2498.png" width="500px"/>
</div>

**Step 3.** After pressing the `Run` button you will be redirected to the `Tasks` page

<div align="center" markdown>
  <img src="https://user-images.githubusercontent.com/48913536/215511131-8f9b863f-4335-4768-acfe-5c04fe2bc0a8.png" width="700px"/>
</div>

# Results

Result project will be saved in your current `Workspace` with name `Original COCO` if you haven't specified project name in the modal window.

<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/215511125-afa52475-bb7f-4963-a4f9-e16017b3d9de.png"/>
</div>
