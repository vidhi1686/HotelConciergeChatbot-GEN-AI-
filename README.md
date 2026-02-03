<div class="mermaid">
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
        ROUTE --> MENU
        MENU --> M_DATA
        ROUTE --> ATTR
        ATTR --> T_CFG
        
        ID --> STR
        MENU --> STR
        ATTR --> STR
        STR --> UI
</div>
