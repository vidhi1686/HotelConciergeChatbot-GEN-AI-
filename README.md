flowchart TD
    %% Node Definitions
    G(fa:fa-user Guest / Mobile)
    UI[[fa:fa-hotel Glass UI]]
    API{{"fa:fa-bolt FastAPI Gateway"}}
    
    subgraph Logic_Layer [Concierge Controller]
        direction TB
        ROUTE[fa:fa-route Intent Router]
        CACHE{fa:fa-clock TTL Cache}
    end

    subgraph Engines [Intelligence Modules]
        ID[fa:fa-magnifying-glass Intent Detector]
        STR[fa:fa-comment-dots SSE Streamer]
        MENU[fa:fa-utensils Menu Builder]
        ATTR[fa:fa-map-location Attraction Finder]
    end

    subgraph Data_Storage [Knowledge Base]
        KCARDS[(fa:fa-id-card Knowledge Cards)]
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
    ROUTE --> MENU --> M_DATA
    ROUTE --> ATTR --> T_CFG
    
    ID & MENU & ATTR --> STR
    STR --> UI

    %% Styling
    style G fill:#22c55e,stroke:#fff,stroke-width:2px,color:#fff
    style API fill:#06b6d4,stroke:#0891b2,stroke-width:2px,color:#fff
    style ROUTE fill:#f59e0b,stroke:#d97706,color:#fff
    style Engines fill:#1a1a1a,stroke:#444,color:#fff
    style Data_Storage fill:#1a1a1a,stroke:#444,color:#fff
    style KCARDS fill:#00d2ff,stroke:#0086a3,color:#000
    style M_DATA fill:#00d2ff,stroke:#0086a3,color:#000
