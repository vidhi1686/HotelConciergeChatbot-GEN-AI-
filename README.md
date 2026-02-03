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
