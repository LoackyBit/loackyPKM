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

function isPacrarTable(table) {
    if (!table) return false;
    const headerRow = table.querySelector('thead tr') || table.querySelector('tr');
    if (!headerRow) return false;
    const ths = Array.from(headerRow.querySelectorAll('th, td')).map(el => el.textContent.trim().toUpperCase());
    return ths.length >= 7 && ths.slice(1, 7).join(',') === 'P,A,C,R,A,R';
}

function extractCheckboxState(cell) {
    if (!cell) return null;
    const txt = cell.textContent || '';
    if (txt.includes('[x]') || txt.includes('[X]')) return '[x]';
    if (txt.includes('[-]')) return '[-]';
    if (txt.includes('[ ]')) return '[ ]';
    const input = cell.querySelector('input[type="checkbox"]');
    if (input) {
        if (input.indeterminate) return '[-]';
        return input.checked ? '[x]' : '[ ]';
    }
    return null;
}

function extractLessonKey(text) {
    if (!text) return '';
    let clean = text.trim();
    const match = clean.match(/\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]/);
    if (match) {
        clean = match[1];
    }
    clean = clean.replace(/[*_`]/g, '').trim().toLowerCase();
    return clean;
}

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
        this.registerEvent(this.app.workspace.on('active-leaf-change', () => {
            this.scanAndRenderPacrarTables();
        }));
        this.registerEvent(this.app.vault.on('modify', (file) => {
            if (file && file.path && file.path.startsWith('01 - Map of Content/')) {
                this.scanAndRenderPacrarTables();
            }
        }));
        this.registerInterval(window.setInterval(() => {
            this.scanAndRenderPacrarTables();
        }, 1500));
    }

    scanAndRenderPacrarTables() {
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!activeView || !activeView.contentEl) return;
        this.renderAllPacrar(activeView.contentEl);
    }

    processPacrarSection(el, ctx) {
        if (!el) return;
        if (el.querySelector('table') || el.querySelector('.pacrar-progress-widget') || (el.classList && el.classList.contains('pacrar-progress-widget'))) {
            const root = el.closest('.markdown-rendered, .markdown-preview-view') || el.parentElement || el;
            this.renderAllPacrar(root);
        }
    }

    renderAllPacrar(rootEl) {
        if (!rootEl) return;
        const allTables = Array.from(rootEl.querySelectorAll('table'));
        const pacrarTables = allTables.filter(isPacrarTable);
        if (pacrarTables.length === 0) return;

        // 1. Style every table's cells & borders and collect stats
        const tableStats = pacrarTables.map(table => this.stylePacrarTable(table));

        // 2. Discover all widgets present in the container
        const widgets = Array.from(rootEl.querySelectorAll('.pacrar-progress-widget'));

        // Case A: No widgets in markdown -> Mount a ring before each table
        if (widgets.length === 0) {
            pacrarTables.forEach((table, idx) => {
                const stat = tableStats[idx];
                this.mountSvgRing(table, stat.pct, stat.totalScore, stat.maxScore);
            });
            return;
        }

        // Case B: Exactly 1 widget and multiple tables (Global Master Hub like Ingegneria Informatica MOC)
        if (widgets.length === 1 && pacrarTables.length > 1) {
            let grandTotal = 0;
            let grandMax = 0;
            tableStats.forEach(st => {
                grandTotal += st.totalScore;
                grandMax += st.maxScore;
            });
            const grandPct = grandMax > 0 ? Math.round((grandTotal / grandMax) * 100) : 0;
            this.renderSvgIntoContainer(widgets[0], grandPct, grandTotal, grandMax);
            widgets[0].style.display = 'flex';

            // Remove any dynamically created duplicate widgets sitting directly before tables
            pacrarTables.forEach(table => {
                if (table.previousElementSibling && table.previousElementSibling.classList.contains('pacrar-progress-widget') && table.previousElementSibling !== widgets[0]) {
                    table.previousElementSibling.remove();
                }
            });
            return;
        }

        // Case C: 1 widget and 1 table (Single Course Hub)
        if (widgets.length === 1 && pacrarTables.length === 1) {
            const stat = tableStats[0];
            this.renderSvgIntoContainer(widgets[0], stat.pct, stat.totalScore, stat.maxScore);
            widgets[0].style.display = 'flex';
            if (pacrarTables[0].previousElementSibling && pacrarTables[0].previousElementSibling.classList.contains('pacrar-progress-widget') && pacrarTables[0].previousElementSibling !== widgets[0]) {
                pacrarTables[0].previousElementSibling.remove();
            }
            return;
        }

        // Case D: Multiple widgets and multiple tables (1-to-1 or section-based)
        pacrarTables.forEach((table, idx) => {
            const stat = tableStats[idx];
            const widget = this.findWidgetContainer(table) || widgets[idx] || null;
            if (widget) {
                this.renderSvgIntoContainer(widget, stat.pct, stat.totalScore, stat.maxScore);
                widget.style.display = 'flex';
                if (table.previousElementSibling && table.previousElementSibling.classList.contains('pacrar-progress-widget') && table.previousElementSibling !== widget) {
                    table.previousElementSibling.remove();
                }
            } else {
                this.mountSvgRing(table, stat.pct, stat.totalScore, stat.maxScore);
            }
        });

        // Hide any unpopulated orphan widgets
        widgets.forEach(w => {
            if (!w.querySelector('.pacrar-ring-wrap')) {
                w.style.display = 'none';
            }
        });
    }

    stylePacrarTable(table) {
        let totalScore = 0;
        const rows = table.querySelectorAll('tbody tr').length > 0
            ? Array.from(table.querySelectorAll('tbody tr'))
            : Array.from(table.querySelectorAll('tr')).slice(1);
        const maxScore = rows.length * 6;

        rows.forEach((row) => {
            let rowScore = 0;
            const cells = row.querySelectorAll('td');
            for (let c = 1; c <= 6; c++) {
                const cell = cells[c];
                if (!cell) continue;
                const txt = extractCheckboxState(cell);
                if (txt && txt in SCORES) {
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
        return { totalScore, maxScore, pct };
    }

    renderPacrarTable(table) {
        const stats = this.stylePacrarTable(table);
        this.mountSvgRing(table, stats.pct, stats.totalScore, stats.maxScore);
        return stats;
    }

    findWidgetContainer(table) {
        // 1. Direct preceding sibling widget
        if (table.previousElementSibling && table.previousElementSibling.classList.contains('pacrar-progress-widget')) {
            return table.previousElementSibling;
        }

        // 2. Look backwards through sibling blocks in Reading View or Live Preview
        const block = table.closest('.el-table, .cm-embed-block, .cm-table-widget, .block-language-table') || table.parentElement;
        if (block) {
            let prevBlock = block.previousElementSibling;
            while (prevBlock) {
                if (prevBlock.classList && prevBlock.classList.contains('pacrar-progress-widget')) {
                    return prevBlock;
                }
                const found = prevBlock.querySelector ? prevBlock.querySelector('.pacrar-progress-widget') : null;
                if (found) {
                    return found;
                }
                // Stop searching backwards if we encounter another PACRAR table
                if (prevBlock.querySelector && prevBlock.querySelector('table')) {
                    const otherTable = prevBlock.querySelector('table');
                    if (isPacrarTable(otherTable)) {
                        break;
                    }
                }
                // Stop searching backwards if we encounter an H1 or H2
                if (prevBlock.matches && prevBlock.matches('h1, h2, .el-h1, .el-h2')) {
                    break;
                }
                prevBlock = prevBlock.previousElementSibling;
            }
        }

        // 3. Document-wide search within the active Markdown view
        const root = table.closest('.markdown-rendered, .markdown-preview-view, .cm-content') || (table.ownerDocument ? table.ownerDocument.body : null);
        if (root) {
            const allWidgets = Array.from(root.querySelectorAll('.pacrar-progress-widget'));
            for (let i = allWidgets.length - 1; i >= 0; i--) {
                const w = allWidgets[i];
                if (w.compareDocumentPosition(table) & Node.DOCUMENT_POSITION_FOLLOWING) {
                    return w;
                }
            }
            if (allWidgets.length > 0) {
                return allWidgets[0];
            }
        }

        return null;
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

    renderSvgIntoContainer(container, pct, totalScore, maxScore) {
        if (!container) return;

        if (maxScore === 0) {
            container.innerHTML = `
                <div class="pacrar-ring-wrap" style="color: var(--text-muted); font-size: 0.85em; padding: 0.5rem; text-align: center;">
                    <em>Matrice PACRAR pronta — In attesa di lezioni caricate</em>
                </div>
            `;
            container.style.display = 'flex';
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
        container.style.display = 'flex';
    }

    mountSvgRing(table, pct, totalScore, maxScore) {
        const container = this.findWidgetContainer(table);
        if (container) {
            this.renderSvgIntoContainer(container, pct, totalScore, maxScore);
            if (table.previousElementSibling && table.previousElementSibling.classList.contains('pacrar-progress-widget') && table.previousElementSibling !== container) {
                table.previousElementSibling.remove();
            }
            return;
        }

        let fallback = table.previousElementSibling;
        if (!fallback || !fallback.classList.contains('pacrar-progress-widget')) {
            if (table.parentElement) {
                fallback = document.createElement('div');
                fallback.className = 'pacrar-progress-widget';
                table.parentElement.insertBefore(fallback, table);
            }
        }
        if (fallback) {
            this.renderSvgIntoContainer(fallback, pct, totalScore, maxScore);
        }
    }

    async updatePacrarFile(file, lessonKey, cellIdx, nextState) {
        try {
            const content = await this.app.vault.read(file);
            const lines = content.split('\n');
            let modified = false;

            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (!line.includes('|')) continue;
                const cells = line.split('|');
                if (cells.length < 8) continue;
                const rawArg = cells[1] || '';
                const lineKey = extractLessonKey(rawArg);
                if (!lineKey || lineKey !== lessonKey) continue;

                const hasLeadingPipe = line.trim().startsWith('|');
                const targetPartIdx = hasLeadingPipe ? cellIdx + 1 : cellIdx;

                if (targetPartIdx < cells.length) {
                    const currentVal = cells[targetPartIdx].trim();
                    if (currentVal in CHECKBOX_CYCLE) {
                        cells[targetPartIdx] = ` ${nextState} `;
                        lines[i] = cells.join('|');
                        modified = true;
                        break;
                    }
                }
            }

            if (modified) {
                await this.app.vault.modify(file, lines.join('\n'));
                return true;
            }
        } catch (err) {
            console.error('Error updating PACRAR file:', file.path, err);
        }
        return false;
    }

    async handleCheckboxClick(evt) {
        const cell = evt.target.closest('td');
        if (!cell) return;

        const table = cell.closest('table');
        if (!table || !isPacrarTable(table)) return;

        const row = cell.parentElement;
        const cellIdx = Array.from(row.children).indexOf(cell);
        if (cellIdx < 1 || cellIdx > 6) return;

        const txt = extractCheckboxState(cell);
        if (!txt || !(txt in CHECKBOX_CYCLE)) return;

        evt.preventDefault();
        evt.stopPropagation();
        const next = CHECKBOX_CYCLE[txt];

        // 1. Optimistic DOM update: immediate visual feedback in current view
        cell.textContent = next;
        const root = table.closest('.markdown-rendered, .markdown-preview-view, .cm-content') || document;
        this.renderAllPacrar(root);

        // 2. Identify the lesson key
        const argCell = row.children[0];
        const lessonKey = extractLessonKey(argCell ? argCell.textContent : '');

        // 3. Update the active file on disk
        const view = this.app.workspace.getActiveViewOfType(MarkdownView);
        let activeFilePath = '';
        if (view && view.file) {
            activeFilePath = view.file.path;
            await this.updatePacrarFile(view.file, lessonKey, cellIdx, next);
        }

        // 4. Synchronize linked MOC files in 01 - Map of Content/ (e.g. Master MOC <-> Course MOCs)
        if (lessonKey) {
            const allFiles = this.app.vault.getMarkdownFiles();
            const mocFiles = allFiles.filter(f => f.path.startsWith('01 - Map of Content/') && f.path !== activeFilePath);

            for (const otherFile of mocFiles) {
                await this.updatePacrarFile(otherFile, lessonKey, cellIdx, next);
            }

            // 5. Update any other visible tables in the DOM that display this lesson
            const otherTables = Array.from(document.querySelectorAll('table')).filter(t => t !== table && isPacrarTable(t));
            let needsRerender = false;
            otherTables.forEach(ot => {
                const oRows = Array.from(ot.querySelectorAll('tbody tr')).length > 0
                    ? Array.from(ot.querySelectorAll('tbody tr'))
                    : Array.from(ot.querySelectorAll('tr')).slice(1);
                oRows.forEach(orow => {
                    const oArg = orow.children[0];
                    if (oArg && extractLessonKey(oArg.textContent) === lessonKey) {
                        const oCell = orow.children[cellIdx];
                        if (oCell) {
                            oCell.textContent = next;
                            needsRerender = true;
                        }
                    }
                });
            });

            if (needsRerender) {
                this.renderAllPacrar(document);
            }
        }
    }
}

module.exports = PacrarTrackerPlugin;
module.exports.default = PacrarTrackerPlugin;
