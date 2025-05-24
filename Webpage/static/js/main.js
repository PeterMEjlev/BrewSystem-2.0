"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function fetchAndRender() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const res = yield fetch('/api/data');
            const d = (yield res.json());
            // BK card
            document.getElementById('bkPot').textContent = d.BK_pot;
            document.getElementById('bkEff').textContent = d.BK_eff;
            const bkTempEl = document.getElementById('bkTemp');
            bkTempEl.textContent =
                d.BK_reg === 'On'
                    ? `${d.BK_temp.toFixed(1)} / ${d.BK_regTemp.toFixed(1)}`
                    : d.BK_temp.toFixed(1);
            document.getElementById('bkReg').textContent = d.BK_reg;
            // BK indicator
            const bkInd = document.getElementById('bkIndicator');
            const bkOn = d.BK_pot === 'On';
            bkInd.classList.toggle('on', bkOn);
            bkInd.classList.toggle('off', !bkOn);
            // HLT card
            document.getElementById('hltPot').textContent = d.HLT_pot;
            document.getElementById('hltEff').textContent = d.HLT_eff;
            const hltTempEl = document.getElementById('hltTemp');
            hltTempEl.textContent =
                d.HLT_reg === 'On'
                    ? `${d.HLT_temp.toFixed(1)} / ${d.HLT_regTemp.toFixed(1)}`
                    : d.HLT_temp.toFixed(1);
            document.getElementById('hltReg').textContent = d.HLT_reg;
            // HLT indicator
            const hltInd = document.getElementById('hltIndicator');
            const hltOn = d.HLT_pot === 'On';
            hltInd.classList.toggle('on', hltOn);
            hltInd.classList.toggle('off', !hltOn);
            // MLT card (temp only)
            const mltTempEl = document.getElementById('mltTemp');
            mltTempEl.textContent = d.MLT_temp.toFixed(1);
            // Pump 1
            document.getElementById('pump1').textContent = d.Pump1;
            document.getElementById('pump1Speed').textContent = d.Pump1_speed;
            const p1Ind = document.getElementById('p1Indicator');
            const p1On = d.Pump1 === 'On';
            p1Ind.classList.toggle('on', p1On);
            p1Ind.classList.toggle('off', !p1On);
            // Pump 2
            document.getElementById('pump2').textContent = d.Pump2;
            document.getElementById('pump2Speed').textContent = d.Pump2_speed;
            const p2Ind = document.getElementById('p2Indicator');
            const p2On = d.Pump2 === 'On';
            p2Ind.classList.toggle('on', p2On);
            p2Ind.classList.toggle('off', !p2On);
        }
        catch (err) {
            console.error('Failed to fetch brew data:', err);
        }
    });
}
document.addEventListener('DOMContentLoaded', () => __awaiter(void 0, void 0, void 0, function* () {
    // load poll interval from server
    let interval = 10000; // default
    try {
        const resp = yield fetch('/api/config');
        if (resp.ok) {
            const cfg = (yield resp.json());
            interval = cfg.poll_interval;
        }
    }
    catch (e) {
        console.warn('Could not load poll interval, using default', e);
    }
    // initial render + schedule updates
    fetchAndRender();
    setInterval(fetchAndRender, interval);
}));
