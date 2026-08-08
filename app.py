import os
import sys
import tempfile
import json
import re
from pathlib import Path

import streamlit as st

sys.path.append("src")

from search import SearchEngine
from investigation import InvestigationEngine
from report import ReportGenerator
from assistant import InvestigationAssistant
from llm import OllamaLLM


st.set_page_config(
    page_title="NOVA | Investigation Console",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path("styles/style.css")

if css_path.exists():
    css = css_path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )
else:
    st.warning("styles/style.css not found.")



@st.cache_resource
def load_backend():
    return (
        SearchEngine(),
        InvestigationEngine(),
        ReportGenerator(),
    )


search_engine, investigation, report_generator = load_backend()

llm = OllamaLLM(model="llama3.2")
assistant = InvestigationAssistant(llm)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "report" not in st.session_state:
    st.session_state.report = None

if "video_request" not in st.session_state:
    st.session_state.video_request = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">N.O.V.A.</div>
        <div class="sidebar-subtitle">INVESTIGATION CONSOLE</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Case")

    if st.session_state.report:
        report = st.session_state.report

        st.markdown(
            f"""
            <div class="sidebar-case">Case ID</div>
            <div class="sidebar-case-id">{report['case_id']}</div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()
        st.metric("Detections", report["matches"])
        st.metric("Cameras", len(report["cameras"]))
        st.metric("Associations", report["association_count"])

        st.markdown("### Camera Network")
        for camera in report["cameras"]:
            st.markdown(f"📍 `{camera}`")

        st.divider()

        st.download_button(
            "⬇ Export Investigation",
            json.dumps(report, indent=4),
            file_name=f"{report['case_id']}.json",
            mime="application/json",
            use_container_width=True,
        )
    else:
        st.caption("No active investigation.")

    st.divider()
    st.caption("N.O.V.A. v1.0")
    st.caption("AI Surveillance Investigation")


st.markdown(
    """
    <div class="echo-header">
        <div class="echo-brand">N.O.V.<span>A.</span></div>
        <div class="echo-subtitle">
            Enhanced Conversational Heuristic Observation
        </div>
        <div class="system-status">● SYSTEM READY</div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="section-title">New Investigation</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Upload a reference image to search the indexed surveillance network.</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload reference image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    st.image(uploaded_file, width=210)

search = st.button(
    "🔍 Start Investigation",
    use_container_width=True,
)


if uploaded_file is not None and search:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg",
    ) as temp:
        temp.write(uploaded_file.read())
        query_path = temp.name

    with st.status("Running investigation...", expanded=True) as status:

        st.write("Searching visual embeddings...")
        results = search_engine.search_image(query_path)

        st.write("Grouping detections...")
        tracks = investigation.group_tracks(results)

        st.write("Building timeline...")
        timeline = investigation.build_timeline(tracks)

        st.write("Reconstructing journey...")
        journey = investigation.reconstruct_journey(timeline)

        associations = investigation.associate_tracks(journey)

        report = report_generator.generate(
            query_path,
            associations,
        )

        st.session_state.report = report
        st.session_state.chat_history = []
        st.session_state.video_request = None

        status.update(
            label="Investigation complete",
            state="complete",
            expanded=False,
        )

    st.success(
        f"Investigation complete • {report['matches']} matching detections found."
    )


if st.session_state.report:

    report = st.session_state.report
    summary = report["summary"]
    journey = report["journey"]

    st.markdown(
        '<div class="section-title">Investigation Overview</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    stats = [
        ("Matching Detections", report["matches"]),
        ("Cameras Visited", len(report["cameras"])),
        ("Tracking Duration", f"{summary['total_tracking_time']:.1f}s"),
        ("Peak Similarity", f"{summary['highest_similarity']:.3f}"),
    ]

    for column, (label, value) in zip((c1, c2, c3, c4), stats):
        with column:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Investigation Timeline</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Reconstructed movement across the surveillance network.</div>',
        unsafe_allow_html=True,
    )

    if not journey:
        st.info("No investigation journey could be reconstructed.")
    else:
        for event in journey:

            left, right = st.columns([1, 4], gap="large")

            with left:
                if os.path.exists(event["crop"]):
                    st.image(event["crop"], use_container_width=True)
                else:
                    st.caption("Evidence unavailable")

            with right:
                st.markdown(
                    f"""
                    <div class="timeline-line">
                        <div class="timeline-dot">
                            <div class="camera-title">📍 {event['camera']}</div>
                            <div class="camera-meta">
                                Track {event['track_id']} • {event['class']}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                a, b, c = st.columns(3)

                with a:
                    st.caption("APPEARED")
                    st.write(event["start"])

                with b:
                    st.caption("LEFT")
                    st.write(event["end"])

                with c:
                    st.caption("DURATION")
                    st.write(f"{event['duration']:.2f}s")

                score = max(0.0, min(1.0, float(event["score"])))
                st.caption(f"Visual similarity • {score:.4f}")
                st.progress(score)

    st.markdown(
        '<div class="section-title">Evidence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Representative detections selected from the investigation.</div>',
        unsafe_allow_html=True,
    )

    if journey:
        columns = st.columns(3)

        for i, event in enumerate(journey):
            crop = event["crop"]

            if not os.path.exists(crop):
                continue

            with columns[i % 3]:
                st.markdown(
                    '<div class="evidence-label">'
                    f"{event['camera']} • Track {event['track_id']}"
                    "</div>",
                    unsafe_allow_html=True,
                )

                st.image(crop, use_container_width=True)
                st.caption(
                    f"Similarity {event['score']:.4f} • "
                    f"{event['duration']:.2f}s"
                )

    if st.session_state.video_request is not None:

        video_request = st.session_state.video_request
        camera = video_request["camera"]
        video_path = video_request["video_path"]
        timestamp = video_request["timestamp"]

        st.markdown(
            '<div class="section-title">🎥 Evidence Playback</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="playback-title">{camera}</div>
            <div class="playback-meta">
                Investigation evidence • playback begins at {timestamp:.2f}s
            </div>
            """,
            unsafe_allow_html=True,
        )

        if os.path.exists(video_path):
            st.video(video_path, start_time=timestamp)
        else:
            st.error(f"Video file not found: {video_path}")

    st.markdown(
        '<div class="section-title">Ask N.O.V.A.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="chat-intro">Ask questions about the reconstructed journey, cameras, detections or evidence.</div>',
        unsafe_allow_html=True,
    )

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("📍 First sighting", use_container_width=True):
            st.session_state.pending_question = "Where was the suspect first seen?"

    with q2:
        if st.button("📍 Last sighting", use_container_width=True):
            st.session_state.pending_question = "Which camera saw the suspect last?"

    with q3:
        if st.button("🎥 Open evidence", use_container_width=True):
            st.session_state.pending_question = (
                "Open the video where the suspect was first detected."
            )

    with q4:
        if st.button("📝 Summary", use_container_width=True):
            st.session_state.pending_question = "Summarize the investigation."

    if st.button("🗑 Clear Conversation"):
        st.session_state.chat_history = []
        st.session_state.video_request = None
        st.rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    pending = st.session_state.pop("pending_question", None)
    question = st.chat_input("Ask N.O.V.A. about this investigation...")

    if pending and not question:
        question = pending

    if question:

        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("N.O.V.A. is analyzing..."):
                answer = assistant.ask(
                    question,
                    st.session_state.report,
                )

            action = None

            try:
                action = json.loads(answer.strip())
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", answer, re.DOTALL)
                if match:
                    try:
                        action = json.loads(match.group(0))
                    except json.JSONDecodeError:
                        action = None

            if (
                isinstance(action, dict)
                and action.get("action") == "play_video"
            ):

                requested_camera = action.get("camera")
                requested_timestamp = action.get("timestamp_seconds")

                matching_events = [
                    event
                    for event in report["journey"]
                    if event["camera"] == requested_camera
                ]

                if matching_events:

                    selected_event = matching_events[0]

                    if requested_timestamp is not None:
                        try:
                            requested_timestamp = float(requested_timestamp)
                            selected_event = min(
                                matching_events,
                                key=lambda event: abs(
                                    float(event["start_seconds"])
                                    - requested_timestamp
                                ),
                            )
                        except (ValueError, TypeError):
                            pass

                    timestamp = float(selected_event["start_seconds"])

                    st.session_state.video_request = {
                        "camera": selected_event["camera"],
                        "video_path": selected_event["video_path"],
                        "timestamp": max(0, timestamp - 5),
                    }

                    message = (
                        f"🎥 Opening **{selected_event['camera']}** "
                        f"around **{timestamp:.2f}s**."
                    )

                    st.markdown(message)

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": message}
                    )

                    st.rerun()

                else:

                    message = (
                        "I couldn't find that camera "
                        "in the current investigation."
                    )

                    st.warning(message)

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": message}
                    )

            else:

                st.markdown(answer)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

else:

    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## ◉")
        st.markdown("### Ready for Investigation")
        st.caption(
            "Upload a reference image to begin searching "
            "the surveillance network."
        )