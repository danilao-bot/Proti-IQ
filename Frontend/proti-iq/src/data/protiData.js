export const COUNTRY_MARKETS = {
  Nigeria: { symbol: '₦', multiplier: 1, soyPriceKg: 4200, eggCratePrice: 5400, dairyMilkPrice: 3200 },
  Ghana: { symbol: 'GH₵', multiplier: 0.013, soyPriceKg: 55, eggCratePrice: 70, dairyMilkPrice: 42 },
  Kenya: { symbol: 'KSh', multiplier: 0.125, soyPriceKg: 520, eggCratePrice: 680, dairyMilkPrice: 400 },
  'South Africa': { symbol: 'R', multiplier: 0.017, soyPriceKg: 72, eggCratePrice: 95, dairyMilkPrice: 55 },
};

// 8 Curated African & Benchmark Legumes screened by ESM-2 650M
export const AFRICAN_CROPS = [
  {
    id: 'bambara',
    name: 'Bambara Groundnut',
    localNames: 'Okpa / Gurjiya / Jugo Bean',
    origin: 'Indigenous West & Southern Africa',
    globulinFocus: '7S Vicilin & 11S Legumin Balanced',
    proteinPer100g: 21.5,
    solubilityPct: 82.6,
    baseCostNairaKg: 1500,
    scores: {
      milk: 95,
      yogurt: 91,
      egg: 87,
      wara: 84,
      meat: 80,
      fortify: 90,
    },
    strengths: ['82.6% Natural Solubility', 'Creamy Emulsion', 'Zero Lactose'],
    pI: '4.7',
    gravy: '-0.48',
    cysteine: '1.1%',
    prepSteps: [
      { title: 'Blanch de-hulled seeds at 90°C for 3 minutes', detail: 'Removes beany lipoxygenase notes and softens seed coat.' },
      { title: 'Blend 1 cup seeds with 5.5 cups warm water', detail: 'High-shear blend for 2 minutes for maximum protein extraction.' },
      { title: 'Strain & finish for your target dish', detail: 'Use as creamy milk, culture at 42°C for yogurt, or whisk with starch for egg/baking.' },
    ],
  },
  {
    id: 'cowpea',
    name: 'Cowpea (Black-Eyed / Brown)',
    localNames: 'Ewa / Wake / Kunde',
    origin: 'Pan-African Drought-Resilient Staple',
    globulinFocus: '7S Vicilin Dominant',
    proteinPer100g: 23.8,
    solubilityPct: 80.4,
    baseCostNairaKg: 1350,
    scores: {
      milk: 92,
      yogurt: 94,
      egg: 91,
      wara: 83,
      meat: 82,
      fortify: 96,
    },
    strengths: ['Lowest Cost / kg', 'High Digestibility', 'Widely Available'],
    pI: '4.6',
    gravy: '-0.51',
    cysteine: '1.0%',
    prepSteps: [
      { title: 'Soak & blanch de-hulled cowpeas at 90°C for 3 minutes', detail: 'Reduces oligosaccharides and phytates by up to 78%.' },
      { title: 'Wet-mill 1 cup seeds with 5 cups water', detail: 'Produces a smooth, neutral protein suspension.' },
      { title: 'Strain, culture, or enzymatically hydrolyze', detail: 'Ideal for probiotic yogurt, egg-free batters, or swallow fortification.' },
    ],
  },
  {
    id: 'african_yam_bean',
    name: 'African Yam Bean',
    localNames: 'Odudu / Azama / Girigiri',
    origin: 'West & Central Africa',
    globulinFocus: '11S Legumin Hexameric Rich',
    proteinPer100g: 24.6,
    solubilityPct: 76.2,
    baseCostNairaKg: 1650,
    scores: {
      milk: 78,
      yogurt: 82,
      egg: 85,
      wara: 94,
      meat: 96,
      fortify: 88,
    },
    strengths: ['Fibrous Meat Bite', 'Firm Curd Network', 'High Lysine & Methionine'],
    pI: '4.8',
    gravy: '-0.39',
    cysteine: '1.5%',
    prepSteps: [
      { title: 'Blanch & alkaline-extract flour at pH 8.5', detail: 'Solubilizes 11S legumin subunits for structural binding.' },
      { title: 'Precipitate at pH 4.6 & cross-link with 0.3% CaCl₂', detail: 'Creates disulfide-stabilized protein fibers.' },
      { title: 'Heat-denature (85°C–92°C) & press', detail: 'Forms firm wara curds or chewable Suya meat extrudates.' },
    ],
  },
  {
    id: 'pigeon_pea',
    name: 'Pigeon Pea',
    localNames: 'Fio-Fio / Otili / Mbaazi',
    origin: 'East, Southern & West Africa',
    globulinFocus: '7S Vicilin + 11S Legumin',
    proteinPer100g: 22.3,
    solubilityPct: 79.1,
    baseCostNairaKg: 1450,
    scores: {
      milk: 83,
      yogurt: 85,
      egg: 95,
      wara: 89,
      meat: 91,
      fortify: 89,
    },
    strengths: ['Superior Thermal Gelation', 'Bakery Egg Match', 'Drought Hardiness'],
    pI: '4.7',
    gravy: '-0.44',
    cysteine: '1.3%',
    prepSteps: [
      { title: 'Blanch & wet-mill de-hulled pigeon pea', detail: 'Neutralizes raw legume flavor while preserving 7S vicilin trimers.' },
      { title: 'Adjust to pH 6.8 with 0.3% CaCl₂ binder', detail: 'Matches hen egg albumen thermal setting window (78°C–85°C).' },
      { title: 'Whisk into cake/pastry batter or extrude', detail: 'Traps air bubbles and moisture cleanly without poultry eggs.' },
    ],
  },
  {
    id: 'groundnut',
    name: 'African Groundnut (Peanut)',
    localNames: 'Epa / Gyada / Njugu',
    origin: 'Pan-African',
    globulinFocus: 'Arachin (11S) & Conarachin (7S)',
    proteinPer100g: 25.8,
    solubilityPct: 74.5,
    baseCostNairaKg: 1700,
    scores: {
      milk: 88,
      yogurt: 86,
      egg: 76,
      wara: 87,
      meat: 85,
      fortify: 87,
    },
    strengths: ['Highest Crude Protein (25.8%)', 'Rich Mouthfeel', 'Abundant Supply'],
    pI: '4.5',
    gravy: '-0.35',
    cysteine: '1.2%',
    prepSteps: [
      { title: 'Lightly roast or blanch de-skinned kernels at 90°C', detail: 'Balances roasted aroma and removes skin tannins.' },
      { title: 'Blend 1 cup kernels with 6 cups warm water', detail: 'Creates a naturally rich, creamy plant milk.' },
      { title: 'Strain & coagulate or ferment', detail: 'Works well for rich beverages, yogurt, and pressed protein curds.' },
    ],
  },
  {
    id: 'locust_bean',
    name: 'African Locust Bean',
    localNames: 'Iru / Dawadawa / Soumbala',
    origin: 'West & Central Savanna',
    globulinFocus: 'Bioactive Hydrolyzed Peptides',
    proteinPer100g: 30.2,
    solubilityPct: 81.0,
    baseCostNairaKg: 1950,
    scores: {
      milk: 70,
      yogurt: 79,
      egg: 74,
      wara: 81,
      meat: 88,
      fortify: 93,
    },
    strengths: ['30.2% Protein Density', 'Pre-Digested Peptides', 'Umami Depth'],
    pI: '4.6',
    gravy: '-0.46',
    cysteine: '1.4%',
    prepSteps: [
      { title: 'De-hull & steam-blanch clean cotyledons', detail: 'Softens seed matrix and unlocks soluble peptides.' },
      { title: 'Mill into fine protein flour or paste', detail: 'Concentrates 30g+ protein per 100g dry matter.' },
      { title: 'Blend into savory meat analogs or swallows', detail: 'Boosts savory umami and amino acid density.' },
    ],
  },
  {
    id: 'lima_bean',
    name: 'African Lima / Butter Bean',
    localNames: 'Awuje / Kapala',
    origin: 'West & East Africa',
    globulinFocus: '7S Vicilin Smooth Gel',
    proteinPer100g: 21.0,
    solubilityPct: 77.8,
    baseCostNairaKg: 1600,
    scores: {
      milk: 81,
      yogurt: 84,
      egg: 88,
      wara: 85,
      meat: 79,
      fortify: 85,
    },
    strengths: ['Silky Crumb Binding', 'Mild Neutral Flavor', 'Low Fat'],
    pI: '4.7',
    gravy: '-0.49',
    cysteine: '1.0%',
    prepSteps: [
      { title: 'Blanch de-hulled seeds at 90°C for 4 minutes', detail: 'Inactivates antinutrients and softens starch-protein matrix.' },
      { title: 'Blend with water (1:5 ratio) & strain', detail: 'Produces a mild, white protein base.' },
      { title: 'Use in baking batters or plant curds', detail: 'Delivers clean color and gentle texture.' },
    ],
  },
  {
    id: 'kersting_groundnut',
    name: "Kersting's Groundnut",
    localNames: 'Doyi / Kandela',
    origin: 'West African Savanna',
    globulinFocus: 'High-Arginine 7S/11S Globulins',
    proteinPer100g: 22.9,
    solubilityPct: 80.1,
    baseCostNairaKg: 1850,
    scores: {
      milk: 85,
      yogurt: 83,
      egg: 84,
      wara: 86,
      meat: 83,
      fortify: 91,
    },
    strengths: ['Superior Amino Balance', 'High Arginine & Lysine', 'Clean Taste'],
    pI: '4.6',
    gravy: '-0.47',
    cysteine: '1.2%',
    prepSteps: [
      { title: 'Blanch de-hulled seeds at 90°C for 3 minutes', detail: 'Preserves delicate flavor while boosting solubility.' },
      { title: 'Blend 1 cup seeds with 5.5 cups water', detail: 'Yields a smooth, high-protein liquid base.' },
      { title: 'Strain & fortify porridges or beverages', detail: 'Ideal for clinical recovery and senior nutrition.' },
    ],
  },
];

export const TARGET_APPLICATIONS = [
  {
    id: 'milk',
    label: 'Plant-Based Milk',
    category: 'Dairy Replacement',
    benchmark: 'Commercial Dairy / Imported Soy Milk',
    description: 'Creamy, lactose-free milk for tea, cereal, and daily drinking.',
    focusReason: 'Ranked by 7S Vicilin solubility, smooth emulsion stability, and neutral flavor.',
  },
  {
    id: 'yogurt',
    label: 'Plant-Based Yogurt',
    category: 'Fermented Dairy',
    benchmark: 'Commercial Cow Yogurt',
    description: 'Thick, spoonable probiotic yogurt gentle on mature stomachs.',
    focusReason: 'Ranked by acid-induced gelation at pH 4.5 without whey separation.',
  },
  {
    id: 'egg',
    label: 'Plant-Based Egg & Bakery Replacer',
    category: 'Egg Replacement',
    benchmark: 'Poultry Hen Egg (>₦5,000/crate)',
    description: 'Scrambled egg base or cake/pastry binder with strong thermal setting.',
    focusReason: 'Ranked by 78°C–85°C thermal gelation and foaming capacity.',
  },
  {
    id: 'wara',
    label: 'Plant-Based Wara / Cheese Curd',
    category: 'Coagulated Curd',
    benchmark: 'Traditional Dairy Wara / Tofu',
    description: 'Firm, sliceable protein curds coagulated with food-grade CaCl₂.',
    focusReason: 'Ranked by 11S Legumin cross-linking and curd firmness.',
  },
  {
    id: 'meat',
    label: 'Textured Plant Meat / Suya',
    category: 'Meat Analog',
    benchmark: 'Beef / Imported Soy SPI Extrudate',
    description: 'Fibrous, chewy plant-meat chunks that absorb spice and grill heat.',
    focusReason: 'Ranked by cysteine disulfide density and fibrous extrusion texture.',
  },
  {
    id: 'fortify',
    label: 'Swallow & Porridge Protein Booster',
    category: 'Clinical & Family Nutrition',
    benchmark: 'Whey / Commercial Fortifiers',
    description: 'High-protein flour or hydrolysate to enrich Amala, Tuwo, Ogi, or Eba.',
    focusReason: 'Ranked by essential amino acid completeness and easy digestibility.',
  },
];

export const NUTRITIONIST_COHORTS = [
  {
    id: 'sarcopenia',
    title: 'Older-Person Sarcopenia (Age 50+)',
    tag: 'AGING MUSCLE HEALTH',
    summary: 'Prevents muscle wasting in older adults eating 90%+ carbohydrate swallow meals.',
    targetGramsPerMeal: 30,
  },
  {
    id: 'lactose',
    title: 'Lactose-Intolerant Adults (70%+ Pop.)',
    tag: 'DIGESTIVE COMFORT',
    summary: 'Replaces cow dairy with zero-lactose, low-flatulence African legume proteins.',
    targetGramsPerMeal: 25,
  },
  {
    id: 'pediatric',
    title: 'Growing Children & Maternal Care',
    tag: 'GROWTH & RECOVERY',
    summary: 'Boosts lysine-rich protein density in affordable family porridges and meals.',
    targetGramsPerMeal: 22,
  },
  {
    id: 'glycemic',
    title: 'Metabolic & Blood-Sugar Management',
    tag: 'LOW-GI FORTIFICATION',
    summary: 'Lowers glycemic spike of starchy staples by blending slow-digesting legume protein.',
    targetGramsPerMeal: 28,
  },
];

export const STAPLE_VEHICLES = [
  { id: 'amala', name: 'Amala (Yam Flour)', baseProteinG: 2.1, servingG: 250 },
  { id: 'tuwo', name: 'Tuwo Shinkafa / Masara', baseProteinG: 3.4, servingG: 250 },
  { id: 'ogi', name: 'Ogi / Akamu Porridge', baseProteinG: 1.8, servingG: 300 },
  { id: 'eba', name: 'Eba / Garri Swallow', baseProteinG: 1.5, servingG: 250 },
];

// Dynamic AI Ranking Engine (simulates ESM-2 650M + Multi-Objective Decision Engine)
export function rankCropsForTarget({ targetId, customGoal = '', availableCropIds = [] }) {
  const pool =
    availableCropIds.length > 0
      ? AFRICAN_CROPS.filter((c) => availableCropIds.includes(c.id))
      : AFRICAN_CROPS;

  // Infer best scoring dimension if user typed a custom goal
  let effectiveKey = targetId || 'milk';
  const q = customGoal.toLowerCase();
  if (q) {
    if (q.includes('egg') || q.includes('cake') || q.includes('bake') || q.includes('moi')) effectiveKey = 'egg';
    else if (q.includes('meat') || q.includes('suya') || q.includes('burger') || q.includes('chew')) effectiveKey = 'meat';
    else if (q.includes('cheese') || q.includes('wara') || q.includes('tofu') || q.includes('curd')) effectiveKey = 'wara';
    else if (q.includes('yogurt') || q.includes('ferment')) effectiveKey = 'yogurt';
    else if (q.includes('amala') || q.includes('tuwo') || q.includes('ogi') || q.includes('swallow')) effectiveKey = 'fortify';
  }

  return [...pool]
    .map((crop) => {
      const matchScore = crop.scores[effectiveKey] || crop.scores.milk;
      const confidence = matchScore >= 90 ? 'High Confidence' : matchScore >= 82 ? 'Strong Match' : 'Moderate Match';
      return {
        ...crop,
        matchScore,
        confidence,
      };
    })
    .sort((a, b) => b.matchScore - a.matchScore);
}

export function formatLocalCurrency(nairaAmount, market) {
  const converted = Math.round(nairaAmount * market.multiplier);
  return `${market.symbol}${converted.toLocaleString()}`;
}