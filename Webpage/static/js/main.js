"use strict";
// static/js/main.ts
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
            // ─── BK card ──────────────────────────────────────────────────────────
            document.getElementById('bkPot').textContent = d.BK_pot;
            document.getElementById('bkEff').textContent = d.BK_eff;
            const bkTempEl = document.getElementById('bkTemp');
            bkTempEl.textContent =
                d.BK_reg === 'On'
                    ? `${d.BK_temp.toFixed(1)} / ${d.BK_regTemp.toFixed(1)}`
                    : d.BK_temp.toFixed(1);
            document.getElementById('bkReg').textContent = d.BK_reg;
            // BK indicator: green gradient if we've reached set-temp while REG is on,
            // red gradient if REG is on but not yet reached, grey if REG is off.
            const bkInd = document.getElementById('bkIndicator');
            if (d.BK_reg === 'On') {
                bkInd.classList.toggle('reached', d.set_temp_reached_BK);
                bkInd.classList.toggle('on', !d.set_temp_reached_BK);
                bkInd.classList.remove('off');
            }
            else {
                bkInd.classList.add('off');
                bkInd.classList.remove('on', 'reached');
            }
            // ─── HLT card ─────────────────────────────────────────────────────────
            document.getElementById('hltPot').textContent = d.HLT_pot;
            document.getElementById('hltEff').textContent = d.HLT_eff;
            const hltTempEl = document.getElementById('hltTemp');
            hltTempEl.textContent =
                d.HLT_reg === 'On'
                    ? `${d.HLT_temp.toFixed(1)} / ${d.HLT_regTemp.toFixed(1)}`
                    : d.HLT_temp.toFixed(1);
            document.getElementById('hltReg').textContent = d.HLT_reg;
            // HLT indicator: same logic as BK
            const hltInd = document.getElementById('hltIndicator');
            if (d.HLT_reg === 'On') {
                hltInd.classList.toggle('reached', d.set_temp_reached_HLT);
                hltInd.classList.toggle('on', !d.set_temp_reached_HLT);
                hltInd.classList.remove('off');
            }
            else {
                hltInd.classList.add('off');
                hltInd.classList.remove('on', 'reached');
            }
            // ─── MLT card (temp only) ──────────────────────────────────────────────
            document.getElementById('mltTemp').textContent = d.MLT_temp.toFixed(1);
            // ─── PUMPS ─────────────────────────────────────────────────────────────
            document.getElementById('pump1').textContent = d.Pump1;
            document.getElementById('pump1Speed').textContent = d.Pump1_speed;
            const p1Ind = document.getElementById('p1Indicator');
            if (d.Pump1 === 'On') {
                p1Ind.classList.add('on');
                p1Ind.classList.remove('off');
            }
            else {
                p1Ind.classList.add('off');
                p1Ind.classList.remove('on');
            }
            document.getElementById('pump2').textContent = d.Pump2;
            document.getElementById('pump2Speed').textContent = d.Pump2_speed;
            const p2Ind = document.getElementById('p2Indicator');
            if (d.Pump2 === 'On') {
                p2Ind.classList.add('on');
                p2Ind.classList.remove('off');
            }
            else {
                p2Ind.classList.add('off');
                p2Ind.classList.remove('on');
            }
        }
        catch (err) {
            console.error('Failed to fetch brew data:', err);
        }
    });
}
document.addEventListener('DOMContentLoaded', () => __awaiter(void 0, void 0, void 0, function* () {
    // 1) grab poll interval from Flask
    let interval = 10000;
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
    // 2) initial fetch + schedule
    fetchAndRender();
    setInterval(fetchAndRender, interval);
}));
