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
            // ─── BK card ────────────────────────────────────────────
            document.getElementById('bkEff').textContent = d.BK_eff.replace('%', '');
            document.getElementById('bkTemp').textContent =
                d.BK_reg === 'On'
                    ? `${d.BK_temp.toFixed(1)} / ${d.BK_regTemp.toFixed(1)}`
                    : d.BK_temp.toFixed(1);
            document.getElementById('bkReg').textContent = d.BK_reg;
            const BKTimerNum = d.timer_progress_BK.replace(/min$/, '');
            document.getElementById('timerBK').textContent = BKTimerNum;
            const bkInd = document.getElementById('bkIndicator');
            if (d.BK_reg === 'On' && d.set_temp_reached_BK) {
                bkInd.classList.add('reached');
                bkInd.classList.remove('on', 'off');
            }
            else if (d.BK_pot === 'On') {
                bkInd.classList.add('on');
                bkInd.classList.remove('reached', 'off');
            }
            else {
                bkInd.classList.add('off');
                bkInd.classList.remove('on', 'reached');
            }
            // ─── HLT card ────────────────────────────────────────────
            document.getElementById('hltEff').textContent = d.HLT_eff.replace('%', '');
            document.getElementById('hltTemp').textContent =
                d.HLT_reg === 'On'
                    ? `${d.HLT_temp.toFixed(1)} / ${d.HLT_regTemp.toFixed(1)}`
                    : d.HLT_temp.toFixed(1);
            document.getElementById('hltReg').textContent = d.HLT_reg;
            const hltInd = document.getElementById('hltIndicator');
            if (d.HLT_reg === 'On' && d.set_temp_reached_HLT) {
                hltInd.classList.add('reached');
                hltInd.classList.remove('on', 'off');
            }
            else if (d.HLT_pot === 'On') {
                hltInd.classList.add('on');
                hltInd.classList.remove('reached', 'off');
            }
            else {
                hltInd.classList.add('off');
                hltInd.classList.remove('on', 'reached');
            }
            // ─── MLT card ────────────────────────────────────────────
            document.getElementById('mltTemp').textContent = d.MLT_temp.toFixed(1);
            const mltTimerNum = d.timer_progress_MLT.replace(/min$/, '');
            document.getElementById('timerMLT').textContent = mltTimerNum;
            // ─── PUMP 1 ─────────────────────────────────────────────
            // strip off trailing '%' since html now adds it
            document.getElementById('pump1Speed').textContent = d.Pump1_speed.replace('%', '');
            const p1Ind = document.getElementById('p1Indicator');
            if (d.Pump1 === 'On') {
                p1Ind.classList.add('reached');
                p1Ind.classList.remove('off', 'on');
            }
            else {
                p1Ind.classList.add('off');
                p1Ind.classList.remove('on', 'reached');
            }
            // ─── PUMP 2 ─────────────────────────────────────────────
            document.getElementById('pump2Speed').textContent = d.Pump2_speed.replace('%', '');
            const p2Ind = document.getElementById('p2Indicator');
            if (d.Pump2 === 'On') {
                p2Ind.classList.add('reached');
                p2Ind.classList.remove('off', 'on');
            }
            else {
                p2Ind.classList.add('off');
                p2Ind.classList.remove('on', 'reached');
            }
        }
        catch (err) {
            console.error('Failed to fetch brew data:', err);
        }
    });
}
document.addEventListener('DOMContentLoaded', () => __awaiter(void 0, void 0, void 0, function* () {
    let interval = 10000;
    try {
        const resp = yield fetch('/api/config');
        if (resp.ok) {
            const cfg = yield resp.json();
            interval = cfg.poll_interval;
        }
    }
    catch (_a) {
        /* use default */
    }
    fetchAndRender();
    setInterval(fetchAndRender, interval);
}));
