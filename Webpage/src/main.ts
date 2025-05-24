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

    // Pots → BK
    document.getElementById('bkPot')!.textContent   = d.BK_pot;
    document.getElementById('bkEff')!.textContent   = d.BK_eff;
    document.getElementById('bkTemp')!.textContent  = d.BK_temp.toFixed(1);
    document.getElementById('bkReg')!.textContent   = d.BK_reg;
    document.getElementById('bkRegTemp')!.textContent  = d.BK_regTemp.toFixed(1);

    // toggle BK indicator
    const bkInd = document.getElementById('bkIndicator')!;
    if (d.BK_pot === 'On') {
      bkInd.classList.add('on');
      bkInd.classList.remove('off');
    } else {
      bkInd.classList.add('off');
      bkInd.classList.remove('on');
    }

    // Pots → HLT
    document.getElementById('hltPot')!.textContent  = d.HLT_pot;
    document.getElementById('hltEff')!.textContent  = d.HLT_eff;
    document.getElementById('hltTemp')!.textContent = d.HLT_temp.toFixed(1);
    document.getElementById('hltReg')!.textContent  = d.HLT_reg;
    document.getElementById('hltRegTemp')!.textContent  = d.HLT_regTemp.toFixed(1);


    // toggle HLT indicator
    const hltInd = document.getElementById('hltIndicator')!;
    if (d.HLT_pot === 'On') {
      hltInd.classList.add('on');
      hltInd.classList.remove('off');
    } else {
      hltInd.classList.add('off');
      hltInd.classList.remove('on');
    }

    // Pots → MLT (temp only)
    document.getElementById('mltTemp')!.textContent = d.MLT_temp.toFixed(1);

    // Pumps → P1
    document.getElementById('pump1')!.textContent      = d.Pump1;
    document.getElementById('pump1Speed')!.textContent = d.Pump1_speed;

    // toggle P1 indicator
    const p1Ind = document.getElementById('p1Indicator')!;
    if (d.Pump1 === 'On') {
      p1Ind.classList.add('on');
      p1Ind.classList.remove('off');
    } else {
      p1Ind.classList.add('off');
      p1Ind.classList.remove('on');
    }

    // Pumps → P2
    document.getElementById('pump2')!.textContent      = d.Pump2;
    document.getElementById('pump2Speed')!.textContent = d.Pump2_speed;

    // toggle P2 indicator
    const p2Ind = document.getElementById('p2Indicator')!;
    if (d.Pump2 === 'On') {
      p2Ind.classList.add('on');
      p2Ind.classList.remove('off');
    } else {
      p2Ind.classList.add('off');
      p2Ind.classList.remove('on');
    }

  } catch (err) {
    console.error('Failed to fetch brew data:', err);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  // 1) load the polling interval from Flask
  let interval = 10000; // fallback
  try {
    const resp = await fetch('/api/config');
    if (resp.ok) {
      const cfg = (await resp.json()) as { poll_interval: number };
      interval = cfg.poll_interval;
    }
  } catch (e) {
    console.warn('Could not load poll interval, using default', e);
  }

  // 2) do the first data fetch, then schedule subsequent fetches
  fetchAndRender();
  setInterval(fetchAndRender, interval);
});
