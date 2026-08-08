import os
import pickle


CASE_FOLDER = "cases/apartment_case_001"
METADATA_PATH = "faiss/metadata.pkl"


def main():

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    print(f"Loaded {len(metadata)} metadata entries.")

    video_map = {}

    for filename in os.listdir(CASE_FOLDER):

        if not filename.lower().endswith(".mp4"):
            continue

        camera_id = os.path.splitext(filename)[0]

        video_path = os.path.join(
            CASE_FOLDER,
            filename
        )

        video_map[camera_id] = video_path

    print("\nAvailable videos:")

    for camera_id, path in video_map.items():
        print(f"{camera_id} -> {path}")

    updated = 0
    missing = set()

    for info in metadata:

        camera_id = info.get("camera_id")

        if camera_id in video_map:

            info["video_path"] = video_map[camera_id]

            updated += 1

        else:

            missing.add(camera_id)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("\nMetadata updated successfully.")
    print(f"Updated entries: {updated}")

    if missing:

        print("\nWARNING: No video found for:")

        for camera_id in missing:
            print(f"- {camera_id}")

    else:

        print("Every detection has a video_path.")


if __name__ == "__main__":
    main()