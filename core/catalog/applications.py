"""
Master Alternative-Protein Applications Catalog & Regional Availability Matrix.
Defines the 7 functional target applications, target mechanisms, and benchmark controls.
"""

APPLICATIONS_CATALOG = [
    {
        "id": "egg",
        "name": "Plant-Based Egg Gel",
        "animal_replaced": "Chicken Eggs",
        "benchmark": "Mung bean 8S Vicilin (JUST Egg control, A0A1S3VZW2)",
        "protein_family": "7S Vicilin trimeric storage globulin",
        "top_african_crop": "Pigeon pea (Cajanus cajan)",
        "backup_substitute": "Cowpea (Vigna unguiculata)",
        "cultural_meals": ["Moi moi (steamed bean pudding)", "Akara (whipped bean fritters)", "Breakfast egg scramble"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Rupture Force ~0.8 N, Springiness >85%",
        "biochemical_mechanism": "7S Vicilin trimer unfolds rapidly between 75°C and 85°C, forming an isotropic elastic gel network without sulfur cross-links."
    },
    {
        "id": "milk",
        "name": "Plant-Based Milk & Dairy Drinks",
        "animal_replaced": "Cow Milk & Canned Evaporated Milk",
        "benchmark": "Soybean 7S Beta-conglycinin alpha' (P11827)",
        "protein_family": "High net-negative charge soluble globulin",
        "top_african_crop": "Cowpea (Vigna unguiculata)",
        "backup_substitute": "Bambara groundnut (Vigna subterranea)",
        "cultural_meals": ["Kunu Aya (Tigernut milk)", "Kunu Gyada (Groundnut milk)", "Tea & pap whitener", "Cultured plant yogurt"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Colloidal Stability >90% at 7 days, pH 7 Solubility >80%",
        "biochemical_mechanism": "High net-negative surface charge creates electrostatic repulsion (Zeta potential < -30 mV), preventing colloidal flocculation."
    },
    {
        "id": "gel",
        "name": "Plant-Based Curd & Cheese (Awara / Wagashi)",
        "animal_replaced": "Stew Beef Chunks & Fulani Cow Cheese (Wara / Wagashi)",
        "benchmark": "Soybean 11S Glycinin G4 (P02858)",
        "protein_family": "11S Legumin hexamer with acidic/basic subunits",
        "top_african_crop": "African yam bean (Sphenostylis stenocarpa)",
        "backup_substitute": "Pigeon pea (Cajanus cajan)",
        "cultural_meals": ["Awara (fried plant curd)", "Wagashi (cheese curd alternative)", "Soup meat substitute"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Breaking Stress 1.2 - 1.5 N via 0.3% CaCl2 cross-linking",
        "biochemical_mechanism": "Thermal exposure unfolds 11S hexamers, exposing negatively charged residues for divalent Ca2+ ionic bridging."
    },
    {
        "id": "meat",
        "name": "Textured Plant-Based Meat & Suya",
        "animal_replaced": "Red Meat, Beef & Chewy Goat Meat (Asun)",
        "benchmark": "Soy Textured Vegetable Protein (SPI Extrudate, P02858)",
        "protein_family": "11S Legumin hexamer with structural cysteine dyads",
        "top_african_crop": "Pigeon pea (Cajanus cajan) & African yam bean",
        "backup_substitute": "Groundnut meal & Bambara groundnut press-cake",
        "cultural_meals": ["Beef Suya skewers", "Dried Kilishi strips", "Peppered meat pies", "Stew meat chunks"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Tensile shear modulus matching beef muscle fibers",
        "biochemical_mechanism": "High cysteine fractions enable covalent disulfide bond exchange under shear and heat, aligning protein fibrils into chewy meat-like fibers."
    },
    {
        "id": "crayfish",
        "name": "Savory Umami Peptides & Crayfish Alternative",
        "animal_replaced": "Dried River Crayfish & Smoked Bonga Fish Seasoning",
        "benchmark": "Dried River Crayfish & Smoked Fish Peptides",
        "protein_family": "Low-molecular weight umami peptide hydrolysate (<1 kDa)",
        "top_african_crop": "Fermented African Locust Bean (Iru / Dawadawa)",
        "backup_substitute": "Fermented African yam bean peptides",
        "cultural_meals": ["Egusi soup", "Ogbono soup", "Efo riro", "Gbegiri soup", "Jollof rice seasoning"],
        "plant_based_flag": "100% Plant-Based (Traditional umami secret of West Africa)",
        "target_metric": "High free glutamic acid and sulfurous savory peptides",
        "biochemical_mechanism": "Microbial protease breakdown yields small peptides (<1 kDa) rich in glutamate and aspartate that bind umami T1R1/T1R3 taste receptors."
    },
    {
        "id": "mayo",
        "name": "Plant-Based Mayonnaise & Dressings",
        "animal_replaced": "Commercial Egg-Yolk Mayonnaise & Salad Creams",
        "benchmark": "Egg-Yolk Lecithin Emulsion (70% vegetable oil phase)",
        "protein_family": "Amphiphilic surface-active 7S globulin",
        "top_african_crop": "Pigeon pea (Cajanus cajan) & Groundnut conarachin",
        "backup_substitute": "Cowpea isolate",
        "cultural_meals": ["Nigerian salad dressing (Heinz/Bama style)", "Sandwich spread", "Shawarma sauce"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "Oil-in-Water emulsion stability >12 months without separation",
        "biochemical_mechanism": "Amphiphilic globulin regions anchor hydrophobic domains into oil droplets while hydrophilic loops face water, forming a protective steric barrier."
    },
    {
        "id": "sarcopenia",
        "name": "Clinical Sarcopenia High-Protein Swallows & Porridges",
        "animal_replaced": "Medical Whey Protein Isolate & Meat Broth Fortifiers",
        "benchmark": "Medical Whey Protein Isolate (Oral Nutritional Supplement)",
        "protein_family": "Partially enzymatically hydrolyzed peptides (<5 kDa)",
        "top_african_crop": "Cowpea & Pigeon pea hydrolysate (Papain-digested)",
        "backup_substitute": "Bambara groundnut flour blend",
        "cultural_meals": ["Protein-fortified Amala", "Fortified Tuwo Shinkafa", "Fortified Ogi / Akamu porridge"],
        "plant_based_flag": "100% Plant-Based as cooked",
        "target_metric": "18g protein / 100g portion with zero swallow paste viscosity increase",
        "biochemical_mechanism": "Targeted enzymatic cleavage prevents starch cross-linking, providing high essential amino acids (Leucine > 7.0g/100g) without altering paste texture."
    }
]

REGIONAL_AVAILABILITY = {
    "Nigeria": {
        "primary_crops": ["cowpea", "bambara_groundnut", "pigeon_pea", "african_yam_bean", "groundnut", "african_locust_bean"],
        "notes": "Cowpea and Groundnut widely available nationally; Bambara in East & North; AYB primarily in South & Central.",
        "currency_symbol": "₦",
        "multiplier": 1.0
    },
    "Ghana": {
        "primary_crops": ["cowpea", "bambara_groundnut", "groundnut"],
        "notes": "Cowpea (Adua) and Bambara (Aboboi) are staple market commodities across Greater Accra and Northern regions.",
        "currency_symbol": "GH₵",
        "multiplier": 0.013
    },
    "Kenya": {
        "primary_crops": ["pigeon_pea", "cowpea", "groundnut"],
        "notes": "Pigeon pea (Mbaazi) is an agronomic cash crop across Eastern & Coastal Kenya; widely consumed with coconut rice.",
        "currency_symbol": "KSh",
        "multiplier": 0.125
    },
    "South Africa": {
        "primary_crops": ["bambara_groundnut", "cowpea", "groundnut", "soybean"],
        "notes": "Jugo beans (Bambara) and Cowpea cultivate well in Limpopo and Mpumalanga as drought-hardy legumes.",
        "currency_symbol": "R",
        "multiplier": 0.017
    }
}
