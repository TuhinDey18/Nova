from collections import defaultdict


class InvestigationEngine:

    def __init__(self):
        pass

    def group_tracks(self, results):

        tracks = defaultdict(list)

        for result in results:

            info = result["info"]

            key = (
                info["camera_id"],
                info["track_id"]
            )

            tracks[key].append(result)

        grouped = []

        for (camera_id, track_id), detections in tracks.items():

            detections.sort(
                key=lambda x: x["info"]["frame"]
            )

            first = detections[0]
            last = detections[-1]

            representative = max(
                detections,
                key=lambda x: x["score"]
            )

            grouped.append({

                "camera_id": camera_id,

                "video_path": representative["info"]["video_path"],

                "track_id": track_id,

                "class": representative["info"]["class"],

                "start_frame": first["info"]["frame"],

                "end_frame": last["info"]["frame"],

                "start_timestamp": first["info"]["timestamp"],

                "end_timestamp": last["info"]["timestamp"],

                "start_seconds": first["info"]["timestamp_seconds"],

                "end_seconds": last["info"]["timestamp_seconds"],

                "frames": len(detections),

                "score": representative["score"],

                "crop": representative["info"]["crop_path"]

            })

        grouped.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return grouped

    def build_timeline(self, tracks):

        timeline = []

        for track in tracks:

            duration = round(
                track["end_seconds"] -
                track["start_seconds"],
                2
            )

            timeline.append({

                "camera": track["camera_id"],

                "video_path": track["video_path"],

                "track_id": track["track_id"],

                "class": track["class"],

                "start": track["start_timestamp"],

                "end": track["end_timestamp"],

                "start_seconds": track["start_seconds"],

                "end_seconds": track["end_seconds"],

                "duration": duration,

                "frames": track["frames"],

                "score": track["score"],

                "crop": track["crop"]

            })

        timeline.sort(
            key=lambda x: x["start_seconds"]
        )

        return timeline

    def reconstruct_journey(self, timeline):

        sorted_timeline = sorted(
            timeline,
            key=lambda x: x["start_seconds"]
        )

        journey = []

        visited_cameras = set()

        for event in sorted_timeline:

            camera = event["camera"]

            if camera in visited_cameras:
                continue

            visited_cameras.add(camera)

            journey.append(event)

        return journey

    def associate_tracks(self, journey, similarity_threshold=0.70):

        associations = []

        association_id = 1

        for event in journey:

            if len(associations) == 0:

                event["association_id"] = association_id

            else:

                previous = associations[-1]

                if event["score"] >= similarity_threshold:

                    event["association_id"] = previous["association_id"]

                else:

                    association_id += 1

                    event["association_id"] = association_id

            associations.append(event)

        return associations