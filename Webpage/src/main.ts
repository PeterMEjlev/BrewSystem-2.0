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

    // Pots → BK
    document.getElementById('bkPot')!.textContent      = d.BK_pot;
    document.getElementById('bkEff')!.textContent      = d.BK_eff;
    document.getElementById('bkTemp')!.textContent     = d.BK_temp.toFixed(1);
    document.getElementById('bkReg')!.textContent      = d.BK_reg;

    // Pots → HLT
    document.getElementById('hltPot')!.textContent     = d.HLT_pot;
    document.getElementById('hltEff')!.textContent     = d.HLT_eff;
    document.getElementById('hltTemp')!.textContent    = d.HLT_temp.toFixed(1);
    document.getElementById('hltReg')!.textContent     = d.HLT_reg;

    // Pots → MLT (temp only)
    document.getElementById('mltTemp')!.textContent    = d.MLT_temp.toFixed(1);

    // Pumps
    document.getElementById('pump1')!.textContent      = d.Pump1;
    document.getElementById('pump1Speed')!.textContent = d.Pump1_speed;
    document.getElementById('pump2')!.textContent      = d.Pump2;
    document.getElementById('pump2Speed')!.textContent = d.Pump2_speed;

  } catch (err) {
    console.error('Failed to fetch brew data:', err);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  // 1) load the polling interval from Flask
  let interval = 10000;                        // fallback
  try {
    const resp = await fetch('/api/config');
    if (resp.ok) {
      const cfg = await resp.json() as { poll_interval: number };
      interval = cfg.poll_interval;
    }
  } catch (e) {
    console.warn('Could not load poll interval, using default', e);
  }

  // 2) do the first data fetch, then schedule subsequent fetches
  fetchAndRender();
  setInterval(fetchAndRender, interval);
});
