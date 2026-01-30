# 🏭 Worker Safety Detection System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An AI-powered worker safety detection system that monitors PPE (Personal Protective Equipment) compliance in factory environments using YOLOv8 object detection and sends real-time alerts via Telegram.

## 📋 Features

- 🎯 **Real-time PPE Detection**
  - Hard hats/Helmets
  - Safety vests
  - Safety glasses
  - Face masks
  
- 🚨 **Instant Telegram Alerts**
  - Automatic violation notifications
  - Screenshots with timestamp
  - Cooldown period to prevent spam
  
- 📹 **Video Processing**
  - Process video files frame by frame
  - Save annotated output videos
  - Violation screenshot capture
  
- ⚙️ **Configurable System**
  - YAML-based configuration
  - Adjustable confidence thresholds
  - Enable/disable specific PPE checks
  
- 📊 **Visualization**
  - Color-coded bounding boxes (Red: violation, Green: safe)
  - Real-time violation count
  - Timestamp overlay

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) CUDA-capable GPU for faster inference

### Step 1: Clone the Repository

```bash
git clone https://github.com/Farkhodov721/worker-safety-detection.git
cd worker-safety-detection
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- ultralytics (YOLOv8)
- opencv-python (Computer Vision)
- python-telegram-bot (Telegram alerts)
- PyTorch & torchvision (Deep Learning)
- And more...

## 📦 Download YOLOv8 Model

### Option 1: Use Pre-trained COCO Model (Quick Start)

For initial testing, download YOLOv8 nano model:

```bash
# The model will be automatically downloaded when you first run the script
# Or manually download:
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

Move the downloaded model to the `models/` directory:
```bash
mv yolov8n.pt models/
```

### Option 2: Custom Trained Model (Recommended for Production)

For accurate PPE detection, you'll need a custom-trained model. Training instructions:

1. Collect and label PPE dataset (helmets, vests, masks, glasses)
2. Train YOLOv8 model on your dataset
3. Place trained model in `models/` directory
4. Update `config/config.yaml` with model path

**Note:** The pre-trained COCO model won't detect PPE-specific classes. For production use, train a custom model with PPE dataset.

## 🤖 Telegram Bot Setup

### Step 1: Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the **Bot Token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Your Chat ID

1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Start a chat - it will show your Chat ID
3. Copy your **Chat ID** (looks like: `123456789`)

### Step 3: Configure the Bot

Edit `config/config.yaml`:

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN_HERE"  # Paste your bot token
  chat_id: "YOUR_CHAT_ID_HERE"      # Paste your chat ID
  enable_alerts: true
```

### Step 4: Test the Connection

```python
import asyncio
from src.alert import test_telegram_connection

# Test your Telegram setup
asyncio.run(test_telegram_connection("YOUR_BOT_TOKEN", "YOUR_CHAT_ID"))
```

If successful, you'll receive a test message in Telegram! ✅

## ⚙️ Configuration

Edit `config/config.yaml` to customize the system:

```yaml
# Detection settings
detection:
  model_path: "models/yolov8n.pt"
  confidence_threshold: 0.5  # Adjust detection sensitivity (0.0-1.0)
  
# Video settings
video:
  input_path: "data/videos/test.mp4"  # Path to your video
  save_output: true
  show_preview: false  # Set true to see real-time preview
  
# Alert settings
alerts:
  save_screenshots: true
  min_time_between_alerts: 5  # Seconds between alerts
```

## 🎯 Usage

### Basic Usage

1. Place your test video in `data/videos/` folder:
```bash
cp /path/to/your/video.mp4 data/videos/test.mp4
```

2. Run the detection:
```bash
python src/detect.py
```

3. Check outputs:
   - Annotated video: `output/videos/output_YYYYMMDD_HHMMSS.mp4`
   - Violation screenshots: `output/violations/`
   - Telegram alerts: Check your Telegram chat

### Custom Video Processing

```python
from src.detect import SafetyDetector

detector = SafetyDetector('config/config.yaml')
detector.process_video('data/videos/custom_video.mp4')
```

### Testing with Jupyter Notebook

Open `notebooks/testing.ipynb` for interactive testing:

```bash
jupyter notebook notebooks/testing.ipynb
```

## 📁 Project Structure

```
worker-safety-detection/
├── config/
│   └── config.yaml          # System configuration
├── data/
│   ├── videos/              # Input videos
│   ├── images/              # Input images
│   └── dataset/             # Training dataset (for custom models)
├── models/
│   └── yolov8n.pt          # YOLOv8 model weights
├── src/
│   ├── __init__.py
│   ├── detect.py           # Main detection script
│   ├── alert.py            # Telegram alert system
│   └── utils.py            # Helper functions
├── output/
│   ├── videos/             # Processed videos
│   └── violations/         # Violation screenshots
├── notebooks/
│   └── testing.ipynb       # Testing notebook
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## 🎨 How It Works

1. **Video Input**: System reads video frame by frame
2. **Detection**: YOLOv8 detects objects in each frame
3. **Classification**: Identifies PPE items and violations
4. **Annotation**: Draws bounding boxes (Green: safe, Red: violation)
5. **Alert**: Sends Telegram notification with screenshot if violation detected
6. **Output**: Saves annotated video and violation screenshots

### Detection Classes

**Violation Classes** (Red boxes):
- `no-helmet`
- `no-safety-vest`
- `no-mask`
- `no-safety-glasses`

**Compliant Classes** (Green boxes):
- `helmet`
- `safety-vest`
- `mask`
- `safety-glasses`
- `person`

## 📊 Example Output

### Console Output
```
Loading model from models/yolov8n.pt...
Processing video: data/videos/test.mp4
Frame 45: 2 violation(s) detected
📸 Screenshot saved: output/violations/violation_20240130_153042_123456.jpg
✅ Alert sent to Telegram
Frame 67: 1 violation(s) detected
📸 Screenshot saved: output/violations/violation_20240130_153044_789012.jpg

=== Detection Complete ===
Total frames processed: 300
Frames with violations: 15
Output saved to: output/videos/output_20240130_153042.mp4
```

### Telegram Alert Example
```
⚠️ **SAFETY VIOLATION DETECTED** ⚠️

🕒 Time: 2024-01-30 15:30:42
📍 Type: no-helmet, no-safety-vest
🔢 Count: 2 violation(s)

⚡ Immediate action required!
```

## 🔧 Troubleshooting

### Issue: "No module named 'ultralytics'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "Model not found"
**Solution:** Download YOLOv8 model and place in `models/` directory

### Issue: "Telegram alert failed"
**Solution:** 
- Check bot token and chat ID in `config/config.yaml`
- Ensure you started a chat with your bot
- Test connection using `test_telegram_connection()`

### Issue: "Video file not found"
**Solution:** Check video path in config.yaml and ensure file exists

### Issue: "CUDA out of memory"
**Solution:** 
- Use smaller model (yolov8n.pt instead of yolov8x.pt)
- Reduce video resolution
- Process fewer frames

### Issue: "Low detection accuracy"
**Solution:**
- Train custom model with PPE dataset
- Adjust confidence threshold in config
- Use higher quality input videos

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- [x] Project structure setup
- [x] YOLOv8 integration
- [x] Video processing
- [x] Telegram alerts
- [x] Configuration system

### Phase 2: Live Camera Support
- [ ] Real-time RTSP stream processing
- [ ] Multi-camera support
- [ ] Live dashboard

### Phase 3: Enhanced Features
- [ ] Custom PPE model training
- [ ] Database integration for violation logs
- [ ] Web-based dashboard
- [ ] Email alerts
- [ ] Zone-based detection
- [ ] Person tracking and identification

### Phase 4: Production Ready
- [ ] Docker containerization
- [ ] REST API
- [ ] Mobile app integration
- [ ] Advanced analytics
- [ ] Report generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Development Notes

### Adding New PPE Classes

1. Update `config.yaml` with new class names
2. Train model with new classes
3. No code changes needed - configuration-driven!

### Custom Alert System

To add email or SMS alerts, create new functions in `src/alert.py`:

```python
async def send_email_alert(email, subject, message):
    # Your email implementation
    pass
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection model
- [OpenCV](https://opencv.org/) - Computer vision library
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram API wrapper

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Contact: [Add your contact information]

---

**⚠️ Important Notes:**
- This is an MVP for testing and development
- Custom trained model required for production use
- Ensure compliance with privacy laws when using cameras
- Test thoroughly before deploying in production environment

**Made with ❤️ for Worker Safety**
