"""
Main detection script for worker safety monitoring
Detects PPE violations and triggers alerts
"""

import cv2
import yaml
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime, timedelta
import asyncio
from alert import send_violation_alert
from utils import draw_boxes, save_violation_screenshot

class SafetyDetector:
    def __init__(self, config_path='config/config.yaml'):
        """Initialize the safety detector with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Load YOLO model
        model_path = self.config['detection']['model_path']
        print(f"Loading model from {model_path}...")
        self.model = YOLO(model_path)
        
        # Setup output directories
        Path(self.config['video']['output_path']).mkdir(parents=True, exist_ok=True)
        Path(self.config['alerts']['screenshot_path']).mkdir(parents=True, exist_ok=True)
        
        # Alert cooldown tracking
        self.last_alert_time = None
        self.min_alert_interval = timedelta(seconds=self.config['alerts']['min_time_between_alerts'])
        
    def detect_violations(self, results):
        """Check detection results for safety violations"""
        violations = []
        violation_classes = self.config['violations']['violation_classes']
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                confidence = float(box.conf[0])
                
                if class_name in violation_classes and confidence > self.config['detection']['confidence_threshold']:
                    violations.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': box.xyxy[0].tolist()
                    })
        
        return violations
    
    def process_video(self, video_path=None):
        """Process video and detect safety violations"""
        if video_path is None:
            video_path = self.config['video']['input_path']
        
        print(f"Processing video: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer
        if self.config['video']['save_output']:
            output_path = Path(self.config['video']['output_path']) / f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frame_count = 0
        violation_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Run detection
            results = self.model(frame, conf=self.config['detection']['confidence_threshold'])
            
            # Check for violations
            violations = self.detect_violations(results)
            
            # Draw boxes on frame
            annotated_frame = draw_boxes(frame, results[0], violations)
            
            # Handle violations
            if violations:
                violation_count += 1
                print(f"Frame {frame_count}: {len(violations)} violation(s) detected")
                
                # Save screenshot
                if self.config['alerts']['save_screenshots']:
                    screenshot_path = save_violation_screenshot(
                        annotated_frame, 
                        violations,
                        self.config['alerts']['screenshot_path']
                    )
                
                # Send Telegram alert (with cooldown)
                if self.config['telegram']['enable_alerts']:
                    current_time = datetime.now()
                    if self.last_alert_time is None or (current_time - self.last_alert_time) > self.min_alert_interval:
                        asyncio.run(send_violation_alert(
                            self.config['telegram']['bot_token'],
                            self.config['telegram']['chat_id'],
                            screenshot_path,
                            violations
                        ))
                        self.last_alert_time = current_time
            
            # Save output video
            if self.config['video']['save_output']:
                out.write(annotated_frame)
            
            # Show preview (optional)
            if self.config['video']['show_preview']:
                cv2.imshow('Safety Detection', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        # Cleanup
        cap.release()
        if self.config['video']['save_output']:
            out.release()
        cv2.destroyAllWindows()
        
        print(f"\n=== Detection Complete ===")
        print(f"Total frames processed: {frame_count}")
        print(f"Frames with violations: {violation_count}")
        print(f"Output saved to: {output_path if self.config['video']['save_output'] else 'Not saved'}")

def main():
    """Main entry point"""
    detector = SafetyDetector()
    detector.process_video()

if __name__ == "__main__":
    main()
