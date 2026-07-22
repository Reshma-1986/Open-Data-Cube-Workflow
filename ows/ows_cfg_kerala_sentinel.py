sentinel_2_l2a_bands = {
    "coastal": ["band_01", "B01", "coastal_aerosol"],
    "blue": ["band_02", "B02"],
    "green": ["band_03", "B03"],
    "red": ["band_04", "B04"],
    "rededge1": ["band_05", "B05", "red_edge_1"],
    "rededge2": ["band_06", "B06", "red_edge_2"],
    "rededge3": ["band_07", "B07", "red_edge_3"],
    "nir": ["band_08", "B08", "nir_1"],
    "nir08": ["band_8a", "B8A", "nir_narrow", "nir_2"],
    "nir09": ["band_09", "B09", "water_vapour"],
    "swir16": ["band_11", "B11", "swir_1"],
    "swir22": ["band_12", "B12", "swir_2"],
    "scl": ["mask", "SCL", "qa"],  # FIX: was one bad string "mask, SCL"
    "aot": ["aerosol_optical_thickness", "AOT"],
    "wvp": ["scene_average_water_vapour", "WVP"],
}

# REUSABLE STYLE DEFINITIONS

style_rgb = {
    "name": "simple_rgb",
    "title": "True Colour",
    "abstract": "Simple true-colour image, using the red, green and blue bands",
    "components": {
        "red": {"red": 1.0},
        "green": {"green": 1.0},
        "blue": {"blue": 1.0},
    },
    "scale_range": [0.0, 3000.0],
}

style_rgb_cloud_masked = {
    "name": "simple_rgb_cloud_masked",
    "title": "True Colour (cloud masked)",
    "abstract": "True colour with clouds/shadows/cirrus masked out via SCL",
    "components": {
        "red": {"red": 1.0},
        "green": {"green": 1.0},
        "blue": {"blue": 1.0},
    },
    "scale_range": [0.0, 3000.0],
    "pq_masks": [
        {
            "band": "scl",
            "values": [3, 8, 9, 10],  # cloud shadow, cloud med/high prob, cirrus
            "invert": True,
        },
        {
            "band": "scl",
            "values": [0, 1],  # no data, saturated/defective
            "invert": True,
        },
    ],
}

style_infrared_false_colour = {
    "name": "infrared_false_colour",
    "title": "False Colour (NIR)",
    "abstract": "False colour using NIR, Red, Green",
    "components": {
        "red": {"nir": 1.0},
        "green": {"red": 1.0},
        "blue": {"green": 1.0},
    },
    "scale_range": [0.0, 3000.0],
}

style_ndvi = {
    "name": "ndvi",
    "title": "NDVI",
    "abstract": "Normalized Difference Vegetation Index",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "nir", "band2": "red"},
    },
    "needed_bands": ["red", "nir"],
    "color_ramp": [
        {"value": -1.0, "color": "#8F3F20", "alpha": 0},
        {"value": 0.0, "color": "#8F3F20"},
        {"value": 0.25, "color": "#F7D7A8"},
        {"value": 0.5, "color": "#AAC77C"},
        {"value": 1.0, "color": "#004616"},
    ],
    "legend": {"begin": "-1.0", "end": "1.0", "ticks_every": "0.5"},
}

style_scl_classification = {
    "name": "scl_classification",
    "title": "Scene Classification (SCL)",
    "abstract": "Sen2Cor scene classification layer",
    "value_map": {
        "scl": [
            {"title": "No data", "abstract": "", "values": [0], "color": "#000000"},
            {"title": "Saturated/defective", "abstract": "", "values": [1], "color": "#ff0000"},
            {"title": "Dark area pixels", "abstract": "", "values": [2], "color": "#2f2f2f"},
            {"title": "Cloud shadows", "abstract": "", "values": [3], "color": "#643200"},
            {"title": "Vegetation", "abstract": "", "values": [4], "color": "#00a000"},
            {"title": "Bare soils", "abstract": "", "values": [5], "color": "#ffe65a"},
            {"title": "Water", "abstract": "", "values": [6], "color": "#0000ff"},
            {"title": "Unclassified", "abstract": "", "values": [7], "color": "#808080"},
            {"title": "Cloud medium probability", "abstract": "", "values": [8], "color": "#c0c0c0"},
            {"title": "Cloud high probability", "abstract": "", "values": [9], "color": "#ffffff"},
            {"title": "Thin cirrus", "abstract": "", "values": [10], "color": "#64c8ff"},
            {"title": "Snow or ice", "abstract": "", "values": [11], "color": "#ff96ff"},
        ]
    },
}

# REUSABLE RESOURCE LIMITS

standard_resource_limits = {
    "wms": {
        "zoomed_out_fill_colour": [150, 180, 200, 160],
        "min_zoom_factor": 15.0,
        "max_datasets": 32,
    },
    "wcs": {"max_datasets": 16},
}

# MAIN CONFIGURATION OBJECT

ows_cfg = {
    "global": {
        "response_headers": {"Access-Control-Allow-Origin": "*"},
        "services": {"wms": True, "wmts": True, "wcs": True},
        "title": "Kerala Open Data Cube - WMS/WMTS/WCS",
        "allowed_urls": [
            "http://localhost/odc_ows",
            "http://127.0.0.1:8000/",
            "http://127.0.0.1:5000/",
        ],
        "url": ["http://localhost/odc_ows"],
        "info_url": "http://opendatacube.org",
        "abstract": "Kerala Open Data Cube OWS service, serving Sentinel-2 L2A COGs.",
        "keywords": ["satellite", "sentinel-2", "cogs", "india", "kerala", "time-series"],
        "contact_info": {
            "person": "Your Name",
            "organisation": "Your Org",
            "email": "you@example.com",
        },
        "fees": "",
        "access_constraints": "",
        "published_CRSs": {
            "EPSG:4326": {"geographic": True, "vertical_coord_first": True},
            "EPSG:3857": {"geographic": False, "horizontal_coord": "x", "vertical_coord": "y"},
            "EPSG:32643": {"geographic": False, "horizontal_coord": "x", "vertical_coord": "y"},
        },
    },  # End of "global" section.

    "wms": {
        "s3_url": "https://sentinel-cogs.s3.ap-south-2.amazonaws.com",
        "s3_bucket": "sentinel-cogs",
        "s3_aws_zone": "ap-south-2",
        "max_width": 512,
        "max_height": 512,
    },  # End of "wms" section.

    "wcs": {
        "formats": {
            "GeoTIFF": {
                "renderers": {
                    "1": "datacube_ows.wcs1_utils.get_tiff",
                    "2": "datacube_ows.wcs2_utils.get_tiff",
                },
                "mime": "image/geotiff",
                "extension": "tif",
                "multi-time": False,
            },
        },
        "native_format": "GeoTIFF",
    },  # End of "wcs" section.

    "layers": [
        {
            "title": "Kerala Sentinel-2 L2A",
            "abstract": "Sentinel-2 L2A COG products indexed for Kerala",
            "layers": [
                {
                    "title": "Sentinel-2 L2A",
                    "name": "sentinel_2_l2a",
                    "abstract": (
                        "Sentinel-2a and Sentinel-2b imagery, processed to Level 2A "
                        "(Surface Reflectance) and converted to Cloud Optimized GeoTIFFs"
                    ),
                    "product_name": "sentinel_2_l2a",
                    "bands": sentinel_2_l2a_bands,
                    "resource_limits": standard_resource_limits,
                    "dynamic": False,
                    "time_resolution": "solar",
                    "native_crs": "EPSG:32643",
                    "native_resolution": [10.0, -10.0],
                    "image_processing": {
                        "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                        "always_fetch_bands": [],
                        "manual_merge": False,
                    },
                    "flags": [
                        {
                            "band": "scl",
                            "ignore_time": False,
                            "ignore_info_flags": [],
                        }
                    ],
                    "wcs": {},
                    "styling": {
                        "default_style": "simple_rgb",
                        "styles": [
                            style_rgb,
                            style_rgb_cloud_masked,
                            style_infrared_false_colour,
                            style_ndvi,
                            style_scl_classification,
                        ],
                    },
                }
            ],
        }
    ],  # End of "layers" list.
}  # End of configuration object
