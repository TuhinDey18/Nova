import os
import cv2


class Cropper:

    def __init__(self, output_folder="crops"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def save_crop(
        self,
        frame,
        class_name,
        track_id,
        frame_number,
        x1,
        y1,
        x2,
        y2
    ):

        # Create class folder automatically
        class_folder = os.path.join(self.output_folder, class_name)
        os.makedirs(class_folder, exist_ok=True)

        # Keep coordinates inside image boundaries
        h, w = frame.shape[:2]

        x1 = max(0, min(x1, w - 1))
        y1 = max(0, min(y1, h - 1))
        x2 = max(0, min(x2, w))
        y2 = max(0, min(y2, h))

        if x2 <= x1 or y2 <= y1:
            return None

        crop = frame[y1:y2, x1:x2]

        if crop.size == 0:
            return None

        filename = f"{track_id}_{frame_number}.jpg"

        filepath = os.path.join(class_folder, filename)

        cv2.imwrite(filepath, crop)

        return filepath