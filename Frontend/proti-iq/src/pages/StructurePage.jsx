import { useState } from 'react';

const STRUCTURE_BENCHMARKS = [
  {
    accession: 'A0A1S3VZW2',
    name: 'Mung Bean 8S Vicilin',
    crop: 'Vigna radiata (Mung Bean)',
    role: 'Plant-Based Egg Benchmark (JUST Egg control)',
    family: '7S Vicilin Trimer',
    plddtMean: 78.5,
    cysteines: '0.0%',
    mw: '52.3 kDa',
    description: 'Trimeric cupin fold without covalent disulfide bridges. Undergoes rapid cooperative thermal unfolding at 75°C-85°C to form an elastic heat-set gel network.',
    pdbUrl: 'https://alphafold.ebi.ac.uk/files/AF-A0A1S3VZW2-F1-model_v6.pdb'
  },
  {
    accession: 'P02858',
    name: 'Soybean 11S Glycinin G4',
    crop: 'Glycine max (Soybean)',
    role: 'Textured Meat & Awara Curd Benchmark',
    family: '11S Legumin Hexamer',
    plddtMean: 80.3,
    cysteines: '1.4%',
    mw: '61.2 kDa (Acidic + Basic subunit pair)',
    description: 'High-density hexameric cylinder held by interchain disulfide bonds. In meat analogs and Awara curd, thermal shear unfolds the hexamers for divalent calcium cross-linking.',
    pdbUrl: 'https://alphafold.ebi.ac.uk/files/AF-P02858-F1-model_v6.pdb'
  },
  {
    accession: 'P11827',
    name: 'Soybean 7S Beta-conglycinin alpha',
    crop: 'Glycine max (Soybean)',
    role: 'Plant Milk & Mayo Emulsion Benchmark',
    family: '7S Vicilin Trimer',
    plddtMean: 75.9,
    cysteines: '0.2%',
    mw: '67.0 kDa',
    description: 'Highly soluble globulin with high net-negative surface charge at neutral pH, providing strong electrostatic repulsion for colloidal stability in plant-based milks.',
    pdbUrl: 'https://alphafold.ebi.ac.uk/files/AF-P11827-F1-model_v6.pdb'
  }
];

export default function StructurePage() {
  const [selectedAcc, setSelectedAcc] = useState('P02858');
  const active = STRUCTURE_BENCHMARKS.find((s) => s.accession === selectedAcc) || STRUCTURE_BENCHMARKS[0];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 border border-[#E5E7EB] shadow-xs">
        <h1 className="text-2xl font-bold text-[#111827] tracking-tight">
          AlphaFold 2 3D Molecular Topology & Structural Confidence
        </h1>
        <p className="mt-2 text-sm text-[#4B5563]">
          Biophysical verification of target benchmark storage globulins. Inspect 3D backbone coordinates and per-residue pLDDT confidence scores derived from DeepMind AlphaFold DB v6.
        </p>

        {/* Accession Switcher */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-5">
          {STRUCTURE_BENCHMARKS.map((item) => (
            <button
              key={item.accession}
              type="button"
              onClick={() => setSelectedAcc(item.accession)}
              className={`p-4 rounded-xl text-left border transition-all ${
                selectedAcc === item.accession
                  ? 'border-[#059669] bg-[#ECFDF5] shadow-xs'
                  : 'border-[#E5E7EB] bg-[#FAF9F6] hover:border-[#D1D5DB]'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded bg-white border border-[#E5E7EB] text-[#059669]">
                  {item.accession}
                </span>
                <span className="text-xs font-semibold text-[#059669]">
                  {item.plddtMean} pLDDT
                </span>
              </div>
              <h3 className="mt-2 font-semibold text-sm text-[#111827]">{item.name}</h3>
              <p className="text-xs text-[#6B7280] mt-1">{item.role}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Active Molecule Details & 3D Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Metadata & Biophysical Details */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-white rounded-2xl p-6 border border-[#E5E7EB] shadow-xs space-y-4">
            <h2 className="text-lg font-bold text-[#111827]">{active.name}</h2>
            <div className="text-xs text-[#4B5563] space-y-2">
              <div className="flex justify-between py-1.5 border-b border-[#F3F4F6]">
                <span className="font-medium text-[#6B7280]">UniProt Accession</span>
                <span className="font-mono font-semibold text-[#111827]">{active.accession}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-[#F3F4F6]">
                <span className="font-medium text-[#6B7280]">Source Organism</span>
                <span className="italic text-[#111827]">{active.crop}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-[#F3F4F6]">
                <span className="font-medium text-[#6B7280]">Globulin Family</span>
                <span className="font-semibold text-[#111827]">{active.family}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-[#F3F4F6]">
                <span className="font-medium text-[#6B7280]">Mean pLDDT Confidence</span>
                <span className="font-bold text-[#059669]">{active.plddtMean} / 100</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-[#F3F4F6]">
                <span className="font-medium text-[#6B7280]">Cysteine Proportion</span>
                <span className="font-mono text-[#111827]">{active.cysteines}</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="font-medium text-[#6B7280]">Molecular Weight</span>
                <span className="font-mono text-[#111827]">{active.mw}</span>
              </div>
            </div>

            <p className="text-xs text-[#4B5563] leading-relaxed pt-2 border-t border-[#F3F4F6]">
              {active.description}
            </p>

            {/* pLDDT Legend */}
            <div className="pt-3 border-t border-[#F3F4F6]">
              <h4 className="text-xs font-semibold text-[#374151] mb-2">AlphaFold Confidence Key:</h4>
              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-[#0053D6]"></span>
                  <span>Very High (pLDDT &gt; 90)</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-[#65CBF3]"></span>
                  <span>Confident (70 - 90)</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-[#FFDB13]"></span>
                  <span>Low (50 - 70)</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-[#FF7D45]"></span>
                  <span>Disordered (&lt; 50)</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Embedded Interactive 3D Viewer */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-4 border border-[#E5E7EB] shadow-xs flex flex-col items-center justify-center min-h-[420px]">
          <div className="w-full flex justify-between items-center px-2 pb-3 border-b border-[#F3F4F6]">
            <span className="text-xs font-semibold text-[#111827]">
              AlphaFold Structure: {active.accession}
            </span>
            <a
              href={active.pdbUrl}
              target="_blank"
              rel="noreferrer"
              className="text-xs font-medium text-[#059669] hover:underline"
            >
              Download PDB (.pdb)
            </a>
          </div>

          <div className="w-full h-[360px] rounded-xl overflow-hidden mt-3 bg-[#0F172A] relative flex items-center justify-center">
            {/* Embedded 3Dmol Interactive Canvas */}
            <iframe
              title={`AlphaFold 3D Viewer for ${active.accession}`}
              src={`https://embed.plip-tool.biotec.tu-dresden.de/view?pdb=${active.accession}&style=cartoon`}
              className="w-full h-full border-0 rounded-xl"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
            {/* Fallback Overlay Info */}
            <div className="absolute bottom-3 left-3 bg-[#1E293B]/90 backdrop-blur-xs text-white text-[11px] px-3 py-1.5 rounded-lg border border-slate-700 pointer-events-none">
              Residues colored by AlphaFold pLDDT confidence (Blue = High, Yellow = Flexible)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
