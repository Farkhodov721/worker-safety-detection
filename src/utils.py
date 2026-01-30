"""
Utility functions for detection and visualization
"""

import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

def draw_boxes(frame, results, violations):
    """
    Draw bounding boxes on frame
    Green for safe, Red for violations
    """
    annotated_frame = frame.copy()
    
    boxes = results.boxes
    violation_classes = [v['class'] for v in violations]
    
    for box in boxes:
        # Get box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Get class info
        class_id = int(box.cls[0])
        class_name = results.names[class_id]
        confidence = float(box.conf[0])
        
        # Determine color (Red for violations, Green for safe)
        if class_name in violation_classes:
            color = (0, 0, 255)  # Red
            label = f"⚠️ {class_name} {confidence:.2f}"
        else:
            color = (0, 255, 0)  # Green
            label = f"✓ {class_name} {confidence:.2f}"
        
        # Draw box
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw label background
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(annotated_frame, (x1, y1 - 25), (x1 + label_size[0], y1), color, -1)
        
        # Draw label text
        cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Add timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.putText(annotated_frame, timestamp, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Add violation count if any
    if violations:
        violation_text = f"VIOLATIONS: {len(violations)}"
        cv2.putText(annotated_frame, violation_text, (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return annotated_frame

def save_violation_screenshot(frame, violations, output_dir):
    """Save screenshot of violation"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"violation_{timestamp}.jpg"
    output_path = Path(output_dir) / filename
    
    success = cv2.imwrite(str(output_path), frame)
    if success:
        print(f"📸 Screenshot saved: {output_path}")
        return str(output_path)
    else:
        print(f"❌ Failed to save screenshot: {output_path}")
        return None
