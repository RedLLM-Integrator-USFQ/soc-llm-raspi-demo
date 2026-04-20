GLOBAL_CSS = """
<style>
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer { display: none; }
    .block-container { padding: 2rem 2.5rem 2rem; max-width: 1200px; }
    div[data-testid="stHorizontalBlock"] { gap: 16px; }

    /* KPI */
    .kpi { background:#f7f7f5; border-radius:12px; padding:20px 22px; }
    .kpi-lbl { font-size:12px; color:#888; margin-bottom:4px; }
    .kpi-val { font-size:36px; font-weight:700; line-height:1.1; margin:0; }
    .kpi-d   { font-size:12px; margin-top:6px; }

    /* Section label */
    .sec { font-size:11px; font-weight:700; letter-spacing:1.5px; color:#999;
           text-transform:uppercase; margin:28px 0 12px; }

    /* Panel card */
    .panel { background:#fff; border:1px solid #e8e8e8; border-radius:12px; padding:20px 22px; }
    .ptitle { font-size:15px; font-weight:600; color:#111; margin-bottom:14px; }

    /* Incident table */
    .inc-table { width:100%; border-collapse:collapse; font-size:13px; }
    .inc-table th { color:#999; font-weight:600; font-size:11px; padding:6px 8px;
                    border-bottom:1px solid #eee; text-align:left; }
    .inc-table td { padding:9px 8px; border-bottom:1px solid #f0f0f0; color:#222; }

    /* Badges */
    .badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; }
    .b-inv  { background:#e8f0fe; color:#1a73e8; }
    .b-open { background:#fff3e0; color:#e65100; }
    .b-res  { background:#e8f5e9; color:#2e7d32; }
    .b-crit { background:#fce4ec; color:#c62828; }
    .b-alta { background:#fff3e0; color:#e65100; }
    .b-med  { background:#e3f2fd; color:#1565c0; }

    /* Bar rows */
    .bar-row { display:flex; align-items:center; gap:10px; margin-bottom:10px; font-size:13px; }
    .bar-bg  { flex:1; background:#f0f0f0; border-radius:6px; height:10px; overflow:hidden; }
    .bar-fill{ height:100%; border-radius:6px; }
    .bar-cnt { width:36px; text-align:right; color:#555; font-size:13px; }

    /* Users */
    .user-row { display:flex; justify-content:space-between; align-items:center;
                padding:9px 0; border-bottom:1px solid #f5f5f5; font-size:13px; }
    .user-row:last-child { border-bottom:none; }

    /* Endpoint bars */
    .ep-row { display:flex; align-items:center; gap:10px; margin-bottom:10px; font-size:13px; }
    .ep-lbl { width:95px; color:#333; }
    .ep-bar { flex:1; background:#f0f0f0; border-radius:6px; height:10px; overflow:hidden; }
    .ep-cnt { width:36px; text-align:right; color:#555; }

    /* Malware rows */
    .mal-row { display:flex; justify-content:space-between;
               padding:7px 0; border-bottom:1px solid #f5f5f5; font-size:13px; color:#333; }
    .mal-row:last-child { border-bottom:none; }

    /* Compliance bars */
    .comp-row { display:flex; align-items:center; gap:10px; margin-bottom:10px; font-size:13px; }
    .comp-lbl { width:72px; color:#333; }
    .comp-bar { flex:1; background:#f0f0f0; border-radius:6px; height:10px; overflow:hidden; }
    .comp-pct { width:36px; text-align:right; color:#555; }

    /* Timeline */
    .tl-item { padding:12px 0; border-bottom:1px solid #f0f0f0; }
    .tl-item:last-child { border-bottom:none; }
    .tl-time { font-size:13px; color:#888; font-weight:600; min-width:42px; }
    .tl-main { font-size:13px; font-weight:600; color:#111; }
    .tl-sub  { font-size:12px; color:#999; margin-top:2px; }

    /* Live badge */
    .live-badge { display:inline-flex; align-items:center; gap:6px; background:#fff0f0;
                  border-radius:20px; padding:5px 14px; font-size:13px; font-weight:600; color:#e53935; }
    .live-dot   { width:8px; height:8px; background:#e53935; border-radius:50%; }

    /* Chat */
    .chat-wrap  { display:flex; flex-direction:column; gap:10px; max-height:420px;
                  overflow-y:auto; padding:4px 0 8px; }
    .msg-user   { align-self:flex-end; background:#1a73e8; color:#fff;
                  border-radius:16px 16px 4px 16px; padding:9px 14px;
                  max-width:75%; font-size:13px; line-height:1.5; }
    .msg-ai     { align-self:flex-start; background:#f1f3f4; color:#111;
                  border-radius:16px 16px 16px 4px; padding:9px 14px;
                  max-width:75%; font-size:13px; line-height:1.5; }
    .msg-label  { font-size:10px; color:#aaa; margin-bottom:2px; }
</style>
"""

SEV_DOT = {"critica": "🔴", "alta": "🟠", "media": "🔵", "baja": "🟢"}
SEV_COLOR = {"critica": "#e53935", "alta": "#fb8c00", "media": "#1565c0", "baja": "#2e7d32"}

ESTADO_CLASS = {"Investigando": "b-inv", "Abierto": "b-open", "Resuelto": "b-res"}
PRIO_CLASS   = {"Crítica": "b-crit", "Alta": "b-alta", "Media": "b-med"}

BAR_COLORS_ATAQUE = ["#e53935","#fb8c00","#fb8c00","#42a5f5","#42a5f5","#66bb6a"]
EP_COLORS = {"Protegidos": "#43a047", "Sin parche": "#fb8c00", "Comprometidos": "#e53935"}
COMP_COLOR = lambda p: "#43a047" if p >= 80 else "#fb8c00"
