from nicegui import ui
import asyncio
from src.components.Icons import get_icon
from src.data import CHURN_FEATURES

class ChurnPrediction:
    def __init__(self, customers, theme: str):
        self.customers = customers
        self.theme = theme

        self.selected_model = 'xgboost' # logistic, randomforest, xgboost
        self.risk_threshold = 45
        self.calibrating = False

        # References
        self.main_container = None

    async def run_recalibration(self):
        self.calibrating = True
        self.refresh()
        await asyncio.sleep(1.0)
        self.calibrating = False
        self.refresh()

    def set_model(self, model: str):
        self.selected_model = model
        self.refresh()

    def set_threshold(self, val: int):
        self.risk_threshold = val
        self.refresh()

    def calculate_churn_predictions(self):
        res = []
        for c in self.customers:
            base_score = 50.0

            # 1. Retention score correlation (Direct inverse)
            base_score += (75.0 - c["retentionScore"]) * 0.6

            # 2. Spend behavior
            if c["activityTrend"] == 'Declining':
                base_score += 18.0
            elif c["activityTrend"] == 'Upward':
                base_score -= 12.0

            # 3. Tenure
            if c["tenureMonths"] < 12:
                base_score += 10.0
            elif c["tenureMonths"] > 36:
                base_score -= 15.0

            # 4. Multipliers based on model choice
            id_val = ord(c["id"][-1]) if c["id"] else 0
            if self.selected_model == 'logistic':
                base_score += (id_val % 5 - 2) * 1.5
            elif self.selected_model == 'randomforest':
                base_score += (id_val % 4 - 1.5) * 2.0
            else:
                base_score += (id_val % 3 - 1) * 3.0

            final_prob = min(max(round(base_score), 2), 98)
            is_risk = final_prob >= self.risk_threshold

            recommendation = ''
            if final_prob >= 75:
                recommendation = 'Assign Senior VP account executive for high-touch contract negotiation.'
            elif final_prob >= 45:
                recommendation = 'Deploy Customer Success rep to run system health-check and product review.'
            else:
                recommendation = 'Maintain standard automated email check-in flow.'

            cust_pred = c.copy()
            cust_pred.update({
                "churnProbability": final_prob,
                "isRisk": is_risk,
                "recommendation": recommendation
            })
            res.append(cust_pred)
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

        predictions = self.calculate_churn_predictions()
        high_risk_accounts = [p for p in predictions if p["isRisk"]]
        total_risky_spend = sum(p["monthlySpend"] for p in high_risk_accounts)

        # Gauge needle calculations
        aggregate_score = round(sum(p["churnProbability"] for p in predictions) / len(predictions)) if predictions else 0
        needle_rotation = -90 + (aggregate_score / 100) * 180

        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full'):
                with ui.element('div'):
                    ui.label('AI Prediction Laboratory').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Train neural classifiers, adjust decision frontiers, and execute customer retention strategy.').classes('text-xs text-slate-500')
                
                # Calibration button
                btn_recal = ui.button(on_click=self.run_recalibration).classes(
                    f'px-4 py-2.5 rounded-xl text-xs font-semibold border transition-all p-0 min-h-0'
                ).style('text-transform: none !important; height: 38px;')
                btn_recal_bg = 'bg-[#1E293B] border-slate-700 hover:bg-slate-800 text-slate-300' if is_dark else 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
                btn_recal.classes(btn_recal_bg)
                with btn_recal:
                    with ui.element('div').classes('flex items-center gap-2 px-3 py-1'):
                        ui.html(get_icon('refresh-cw', f'h-3.5 w-3.5 text-indigo-400 {"animate-spin" if self.calibrating else ""}'))
                        ui.label('Rebuilding Tree Structures...' if self.calibrating else 'Retrain ML Models')

            # Controls grid
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                # Left console controls
                with ui.element('div').classes(f'lg:col-span-8 p-5 rounded-2xl border flex flex-col md:flex-row gap-8 items-center {card_bg}'):
                    # Model selector
                    with ui.element('div').classes('space-y-3 w-full md:w-1/2 text-left'):
                        ui.label('Classifying Architecture').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block')
                        with ui.element('div').classes('grid grid-cols-3 gap-2 p-1 rounded-xl bg-white/5 border border-white/5'):
                            for model_id, model_lbl in [('logistic', 'LOGISTIC'), ('randomforest', 'R-FOREST'), ('xgboost', 'XGBOOST')]:
                                is_sel = self.selected_model == model_id
                                m_btn = ui.button(model_lbl, on_click=lambda m=model_id: self.set_model(m)).classes('py-2 rounded-lg text-[10px] font-mono font-bold transition-all p-0 min-h-0').style('text-transform: none !important;')
                                if is_sel:
                                    m_btn.classes('bg-indigo-500/20 text-indigo-300 border border-indigo-500/20')
                                else:
                                    m_btn.classes('text-slate-400 hover:text-white')

                        # Model info text
                        with ui.element('div').classes('text-[10px] text-slate-500 flex items-start gap-1.5 leading-normal'):
                            ui.html(get_icon('help-circle', 'h-3.5 w-3.5 text-indigo-400 shrink-0 mt-0.5'))
                            if self.selected_model == 'logistic':
                                ui.label('Logistic Regression: Fits linear boundaries. Fast, lightweight baseline model.').classes('w-full block')
                            elif self.selected_model == 'randomforest':
                                ui.label('Random Forest: Aggregates random decision tree ensembles to resolve complex features.').classes('w-full block')
                            else:
                                ui.label('XGBoost: Extreme Gradient Boosting. Premium algorithm optimized for tabular loss vectors.').classes('w-full block')

                    # Decision slider
                    with ui.element('div').classes('space-y-3 w-full md:w-1/2 text-left'):
                        with ui.element('div').classes('flex justify-between items-center text-[10px] font-mono font-bold uppercase text-slate-500'):
                            ui.label('Decision Threshold')
                            ui.label(f'{self.risk_threshold}% Trigger').classes('text-indigo-400 text-xs')
                        
                        ui.slider(
                            min=10, max=90, step=1, value=self.risk_threshold,
                            on_change=lambda e: self.set_threshold(int(e.value))
                        ).classes('w-full accent-indigo-500 h-1.5 bg-slate-800 rounded-lg dark')
                        
                        ui.label(f'Classify clients with a predicted probability greater than or equal to {self.risk_threshold}% as High Risk accounts.').classes(f'text-[10px] {sub_text_class} block')

                # Right stats overview
                with ui.element('div').classes(f'lg:col-span-4 p-5 rounded-2xl border {card_bg} text-left flex flex-col justify-center'):
                    ui.label('Exposure Summary').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block mb-1')
                    ui.label(f"{len(high_risk_accounts)} Account(s)").classes('text-2xl font-bold font-display tracking-tight text-red-400')
                    ui.label(f"${total_risky_spend:,}/mo spend exposed").classes('text-xs text-slate-300 font-semibold font-mono mt-1')

            # Split details row
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Gauge Meter
                with ui.element('div').classes(f'lg:col-span-4 p-5 rounded-2xl border flex flex-col items-center justify-between {card_bg}'):
                    with ui.element('div').classes('text-center w-full pb-4 border-b border-white/5 mb-4'):
                        ui.label('Mean Risk Integrity').classes(f'font-display font-bold text-sm {text_color}')
                        ui.label('Combined portfolio probability average').classes('text-[10px] font-mono text-slate-500')

                    # Custom gauge diagram render
                    gauge_html = f"""
                    <div class="relative w-48 h-28 flex items-end justify-center mb-4">
                      <svg class="w-full h-full" viewBox="0 0 100 50">
                        <defs>
                          <linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="0">
                            <stop offset="0%" stop-color="#10b981" />
                            <stop offset="50%" stop-color="#f59e0b" />
                            <stop offset="100%" stop-color="#ef4444" />
                          </linearGradient>
                        </defs>
                        <path d="M 10,45 A 35,35 0 0,1 90,45" fill="none" stroke="url(#gaugeGrad)" stroke-width="8" stroke-linecap="round" />
                        <path d="M 12,45 A 33,33 0 0,1 88,45" fill="none" stroke="rgba(0,0,0,0.15)" stroke-width="1" />
                        <circle cx="50" cy="45" r="4" fill="#f8fafc" />
                        <line x1="50" y1="45" x2="50" y2="15" stroke="#f8fafc" stroke-width="2.5" stroke-linecap="round" transform="rotate({needle_rotation} 50 45)" style="transition: transform 1s ease-out;" />
                      </svg>
                      <div class="absolute bottom-1 text-center select-none">
                        <span class="block text-2xl font-bold font-display tracking-tight text-slate-100">{aggregate_score}%</span>
                        <span class="text-[9px] font-mono text-slate-500 uppercase tracking-widest">Aggregate Mean</span>
                      </div>
                    </div>
                    """
                    ui.html(gauge_html)

                    # Alert details
                    with ui.element('div').classes('w-full p-3 rounded-xl bg-white/5 border border-white/5 text-left text-xs text-slate-400 leading-normal'):
                        if aggregate_score >= 65:
                            ui.label('⚠️ SYSTEM ALERT: HIGH EXPOSURE').classes('text-red-400 font-bold block mb-1')
                        elif aggregate_score >= 40:
                            ui.label('⚠️ WORKSPACE STATUS: MODERATE DRIFT').classes('text-amber-400 font-bold block mb-1')
                        else:
                            ui.label('✓ PORTFOLIO HEALTH INDEX SECURED').classes('text-emerald-400 font-bold block mb-1')
                        
                        ui.label(f"Average risk index is calibrated against {len(predictions)} corporate subscription licenses.")

                # Feature weights list
                with ui.element('div').classes(f'lg:col-span-8 p-5 rounded-2xl border {card_bg} text-left'):
                    ui.label('Neural Feature Weighting (Shapley Values)').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                    ui.label('Determines algorithmic impact on prediction values').classes('text-[10px] font-mono text-slate-500 mb-6')
                    
                    with ui.element('div').classes('space-y-4'):
                        for feat in CHURN_FEATURES:
                            pct = feat["importance"] * 100
                            with ui.element('div').classes('space-y-1'):
                                with ui.element('div').classes('flex justify-between items-center text-xs'):
                                    with ui.element('div'):
                                        ui.label(feat["name"]).classes('font-semibold text-slate-200')
                                        ui.label(feat["desc"]).classes('text-[10px] text-slate-500 block')
                                    ui.label(f"{pct:.0f}% Weight").classes('font-mono text-indigo-400 font-bold')
                                with ui.element('div').classes('h-1.5 rounded-full bg-slate-800 overflow-hidden'):
                                    ui.element('div').classes('bg-indigo-600 h-full').style(f'width: {pct}%;')

            # Churn prediction list table
            with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} w-full text-left'):
                ui.label('Algorithmic Predictive Ledger').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                ui.label(f'Real-time inference generated using {self.selected_model.upper()} architecture').classes('text-[10px] font-mono text-slate-500 mb-4')

                table_html = """
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-left border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-[10px] font-mono text-slate-500 uppercase">
                        <th class="py-2.5 px-3">Account</th>
                        <th class="py-2.5 px-3">Monthly Spend</th>
                        <th class="py-2.5 px-3">Tenure Length</th>
                        <th class="py-2.5 px-3">Churn Probability</th>
                        <th class="py-2.5 px-3">Decision Zone</th>
                        <th class="py-2.5 px-3">Prescriptive Retention Action</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-xs">
                """
                for cust in predictions:
                    prob = cust["churnProbability"]
                    prob_color = 'text-red-400' if prob >= 75 else 'text-amber-400' if prob >= 45 else 'text-emerald-400'
                    prob_bg = 'bg-red-500' if prob >= 75 else 'bg-amber-500' if prob >= 45 else 'bg-emerald-500'
                    row_bg = 'bg-red-500/5' if cust["isRisk"] else ''

                    decision_tag = f"""
                      <span class="inline-block px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-red-500/10 text-red-400 border border-red-500/15">
                        TRIGGER ALERT
                      </span>
                    """ if cust["isRisk"] else f"""
                      <span class="inline-block px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400">
                        SAFE ZONE
                      </span>
                    """

                    table_html += f"""
                      <tr class="hover:bg-white/5 transition-colors {row_bg}">
                        <td class="py-3 px-3">
                          <span class="block font-semibold text-slate-200">{cust["name"]}</span>
                          <span class="text-[10px] text-slate-500 font-mono">{cust["id"]} | {cust["region"]}</span>
                        </td>
                        <td class="py-3 px-3 font-semibold font-mono">${cust["monthlySpend"]:,}/mo</td>
                        <td class="py-3 px-3 font-mono">{cust["tenureMonths"]} Months</td>
                        <td class="py-3 px-3">
                          <div class="flex items-center gap-2">
                            <div class="flex-1 bg-slate-800 h-1.5 rounded-full overflow-hidden w-20">
                              <div style="width: {prob}%;" class="h-full {prob_bg}"></div>
                            </div>
                            <span class="font-mono font-bold {prob_color}">{prob}%</span>
                          </div>
                        </td>
                        <td class="py-3 px-3">{decision_tag}</td>
                        <td class="py-3 px-3 text-slate-400 leading-tight italic max-w-[250px]">{cust["recommendation"]}</td>
                      </tr>
                    """
                table_html += """
                    </tbody>
                  </table>
                </div>
                """
                ui.html(table_html).classes('w-full')

    def render(self):
        self.main_container = ui.element('div').classes('w-full')
        with self.main_container:
            self.render_content()
