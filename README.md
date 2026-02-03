# 🏨 Magical Palace Concierge (Gen-AI)

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-202020?style=for-the-badge&logo=uvicorn&logoColor=white)
![UI](https://img.shields.io/badge/UI-Glassmorphism-06b6d4?style=for-the-badge)

**A high-performance, precision-engineered hospitality assistant.** *Experience sub-10ms latency, zero-hallucination responses, and a stunning "Glassmorphism" interface.*

[Features](#-key-features) • [Architecture](#-system-architecture) • [Benchmarks](#-performance-benchmarks) • [Quick Start](#-getting-started)

</div>

---

## 🌟 Overview

**Magical Palace Concierge** is a production-ready, single-file hospitality intelligence engine. Unlike traditional LLM bots that are slow and expensive, this system uses an **Intent-Based Retrieval Engine** to provide guests with instant, deterministic information about hotel services, menus, and local attractions.

---

## 🚀 Key Features

* ⚡ **Ultra-Low Latency:** Optimized via an in-memory **TTL Cache** and keyword overlap scoring for responses in under 10ms.
* 💎 **Glassmorphism UI:** A sleek, modern frontend built with Vanilla JS and CSS—no heavy frameworks required.
* 📡 **Hybrid Streaming:** Supports both standard **JSON POST** and **Server-Sent Events (SSE)** for real-time response "typing" effects.
* 🧠 **Deterministic AI:** Uses pre-configured **Knowledge Cards** to ensure 100% accuracy with zero API costs or hallucinations.
* 📦 **Single-File Portability:** The entire app lives in a single `app.py`, making it ideal for Docker, AWS Lambda, or Heroku.

---


## 🏗️ System Architecture

The following diagram illustrates the high-performance flow from guest interaction through our intent-matching engines to the local knowledge base.

```mermaid
flowchart TD
    %% Node Definitions
    G(Guest / Mobile)
    UI[[Hotel Glass UI]]
    API{{"FastAPI Gateway"}}
    
    subgraph Logic_Layer [Concierge Controller]
        direction TB
        ROUTE[Intent Router]
        CACHE{TTL Cache}
    end

    subgraph Engines [Intelligence Modules]
        ID[Intent Detector]
        STR[SSE Streamer]
        MENU[Menu Builder]
        ATTR[Attraction Finder]
    end

    subgraph Data_Storage [Knowledge Base]
        KCARDS[(Knowledge Cards)]
        M_DATA[(Menu Schemas)]
        T_CFG[(Timing & Policy Config)]
    end

    %% Connections
    G --> UI
    UI --> API
    API --> CACHE
    CACHE -- Hit --> UI
    CACHE -- Miss --> ROUTE

    ROUTE --> ID
    ID --> KCARDS
    ROUTE --> MENU
    MENU --> M_DATA
    ROUTE --> ATTR
    ATTR --> T_CFG
    
    ID --> STR
    MENU --> STR
    ATTR --> STR
    STR --> UI

    %% Styling for GitHub Dark/Light Mode
    style G fill:#22c55e,stroke:#fff,stroke-width:2px,color:#fff
    style API fill:#06b6d4,stroke:#0891b2,stroke-width:2px,color:#fff
    style ROUTE fill:#f59e0b,stroke:#d97706,color:#fff
    style Engines fill:#1a1a1a,stroke:#444,color:#fff
    style Data_Storage fill:#1a1a1a,stroke:#444,color:#fff
    style KCARDS fill:#00d2ff,stroke:#0086a3,color:#000
    style M_DATA fill:#00d2ff,stroke:#0086a3,color:#000
    style T_CFG fill:#00d2ff,stroke:#0086a3,color:#000

    <img width="1198" height="742" alt="image" src="https://github.com/user-attachments/assets/88fca24a-197c-4545-a8af-6554c75577a6" />

