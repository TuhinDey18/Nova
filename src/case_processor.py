import os
from detector import Detector


class CaseProcessor:

    def __init__(self):
        self.detector = Detector()

    def process_case(self, case_folder):

        videos = sorted([
            file
            for file in os.listdir(case_folder)
            if file.lower().endswith(".mp4")
        ])

        print(f"\nFound {len(videos)} videos.\n")

        for video in videos:

            video_path = os.path.join(case_folder, video)

            camera_id = os.path.splitext(video)[0]

            print("=" * 60)
            print(f"Processing {camera_id}")
            print("=" * 60)

            self.detector.detect(
                video_path=video_path,
                camera_id=camera_id
            )

        print("\nCase Finished.")