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
            document.getElementById('bkTemp').textContent = d.BK_temp.toFixed(1);
            document.getElementById('mltTemp').textContent = d.MLT_temp.toFixed(1);
            document.getElementById('hltTemp').textContent = d.HLT_temp.toFixed(1);
            document.getElementById('bkPot').textContent = d.BK_pot;
            document.getElementById('hltPot').textContent = d.HLT_pot;
            document.getElementById('bkReg').textContent = d.BK_reg;
            document.getElementById('hltReg').textContent = d.HLT_reg;
            document.getElementById('pump1').textContent = d.Pump1;
            document.getElementById('pump2').textContent = d.Pump2;
            document.getElementById('pump1Speed').textContent = d.Pump1_speed;
            document.getElementById('pump2Speed').textContent = d.Pump2_speed;
            document.getElementById('bkEff').textContent = d.BK_eff;
            document.getElementById('hltEff').textContent = d.HLT_eff;
        }
        catch (err) {
            console.error('Failed to fetch brew data:', err);
        }
    });
}
document.addEventListener('DOMContentLoaded', () => {
    fetchAndRender();
    setInterval(fetchAndRender, 10000);
});
