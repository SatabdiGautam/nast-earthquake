# NAST Earthquake Visualization

## 1) Project Title  
**NAST Earthquake Visualization**

---

## 2) Description  
This project provides tools to download and visualize earthquake data via two interfaces:

- A simple **Command-Line Interface (CLI)**
- A lightweight **Web Application** powered by Flask

It demonstrates earthquake data visualization techniques and is fully containerized for easy deployment using Docker and Docker Compose.

---

## 3) Features  
- Visualize earthquake data in real-time  
- CLI-based interaction for quick tasks  
- Web-based interface accessible via browser  
- Dockerized environment for simplified setup and deployment

---

## 4) Prerequisites  
- [Docker](https://docs.docker.com/get-docker/) (for containerized deployment)  
- Python 3.10+ (if running without Docker)  

---

## 5) Installation & Setup

### Option 1: Using Docker Compose (Recommended)

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Build and start the services:
    ```bash
    docker-compose up --build
    ```

3. Access the web app by opening [http://localhost:3000](http://localhost:3000) in your browser.

4. To stop the containers, press `Ctrl+C` and then run:
    ```bash
    docker-compose down
    ```

### Option 2: Running Locally without Docker

1. Ensure Python 3.10+ is installed.

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the web app:
    ```bash
    python webapp/app.py
    ```

4. Access the web app at [http://localhost:3000](http://localhost:3000).

---

## 6) Usage

### CLI Interface

Run the CLI script to interact via command line:
```bash
python cli/cli_view.py
