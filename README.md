# CloudCacheOptimizer
### AI-Based Intelligent Cache Optimizer for Cloud Storage

## 1. Introduction
CloudCacheOptimizer is a Python-based project that aims to improve file retrieval performance using intelligent caching techniques. It combines local file caching with an AI-based cache replacement strategy to reduce repeated access to remote storage.

## 2. Problem Statement
Retrieving files repeatedly from cloud storage can increase retrieval time, network usage, and storage requests. Traditional cache replacement algorithms may not always make the best decisions about which files should remain in the cache.

## 3. Objectives
- Reduce file retrieval time.
- Minimize repeated access to remote storage.
- Improve cache hit rate.
- Implement an AI-based cache replacement strategy.
- Compare AI caching with traditional LRU and FIFO algorithms.

## 4. Technologies Used
- **Programming Language:** Python
- **Backend Framework:** Flask
- **Machine Learning:** Random Forest
- **Libraries:** Scikit-learn, Joblib, Requests, Cachetools
- **Development Environment:** PyCharm and Anaconda

## 5. Main Features
- File upload and retrieval through API endpoints.
- Local file caching.
- AI-based cache replacement.
- Cache performance statistics.
- Comparison of AI, LRU, and FIFO caching strategies.
- Dashboard for monitoring cache performance.

## 6. Cache Strategies
- **LRU (Least Recently Used):** Removes the least recently accessed file.
- **FIFO (First In First Out):** Removes the file that entered the cache first.
- **AI Cache:** Uses a machine learning model to estimate the likelihood of future file reuse and help make cache replacement decisions.

## 7. Project Status
The local caching system, Flask API, AI-based caching strategy, and workload testing have been implemented.

Cloud storage integration is planned as a future enhancement.

## 8. How to Run the Project
1. Install Python and the required project dependencies.
2. Open the project folder in PyCharm.
3. Activate the project's Python environment.
4. Run `api/app.py`.
5. Open `http://127.0.0.1:5000` in your browser.

## 9. Future Enhancements
- Integrate Google Drive or another cloud storage provider.
- Deploy the application on a cloud server.
- Improve AI prediction accuracy.
- Support larger files and multiple users.

## 10. Conclusion
CloudCacheOptimizer demonstrates how machine learning can be used to improve cache replacement decisions. It compares intelligent caching with traditional algorithms and provides a foundation for future cloud storage integration.
