const { Plugin, MarkdownView } = require('obsidian');

const CHECKBOX_CYCLE = {
    '[ ]': '[-]',
    '[-]': '[x]',
    '[x]': '[ ]'
};

const SCORES = {
    '[ ]': 0.0,
    '[-]': 0.5,
    '[x]': 1.0
};

class PacrarTrackerPlugin extends Plugin {
    async onload() {
        // 1. Reading View Processor
        this.registerMarkdownPostProcessor((el, ctx) => {
            this.processPacrarSection(el, ctx);
        });

        // 2. Interactive DOM Click Listener (supports Reading View & Live Preview)
        this.registerDomEvent(document, 'click', (evt) => {
            this.handleCheckboxClick(evt);
        }, true);
    }

    processPacrarSection(el, ctx) {
        const tables = el.querySelectorAll('table');
        tables.forEach((table) => {
            const ths = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim().toUpperCase());
            if (ths.length === 7 && ths.slice(1).join(',') === 'P,A,C,R,A,R') {
                this.renderPacrarTable(table);
            }
        });
    }

    renderPacrarTable(table) {
        let totalScore = 0;
        const rows = table.querySelectorAll('tbody tr');
        const maxScore = rows.length * 6;

        rows.forEach((row) => {
            let rowScore = 0;
            const cells = row.querySelectorAll('td');
            for (let c = 1; c <= 6; c++) {
                const cell = cells[c];
                if (!cell) continue;
                const txt = cell.textContent.trim();
                if (txt in SCORES) {
                    const val = SCORES[txt];
                    rowScore += val;
                    totalScore += val;
                    cell.setAttribute('data-pacrar-state', txt === '[x]' ? 'completed' : txt === '[-]' ? 'partial' : 'empty');
                    cell.classList.add('pacrar-cell');
                }
            }
            if (cells[0]) {
                const rowPct = rowScore / 6;
                cells[0].style.borderLeft = `3px solid ${this.interpolateColor(rowPct)}`;
            }
        });

        const pct = maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0;
        this.mountSvgRing(table, pct, totalScore, maxScore);
    }

    interpolateColor(ratio) {
        // Linear RGB interpolation: 0.0 (red #ef4444) -> 0.5 (amber #f59e0b) -> 1.0 (green #22c55e)
        if (ratio < 0.5) {
            const f = ratio * 2;
            const r = Math.round(239 + (245 - 239) * f);
            const g = Math.round(68 + (158 - 68) * f);
            const b = Math.round(68 + (11 - 68) * f);
            return `rgb(${r}, ${g}, ${b})`;
        } else {
            const f = (ratio - 0.5) * 2;
            const r = Math.round(245 + (34 - 245) * f);
            const g = Math.round(158 + (197 - 158) * f);
            const b = Math.round(11 + (94 - 11) * f);
            return `rgb(${r}, ${g}, ${b})`;
        }
    }

    mountSvgRing(table, pct, totalScore, maxScore) {
        let container = table.parentElement.querySelector('.pacrar-progress-widget');
        if (!container) {
            container = document.createElement('div');
            container.className = 'pacrar-progress-widget';
            table.parentElement.insertBefore(container, table);
        }

        const r = 50;
        const circ = 2 * Math.PI * r;
        const offset = circ * (1 - pct / 100);
        const strokeColor = this.interpolateColor(pct / 100);

        container.innerHTML = `
            <div class="pacrar-ring-wrap">
                <svg width="120" height="120" viewBox="0 0 120 120">
                    <circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--background-modifier-border, #333)" stroke-width="4" />
                    <circle cx="60" cy="60" r="${r}" fill="none" stroke="${strokeColor}" stroke-width="4"
                            stroke-dasharray="${circ}" stroke-dashoffset="${offset}"
                            stroke-linecap="round" transform="rotate(-90 60 60)" style="transition: stroke-dashoffset 0.4s ease, stroke 0.4s ease;" />
                    <text x="60" y="56" text-anchor="middle" font-size="20" font-weight="bold" fill="var(--text-normal)">${pct}%</text>
                    <text x="60" y="74" text-anchor="middle" font-size="11" fill="var(--text-muted)">${totalScore} / ${maxScore} fasi</text>
                </svg>
            </div>
        `;
    }

    async handleCheckboxClick(evt) {
        const cell = evt.target.closest('td.pacrar-cell');
        if (!cell) return;
        const txt = cell.textContent.trim();
        if (!(txt in CHECKBOX_CYCLE)) return;

        evt.preventDefault();
        evt.stopPropagation();
        const next = CHECKBOX_CYCLE[txt];

        const view = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!view || !view.file) return;

        const file = view.file;
        const content = await this.app.vault.read(file);
        const row = cell.parentElement;
        const cellIdx = Array.from(row.children).indexOf(cell);
        const argCell = row.children[0];
        const argText = argCell.textContent.trim();

        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
            if (lines[i].includes(argText) && lines[i].includes('|')) {
                const parts = lines[i].split('|');
                if (parts.length >= 8 && parts[cellIdx].trim() === txt) {
                    parts[cellIdx] = ` ${next} `;
                    lines[i] = parts.join('|');
                    await this.app.vault.modify(file, lines.join('\n'));
                    break;
                }
            }
        }
    }
}

module.exports = PacrarTrackerPlugin;
module.exports.default = PacrarTrackerPlugin;
