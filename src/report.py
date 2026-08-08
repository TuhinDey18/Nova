import os
import json
from datetime import datetime


class ReportGenerator:

    def __init__(self):
        pass

    def generate(self, query_image, associations):

        report = {}

        report["case_id"] = (
            "CASE_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        report["generated_at"] = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        report["query_image"] = query_image

        report["matches"] = len(associations)

        report["association_count"] = len(
            set(
                event["association_id"]
                for event in associations
            )
        )

        report["cameras"] = sorted(
            set(
                event["camera"]
                for event in associations
            )
        )

        report["journey"] = associations

        # -----------------------------
        # Investigation Summary
        # -----------------------------
        if associations:

            total_duration = sum(
                event["duration"]
                for event in associations
            )

            first = min(
                associations,
                key=lambda x: x["start_seconds"]
            )

            last = max(
                associations,
                key=lambda x: x["end_seconds"]
            )

            best = max(
                associations,
                key=lambda x: x["score"]
            )

            report["summary"] = {

                "total_tracking_time": round(
                    total_duration,
                    2
                ),

                "first_camera": first["camera"],

                "first_time": first["start"],

                "last_camera": last["camera"],

                "last_time": last["end"],

                "highest_similarity": round(
                    best["score"],
                    4
                )

            }

        else:

            report["summary"] = {

                "total_tracking_time": 0,

                "first_camera": None,

                "first_time": None,

                "last_camera": None,

                "last_time": None,

                "highest_similarity": 0

            }

        return report

    def print_report(self, report):

        print("\n")
        print("=" * 80)
        print("                 E.C.H.O. INVESTIGATION REPORT")
        print("=" * 80)

        print(f"Case ID          : {report['case_id']}")
        print(f"Generated At     : {report['generated_at']}")
        print(f"Query Image      : {report['query_image']}")
        print(f"Total Matches    : {report['matches']}")
        print(f"Associations     : {report['association_count']}")

        print("\nCameras Visited")
        print("-" * 80)

        for camera in report["cameras"]:
            print(f"• {camera}")

        summary = report["summary"]

        print("\nInvestigation Summary")
        print("-" * 80)

        print(
            f"Total Cameras Visited : {len(report['cameras'])}"
        )

        print(
            f"Total Associations    : {report['association_count']}"
        )

        print(
            f"Total Matches         : {report['matches']}"
        )

        print(
            f"Total Tracking Time   : {summary['total_tracking_time']} sec"
        )

        print()

        print(
            f"First Appearance      : {summary['first_camera']}"
        )

        print(
            f"Time                  : {summary['first_time']}"
        )

        print()

        print(
            f"Last Appearance       : {summary['last_camera']}"
        )

        print(
            f"Time                  : {summary['last_time']}"
        )

        print()

        print(
            f"Highest Similarity    : {summary['highest_similarity']}"
        )

        print("\nJourney")
        print("-" * 80)

        for event in report["journey"]:

            print(f"Association ID : {event['association_id']}")
            print(f"Camera         : {event['camera']}")
            print(f"Track ID       : {event['track_id']}")
            print(f"Class          : {event['class']}")
            print(f"Appeared       : {event['start']}")
            print(f"Left           : {event['end']}")
            print(f"Duration       : {event['duration']} sec")
            print(f"Frames         : {event['frames']}")
            print(f"Similarity     : {event['score']:.4f}")
            print(f"Representative : {event['crop']}")
            print("-" * 80)

        print("End of Report")
        print("=" * 80)

    def save_report(self, report):

        os.makedirs("reports", exist_ok=True)

        filename = report["case_id"] + ".json"

        filepath = os.path.join(
            "reports",
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(f"\nReport successfully saved to:\n{filepath}")