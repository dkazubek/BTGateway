BTGateway
=========

Bluetooth Gateway

## System Architecture

```mermaid
graph TD
    subgraph Sensors [Field Layer]
        BT[BLE Thermometers<br/>Multiple Rooms / Outbuildings]
    end

    subgraph Edge_Gateway [Raspberry Pi Zero 2 W - Bare-Metal OS]
        BTM[Built-in BLE Module]
        PY[Python Script<br/>Data Collector]
        L_MQ[Local Mosquitto Broker]
        NR[Node-RED Flow<br/>Filter & Router]

        BT -- "Bluetooth LE Broadcast" --> BTM
        BTM -- Raw Sensor Data --> PY
        PY -- "MQTT (Localhost)" --> L_MQ
        L_MQ -- "Raw Payload" --> NR
    end

    subgraph Local_Storage [On-Premises Infrastructure]
        NAS[Synology NAS Host]
        subgraph Docker_Engine [Container Space]
            MQ[Central Mosquitto Broker]
        end
        NAS --- Docker_Engine
    end

    subgraph Cloud_Storage [Cloud Infrastructure]
        AZ[Azure IoT Hub]
    end

    %% Data Pipeline Paths
    NR -- "MQTT (Filtered - Port 1883)" --> MQ
    NR -- "MQTT over TLS (Port 8883)" --> AZ

    %% High-Contrast Styling Realignment
    style BT fill:#ff66cc,stroke:#222,stroke-width:2px,color:#000000
    style BTM fill:#99ccff,stroke:#222,stroke-width:2px,color:#000000
    style PY fill:#333333,stroke:#ccc,stroke-width:2px,color:#ffffff
    style L_MQ fill:#99ff99,stroke:#222,stroke-width:2px,color:#000000
    style NR fill:#ff9999,stroke:#222,stroke-width:2px,color:#000000
    style NAS fill:#444444,stroke:#ccc,stroke-width:1px,color:#ffffff
    style MQ fill:#99ff99,stroke:#222,stroke-width:2px,color:#000000
    style AZ fill:#ffff99,stroke:#222,stroke-width:2px,color:#000000
```

### Data Pipeline & Architecture Layers

1. **Physical / Wireless Layer:** Battery-powered BLE thermometers distributed across rooms and outbuildings continuously broadcast advertising packets containing temperature data.
2. **Hardware Ingestion:** The built-in Bluetooth Low Energy module on the Raspberry Pi Zero 2 W scans the airwaves and intercepts these BLE broadcasts.
3. **Data Collection Layer:** A background Python script parses the raw BLE payloads, extracts the thermometer readings, and immediately publishes them to a localized, bare-metal instance of Eclipse Mosquitto running on the Pi.
4. **Edge Orchestration & Filtering:** A local bare-metal Node-RED flow subscribes to the local broker. It acts as an intelligent firewall, filtering out MAC addresses from foreign, ambient Bluetooth devices to keep data clean.
5. **Dual Route Data Transmission:** The filtered, verified thermometer data is split into two pathways by Node-RED:
   * **Local Storage Route:** Transmitted across the local network over TCP (Port 1883) to the primary, containerised Eclipse Mosquitto broker running on the Synology NAS.
   * **Cloud Ingestion Route:** Encrypted and transmitted over WAN using MQTT over TLS (Port 8883) directly into **Azure IoT Hub** for off-site monitoring and retention.
