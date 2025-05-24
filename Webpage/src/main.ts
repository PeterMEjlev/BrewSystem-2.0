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
  BK_regTemp: number;
  HLT_regTemp: number;
}

async function fetchAndRender(): Promise<void> {
  try {
    const res = await fetch('/api/data');
    const d = (await res.json()) as BrewData;

    // BK card
    document.getElementById('bkPot')!.textContent  = d.BK_pot;
    document.getElementById('bkEff')!.textContent  = d.BK_eff;
    // Temperature: actual / set-point if regulator on
    const bkTempEl = document.getElementById('bkTemp')!;
    bkTempEl.textContent = d.BK_reg === 'On'
      ? `${d.BK_temp.toFixed(1)} / ${d.BK_regTemp.toFixed(1)}`
      : d.BK_temp.toFixed(1);
    document.getElementById('bkReg')!.textContent = d.BK_reg;
    // indicator pill
    document.getElementById('bkIndicator')!
      .classList.toggle('on', d.BK_pot === 'On');

    // HLT card
    document.getElementById('hltPot')!.textContent  = d.HLT_pot;
    document.getElementById('hltEff')!.textContent  = d.HLT_eff;
    const hltTempEl = document.getElementById('hltTemp')!;
    hltTempEl.textContent = d.HLT_reg === 'On'
      ? `${d.HLT_temp.toFixed(1)} / ${d.HLT_regTemp.toFixed(1)}`
      : d.HLT_temp.toFixed(1);
    document.getElementById('hltReg')!.textContent = d.HLT_reg;
    document.getElementById('hltIndicator')!
      .classList.toggle('on', d.HLT_pot === 'On');

    // MLT pot
    document.getElementById('mltTemp')!.textContent = d.MLT_temp.toFixed(1);

    // Pump 1
    document.getElementById('pump1')!.textContent      = d.Pump1;
    document.getElementById('pump1Speed')!.textContent = d.Pump1_speed;
    document.getElementById('p1Indicator')!
      .classList.toggle('on', d.Pump1 === 'On');

    // Pump 2
    document.getElementById('pump2')!.textContent      = d.Pump2;
    document.getElementById('pump2Speed')!.textContent = d.Pump2_speed;
    document.getElementById('p2Indicator')!
      .classList.toggle('on', d.Pump2 === 'On');

  } catch (err) {
    console.error('Failed to fetch brew data:', err);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  // Load poll interval
  let interval = 10000;
  try {
    const resp = await fetch('/api/config');
    if (resp.ok) {
      const cfg = await resp.json() as { poll_interval: number };
      interval = cfg.poll_interval;
    }
  } catch {}

  // First fetch + schedule
  fetchAndRender();
  setInterval(fetchAndRender, interval);
});
