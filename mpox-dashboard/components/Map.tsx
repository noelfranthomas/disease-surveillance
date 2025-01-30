// components/Map.tsx
"use client";

import { useState, useMemo } from "react";
import Map, { Marker, Source, Layer } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";

interface MpoxCase {
  lat: number;
  lng: number;
  count: number;
}

interface MapProps {
  cases: MpoxCase[];
  countriesWithData: string[]; // List of ISO 3166-1 alpha-3 codes with data
}

export function MpoxMap({ cases, countriesWithData }: MapProps) {
  const [viewState, setViewState] = useState({
    latitude: 20,
    longitude: 0,
    zoom: 1.5,
  });

  // We'll style countries: if iso_3166_1_alpha_3 is in countriesWithData, highlight it; else dim
  const fillLayer: mapboxgl.Layer = {
    id: "country-fills",
    type: "fill",
    source: "country-boundaries",
    "source-layer": "country_boundaries",
    paint: {
      // We'll highlight countries in our data list in red, others light gray
      "fill-color": [
        "case",
        ["in", ["get", "iso_3166_1_alpha_3"], ["literal", countriesWithData]],
        "#e63946", // highlight color for countries with data
        "#dde2e8", // neutral color for others
      ],
      "fill-opacity": 0.5,
    },
  };

  const lineLayer: mapboxgl.Layer = {
    id: "country-borders",
    type: "line",
    source: "country-boundaries",
    "source-layer": "country_boundaries",
    paint: {
      "line-color": "#ffffff",
      "line-width": 0.5,
    },
  };

  return (
    <div className="absolute inset-0">
      <Map
        {...viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        style={{ width: "100%", height: "100%" }}
        mapStyle="mapbox://styles/mapbox/light-v10"
        mapboxAccessToken={process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN}
      >
        {/* Add vector source for country boundaries */}
        <Source
          id="country-boundaries"
          type="vector"
          url="mapbox://mapbox.country-boundaries-v1"
        >
          <Layer {...fillLayer} />
          <Layer {...lineLayer} />
        </Source>

        {cases.map((c, i) => (
          <Marker key={i} longitude={c.lng} latitude={c.lat}>
            <div className="text-red-600 text-xl font-bold">●</div>
          </Marker>
        ))}
      </Map>
    </div>
  );
}
