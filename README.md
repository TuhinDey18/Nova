# N.O.V.A. — Networked Observation & Visual Analytics

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Space+Mono&weight=700&size=24&pause=1000&color=7C3AED&center=true&vCenter=true&width=720&lines=Turn+hours+of+CCTV+review+into+actionable+leads.;Networked+Observation.+Visual+Analytics." alt="N.O.V.A. animated introduction" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-7C3AED?style=for-the-badge" alt="AI Powered" />
  <img src="https://img.shields.io/badge/Computer-Vision-06B6D4?style=for-the-badge" alt="Computer Vision" />
  <img src="https://img.shields.io/badge/Status-Hackathon%20Project-F59E0B?style=for-the-badge" alt="Hackathon Project" />
</p>

<p align="center">
  <strong>Upload one image. Search every camera. Reconstruct the journey.</strong>
</p>

---

## ✨ What is N.O.V.A.?

**N.O.V.A.** is an AI-powered surveillance investigation assistant built for fast, explainable video review. An investigator uploads a query image and N.O.V.A. searches pre-indexed CCTV footage, groups visually similar detections into tracks, reconstructs a time-ordered journey across cameras, and answers questions about the results.

> **The goal:** transform a large, fragmented set of camera feeds into a focused set of visual leads in seconds.

## 🎯 Key capabilities

| Capability | How N.O.V.A. does it |
| --- | --- |
| **Multi-camera indexing** | Processes CCTV videos with YOLOv11 detection and tracking. |
| **Visual similarity search** | Uses CLIP embeddings and FAISS cosine-similarity search. |
| **Journey reconstruction** | Groups matches by camera and track, then orders them chronologically. |
| **Evidence-first interface** | Shows representative crops, timestamps, duration, track IDs, and scores. |
| **Conversational investigation** | Uses a local Ollama model to answer questions from the generated report. |
| **Auditable outputs** | Writes detection records to SQLite, CSV, crops, and a FAISS index. |

## 🧠 System architecture

<p align="center">
  <a href="assets/nova-dataflow.svg">
    <img src="assets/nova-dataflow.svg" width="760" alt="Animated N.O.V.A. data-flow diagram: CCTV videos are indexed with YOLO and CLIP; a query image searches FAISS to produce a timeline, dashboard, and assistant response." />
  </a>
</p>

## 🚀 Quick start

### 1. Clone and create an environment

```bash
git clone https://github.com/<your-username>/ECHO.git
cd ECHO

python -m venv venv
```

**Windows**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install open-clip-torch
```

### 3. Start the local assistant

N.O.V.A. uses Ollama locally; install it from [ollama.com](https://ollama.com), then run:

```bash
ollama pull llama3.2
ollama serve
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, upload a query image, and select **Start Investigation**.

## 🗂️ Prepare a case for search

Place one or more `.mp4` videos in a case folder. The detector processes each video, saves visual crops, writes detection records, and creates the FAISS index used by the application.

```python
from src.case_processor import CaseProcessor

CaseProcessor().process_case("cases/apartment_case_001")
```

This creates or updates:

```text
crops/              # detected object images
data/               # per-camera CSV detection exports
database/echo.db    # SQLite detection audit trail
faiss/faiss.index   # visual-search index
faiss/metadata.pkl  # metadata paired with vectors
runs/               # YOLO annotated video output
```

## 🕵️ Investigation flow

1. **Upload** a reference image of a person or object.
2. **Search** the visual index for the closest matching detections.
3. **Group** raw frame matches into camera-specific tracks.
4. **Reconstruct** a chronological journey across all matching cameras.
5. **Review** supporting crops, times, durations, and similarity scores.
6. **Ask** N.O.V.A. questions such as “Where was the subject first seen?”

## 🛠️ Tech stack

<p>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/YOLOv11-Detection-111827" alt="YOLOv11" />
  <img src="https://img.shields.io/badge/CLIP-Embeddings-8B5CF6" alt="CLIP" />
  <img src="https://img.shields.io/badge/FAISS-Vector%20Search-009688" alt="FAISS" />
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-111827" alt="Ollama" />
  <img src="https://img.shields.io/badge/SQLite-Audit%20Store-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
</p>

## 🔮 Roadmap

- [ ] Filter search results by object class and camera
- [ ] Use track-level, cross-camera ReID rather than frame-level matches
- [ ] Add a floor-plan / camera-map journey visualisation
- [ ] Add source-video jump links at each event timestamp
- [ ] Support vehicle attributes and licence-plate OCR
- [ ] Add investigator feedback: **same subject** / **not the same subject**
- [ ] Add privacy controls, retention rules, and comprehensive audit logs

## ⚖️ Responsible use

N.O.V.A. produces **investigative leads**, not identity confirmation. Visual similarity can be wrong or biased, especially with poor imagery, occlusion, or changes in appearance. Every result should be reviewed by a trained human, used only with appropriate authorization, and handled according to applicable privacy and surveillance laws.

## 👥 Team

Built with curiosity, computer vision, and a belief that investigators deserve better tools for finding the right evidence.

<p align="center">
  <sub>Made for a hackathon · Built for explainable investigations</sub><br />
  <strong>🔎 Find the signal. Follow the story.</strong>
</p>
