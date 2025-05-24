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
  Pump1_speed: string;    // e.g. "25%"
  Pump2_speed: string;    // e.g. "100%"
  BK_eff: string;         // e.g. "100%"
  HLT_eff: string;        // e.g. "36%"
  BK_regTemp: number;
  HLT_regTemp: number;
  set_temp_reached_BK: boolean;
  set_temp_reached_HLT: boolean;
  timer_progress_MLT: number;
  timer_progress_BK: number;
}

async function fetchAndRender(): Promise<void> {
  try {
    const res = await fetch('/api/data');
    const d = (await res.json()) as BrewData;

    // BK
    document.getElementById('bkEff')!.textContent      = parseFloat(d.BK_eff).toFixed(0);
    (document.getElementById('bkTemp')!).textContent   =
      d.BK_reg === 'On'
        ? `${d.BK_temp.toFixed(1)} / ${d.BK_regTemp.toFixed(1)}`
        : d.BK_temp.toFixed(1);
    document.getElementById('bkReg')!.textContent      = d.BK_reg;
    document.getElementById('timerBK')!.textContent    = d.timer_progress_BK.toFixed(0);

    const bkInd = document.getElementById('bkIndicator')!;
    if (d.BK_reg === 'On' && d.set_temp_reached_BK) {
      bkInd.classList.add('reached'); bkInd.classList.remove('on','off');
    } else if (d.BK_pot === 'On' && !d.set_temp_reached_BK) {
      bkInd.classList.add('on');      bkInd.classList.remove('reached','off');
    } else {
      bkInd.classList.add('off');     bkInd.classList.remove('on','reached');
    }

    // HLT
    document.getElementById('hltEff')!.textContent     = parseFloat(d.HLT_eff).toFixed(0);
    (document.getElementById('hltTemp')!).textContent  =
      d.HLT_reg === 'On'
        ? `${d.HLT_temp.toFixed(1)} / ${d.HLT_regTemp.toFixed(1)}`
        : d.HLT_temp.toFixed(1);
    document.getElementById('hltReg')!.textContent     = d.HLT_reg;

    const hltInd = document.getElementById('hltIndicator')!;
    if (d.HLT_reg === 'On' && d.set_temp_reached_HLT) {
      hltInd.classList.add('reached'); hltInd.classList.remove('on','off');
    } else if (d.HLT_pot === 'On' && !d.set_temp_reached_HLT) {
      hltInd.classList.add('on');      hltInd.classList.remove('reached','off');
    } else {
      hltInd.classList.add('off');     hltInd.classList.remove('on','reached');
    }

    // MLT
    document.getElementById('mltTemp')!.textContent    = d.MLT_temp.toFixed(1);
    document.getElementById('timerMLT')!.textContent   = d.timer_progress_MLT.toFixed(0);

    // P1
    document.getElementById('pump1Speed')!.textContent = parseFloat(d.Pump1_speed).toFixed(0);
    const p1Ind = document.getElementById('p1Indicator')!;
    if (d.Pump1 === 'On') {
      p1Ind.classList.add('reached'); p1Ind.classList.remove('off','on');
    } else {
      p1Ind.classList.add('off');     p1Ind.classList.remove('on','reached');
    }

    // P2
    document.getElementById('pump2Speed')!.textContent = parseFloat(d.Pump2_speed).toFixed(0);
    const p2Ind = document.getElementById('p2Indicator')!;
    if (d.Pump2 === 'On') {
      p2Ind.classList.add('reached'); p2Ind.classList.remove('off','on');
    } else {
      p2Ind.classList.add('off');     p2Ind.classList.remove('on','reached');
    }

  } catch (err) {
    console.error('Failed to fetch brew data:', err);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  let interval = 10000;
  try {
    const resp = await fetch('/api/config');
    if (resp.ok) {
      const cfg = await resp.json() as { poll_interval: number };
      interval = cfg.poll_interval;
    }
  } catch {/* fallback */}

  fetchAndRender();
  setInterval(fetchAndRender, interval);
});
