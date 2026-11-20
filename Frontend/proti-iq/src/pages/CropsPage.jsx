import { useState } from 'react';

const CROPS_CATALOG = [
  {
    id: 'cowpea',
    commonName: 'Cowpea (Black-eyed pea)',
    scientificName: 'Vigna unguiculata',
    role: 'Candidate Staple',
    region: 'West Africa (Nigeria, Niger, Ghana)',
    protein: '23% - 26%',
    globulin: '7S Beta-vignin (Trimer)',
    status: 'Sequenced (45 UniProt entries)',
    summary: 'Drought-hardy pan-African staple. Low least gelation concentration and rapid thermal unfold make it ideal for scrambled egg replacers, Akara, and plant-based milks.'
  },
  {
    id: 'pigeon_pea',
    commonName: 'Pigeon Pea',
    scientificName: 'Cajanus cajan',
    role: 'Candidate Staple',
    region: 'West & East Africa (Nigeria, Kenya, Malawi)',
    protein: '21% - 25%',
    globulin: '7S Vicilin & 11S Legumin Balanced',
    status: 'Sequenced (87 UniProt entries)',
    summary: 'Deep-rooted perennial legume with high cysteine fraction. Unfolds into fibrous protein strands under thermal extrusion, making it the #1 match for textured meat (96.0%).'
  },
  {
    id: 'african_yam_bean',
    commonName: 'African Yam Bean',
    scientificName: 'Sphenostylis stenocarpa',
    role: 'Candidate Staple',
    region: 'West & Central Africa (Nigeria, Cameroon, DRC)',
    protein: '21% - 29%',
    globulin: '11S Legumin Hexameric Rich',
    status: 'Sequenced (28 UniProt entries)',
    summary: 'Underutilized indigenous tuber-legume. High hexamer density provides the firmest gelation (6.0% LGC) under 0.3% CaCl2 cross-linking, perfect for Awara cheese curd.'
  },
  {
    id: 'groundnut',
    commonName: 'Groundnut (Peanut)',
    scientificName: 'Arachis hypogaea',
    role: 'Candidate Staple',
    region: 'Pan-African (Nigeria, Senegal, Sudan)',
    protein: '25% - 28%',
    globulin: 'Arachin (11S) & Conarachin (7S)',
    status: 'Sequenced (52 UniProt entries)',
    summary: 'Widely cultivated oilseed. Defatted press-cake provides high-solubility emulsifying protein for plant-based mayonnaise and salad dressings.'
  },
  {
    id: 'bambara_groundnut',
    commonName: 'Bambara Groundnut',
    scientificName: 'Vigna subterranea',
    role: 'Candidate Staple',
    region: 'West & Southern Africa (Nigeria, Ghana, South Africa)',
    protein: '19% - 24%',
    globulin: '7S Vicilin & 11S Legumin',
    status: 'Tier 1 Wet-Lab Priority (0 UniProt entries)',
    summary: 'Extremely drought-resilient subterranean legume. Bypasses speculative sequence AI; verified empirically by Pretoria wet-lab data (82.27% solubility at pH 7).'
  },
  {
    id: 'african_locust_bean',
    commonName: 'African Locust Bean (Iru / Dawadawa)',
    scientificName: 'Parkia biglobosa',
    role: 'Orphan Expansion',
    region: 'West African Savannah Belt',
    protein: '30% - 35% (Fermented)',
    globulin: 'Hydrolyzed Umami Peptides (<1 kDa)',
    status: 'Biochemical Precedent',
    summary: 'Traditional alkaline fermented seasoning seed. High free glutamic acid and sulfurous peptides replicate the savory umami profile of dried river crayfish.'
  },
  {
    id: 'kerstings_groundnut',
    commonName: "Kersting's Groundnut",
    scientificName: 'Macrotyloma geocarpum',
    role: 'Orphan Expansion',
    region: 'West Africa (Benin, Togo, Nigeria)',
    protein: '19% - 22%',
    globulin: 'Storage Globulin Complex',
    status: 'Orphan',
    summary: 'Subterranean micro-legume cultivated by smallholder women farmers. High essential amino acid density suitable for regional nutrition fortification.'
  },
  {
    id: 'soybean',
    commonName: 'Soybean (Commercial Control)',
    scientificName: 'Glycine max',
    role: 'Commercial Benchmark',
    region: 'Global Benchmark',
    protein: '36% - 40%',
    globulin: '11S Glycinin & 7S Beta-conglycinin',
    status: 'Benchmark Control',
    summary: 'Global commercial standard used to benchmark industrial SPI texturization and tofu curds.'
  },
  {
    id: 'mung_bean',
    commonName: 'Mung Bean (Commercial Control)',
    scientificName: 'Vigna radiata',
    role: 'Commercial Benchmark',
    region: 'Global Benchmark',
    protein: '24% - 27%',
    globulin: '8S Vicilin (A0A1S3VZW2)',
    status: 'Benchmark Control',
    summary: 'Commercial control protein used in global commercial plant-based egg formulations (JUST Egg).'
  }
];

export default function CropsPage() {
  const [filterRole, setFilterRole] = useState('All');
  const roles = ['All', 'Candidate Staple', 'Orphan Expansion', 'Commercial Benchmark'];

  const filtered = filterRole === 'All'
    ? CROPS_CATALOG
    : CROPS_CATALOG.filter((c) => c.role === filterRole);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 border border-[#E5E7EB] shadow-xs">
        <h1 className="text-2xl font-bold text-[#111827] tracking-tight">
          Pan-African Legume & Commercial Benchmark Catalog
        </h1>
        <p className="mt-2 text-sm text-[#4B5563]">
          Master repository of 14 climate-resilient African candidates, underutilized orphan legumes, and commercial control benchmarks screened by the Proti IQ engine.
        </p>

        {/* Filter Badges */}
        <div className="flex flex-wrap gap-2 mt-4">
          {roles.map((r) => (
            <button
              key={r}
              type="button"
              onClick={() => setFilterRole(r)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition-all ${
                filterRole === r
                  ? 'bg-[#059669] text-white shadow-xs'
                  : 'bg-[#F3F4F6] text-[#4B5563] hover:bg-[#E5E7EB]'
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {/* Grid of Crop Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((crop) => (
          <div
            key={crop.id}
            className="bg-white rounded-2xl p-5 border border-[#E5E7EB] shadow-xs space-y-3"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-base text-[#111827]">{crop.commonName}</h3>
                <p className="text-xs italic text-[#6B7280]">{crop.scientificName}</p>
              </div>
              <span
                className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${
                  crop.role === 'Commercial Benchmark'
                    ? 'bg-[#EFF6FF] text-[#1D4ED8]'
                    : crop.role === 'Orphan Expansion'
                    ? 'bg-[#FEF3C7] text-[#92400E]'
                    : 'bg-[#ECFDF5] text-[#059669]'
                }`}
              >
                {crop.role}
              </span>
            </div>

            <p className="text-xs text-[#4B5563] leading-relaxed">
              {crop.summary}
            </p>

            <div className="grid grid-cols-2 gap-2 text-[11px] pt-3 border-t border-[#F3F4F6]">
              <div>
                <span className="text-[#6B7280] block">Protein Content:</span>
                <span className="font-semibold text-[#111827]">{crop.protein}</span>
              </div>
              <div>
                <span className="text-[#6B7280] block">Primary Globulin:</span>
                <span className="font-semibold text-[#111827]">{crop.globulin}</span>
              </div>
              <div>
                <span className="text-[#6B7280] block">Sequence Status:</span>
                <span className="font-semibold text-[#059669]">{crop.status}</span>
              </div>
              <div>
                <span className="text-[#6B7280] block">Geography:</span>
                <span className="text-[#111827]">{crop.region}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
