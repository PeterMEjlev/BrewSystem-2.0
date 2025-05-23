interface BrewData {
  BK_temp: number;
  MLT_temp: number;
  HLT_temp: number;
  BK_pot: "On" | "Off";
  HLT_pot: "On" | "Off";
  BK_reg: "On" | "Off";
  HLT_reg: "On" | "Off";
  Pump1: "On" | "Off";
  Pump2: "On" | "Off";
  Pump1_speed: string;
  Pump2_speed: string;
  BK_eff: string;
  HLT_eff: string;
}

async function fetchAndRender(): Promise<void> {
  try {
    const res = await fetch('/api/data');
    const d = (await res.json()) as BrewData;

    document.getElementById('bkTemp')!.textContent      = d.BK_temp.toFixed(1);
    document.getElementById('mltTemp')!.textContent     = d.MLT_temp.toFixed(1);
    document.getElementById('hltTemp')!.textContent     = d.HLT_temp.toFixed(1);

    document.getElementById('bkPot')!.textContent       = d.BK_pot;
    document.getElementById('hltPot')!.textContent      = d.HLT_pot;

    document.getElementById('bkReg')!.textContent       = d.BK_reg;
    document.getElementById('hltReg')!.textContent      = d.HLT_reg;

    document.getElementById('pump1')!.textContent       = d.Pump1;
    document.getElementById('pump2')!.textContent       = d.Pump2;

    document.getElementById('pump1Speed')!.textContent  = d.Pump1_speed;
    document.getElementById('pump2Speed')!.textContent  = d.Pump2_speed;

    document.getElementById('bkEff')!.textContent       = d.BK_eff;
    document.getElementById('hltEff')!.textContent      = d.HLT_eff;
  } catch (err) {
    console.error('Failed to fetch brew data:', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAndRender();
  setInterval(fetchAndRender, 10_000);
});
