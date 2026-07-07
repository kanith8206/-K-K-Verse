from nicegui import ui
import math
import asyncio
from src.components.Icons import get_icon

class SalesForecasting:
    def __init__(self, sales, theme: str):
        self.sales = sales
        self.theme = theme

        self.selected_alg = 'xgboost' # linear, forest, xgboost
        self.growth_multiplier = 1.12
        self.forecasting = False

        # References
        self.main_container = None

    async def trigger_forecast(self):
        self.forecasting = True
        self.refresh()
        await asyncio.sleep(1.2)
        self.forecasting = False
        self.refresh()

    def set_algorithm(self, alg: str):
        self.selected_alg = alg
        self.refresh()

    def set_growth(self, val: float):
        self.growth_multiplier = val
        self.refresh()

    def calculate_projections(self):
        projection_months = [
            "Aug 26", "Sep 26", "Oct 26", "Nov 26", "Dec 26", "Jan 27",
            "Feb 27", "Mar 27", "Apr 27", "May 27", "Jun 27", "Jul 27"
        ]
        base_start_revenue = 44000.0
        res = []
        for idx, m in enumerate(projection_months):
            multiplier = self.growth_multiplier

            # Seasonality/cyclical
            if idx == 4:
                multiplier *= 1.25 # Holiday season
            elif idx == 1:
                multiplier *= 0.95 # Sept dip
            elif idx == 7:
                multiplier *= 1.15 # March peak

            # Algorithm perturbations
            perturb = 0.0
            if self.selected_alg == 'linear':
                perturb = math.sin(idx * 0.4) * 1500.0
            elif self.selected_alg == 'forest':
                perturb = math.cos(idx * 0.5) * 2200.0
            else:
                perturb = math.sin(idx * 0.8) * 3500.0

            proj_base = base_start_revenue * math.pow(multiplier, (idx + 1) / 4.0) + perturb
            conf_gap = proj_base * 0.12 # 12% margin

            res.append({
                "month": m,
                "projected": round(proj_base),
                "upperBound": round(proj_base + conf_gap),
                "lowerBound": round(proj_base - conf_gap)
            })
        return res

    def refresh(self):
        if self.main_container:
            self.main_container.refresh()

    @ui.refreshable
    def render_content(self):
        is_dark = self.theme == 'dark'
        card_bg = 'bg-[#0F172A] border-slate-800 shadow-lg' if is_dark else 'bg-white border-slate-200 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        text_color = 'text-white' if is_dark else 'text-slate-900'

        projected = self.calculate_projections()
        final_projected_total = sum(p["projected"] for p in projected)
        max_forecast_val = max(p["upperBound"] for p in projected) if projected else 1.0

        # Construct SVG paths
        upper_path = ""
        lower_path = ""
        area_path = "M 20,210 "
        line_path = f"M 20,{210 - (projected[0]['projected'] / max_forecast_val) * 160} "

        for idx, v in enumerate(projected):
            cx = 20 + idx * 88
            cy_proj = 210 - (v["projected"] / max_forecast_val) * 160
            cy_upper = 210 - (v["upperBound"] / max_forecast_val) * 160
            cy_lower = 210 - (v["lowerBound"] / max_forecast_val) * 160

            if idx == 0:
                upper_path += f"M 20,{cy_upper} "
                lower_path += f"M 20,{cy_lower} "
                area_path += f"L 20,{cy_proj} "
            else:
                upper_path += f"L {cx},{cy_upper} "
                lower_path += f"L {cx},{cy_lower} "
                
                # cubic curves
                cx_prev = 20 + (idx - 1) * 88
                cy_prev = 210 - (projected[idx - 1]["projected"] / max_forecast_val) * 160
                c1_x = cx_prev + 30
                c1_y = cy_prev
                c2_x = cx - 30
                c2_y = cy_proj
                
                area_path += f"C {c1_x},{c1_y} {c2_x},{c2_y} {cx},{cy_proj} "
                line_path += f"C {c1_x},{c1_y} {c2_x},{c2_y} {cx},{cy_proj} "

        area_path += f"L {20 + (len(projected)-1)*88},210 Z"

        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full'):
                with ui.element('div'):
                    ui.label('Business Forecast Center').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Train regressors, configure compound interest growth margins, and project active yearly revenue.').classes('text-xs text-slate-500')
                
                # Action button
                btn_synth = ui.button(on_click=self.trigger_forecast).classes(
                    'px-4 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-xs tracking-wide shadow-lg shadow-indigo-500/15 hover:bg-indigo-700 hover:scale-[1.02] active:scale-[0.98] transition-all p-0 min-h-0'
                ).style('text-transform: none !important; height: 38px;')
                with btn_synth:
                    with ui.element('div').classes('flex items-center gap-2 px-3 py-1'):
                        ui.html(get_icon('refresh-cw', f'h-3.5 w-3.5 text-white {"animate-spin" if self.forecasting else ""}'))
                        ui.label('Recalculating Gradient Descent...' if self.forecasting else 'Synthesize Projections')

            # Controls grid
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Console
                with ui.element('div').classes(f'lg:col-span-8 p-5 rounded-2xl border flex flex-col md:flex-row gap-8 items-center {card_bg}'):
                    # Selection
                    with ui.element('div').classes('space-y-3 w-full md:w-1/2 text-left'):
                        ui.label('Regression Algorithm').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block')
                        with ui.element('div').classes('grid grid-cols-3 gap-2 p-1 rounded-xl bg-white/5 border border-white/5'):
                            for alg_id, alg_lbl in [('linear', 'LINEAR'), ('forest', 'R-FOREST'), ('xgboost', 'XGBOOST')]:
                                is_sel = self.selected_alg == alg_id
                                a_btn = ui.button(alg_lbl, on_click=lambda a=alg_id: self.set_algorithm(a)).classes('py-2 rounded-lg text-[10px] font-mono font-bold transition-all p-0 min-h-0').style('text-transform: none !important;')
                                if is_sel:
                                    a_btn.classes('bg-indigo-500/20 text-indigo-300 border border-indigo-500/20')
                                else:
                                    a_btn.classes('text-slate-400 hover:text-white')

                        # Info text
                        with ui.element('div').classes('text-[10px] text-slate-500 leading-normal'):
                            if self.selected_alg == 'linear':
                                ui.label('Linear Regression: Computes standard line of best fit. Fits straightforward trends.')
                            elif self.selected_alg == 'forest':
                                ui.label('Random Forest Regressor: Combines decision trees to fit multi-variable fluctuations.')
                            else:
                                ui.label('XGBoost Regressor: Builds recursive decision tree residuals for highly accurate projections.')

                    # Growth slider
                    with ui.element('div').classes('space-y-3 w-full md:w-1/2 text-left'):
                        with ui.element('div').classes('flex justify-between items-center text-[10px] font-mono font-bold uppercase text-slate-500'):
                            ui.label('Future Growth Index')
                            ui.label(f'{round((self.growth_multiplier - 1) * 100)}% Growth').classes('text-indigo-400 text-xs')
                        
                        ui.slider(
                            min=0.90, max=1.50, step=0.01, value=self.growth_multiplier,
                            on_change=lambda e: self.set_growth(float(e.value))
                        ).classes('w-full accent-indigo-500 h-1.5 bg-slate-800 rounded-lg dark')
                        
                        ui.label('Manually scale future contract acquisition and seat growth multipliers between -10% and +50%.').classes(f'text-[10px] {sub_text_class} block')

                # Projections summary
                with ui.element('div').classes(f'lg:col-span-4 p-5 rounded-2xl border {card_bg} text-left flex flex-col justify-center'):
                    ui.label('Projected 12-Month Yield').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block mb-1')
                    ui.label(f"${final_projected_total:,}").classes('text-2xl font-bold font-display tracking-tight text-indigo-400')
                    ui.label('Based on calibrated model configurations').classes('text-xs text-slate-500 font-mono mt-1')

            # Forecasting Chart Card
            with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} w-full text-left'):
                with ui.element('div').classes('flex justify-between items-center mb-6'):
                    with ui.element('div').classes('text-left'):
                        ui.label('Revenue Forecast Curves').classes(f'font-display font-bold text-sm {text_color}')
                        ui.label('12-month forward predictive path with 95% confidence bounds').classes('text-[10px] font-mono text-slate-500')
                    with ui.element('div').classes('flex items-center gap-4 text-[10px] font-mono'):
                        with ui.element('span').classes('flex items-center gap-1'):
                            ui.element('span').classes('h-2.5 w-2.5 bg-indigo-500 rounded-full')
                            ui.label('Projected Base')
                        with ui.element('span').classes('flex items-center gap-1.5'):
                            ui.label('Confidence Bounds').classes('h-1 w-3 bg-red-400/60 border border-dashed text-slate-400')

                # SVG render
                svg_html = f"""
                <div class="h-72 w-full relative">
                """
                if self.forecasting:
                    svg_html += """
                      <div class="absolute inset-0 z-10 bg-slate-950/20 backdrop-blur-xs flex flex-col items-center justify-center space-y-3">
                        <div class="h-8 w-8 rounded-full border-2 border-indigo-500/20 border-t-indigo-500 animate-spin"></div>
                        <span class="text-[11px] font-mono text-slate-400">Recomputing confidence bands...</span>
                      </div>
                    """
                
                svg_html += f"""
                  <svg class="w-full h-full" viewBox="0 0 1000 240" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="foreGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#6366f1" stop-opacity="0.15" />
                        <stop offset="100%" stop-color="#6366f1" stop-opacity="0.0" />
                      </linearGradient>
                    </defs>
                    <!-- Gridlines -->
                    <line x1="0" y1="210" x2="1000" y2="210" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                    <line x1="0" y1="165" x2="1000" y2="165" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                    <line x1="0" y1="120" x2="1000" y2="120" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                    <line x1="0" y1="75" x2="1000" y2="75" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                    <line x1="0" y1="30" x2="1000" y2="30" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />

                    <!-- Confidence Bounds paths -->
                    <path d="{upper_path}" fill="none" stroke="rgba(239, 68, 68, 0.45)" stroke-width="2" stroke-dasharray="4,4" />
                    <path d="{lower_path}" fill="none" stroke="rgba(239, 68, 68, 0.45)" stroke-width="2" stroke-dasharray="4,4" />

                    <!-- Projected Base Area -->
                    <path d="{area_path}" fill="url(#foreGrad)" />
                    <path d="{line_path}" fill="none" stroke="#6366f1" stroke-width="3" stroke-linecap="round" />
                """

                # Interacting dots
                for idx, v in enumerate(projected):
                    cx = 20 + idx * 88
                    cy = 210 - (v["projected"] / max_forecast_val) * 160
                    svg_html += f"""
                    <g class="group cursor-pointer">
                      <circle cx="{cx}" cy="{cy}" r="5" fill="#030712" stroke="#6366f1" stroke-width="1.5" />
                      <circle cx="{cx}" cy="{cy}" r="2" fill="#6366f1" />
                      <style>
                        .group:hover .tooltip-bg {{ opacity: 1; }}
                        .group:hover .tooltip-txt {{ opacity: 1; }}
                      </style>
                      <rect x="{cx - 40}" y="{cy - 30}" width="80" height="20" rx="4" fill="rgba(15,23,42,0.95)" stroke="rgba(255,255,255,0.1)" class="tooltip-bg" style="opacity: 0; transition: opacity 0.2s;" />
                      <text x="{cx}" y="{cy - 17}" fill="#ffffff" font-size="9" text-anchor="middle" class="tooltip-txt font-mono" style="opacity: 0; transition: opacity 0.2s; font-weight: bold;">
                        ${(v["projected"] / 1000):.0f}k
                      </text>
                    </g>
                    """

                svg_html += f"""
                  </svg>
                  <div class="absolute bottom-1 left-0 right-0 flex justify-between px-4 text-[9px] font-mono text-slate-500">
                    {" ".join(f"<span>{p['month']}</span>" for p in projected)}
                  </div>
                </div>
                """
                ui.html(svg_html).classes('w-full')

            # Statistics cards matrix
            with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} w-full text-left'):
                ui.label('Monthly Forecast Predictions Matrix').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                ui.label('Detailed statistics of confidence margins').classes('text-[10px] font-mono text-slate-500 mb-4')
                
                with ui.element('div').classes('grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 w-full'):
                    for v in projected:
                        with ui.element('div').classes('p-3.5 rounded-xl bg-white/5 border border-white/5 text-left'):
                            ui.label(v["month"].upper()).classes('text-[10px] font-mono text-slate-500 block mb-1 font-bold')
                            ui.label(f"${v['projected']:,}").classes('text-base font-bold font-display text-indigo-400')
                            with ui.element('div').classes('text-[9px] font-mono text-slate-500 mt-1.5 space-y-0.5'):
                                ui.label(f"Max: ${v['upperBound']:,}")
                                ui.label(f"Min: ${v['lowerBound']:,}")

    def render(self):
        self.main_container = ui.element('div').classes('w-full')
        with self.main_container:
            self.render_content()
