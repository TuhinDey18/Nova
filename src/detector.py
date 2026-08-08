from database import EchoDatabase
from cropper import Cropper
from ultralytics import YOLO
from embedding import EmbeddingExtractor
from faiss_index import FaissIndex

import pandas as pd
import os
import cv2
import datetime


class Detector:

    def __init__(self, model_name="yolo11n.pt"):

        self.model = YOLO(model_name)

        self.embedder = EmbeddingExtractor()
        self.faiss = FaissIndex()

    def detect(
        self,
        video_path,
        camera_id="camera_1",
        confidence=0.4,
        save=True,
        show=False
    ):

        db = EchoDatabase()
        cropper = Cropper()

        cap = cv2.VideoCapture(video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps == 0:
            fps = 30

        cap.release()

        results = self.model.track(
            source=video_path,
            conf=confidence,
            save=save,
            show=show,
            stream=True,
            persist=True
        )

        detections = []

        for frame_number, result in enumerate(results):

            if frame_number % 3 != 0:
                continue

            frame = result.orig_img

            timestamp_seconds = frame_number / fps

            timestamp = str(
                datetime.timedelta(
                    seconds=timestamp_seconds
                )
            )

            if result.boxes is None:
                continue

            for box in result.boxes:

                cls = int(box.cls[0])
                class_name = self.model.names[cls]

                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                track_id = -1

                if box.id is not None:
                    track_id = int(box.id[0])

                crop_path = cropper.save_crop(
                    frame=frame,
                    class_name=class_name,
                    track_id=track_id,
                    frame_number=frame_number,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                )

                if crop_path is None:
                    continue

                embedding = self.embedder.extract(
                    crop_path
                )

                self.faiss.add(
                    embedding,
                    {
                        "camera_id": camera_id,
                        "video_path": video_path,
                        "track_id": track_id,
                        "frame": frame_number,
                        "timestamp": timestamp,
                        "timestamp_seconds": timestamp_seconds,
                        "class": class_name,
                        "confidence": round(conf, 3),
                        "crop_path": crop_path
                    }
                )

                detection = {
                    "camera_id": camera_id,
                    "video_path": video_path,
                    "frame": frame_number,
                    "timestamp": timestamp,
                    "timestamp_seconds": round(
                        timestamp_seconds,
                        3
                    ),
                    "track_id": track_id,
                    "class": class_name,
                    "confidence": round(conf, 3),
                    "crop_path": crop_path,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                }

                detections.append(detection)

                db.insert_detection(
                    camera_id=camera_id,
                    frame=frame_number,
                    timestamp=timestamp,
                    timestamp_seconds=timestamp_seconds,
                    track_id=track_id,
                    class_name=class_name,
                    confidence=conf,
                    crop_path=crop_path,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                )

        os.makedirs(
            "faiss",
            exist_ok=True
        )

        self.faiss.save(
            "faiss/faiss.index"
        )

        db.close()

        os.makedirs(
            "data",
            exist_ok=True
        )

        csv_path = (
            f"data/{camera_id}_detections.csv"
        )

        df = pd.DataFrame(
            detections
        )

        df.to_csv(
            csv_path,
            index=False
        )

        print(df.head())

        print(
            f"\nSaved {len(df)} detections."
        )

        print(
            f"CSV saved to: {csv_path}"
        )

        print(
            "SQLite database updated successfully."
        )

        print(
            "FAISS index saved successfully."
        )