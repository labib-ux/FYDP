# Fabric Defect Detection and Leadtime Prediction

**By**

| Name | ID |
|------|-----|
| Ms. Riya Akter Satu | 0112310147 |
| Nafiz Imtiaz Labib | 0112310422 |
| Mohammad Amin | 0112310412 |
| Abdullah Al Fahim Zahin | 0112310314 |
| Mustafizur Rahman Murad | 0112310426 |
| Fahim Ferdous Niloy | 0112310307 |

Submitted in partial fulfilment of the requirements
of the degree of Bachelor of Science in Computer Science and Engineering

27 September 2026

Department of Computer Science and Engineering
United International University

---
# Abstract

The current research focuses on building a unified solution for fabric defects detection from images and lead time prediction based on the detected quality conditions for the textile and ready-made garments industry of Bangladesh. Despite the development of automatic defect detection solutions for a number of different fields, fabric inspection in most factories in Bangladesh remains manual and depends heavily on the experience of individual inspectors. Additionally, the production planning process uses fixed lead-time tables without consideration of the quality of fabrics which are used for production at the moment. It results in difficulties in managing delivery time and costs for one of the major export sectors of Bangladesh.

Detection of fabric defects is a field of application of computer vision and image processing for the purposes of industrial quality control. On the other hand, lead-time prediction is a machine learning regression task. Together, these two methods form a feedback loop in which visible quality conditions affect the production planning process. Such a concept is not limited to the textile manufacturing industry but can be applied to other production fields where the quality of products affects the time of its completion.

Previous research on this topic encountered multiple limitations related to a small dataset or lack of information about the data used, using duplicated images for evaluation, defect detection solutions which are not integrated with production planning process and synthetical planning data which was not relevant to actual factory situation. These limitations make necessary a better approach.

To address this issue, this research is based on the dataset auditing process in which each image will be cryptographically hashed to find duplicates, exact duplicate samples will be excluded, cross-labeled files will be quarantined after visual validation and will be divided by fabric group to exclude the appearance of the same swatch in both train and test sets. The pilot dataset consists of 2,550 images divided into six classes and the evaluation metric is designed on the basis of transparent metrics: mean Average Precision (mAP) for defect detection and Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and R² for production planning.

For the defect detection problem, the project will use YOLO-family detectors with YOLOv11-seg as a target model combined with the image processing algorithm to estimate defect area. For lead-time prediction, random forest regression will be used together with the comparison of the solution to XGBoost and MLP models.

---

# Acknowledgements

Without the help and contribution of many people, this paper could not be produced in the last two trimesters. It is our pleasure to thank all of those who supported us during the process of developing this paper.

To begin with, we wish to show our deepest appreciation to our supervisor, who always provided us with constant guidance, useful feedback, constructive suggestions, and encouragement.

We would like to thank the Department of Computer Science and Engineering, United International University, for allowing us access to the laboratory GPU facilities that were necessary in this study.

Also, we would like to thank the Almighty for the strength and patience that was given to us to conduct this study.

Last but not least, we would like to thank our family members and especially our parents for their constant emotional support during this study.

---



# Table of Contents

- Abstract
- Acknowledgements
- Chapter 1 — Introduction
  - 1.1 Project Overview
  - 1.2 Motivation
  - 1.3 Objectives
  - 1.4 Methodology
  - 1.5 Organization Of the Report
- Chapter 2 — Background
  - 2.1 Preliminaries
  - 2.2 Literature Review (20 Papers, 3 Themes)
  - 2.3 Summary
- Chapter 3 — Project Design
  - 3.1 Requirement Analysis
  - 3.2 Methodology & Design
- Chapter 4 — Implementation and Results
  - 4.1 Environment Setup
  - 4.2 Testing and Evaluation
  - 4.3 Results and Discussion
  - 4.4 Summary
- Chapter 5 — Standards and Design Constraints
  - 5.1 Standards and Design Constraints
  - 5.2 Design Constraints
  - 5.3 Cost Analysis
  - 5.4 Complex Engineering Problem
  - 5.5 Summary
- Chapter 6 — Conclusion
  - 6.1 Summary
  - 6.2 Project Plan
  - 6.3 Future Work
  - 6.4 Limitations and Final Remarks
  - 6.5 Final Conclusion
- Bibliography

---

# List of Figures

- Figure 3.1: Context Diagram
- Figure 3.2: Proposed System Diagram
- Figure 3.3: Architectural Design
- Figure 3.4: Use Case Diagram
- Figure 3.5: System Workflow
- Figure 3.6: Metadata Bridge
- Figure 3.7: Machine Learning Pipeline
- Figure 3.8: Four-Point Inspection Grading Logic
- Figure 3.9: Project Task Allocation Gantt Chart

---

# List of Tables

- Table 2.1: Literature Analysis
- Table 3.1: Dataset Classes and Descriptions
- Table 3.2: Audited Dataset Composition
- Table 3.3: Quarantine Ledger (Summary)
- Table 3.4: Training and Testing Split (Group-Aware Manifest)
- Table 3.5: Requirement Summary
- Table 3.6: Main Project Modules
- Table 3.7: Project Plan
- Table 3.8: Task Allocation
- Table 4.1: Estimated Project Budget
- Table 4.2: Complex Engineering Problem Mapping
- Table 5.1: Estimated Project Budget
- Table 5.2: Mapping with Complex Problem Solving
- Table 5.3: Mapping with Complex Engineering Activities
- Table 6.1: Pilot Reference and Upper Bound

---


# Chapter 1 — Introduction

This paper shows a way to bring together YOLO-based fabric defect detection and Random Forest lead-time prediction using one number the Defect Density Score (DS).

## 1.1 Project Overview

Machine learning and computer vision are both parts of artificial intelligence; machine learning helps systems to find patterns in data, whereas computer vision lets them to understand the visuals. Thus, in textile manufacturing, computer vision can be applied for checking the fabric quality in terms of images, and machine learning can help to determine production time according to this quality.

At the moment, these processes are done independently. Defects are found by inspectors, and their amount is calculated; however, the impact of these defects on production time is not determined.


That is why creating an adequate connection between the quality and production time is difficult; without any way of turning information from visuals into reasonable time estimations, factories may experience late deliveries or use excessive buffers when scheduling. Information about the impact of defects is missing during production planning.

In this paper, an approach to integrate YOLO-based fabric defect detection and Random Forest-based lead-time prediction with a single parameter called Defect Density Score (DS) is suggested.

## 1.2 Motivation

One example of this problem occurring in practice is that an inspector may manually spot defects over several hours of work, and then a production planner develops delivery plans based on precomputed tables built under certain assumptions. It makes a difference between real fabric states and planning. Quality data acquired during inspection is not used efficiently in planning processes.

Integration of data is the main motivation for conducting this research.

Closed-loop methodology could also be extended to other industrial applications, where visible changes in quality affect the length of the production process, such as predictive maintenance and estimation of waste amounts.

Initial stage of this project includes literature survey and collecting of a pilot dataset of about 2,550 images. The future product will include a dashboard allowing planners to see defect categories, Defect Density Score, and estimated hours of production in real time.

The reliability of the dataset is the major challenge at this moment. There is currently no reliable audit and separation of evaluation and training groups in datasets. In order to ensure better data reliability, all images were indexed by their hash sums, 17 duplicated images were removed, and 12 cross-labeled files were quarantined visually. The current pilot system scored 98% on a randomly split test set. Nevertheless, the score should be considered as a reference point and verified by a more honest disjoint evaluation method.

## 1.3 Objectives

Construct an audited fabric imagery database comprising six defect categories including hole, horizontal, vertical, lines, stain, and no defects. The database should contain a hash inventory, quarantine register, and split manifest by class.

Design YOLOv11-seg target detector to classify defect classes and quantify defect pixel areas. The performance will be assessed in terms of mAP.

Design Random Forest model for prediction of lead times using machine speed, order quantity, and Ds as predictors. The performance will be assessed in terms of MAE, RMSE, and R² in comparison to models lacking Ds information.

Deploy all models within a real-time closed-loop architecture with a planner dashboard.

Make sure that all the results are verified through the use of disjoint databases, where no common swatch families occur between train and test sets.

## 1.4 Methodology

Methodology describes the process that occurs at each step of the proposed system.

Firstly, defect detection will be done by using YOLO family classification and detection models. Then defect regions will be measured using the techniques of image processing like thresholding, contour detection and morphological operations moving towards instance segmentation.

For unknown defect types, few-shot anomaly detection models will be explored like PatchCore and DINOv2 by only using fabric images without any defects in the training stage. Production time prediction will be done using regression models mainly Random Forest while making comparisons between XGBoost and MLP models.

In order to have consistent features, rolling average Defect Density Score (DS) smoothing method will be implemented.

Reproducible seeded data splitting and dashboard will be developed showing defect type, confidence score, (DS) value and production hours prediction for the planners.

The major technologies used in this project are Python, Ultralytics YOLO, OpenCV, scikit-learn and Jetson class edge deployment with TensorRT.

## 1.5 Organization Of the Report

In this Section, we provide an overview of the major work we have carried out throughout the project.

**Introduction:** We represent the project overview, motivation, objectives, methodology for integrating fabric defect detection with production lead-time prediction.

**Background:** We discussed YOLO-based defect detection, segmentation and defect area measurement, anomaly detection, ensemble regression, and related research on fabric datasets and production planning.

**Project Design:** We described the system requirements, proposed methodology, system architecture, workflow, Defect Density Score calculation, lead-time prediction, four-point inspection and project implementation.

**Standard Design and Constraints:** We discussed the relevant software, hardware, and communication standards, design constraints, estimation project and complex engineering considerations.

**Conclusion:** We summarized the major work completed, presented the project plan, discussed future work and highlighted the limitations of the proposed system.

---


---
# Chapter 2 — Background

## 2.1 Preliminaries

This chapter discusses the technical preliminaries that will be used in the proposed system. This includes supervised defect detection, defect measurement through segmentation, anomaly detection, ensemble regression, and procedures.

### 2.1.1 Supervised Defect Detection using YOLO

YOLO (You Only Look Once) is an object detection technique that considers detection as a single regression problem at the image level. While most detection algorithms perform the operation with a number of iterations, YOLO splits the image into grids where each grid cell predicts bounding boxes, confidence scores, and class probabilities [1].

Subsequent improvements of YOLO include improvements in the backbone network, feature extraction methods, and detector head design.

Recent YOLO versions have introduced architectural improvements for better detection performance [2].

The performance of the detection model can be assessed based on evaluation metrics including precision, recall, F1-score, mAP50, and mAP50–95.

Figure 2.1 illustrates the general detection process involving the image grid to bounding boxes and classes.

### 2.1.2 Image Segmentation and Area Calculation

The traditional way of measuring the defect typically involves conversion to grayscale followed by image thresholding through adaptive or Otsu's thresholding. Having separated the image into segments, we then apply morphological operation for contour detection and defect area measurement.

```
Defect area ratio = defect pixels / frame pixels
```

The instance segmentation allows obtaining more information about a defect by generating individual mask for each defect. It is especially useful when dealing with irregular defects, such as stains and pulled threads, as bounding boxes overestimate the area in these cases.

Segmentation quality is measured in terms of Mask IoU, which evaluates the degree of overlap between predicted and ground truth masks. In this project, the ablation study will be carried out comparing defect area estimation based on bounding boxes (Ds) and masks.

### 2.1.3 Unsupervised Anomaly Detection

Unsupervised anomaly detection training is carried out using only defect-free samples to identify anomalous patterns. It is useful when the collection of annotated defect data is difficult or when new defects may emerge in production in the future.

Autoencoders detect defects based on the differences in reconstruction of normal and abnormal samples. The technique of Reverse Distillation detects anomalies by comparing student and teacher models while maintaining fast inference.

PatchCore makes use of a patch memory bank and has demonstrated strong performance on industrial anomaly detection datasets such as MVTec [3]. Few-shot anomaly detection approaches such as AnomalyDINO and PatchEAD aim to identify defects using limited samples without requiring complete defect annotations [4, 5].

Anomaly detection module for this project is intended to detect previously unseen fabric defects.

### 2.1.4 Ensemble Regression

Random Forest proposed by Breiman is an ensemble learning method that averages the results of multiple decision trees to improve prediction stability and reduce variance [6].

Furthermore, its performance will be compared to the one of the static mean forecast and to the ones of models without using (Ds) as a predictor.

### 2.1.5 Methods and Procedures

The process of data collecting follows a certain geometry of setup with an image resolution of 640 pixels. Data preprocessing includes the removal of noise via Gaussian filtering, motion-blur modeling and gamma correction for low light.

As for the defect measurements, morphological techniques as well as four-point grading-based calibration are applied. Defect density is measured based on the Defect Density Score (Ds) which reflects the history of defects detected at any point of time.

The relation between defect density and production lead time is the following:

```
Lead = (Qty / Speed) × 0.1 × (1 + 2 × Ds)
```

For example, when Ds = 0.2, the value of production time will increase by 40%.

### 2.1.6 Works Related to Detection Models

The YOLOv1 to YOLOv11 fabric review reports YOLOv11 as effective for detecting small and occluded defects [2].

Fab-ASLKS reports a 5% improvement in mAP50 on Tianchi, while Fab-ME reports a 3.3% improvement and 59.4% performance over 20 classes. FabricMamba focuses on edge deployment. The anomaly detection line includes PatchCore, RD++, AnomalyDINO, and PatchEAD. Kumar (2008) provides a classical survey of fabric defect detection.

EfficientDet with Jetson TX2 achieved 22.7 FPS, reported as 2.5 times faster than cloud processing. YOLOv11 was also evaluated on Orin Nano, while the NEU-DET comparison reports a 70% average improvement for YOLOv11.

---


## 2.2 Literature Review (20 Papers, 3 Themes)

The recent research in fabric defect detection has shifted from traditional computer vision-based systems to deep learning ones. They are categorized into the following three groups:

- Fabric data sets
- Defect detection models
- Production and manufacturing research

### 2.2.1 Works Related to Fabric Datasets

Some datasets can be used to develop automated fabric defect detection.

Isl-Knit provides a dataset with 3,375 knit-fault images with seven classes collected from dyeing factories in Bangladesh [7].

FabricSpotDefect contains 1,014 images with 3,288 spot defect annotations for different fabric types in COCO and YOLOv8 formats [8].

International fabric datasets include ZJU-Leaper (98,777 woven fabric images), the Tianchi dataset (20 defect types), and some industry anomaly datasets such as MVTec AD and VisA.

Pilot dataset for the project consists of 2,578 images within six classes with each file being hashed.

### 2.2.2 Works Related to Detection Models

The review of fabric defect detection from YOLOv1 to YOLOv11 highlights improvements in detecting small and partially occluded defects [2].

Some other papers to consider:

- Fab-ASLKS that increased mAP50 on the Tianchi dataset by 5%;
- Fab-ME that improved the detection by about 3.3% reaching 59.4% for 20 defect classes;
- FabricMamba – on lightweight edge-based fabric inspection;
- PatchCore, Reverse Distillation, AnomalyDINO, and PatchEAD – for anomaly detection tasks; Survey of classical fabric defect detection techniques by Kumar [9]; EfficientDet with Jetson TX2 delivering 22.7 FPS and demonstrating advantages for edge-based processing [10];
- YOLOv11 implementation on Orin Nano edge devices;
- NEU-DET comparisons where benefits from YOLOv11 were identified.

### 2.2.3 Works Related to Planning and Production

Currently, there is no vision-based Defect Density Score (Ds) and lead-time prediction system. This is the gap this project tries to fill.

The works related to prediction are: CIIS 2024 research investigated textile waste prediction based on defective material data using machine learning models [11].

In addition, the following related papers could be useful:

- 2025 digital quality-control experiments in Bangladeshi factories aimed to reduce defects by 15% and increase DHU by 1.5 to 3 percentage points;
- Industrial monitoring systems like JUKI JaNets increase production visibility. 2026 quality control experiment in Narayanganj involved 94 production lines;
- Predicting textile manufacturing parameters.

## 2.3 Summary

**Table 2.1: Literature Review**

| No. | Paper Name | Method | Dataset | Year |
|-----|------------|--------|---------|------|
| 1 | Kumar fabric survey | Supervised + classical | Collected | 2008 |
| 2 | Isl-Knit + 4-point (BUTEX) | Supervised (YOLOv5) | Own (3,375) | 2024 |
| 3 | FabricSpotDefect (IUB) | Supervised | Own (1,014) | 2024 |
| 4 | YOLOv1–v11 fabric review | Supervised | Collected | 2025 |
| 5 | Fab-ASLKS | Supervised | Tianchi | 2025 |
| 6 | Fab-ME | Supervised | Tianchi (20 cls) | 2024 |
| 7 | FabricMamba edge | Supervised | Own | 2025 |
| 8 | PatchCore | Unsupervised | MVTec/VisA | 2022 |
| 9 | Reverse Distillation (RD++) | Unsupervised | MVTec | 2023 |
| 10 | PatchCore few-shot opt. | Few-shot | MVTec/VisA | 2023 |
| 11 | AnomalyDINO | Few-shot | MVTec | 2025 |
| 12 | PatchEAD | Few/zero-shot | 7 industrial | 2025 |
| 13 | EfficientDet + Jetson TX2 | Supervised | 5 fabric sets | 2021 |
| 14 | YOLOv8 lightweight + edge | Supervised | Own | 2024 |
| 15 | Fabric wastage prediction (CIIS) | Supervised | Own (633) | 2024 |
| 16 | BD RMG digital QC trials | Applied | Factory trials | 2025 |
| 17 | Traffic-light QC Narayanganj | Applied | 94 lines | 2026 |
| 18 | Textile parameter prediction | Supervised | Manufacturing | 2024 |
| 19 | Redmon et al., YOLO | Supervised | VOC/COCO | 2016 |
| 20 | Breiman, Random Forests | Supervised | General | 2001 |

Supervised detection systems deal with known defects, anomaly models detect defects, edge tooling demonstrates feasibility in real time, and BD provides evaluation of local ground truth. The connection between vision and hours is not yet exploited: this is what we contribute.

---


# Chapter 3 — Project Design

This chapter presents the detailed design of the proposed unified fabric defect detection and production lead-time prediction system. The system is designed to connect real-time fabric quality information with production planning. The chapter discusses the system requirements, audited dataset, proposed methodology, system architecture, workflow, metadata bridge, machine learning pipeline, four-point grading logic, software and hardware specifications, and task allocation.

## 3.1 Requirement Analysis

The proposed system has both functional and non-functional requirements. The functional requirements define the main operations that the system must perform, while the non-functional requirements describe the expected performance, robustness, scalability, and maintainability of the system.

**Table 3.1: Requirement Summary**

| Requirement Type | Requirements |
|------------------|--------------|
| Functional | • Take fabric image/stream as input. • Preprocessing. • Detection of defect type. • Identification of defect-free images. • Calculation of area ratio and Ds. • Prediction of lead time. • Result output. |
| Non-functional | • Accurate (with mAP tracking). • Robust in terms of lighting/textures. • Efficient in terms of real-time processing (≥ 15 FPS at the edge). • Scalable in terms of adding new fabrics through few-shot branch. • Modular and easy-to-maintain code with a configuration central point. |

**Table 3.2: Classes and Descriptions for Dataset Images**

| Class | Description |
|-------|-------------|
| Hole | Missing piece of fabric, opening or damage. |
| Horizontal | Horizontal pattern of defects on fabric surface. |
| Vertical | Vertical pattern of defects. |
| Line | Line-like defects (pulled threads). |
| Stain | Fabric contamination or stain. |
| Defect-Free | Normal fabric without visible defects. |

**Table 3.3: Composition of Audited Dataset**

| Class / Action | Count |
|----------------|------:|
| Total scans | 2,578 |
| Defect-Free | 1,505 |
| Stain | 398 |
| Hole | 281 |
| Lines | 157 |
| Horizontal | 136 |
| Vertical | 101 |
| Duplicate samples eliminated | 17 |
| Quarantine samples | 12 |
| Useful samples | 2,549 |

**Table 3.4: Quarantine Record (Summary)**

| Samples | Description | Verdict |
|---------|-------------|---------|
| 9 × hole/line 2018-10-11* + 3 × lines/line 2018-10-10* | Pairs of swatches wrongly labeled as hole vs. lines; some were defect-free. These samples were excluded from both training and testing sets. | suspect cross label / suspect batch |
| hole/20180531* vs. lines/20180531* | The samples were reviewed and cleared as clean. | CLEAN |

**Table 3.5: Group-Aware Manifest and Dataset Split**

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Test fraction | 0.2 |
| Group-aware processing | Processed families and their dated shoots were never separated between train/test sets. |
| Training samples | 2,081 |
| Testing samples | 468 |
| Train/Test overlap | 0 |

---


## 3.2 Methodology & Design

Supervised YOLO detector + image processing is employed for segmentation of areas. Anomalies unknown beforehand are detected via few-shot anomaly branch (PatchCore/DINOv2, only good-fabric). Hours are estimated with Random Forest + XGBoost/MLP ablations. We smooth out Ds by employing rolling-average approach and seeded, group-aware splitting. Planner dashboard shows type, confidence level, Ds and hours. Key technologies: Python, Ultralytics YOLO, OpenCV, scikit-learn, Jetson-class edge with TensorRT.

### 3.2.1 Context Diagram

The context diagram shows how the system works with things like the fabric camera, manufacturing data and the planner or inspector.

**Figure 3.1: Context Diagram (Level 0)**

### 3.2.2 Proposed System Diagram

The system combines fabric defect detection scoring the defects and predicting production lead-time into one process. It takes in fabric inspection data. Gives out results, for production planning.

**Figure 3.2: Proposed System Diagram**

### 3.2.3 Architectural Design

The architectural design shows the parts of the fabric defect detection and lead-time prediction system and how the different parts talk to each other.

**Figure 3.3: Architectural Design of the Proposed System**

### 3.2.4 Use Case Diagram

The use case diagram shows how the users interact with the system. It shows what the inspector, the production planner and other users do.

**Figure 3.4: Use Case Diagram of the Proposed System**

### 3.2.5 System Workflow

The system workflow explains the steps that the system follows starting with a fabric image being put in and then going through defect detection scoring the defects and predicting the lead-time for production.

**Figure 3.5: System Workflow of the Proposed System**

### 3.2.6 Metadata Bridge

The metadata bridge links the defect detection results to the production lead-time prediction part. The defects that are found are turned into defect area and Defect Density Score (Ds) which helps predict how long production will take.

**Figure 3.6: Metadata Bridge for Defect Density Score and Lead-Time Prediction**

### 3.2.7 Machine Learning Pipeline

The machine learning pipeline shows how the features from manufacturing and defects are handled and sent to the Random Forest regression model to guess how long production will take.

**Figure 3.7: Machine Learning Pipeline for Lead-Time Prediction**

### 3.2.8 Four-Point Inspection Grading Logic

The four-point inspection grading logic decides the quality grade of a fabric roll by looking at the size of the defects and the points that are taken off for each.

**Figure 3.8: Four-Point Inspection Grading Logic**

---


**Table 3.6: Main Project Modules**

- config.py
- defect detection.py
- metadata bridge.py
- lead time predictor.py
- integration.py
- scripts/ (inventory, resplit, metrics, reproduce)
- src/metrics.py

**Table 3.7: Project Plan**

| Stage | Schedule / Status |
|-------|-------------------|
| Audit / Split | Completed |
| Reproduction | Weeks 1–2 |
| Segmentation | Weeks 3–10 |
| Anomaly Detection | Weeks 8–14 |
| Lead-Time Planning | Weeks 12–18 |
| Edge Deployment | Weeks 16–24 |
| Testing and Evaluation | Weeks 24–28 |
| Documentation and Write-up | Weeks 24–32 |

**Table 3.8: Task Allocation**

| Team Member | Assigned Tasks |
|-------------|----------------|
| Nafiz Imtiaz Labib | Dataset collection, dataset audit, duplicate removal, quarantine validation, dataset split preparation, edge deployment setup, edge model validation, final evaluation preparation, and camera stream input pipeline |
| Azahin | YOLO environment setup, baseline reproduction, YOLO model training and evaluation, defect segmentation, bounding box and mask comparison, Random Forest model, XGBoost and MLP comparison, model export and quantization |
| Riya | Project planning and management, requirement analysis, literature review, dataset documentation, image preprocessing pipeline, report writing, technical documentation, figure and diagram preparation, and project review |
| Fahim Ferdous Niloy | Defect Density Score (Ds) calculation, rolling average implementation, metadata bridge development, lead-time feature preparation, planner dashboard design, and dashboard implementation |
| Mohammed Amin | Few-shot anomaly detection, anomaly model testing, normal sample preparation, DINOv2 feature extraction evaluation, PatchCore memory bank optimization, anomaly threshold calibration, anomaly heatmap visualization, YOLO–anomaly output fusion, and inference pipeline API development |
| Murad | Testing strategy, functional testing, performance testing, integration testing, and result analysis |

### 3.2.9 Project Task Allocation

The project task allocation chart shows the project activities, the people who are responsible for them and the schedule for the project.

**Figure 3.9: Project Task Allocation Gantt Chart**

### 3.2.10 Summary

The requirements, audited data, modularity, and diagrams are all fixed. All numbers are based on a runnable manifest.

---

# Chapter 4 — Implementation and Results

*[Must be present in Final Report. Incomplete version might be included in FYDP-1 Report, however it is optional.]*

Every chapter should start with 1-2 sentences on the outline of the chapter.

## 4.1 Environment Setup

## 4.2 Testing and Evaluation

## 4.3 Results and Discussion

## 4.4 Summary

---


# Chapter 5 — Standards and Design Constraints

## 5.1 Standards and Design Constraints

The proposed system follows relevant software, hardware, and communication standards to ensure reliable, maintainable, compatible, and efficient operation. These standards and technologies are selected based on the system requirements, real-time processing needs and practical industrial deployment. Different alternatives are also considered based on their advantages, disadvantages and sustainability for the proposed system.

### 5.1.1 Software Standard

The Software Standard will utilize packages, centralized configuration, version control system, reviewable manifests, deterministic training seeding, COCO/YOLO interchange format, and ISO/IEC-style documentation.

### 5.1.2 Hardware Standard

The Hardware Standard needs fixed geometry calibration for grading purposes, a Jetson-class edge computing machine with TensorRT, and factory safe power envelope.

### 5.1.3 Communication Standard

The Communication Standard is REST-based. Files are transferred to MES via RESTful API.

## 5.2 Design Constraints

The proposed system is subject to several design constraints related to cost, environment, ethics, health and safety, social factors, political requirements and sustainability. These constraints influence the selection of hardware, software, datasets, processing methods and deployment strategies.

### 5.2.1 Economic Constraint

The cost of software is none, the benefit would come in form of reduction of DHU or chargeback expenses in 2 to 3 years from now, depending on the outcome of the experiment.

### 5.2.2 Environmental Constraint

The training requires less data and utilizes low energy at the edge, reducing defective shipments.

### 5.2.3 Ethical Constraint

The cameras face fabric and not people, the wrong labels will be corrected not overlooked, the data obtained in planning will be labeled till the factory data takes over.

### 5.2.4 Health and Safety Constraint

The system is enclosed, and that helps to reduce the eye strain.

### 5.2.5 Social Constraint

The labels are in Bangla language and the inspectors will be trained to become supervisors.

### 5.2.6 Political Constraint

None needed. Manufacturability Cost: Computer exists; data gathering is easy; camera and mount is moderate; Jetson is moderate; Deployment is moderate; Maintenance is moderate.

### 5.2.7 Sustainability

Open format is used, the script is maintainable, the dataset is scalable.

## 5.3 Cost Analysis

The proposed unified fabric defect detection and production lead-time prediction system requires resources for dataset preparation, software development, model training, testing, camera based inspection and development. The estimated development budget is BDT 16,000.

The project emphasizes open-source software and existing computing resources to keep the overall cost within available budget.

**Table 5.1: Estimated Project Budget**

| Cost Category | Estimated Cost (BDT) |
|---------------|---------------------:|
| Dataset preparation and auditing | 2,000 |
| Camera and image acquisition resources | 4,000 |
| Computing and development resources | 3,000 |
| Testing and integration | 2,000 |
| Edge deployment and hardware-related resources | 3,000 |
| Documentation and presentation | 1,000 |
| Miscellaneous expenses | 1,000 |
| **Total** | **16,000** |

---


## 5.4 Complex Engineering Problem

The development and evaluation of the proposed unified fabric defect detection and production lead-time prediction system represents a complex engineering problem that goes beyond standard software development. The project combines computer vision, image processing, machine learning, and edge development to develop an integrated solution for industrial fabric inspection and production planning. The main challenge is not only to develop individual machine learning models, but also to integrate multiple components into a reliable and efficient pipeline. The system must balance detection accuracy, real-time processing speed, edge computing limitations, data quality and production planning requirements. The system also needs to handle heterogeneous fabric images, noisy labels, different defect types and previously unseen defects.

### 5.4.1 Complex Problem Solving

**Table 5.2: Mapping with Complex Problem Solving**

| Criterion | Description | Satisfied |
|-----------|-------------|:---------:|
| P1 | Depth of Knowledge | ✓ |
| P2 | Range of Conflicting Requirements | ✓ |
| P3 | Depth of Analysis | ✓ |
| P4 | Familiarity of Issues | ✗ |
| P5 | Extent of Applicable Codes | ✗ |
| P6 | Extent of Stakeholder Involvement | ✓ |
| P7 | Interdependence | ✓ |

**P1: Depth of Knowledge** — Developing the proposed system requires knowledge from several specialized areas, including computer vision, image processing, deep learning, anomaly detection, machine learning, and production planning. The project involves YOLO-based defect detection, image segmentation, defect area measurement, few-shot anomaly detection using PatchCore/DINOv2, and Random Forest-based lead-time prediction. The system also requires knowledge of edge computing and real-time deployment using Jetson-class hardware and TensorRT. Integrating these different technical areas into a single working system requires knowledge beyond basic programming and therefore satisfies the criterion of Depth of Knowledge.

**P2: Range of Conflicting Requirements** — The proposed system involves several conflicting requirements. High defect detection accuracy must be balanced with real-time processing requirements and limited edge computing resources. Increasing model complexity may improve accuracy but can increase computational requirements and reduce processing speed. Similarly, the system must balance the accuracy of the Defect Density Score (Ds) and lead-time prediction with the availability and quality of manufacturing data. These trade-offs require careful engineering decisions and demonstrate a range of conflicting requirements.

**P3: Depth of Analysis** — The project requires detailed analysis of heterogeneous fabric images, defect classes, duplicate samples, quarantined samples, and grouping. It involves performance analysis of detection models using metrics such as mAP and evaluation of lead-time prediction using MAE, RMSE, and R2.

### 5.4.2 Engineering Activities

**Table 5.3: Mapping with Complex Engineering Activities**

| Criterion | Description | Satisfied |
|-----------|-------------|:---------:|
| A1 | Range of Resources | ✓ |
| A2 | Level of Interaction | ✓ |
| A3 | Innovation | ✓ |
| A4 | Consequences for Society and Environment | ✓ |
| A5 | Familiarity | ✓ |

**A4: Consequences for Society and Environment** — The proposed system is intended to improve fabric quality inspection and production planning in textile manufacturing. Improved defect identification can help reduce defective production and unnecessary material waste. More reliable production-time estimation can also support better production planning and delivery management.

**A5: Familiarity** — The project uses both established and advanced technologies. Established tools such as Python, OpenCV, scikit-learn, and machine learning algorithms are combined with YOLO-based detection, few-shot anomaly detection, and edge deployment technologies. Although individual technologies are well established, their integration into a unified fabric inspection and production planning system requires understanding of their limitations and interactions.

## 5.5 Summary

This chapter presented the relevant standards, design constraints, estimated project cost, and complex engineering aspects of the proposed system. The project requires the integration of computer vision, machine learning, anomaly detection, production planning, and edge computing technologies. The system also involves conflicting requirements related to accuracy, processing speed, computational resources, and practical industrial deployment.

---


# Chapter 6 — Conclusion

## 6.1 Summary

The project has established the design and methodological foundation for a unified fabric defect detection and production lead-time prediction system.

## 6.2 Project Plan

The project follows a staged development plan in which dataset preparation and system design are followed by model development, integration, testing, and documentation.

The overall project sequence is: **Analysis → Design → Group-aware Re-evaluation → YOLOv11-seg + Mask-Ds → Anomaly Branch → Factory-log Planning → Edge + Four-point Integration → Thesis and Paper**

The planned timeline is shown in Figure 3.9 (Project Task Allocation Gantt Chart).

## 6.3 Future Work

The future work includes renaming quarantine with a pHash sweep, collecting roll-id-disciplined v2 factory data, developing a Bangla dashboard, benchmarking on Isl-Knit and FabricSpotDefect, and submitting the work to a conference. Public fabric-defect datasets such as Isl-Knit and FabricSpotDefect have been introduced for evaluating automated textile inspection systems [7, 8].

**Table 6.1: Pilot Reference and Upper Bound**

| Metric | Reference / Target |
|--------|-------------------|
| Class accuracy (random split) | 98% |
| Reference preparation time | 5.44 hours |
| MAE improvement (synthetic) | 92.0% |
| Horizontal → Hole | 8% |
| Hole → Horizontal | 7% |

### 6.3.1 Dataset Expansion

The current pilot dataset should be expanded using real factory data. Future data collection should include properly documented roll IDs, fabric groups, production conditions, and defect annotations. A larger and more diverse dataset would help the system handle different fabric textures, lighting conditions, machine settings, and defect appearances.

The quarantined images can also be reviewed again using perceptual hashing and manual verification. This may allow valid samples to be recovered while maintaining strict dataset integrity.

### 6.3.2 Real Factory Production Logs

The lead-time prediction component should be trained and evaluated using real factory production records. Future datasets should contain actual machine speed, order quantity, production start and completion times, defect information, and other relevant manufacturing variables. This would allow the relationship between fabric quality and production time to be evaluated using real observations rather than relying primarily on synthetic planning data.

### 6.3.3 Improved Defect Segmentation

Future work should further investigate YOLOv11-seg and other segmentation architectures for accurate defect localization. Instance segmentation methods provide more detailed defect boundaries compared with bounding-box-based detection approaches [1]. The effect of different image resolutions, lighting conditions, augmentation methods, and model sizes should also be evaluated.

### 6.3.4 Few-shot Anomaly Detection

The anomaly detection branch can be extended using PatchCore, DINOv2-based methods, AnomalyDINO, or other few-shot approaches [3, 4]. This branch is particularly important for defects that are not represented in the six known classes. Future experiments should measure how effectively the anomaly branch identifies previously unseen defects while maintaining acceptable false-positive rates.

---


### 6.3.5 Bangla Planner Dashboard

A future version of the system can include a Bangla-language planner dashboard. The dashboard can display:

- Defect type;
- Detection confidence;
- Defect Density Score (Ds);
- Predicted production hours;
- Four-point inspection grade;
- Anomaly score; and
- Production status.

This would make the system easier to use for local factory inspectors and production planners.

### 6.3.6 Edge Deployment and Real-time Optimization

Future work should evaluate the complete system on Jetson-class hardware under realistic factory conditions. Previous studies have investigated lightweight deep learning models for real-time edge deployment using NVIDIA Jetson devices [10]. Quantization, pruning, and suitable input resolutions can be investigated to improve inference speed while maintaining acceptable detection performance.

The target is to achieve real-time processing of at least 15 FPS on the intended edge platform.

### 6.3.7 Benchmarking and Publication

The proposed system can be benchmarked against relevant fabric-defect datasets and existing methods, including Isl-Knit and FabricSpotDefect [7, 8]. After sufficient experimental validation, the findings can be prepared for submission to a suitable conference or journal.

## 6.4 Limitations and Final Remarks

The pilot localization is estimated, not measured; the planned labels are synthetic and circular; 1,994 files have no group id hence the honest split is partial; there are sparse classes; validation at an industrial scale is not done yet. The framework, however, demonstrates that defect detection and production planning can coexist in a single intelligent system – a practical approach to automated fabric quality control.

## 6.5 Final Conclusion

The project has established the design and methodological foundation for a unified fabric defect detection and production lead-time prediction system. The proposed architecture addresses the gap between quality inspection and production planning by using the Defect Density Score (Ds) as a bridge between the computer-vision and machine-learning components.

The audited dataset, group-aware evaluation strategy, YOLO-based detection, segmentation-based area measurement, anomaly detection branch, Random Forest lead-time prediction, four-point inspection logic, and edge deployment strategy together form the major components of the proposed system.

The final system is intended to provide useful information to both fabric inspectors and production planners by presenting defect information together with an estimated production time. Future validation with real factory data will be essential for determining the practical performance and reliability of the complete framework.

---

# Bibliography

[1] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You only look once: Unified, real-time object detection," in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 2016.

[2] M. Mao et al., "Yolov1–yolov11: A review for fabric defect detection," 2025.

[3] K. Roth, L. Pemula, J. Zepeda, B. Schölkopf, T. Brox, and P. Gehler, "Towards total recall in industrial anomaly detection," in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 2022.

[4] S. Damm et al., "Anomalydino: Few-shot anomaly detection with vision foundation models," in *Proceedings of the IEEE Winter Conference on Applications of Computer Vision*, 2025.

[5] Anonymous, "Patchead: Patch-based efficient anomaly detection," 2025.

[6] L. Breiman, "Random forests," *Machine Learning*, vol. 45, pp. 5–32, 2001.

[7] A. D. Gupta et al., "Isl-knit: A fabric defect dataset," *Heliyon*, vol. 10, no. 17, 2024.

[8] F. Islam et al., "Fabricspotdefect: A fabric defect dataset," *Data in Brief*, 2024.

[9] A. Kumar, "Vision-based fabric defect detection: A survey," *IEEE Transactions on Industrial Electronics*, vol. 55, 2008.

[10] S. Song et al., "Efficientdet-based object detection on nvidia jetson tx2," 2021.

[11] D. P. Kulugammana et al., "Fabric wastage prediction using machine learning," in *Proceedings of CIIS*, 2024.

