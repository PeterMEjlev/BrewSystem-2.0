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
            // Pots → BK
            document.getElementById('bkPot').textContent = d.BK_pot;
            document.getElementById('bkEff').textContent = d.BK_eff;
            document.getElementById('bkTemp').textContent = d.BK_temp.toFixed(1);
            document.getElementById('bkReg').textContent = d.BK_reg;
            // Pots → HLT
            document.getElementById('hltPot').textContent = d.HLT_pot;
            document.getElementById('hltEff').textContent = d.HLT_eff;
            document.getElementById('hltTemp').textContent = d.HLT_temp.toFixed(1);
            document.getElementById('hltReg').textContent = d.HLT_reg;
            // Pots → MLT (temp only)
            document.getElementById('mltTemp').textContent = d.MLT_temp.toFixed(1);
            // Pumps
            document.getElementById('pump1').textContent = d.Pump1;
            document.getElementById('pump1Speed').textContent = d.Pump1_speed;
            document.getElementById('pump2').textContent = d.Pump2;
            document.getElementById('pump2Speed').textContent = d.Pump2_speed;
        }
        catch (err) {
            console.error('Failed to fetch brew data:', err);
        }
    });
}
document.addEventListener('DOMContentLoaded', () => __awaiter(void 0, void 0, void 0, function* () {
    // 1) load the polling interval from Flask
    let interval = 10000; // fallback
    try {
        const resp = yield fetch('/api/config');
        if (resp.ok) {
            const cfg = yield resp.json();
            interval = cfg.poll_interval;
        }
    }
    catch (e) {
        console.warn('Could not load poll interval, using default', e);
    }
    // 2) do the first data fetch, then schedule subsequent fetches
    fetchAndRender();
    setInterval(fetchAndRender, interval);
}));
