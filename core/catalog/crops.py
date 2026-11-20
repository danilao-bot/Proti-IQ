"""
Master Crop Catalog for Proti IQ.
Contains 14 African indigenous candidates, orphan legumes, and commercial benchmarks.
"""

CROPS_CATALOG = [
    {
        "id": "cowpea",
        "common_name": "Cowpea (Black-eyed pea)",
        "scientific_name": "Vigna unguiculata",
        "tax_id": 3899,
        "role": "candidate",
        "primary_region": "West Africa",
        "protein_content_pct": "23% - 26%",
        "sequence_data_status": "Available (45 UniProt entries)",
        "globulin_focus": "7S beta-vignin",
        "description": "Drought-tolerant West African staple legume high in 7S beta-vignin storage globulins."
    },
    {
        "id": "pigeon_pea",
        "common_name": "Pigeon Pea",
        "scientific_name": "Cajanus cajan",
        "tax_id": 3821,
        "role": "candidate",
        "primary_region": "West & East Africa",
        "protein_content_pct": "21% - 25%",
        "sequence_data_status": "Available (87 UniProt entries)",
        "globulin_focus": "7S & 11S balanced",
        "description": "Perennial hardy legume rich in sulfur-containing globulins, highly suitable for plant-based meat and egg alternatives."
    },
    {
        "id": "african_yam_bean",
        "common_name": "African Yam Bean",
        "scientific_name": "Sphenostylis stenocarpa",
        "tax_id": 34149,
        "role": "candidate",
        "primary_region": "West & Central Africa",
        "protein_content_pct": "21% - 29%",
        "sequence_data_status": "Available (28 UniProt entries)",
        "globulin_focus": "11S legumin hexameric",
        "description": "High-protein underutilized tuber-legume yielding firm coagulated curds under calcium cross-linking."
    },
    {
        "id": "groundnut",
        "common_name": "Groundnut (Peanut)",
        "scientific_name": "Arachis hypogaea",
        "tax_id": 3818,
        "role": "candidate",
        "primary_region": "Pan-African",
        "protein_content_pct": "25% - 28%",
        "sequence_data_status": "Available (52 UniProt entries)",
        "globulin_focus": "Arachin (11S) & Conarachin (7S)",
        "description": "Widely cultivated pan-African oilseed whose defatted press-cake provides high-solubility emulsifying protein."
    },
    {
        "id": "bambara_groundnut",
        "common_name": "Bambara Groundnut",
        "scientific_name": "Vigna subterranea",
        "tax_id": 3914,
        "role": "candidate",
        "primary_region": "West & Southern Africa",
        "protein_content_pct": "19% - 24%",
        "sequence_data_status": "Tier 1 Wet-Lab Only (0 UniProt globulin entries)",
        "globulin_focus": "Empirical solubility 82.27% (Pretoria M38)",
        "description": "Extremely drought-resilient subterranean legume; verified empirically by University of Pretoria wet-lab data."
    },
    {
        "id": "african_locust_bean",
        "common_name": "African Locust Bean (Iru / Dawadawa)",
        "scientific_name": "Parkia biglobosa",
        "tax_id": 148714,
        "role": "orphan_expansion",
        "primary_region": "West African Savannah",
        "protein_content_pct": "30% - 35% (fermented)",
        "sequence_data_status": "Orphan (Biochemical validation)",
        "globulin_focus": "Free glutamic acid & savory peptides",
        "description": "Traditional savory seasoning seed whose alkaline fermentation yields high umami peptides replacing dried crayfish."
    },
    {
        "id": "soybean",
        "common_name": "Soybean",
        "scientific_name": "Glycine max",
        "tax_id": 3847,
        "role": "benchmark",
        "primary_region": "Global Commercial Benchmark",
        "protein_content_pct": "36% - 40%",
        "sequence_data_status": "Benchmark (Control)",
        "globulin_focus": "11S Glycinin & 7S Beta-conglycinin",
        "description": "Global commercial alternative-protein standard used for SPI and TVP benchmarking."
    },
    {
        "id": "mung_bean",
        "common_name": "Mung Bean",
        "scientific_name": "Vigna radiata",
        "tax_id": 3916,
        "role": "benchmark",
        "primary_region": "Global Commercial Benchmark",
        "protein_content_pct": "24% - 27%",
        "sequence_data_status": "Benchmark (Control)",
        "globulin_focus": "8S Vicilin (A0A1S3VZW2)",
        "description": "Commercial control protein used in commercial plant-based egg formulations (JUST Egg)."
    }
]
