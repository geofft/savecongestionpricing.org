const MAPTILER_KEY = "ONlrjo5B1L5UvXAAre5c";
const map = new maplibregl.Map({
  style: `https://api.maptiler.com/maps/basic-v2/style.json?key=${MAPTILER_KEY}`,
  center: [-74.0066, 40.7135],
  zoom: 8.5,
  container: "map",
  antialias: true,
});
map.on("load", () => {
  map.addSource("senate", {
    type: "geojson",
    // Use a URL for the value for the `data` property.
    data: "map/updated_Senate.geojson",
  });

  map.addLayer({
    id: "senate",
    type: "fill",
    source: "senate",
    paint: {
      "fill-color": [
        "match",
        ["get", "support"],
        "OPPOSE",
        "green", // blue color fill
        "Unclear",
        "blue",
        "Uknown",
        "black",
        "black",
      ],
      "fill-opacity": 0.5,
    },
  });
});
