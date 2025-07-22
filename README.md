# NAST Earthquake Data Downloader

## 1) Project Title  
**NAST PROJECT - Automated Downloading and Local Storage of Earthquake Data**

---

## 2) Description  
This project automates downloading earthquake data from USGS and stores it locally for further processing.  
It provides a **Command-Line Interface (CLI)** for easy interaction and management of earthquake data.

The entire project is containerized using Docker for easy deployment and consistency across environments. Version control is handled with Git.

---

## 3) Features  
- Automated downloading of earthquake data from USGS  
- Local storage and management of earthquake event data  
- Simple CLI interface for data operations  
- Fully containerized with Docker for easy setup  
- Git for version control and collaboration  

---

## 4) Prerequisites  
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)  
- Python 3.10+ (if running without Docker)  
- Git (for cloning and version control)

---

## 5) Installation & Setup

### Option 1: Using Docker Compose (Recommended)

1. Clone the Git repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Build and start the CLI service:
    ```bash
    docker-compose up --build cli
    ```

3. The CLI will run inside the container to download and manage earthquake data.

4. To stop the container:
    ```bash
    Ctrl+C
    docker-compose down
    ```

---

### Option 2: Running Locally without Docker

1. Clone the Git repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the CLI script locally:
    ```bash
    python cli/cli_view.py
    ```

---

## 6) Usage

Run the CLI script to download and manage earthquake data:

```bash
python cli/cli_view.py
```

## 7) Version Control

The project uses **Git** for source control. Make sure Git is installed to clone and manage the repository.

---

## 8) Notes

- This project focuses on **automated local downloading and storage of earthquake data** using a CLI.  
- Docker ensures the application runs consistently regardless of the local environment.  
- The web application has been removed to focus solely on CLI-based data downloading.
