# CloudCacheOptimizer
### AI-Based Intelligent Cache Optimizer for Cloud Storage

## Introduction

CloudCacheOptimizer is a Python-based project designed to improve file retrieval performance using intelligent caching techniques. It combines Google Drive cloud storage, local file caching, and an AI-based cache replacement strategy to reduce repeated retrievals from remote storage.

The system uses a machine learning model to predict the possibility of future file reuse and supports intelligent cache replacement decisions.

## Problem Statement

Repeatedly retrieving files from remote cloud storage can increase retrieval time, network communication, and the number of cloud requests. Traditional cache replacement algorithms may not always identify which files are likely to be accessed again.

CloudCacheOptimizer addresses this problem through AI-assisted caching, which helps manage locally stored files based on predicted reuse.

## Objectives

- Reduce repeated file retrievals from cloud storage.
- Improve access to previously requested files through local caching.
- Implement an AI-assisted cache replacement strategy.
- Monitor cache performance using statistics.
- Compare AI caching with traditional LRU and FIFO algorithms.
- Integrate Google Drive as the remote storage provider.

## Technologies Used

- **Programming Language:** Python 3.11
- **Backend Framework:** Flask
- **Machine Learning:** Random Forest
- **Cloud Storage:** Google Drive
- **Libraries:** Scikit-learn, Joblib, Requests, Cachetools
- **Development Environment:** PyCharm and Anaconda

## Main Features

- File upload and download through Flask API endpoints.
- Google Drive integration for remote file storage.
- Local file caching.
- AI-assisted cache replacement.
- Cache hit and miss tracking.
- Cache performance statistics.
- Comparison of AI, LRU, and FIFO caching strategies.
- Dashboard for monitoring cache performance.

## Cache Replacement Strategies

**LRU (Least Recently Used):** Removes the file that has not been accessed for the longest time.

**FIFO (First In First Out):** Removes the file that entered the cache first.

**AI-Based Cache:** Uses a Random Forest machine learning model to estimate the possibility of future file reuse. The prediction helps calculate the value of retaining files in the cache.

## System Architecture

The application follows this general workflow:

User Request → Flask API → Local AI Cache → Google Drive (when the file is not cached) → Local Cache Storage → File Response.

## Project Implementation

The following components have been implemented:

- Flask API for file upload, download, and cache statistics.
- Google Drive integration for remote file storage.
- Local AI cache engine for managing retrieved files.
- Random Forest-based reuse prediction.
- Cache hit and miss tracking.
- Dashboard for displaying cache statistics.
- Workload testing for comparing cache replacement strategies.

## How to Run the Project

1. Install Python 3.11 and the required dependencies.
2. Clone or download this repository.
3. Open the project folder in PyCharm.
4. Configure the required Python environment.
5. Install the dependencies listed in the project requirements file, if provided.
6. Configure Google Drive API credentials and the project test folder as described in the project setup.
7. Run `api/app.py`.
8. Open `http://127.0.0.1:5000` in your browser.

**Note:** Google Drive integration requires valid API credentials and configuration. Do not upload private credentials or token files to GitHub.

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Displays application information |
| `/health` | Checks application status |
| `/objects/<filename>` (GET) | Downloads a file |
| `/objects/<filename>` (PUT) | Uploads a file |
| `/stats` | Displays cache statistics |
| `/dashboard` | Opens the cache monitoring dashboard |

## Future Enhancements

- Deploy the application on an actual cloud computing platform.
- Improve machine learning prediction accuracy.
- Support larger files and multiple users.
- Extend caching to website content and other data objects.
- Improve performance monitoring and visualization.

## Conclusion

CloudCacheOptimizer demonstrates the application of machine learning in cloud-based file caching. By integrating Google Drive with local caching and an AI-assisted replacement strategy, the system helps reduce repeated remote file retrievals.

The project provides a working prototype that demonstrates file upload, download, cache management, and performance monitoring. It also provides a foundation for further development and deployment in cloud computing environments.

## Project Repository

GitHub: https://github.com/kishorpkishorp64-beep/CloudCacheOptimizer