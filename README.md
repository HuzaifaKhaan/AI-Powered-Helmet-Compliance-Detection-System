# AI-Powered Helmet Compliance Detection System

![work4](https://github.com/user-attachments/assets/b78249b9-4cf0-478a-84d7-a8538639e4e0)


## Overview
The AI-Powered Helmet Compliance Detection System is designed to enhance safety measures by ensuring that individuals are wearing helmets. Utilizing the YOLOv5 model for object detection, this system can accurately identify whether a person is wearing a helmet or not. The project is deployed using Flask, providing a simple web interface for real-time detection.

## Features
- Real-time helmet detection using YOLOv5
- Easy-to-use web interface built with Flask
- High accuracy and fast processing
- Scalable and flexible architecture

## Tech Stack
- **Machine Learning:** YOLOv5
- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Docker (optional)

## Installation

### Prerequisites
- Python 3.7+
- Flask
- PyTorch
- OpenCV
- YOLOv5

### Steps
1. **Clone the Repository**
    ```bash
    git clone https://github.com/your_username/helmet-compliance-detection.git
    cd helmet-compliance-detection
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download YOLOv5 Weights**
    Download the YOLOv5 weights from the [official YOLOv5 repository](https://github.com/ultralytics/yolov5) or directly via:
    ```bash
    wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt -O yolov5s.pt
    ```

4. **Run the Flask App**
    ```bash
    export FLASK_APP=app.py
    flask run
    ```
    Access the app at `http://127.0.0.1:5000`

## Screenshots
![saved_frame](https://github.com/user-attachments/assets/ccfe5dbd-da76-4892-a11f-e28211b3109d)


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [YOLOv5 by Ultralytics](https://github.com/ultralytics/yolov5)
- Flask Web Framework
- OpenCV

## Contact
For any inquiries or support, please contact.

<div>
  <a href="https://www.linkedin.com/in/huzaifa-khaan/">
    <img src="https://img.shields.io/badge/LinkedIn-Huzaifa%20Khan-blue?logo=linkedin" alt="LinkedIn">
  </a>
  <a href="mailto:huzukham14@gmail.com">
    <img src="https://img.shields.io/badge/Email-huzaifa%40example.com-red?logo=gmail" alt="Email">
  </a>
</div>


