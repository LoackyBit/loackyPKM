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
        // 1. Reading View Markdown Post Processor
        this.registerMarkdownPostProcessor((el, ctx) => {
            this.processPacrarSection(el, ctx);
        });

        // 2. Interactive DOM Click Listener (supports Reading View & Live Preview)
        this.registerDomEvent(document, 'click', (evt) => {
            this.handleCheckboxClick(evt);
        }, true);

        // 3. Periodic and Layout Change Scanner for Live Preview
        this.registerEvent(this.app.workspace.on('layout-change', () => {
            this.scanAndRenderPacrarTables();
        }));
        this.registerInterval(window.setInterval(() => {
            this.scanAndRenderPacrarTables();
        }, 2000));
    }

    scanAndRenderPacrarTables() {
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!activeView || !activeView.contentEl) return;
        const tables = activeView.contentEl.querySelectorAll('table');
        tables.forEach((table) => {
            const ths = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim().toUpperCase());
            if (ths.length === 7 && ths.slice(1).join(',') === 'P,A,C,R,A,R') {
                this.renderPacrarTable(table);
            }
        });
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
                    const state = txt === '[x]' ? 'completed' : txt === '[-]' ? 'partial' : 'empty';
                    cell.setAttribute('data-pacrar-state', state);
                    cell.classList.add('pacrar-cell');
                    if (state === 'completed') {
                        cell.style.setProperty('background-color', 'rgba(34, 197, 94, 0.22)', 'important');
                        cell.style.setProperty('color', '#22c55e', 'important');
                    } else if (state === 'partial') {
                        cell.style.setProperty('background-color', 'rgba(245, 158, 11, 0.22)', 'important');
                        cell.style.setProperty('color', '#f59e0b', 'important');
                    } else {
                        cell.style.setProperty('background-color', 'rgba(239, 68, 68, 0.15)', 'important');
                        cell.style.setProperty('color', '#ef4444', 'important');
                    }
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
        // Find existing container in prior sibling or parent
        let container = table.previousElementSibling;
        if (!container || !container.classList.contains('pacrar-progress-widget')) {
            container = table.parentElement ? table.parentElement.querySelector('.pacrar-progress-widget') : null;
        }
        if (!container && table.parentElement) {
            container = document.createElement('div');
            container.className = 'pacrar-progress-widget';
            table.parentElement.insertBefore(container, table);
        }
        if (!container) return;

        if (maxScore === 0) {
            container.innerHTML = `
                <div class="pacrar-ring-wrap" style="color: var(--text-muted); font-size: 0.85em; padding: 0.5rem; text-align: center;">
                    <em>Matrice PACRAR pronta — In attesa di lezioni caricate</em>
                </div>
            `;
            return;
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
        const cell = evt.target.closest('td');
        if (!cell) return;
        const txt = cell.textContent.trim();
        if (!(txt in CHECKBOX_CYCLE)) return;

        const table = cell.closest('table');
        if (!table) return;
        const ths = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim().toUpperCase());
        if (ths.length !== 7 || ths.slice(1).join(',') !== 'P,A,C,R,A,R') return;

        const row = cell.parentElement;
        const cellIdx = Array.from(row.children).indexOf(cell);
        if (cellIdx < 1 || cellIdx > 6) return;

        evt.preventDefault();
        evt.stopPropagation();
        const next = CHECKBOX_CYCLE[txt];

        const view = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!view || !view.file) return;

        const file = view.file;
        const content = await this.app.vault.read(file);

        const argCell = row.children[0];
        const argText = argCell.textContent.trim();

        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (!line.includes('|')) continue;
            if (!line.toLowerCase().includes(argText.toLowerCase())) continue;

            const parts = line.split('|');
            const hasLeadingPipe = line.trim().startsWith('|');
            const targetPartIdx = hasLeadingPipe ? cellIdx + 1 : cellIdx;

            if (targetPartIdx < parts.length && parts[targetPartIdx].trim() === txt) {
                parts[targetPartIdx] = ` ${next} `;
                lines[i] = parts.join('|');
                await this.app.vault.modify(file, lines.join('\n'));
                break;
            }
        }
    }
}

module.exports = PacrarTrackerPlugin;
module.exports.default = PacrarTrackerPlugin;
