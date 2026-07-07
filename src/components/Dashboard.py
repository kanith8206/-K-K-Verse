from nicegui import ui
import asyncio
from src.components.Icons import get_icon
from src.services.ai import fetch_insights_logic

class Dashboard:
    def __init__(self, sales, customers, products, theme: str, set_active_tab):
        self.sales = sales
        self.customers = customers
        self.products = products
        self.theme = theme
        self.set_active_tab = set_active_tab

        self.ai_summary = None
        self.loading_summary = False
        self.summary_status_message = ''
        
        # Element references for dynamic UI updates
        self.ai_summary_container = None

    async def generate_ai_summary(self):
        self.loading_summary = True
        self.summary_status_message = 'Engaging Gemini 3.5 Neural Engine...'
        self.refresh_ai_summary()

        # Calculate values
        total_revenue = sum(sale["totalRevenue"] for sale in self.sales)
        total_cost = sum(sale["totalCost"] for sale in self.sales)
        total_profit = total_revenue - total_cost
        profit_margin = f"{((total_profit / total_revenue) * 100):.1f}" if total_revenue > 0 else "0"
        
        customer_summary = {}
        for c in self.customers:
            seg = c["segment"]
            customer_summary[seg] = customer_summary.get(seg, 0) + 1
            
        low_stock_count = len([p for p in self.products if p["stock"] <= p["minStockThreshold"]])

        # Direct python call to shared service
        self.ai_summary = await fetch_insights_logic(
            kpis={
                "totalRevenue": total_revenue,
                "totalProfit": total_profit,
                "profitMargin": profit_margin,
                "totalCustomers": len(self.customers)
            },
            customer_summary=customer_summary,
            product_summary={
                "lowStockCount": low_stock_count,
                "totalProducts": len(self.products)
            }
        )

        self.loading_summary = False
        self.refresh_ai_summary()

    def refresh_ai_summary(self):
        if self.ai_summary_container:
            self.ai_summary_container.refresh()

    @ui.refreshable
    def render_ai_summary_panel(self, is_dark: bool):
        card_class = 'bg-[#0F172A] border-slate-800 text-slate-100' if is_dark else 'bg-white border-slate-200 text-slate-900 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        
        with ui.element('div').classes(f'p-6 rounded-2xl border {card_class} relative overflow-hidden text-left h-full'):
            # Ambient glow
            ui.element('div').classes('absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-2xl -z-10')
            
            # Header
            with ui.element('div').classes('flex justify-between items-center mb-5 pb-3 border-b border-white/5'):
                with ui.element('div').classes('flex items-center gap-2'):
                    ui.html(get_icon('bot', 'h-5 w-5 text-indigo-400'))
                    ui.label('Generative Business Audit').classes('font-display font-bold text-sm')
                ui.label('Gemini Active').classes('text-[10px] font-mono text-indigo-400 px-2 py-0.5 rounded bg-indigo-500/10 uppercase tracking-widest font-bold')

            if self.loading_summary:
                with ui.element('div').classes('space-y-4 py-8 text-center flex flex-col items-center justify-center'):
                    ui.spinner(size='md', color='indigo')
                    ui.label(self.summary_status_message).classes(f'text-xs font-mono {sub_text_class}')
            
            elif self.ai_summary:
                with ui.element('div').classes('space-y-5'):
                    ui.label(self.ai_summary.get("executiveSummary", "")).classes('text-xs leading-relaxed text-left ' + ('text-slate-300' if is_dark else 'text-slate-700'))

                    if self.ai_summary.get("isSimulated"):
                        with ui.element('div').classes('p-3 rounded-xl bg-indigo-950/15 border border-indigo-500/10 text-left'):
                            ui.label('LOCAL DIAGNOSTIC COMPLETED').classes('text-[10px] font-mono text-indigo-400 font-bold block mb-0.5')
                            ui.label(self.ai_summary.get("message", "")).classes(f'text-[10px] {sub_text_class} leading-tight block')

                    # Opportunities
                    with ui.element('div').classes('space-y-2.5 text-left'):
                        ui.label('Key Opportunities').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block')
                        for opp in self.ai_summary.get("opportunities", []):
                            with ui.element('div').classes('p-3 rounded-xl bg-white/5 border border-white/5'):
                                with ui.element('div').classes('flex justify-between items-center mb-1'):
                                    ui.label(opp.get("title")).classes('text-xs font-semibold text-indigo-300')
                                    ui.label(f'{opp.get("impact")} Impact').classes('text-[10px] font-mono text-emerald-400 px-1.5 py-0.2 rounded bg-emerald-500/10')
                                ui.label(opp.get("description")).classes(f'text-[11px] {sub_text_class} leading-tight')

                    # Risks
                    with ui.element('div').classes('space-y-2.5 text-left'):
                        ui.label('Exposure Mitigations').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block')
                        for risk in self.ai_summary.get("risks", []):
                            with ui.element('div').classes('p-3 rounded-xl bg-white/5 border border-white/5'):
                                with ui.element('div').classes('flex justify-between items-center mb-1'):
                                    ui.label(risk.get("title")).classes('text-xs font-semibold text-red-300')
                                    ui.label(risk.get("severity")).classes('text-[10px] font-mono text-red-400 px-1.5 py-0.2 rounded bg-red-500/10')
                                ui.label(risk.get("description")).classes(f'text-[11px] {sub_text_class} leading-tight')
            else:
                ui.label('Telemetry diagnostic engine stale. Trigger Recalibrate to generate summary.').classes(f'py-8 text-center text-xs {sub_text_class} font-mono block')

    def render(self):
        # Trigger summary load automatically in background task
        asyncio.create_task(self.generate_ai_summary())

        is_dark = self.theme == 'dark'
        card_bg = 'bg-[#0F172A] border-slate-800 shadow-lg' if is_dark else 'bg-white border-slate-200 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        text_color = 'text-white' if is_dark else 'text-slate-900'

        # Calculations
        total_revenue = sum(sale["totalRevenue"] for sale in self.sales)
        total_cost = sum(sale["totalCost"] for sale in self.sales)
        total_profit = total_revenue - total_cost
        profit_margin = f"{((total_profit / total_revenue) * 100):.1f}" if total_revenue > 0 else "0"
        total_customers_count = len(self.customers)
        low_stock_count = len([p for p in self.products if p["stock"] <= p["minStockThreshold"]])

        # Sales Graph Math
        monthly_revenue = [17500, 15500, 42500, 18000, 24500, 32000, 44000]
        max_rev = max(monthly_revenue)
        
        # Build SVG path elements in Python
        # Area graph points
        area_pts = "M 20,210 "
        glow_pts = f"M 20,{210 - (monthly_revenue[0] / max_rev) * 160} "
        
        for idx, val in enumerate(monthly_revenue):
            cx = 20 + idx * 93.3
            cy = 210 - (val / max_rev) * 160
            if idx == 0:
                area_pts += f"L 20,{cy} "
            else:
                # build cubic curves matching tsx values
                # C cx-50, cy_prev cx-20, cy cx, cy
                cx_prev = 20 + (idx - 1) * 93.3
                cy_prev = 210 - (monthly_revenue[idx - 1] / max_rev) * 160
                c1_x = cx_prev + 40
                c1_y = cy_prev
                c2_x = cx - 40
                c2_y = cy
                area_pts += f"C {c1_x},{c1_y} {c2_x},{c2_y} {cx},{cy} "
                glow_pts += f"C {c1_x},{c1_y} {c2_x},{c2_y} {cx},{cy} "
                
        area_pts += "L 580,210 Z"

        with ui.element('div').classes('space-y-6 text-left w-full'):
            
            # Welcome row
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full'):
                with ui.element('div'):
                    ui.label('Executive Command Center').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Live operational status, generative summaries, and telemetry aggregates.').classes('text-xs text-slate-500')

                # Header actions
                with ui.element('div').classes('flex items-center gap-3'):
                    btn_recal = ui.button(on_click=self.generate_ai_summary).classes(
                        f'px-4 py-2 rounded-xl text-xs font-semibold border transition-all p-0 min-h-0'
                    ).style('text-transform: none !important; height: 38px;')
                    btn_recal_bg = 'bg-[#1E293B] border-slate-700 hover:bg-slate-800 text-slate-300' if is_dark else 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
                    btn_recal.classes(btn_recal_bg)
                    with btn_recal:
                        with ui.element('div').classes('flex items-center gap-2 px-3 py-1'):
                            ui.html(get_icon('refresh-cw', 'h-3.5 w-3.5 text-indigo-400'))
                            ui.label('Recalibrate Metrics')

                    btn_copilot = ui.button(on_click=lambda: self.set_active_tab('copilot')).classes(
                        'px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 text-white flex items-center gap-2 shadow-lg shadow-indigo-500/15 hover:bg-indigo-700 hover:scale-[1.02] active:scale-[0.98] transition-all p-0 min-h-0'
                    ).style('text-transform: none !important; height: 38px;')
                    with btn_copilot:
                        with ui.element('div').classes('flex items-center gap-2 px-3 py-1'):
                            ui.html(get_icon('sparkles', 'h-3.5 w-3.5 text-white'))
                            ui.label('Engage AI Copilot')

            # KPIs Row
            with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 w-full'):
                
                # Revenue
                with ui.element('div').classes(f'p-5 rounded-2xl border transition-all {card_bg}'):
                    with ui.element('div').classes('flex justify-between items-start mb-2'):
                        ui.label('Gross Revenue').classes('text-[11px] font-mono text-slate-500 uppercase tracking-wider')
                        ui.html(get_icon('dollar-sign', 'h-5 w-5 text-indigo-400'))
                    ui.label(f"${total_revenue:,}").classes(f'text-2xl font-bold font-display tracking-tight {text_color}')
                    with ui.element('div').classes('flex items-center gap-1.5 mt-2 text-[10px] font-mono text-emerald-500'):
                        ui.html(get_icon('trending-up', 'h-3.5 w-3.5 text-emerald-500'))
                        ui.label('+12.4% Quarter Target')

                # Profit
                with ui.element('div').classes(f'p-5 rounded-2xl border transition-all {card_bg}'):
                    with ui.element('div').classes('flex justify-between items-start mb-2'):
                        ui.label('Net Profit').classes('text-[11px] font-mono text-slate-500 uppercase tracking-wider')
                        ui.html(get_icon('trending-up', 'h-5 w-5 text-emerald-400'))
                    ui.label(f"${total_profit:,}").classes(f'text-2xl font-bold font-display tracking-tight {text_color}')
                    with ui.element('div').classes('flex items-center gap-1.5 mt-2 text-[10px] font-mono text-emerald-550'):
                        ui.label(f'Margin: {profit_margin}%').classes('font-semibold text-emerald-600')
                        ui.label('| Peak Yield').classes('text-slate-400')

                # Customers
                with ui.element('div').classes(f'p-5 rounded-2xl border transition-all {card_bg}'):
                    with ui.element('div').classes('flex justify-between items-start mb-2'):
                        ui.label('Active Client Assets').classes('text-[11px] font-mono text-slate-500 uppercase tracking-wider')
                        ui.html(get_icon('users', 'h-5 w-5 text-indigo-400'))
                    ui.label(str(total_customers_count)).classes(f'text-2xl font-bold font-display tracking-tight {text_color}')
                    with ui.element('div').classes('flex items-center gap-1.5 mt-2 text-[10px] font-mono text-indigo-400'):
                        ui.label('Enterprise Segment Focused')

                # Inventory Alert
                with ui.element('div').classes(f'p-5 rounded-2xl border transition-all {card_bg}'):
                    with ui.element('div').classes('flex justify-between items-start mb-2'):
                        ui.label('Warehouse Health').classes('text-[11px] font-mono text-slate-500 uppercase tracking-wider')
                        alert_color = 'text-amber-500' if low_stock_count > 0 else 'text-emerald-500'
                        ui.html(get_icon('package', f'h-5 w-5 {alert_color}'))
                    ui.label(str(low_stock_count)).classes(f'text-2xl font-bold font-display tracking-tight {text_color}')
                    
                    with ui.element('div').classes('flex items-center gap-1.5 mt-2 text-[10px] font-mono'):
                        if low_stock_count > 0:
                            ui.html(get_icon('alert-triangle', 'h-3.5 w-3.5 text-amber-500 animate-bounce'))
                            ui.label('Requires Refill Focus').classes('text-amber-500')
                        else:
                            ui.html(get_icon('shield-check', 'h-3.5 w-3.5 text-emerald-500'))
                            ui.label('Fully Stocked Bounds').classes('text-emerald-500')

            # Split content layout
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Left side
                with ui.element('div').classes('lg:col-span-8 space-y-6 text-left'):
                    # Chart Card
                    chart_card_bg = 'bg-[#0F172A] border-slate-800' if is_dark else 'bg-white border-slate-200 shadow-sm'
                    with ui.element('div').classes(f'p-5 rounded-2xl border {chart_card_bg} text-left'):
                        with ui.element('div').classes('flex justify-between items-center mb-6'):
                            with ui.element('div').classes('text-left'):
                                ui.label('Revenue Flow Matrix').classes(f'font-display font-bold text-sm {text_color}')
                                ui.label('Historical performance across 7 rolling sales quarters').classes('text-[10px] font-mono text-slate-500')
                            with ui.element('div').classes('flex items-center gap-4 text-[10px] font-mono'):
                                with ui.element('span').classes('flex items-center gap-1'):
                                    ui.element('span').classes('h-2.5 w-2.5 bg-indigo-500 rounded-full')
                                    ui.label('Revenue')
                                with ui.element('span').classes('flex items-center gap-1'):
                                    ui.element('span').classes('h-2.5 w-2.5 bg-indigo-600 rounded-full')
                                    ui.label('Target Projection')

                        # SVG rendering in NiceGUI
                        svg_html = f"""
                        <div class="h-64 w-full relative">
                          <svg class="w-full h-full" viewBox="0 0 600 240" preserveAspectRatio="none">
                            <defs>
                              <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stop-color="#6366f1" stop-opacity="0.25" />
                                <stop offset="100%" stop-color="#6366f1" stop-opacity="0.0" />
                              </linearGradient>
                            </defs>
                            <!-- Horizontal reference gridlines -->
                            <line x1="0" y1="210" x2="600" y2="210" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                            <line x1="0" y1="165" x2="600" y2="165" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                            <line x1="0" y1="120" x2="600" y2="120" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                            <line x1="0" y1="75" x2="600" y2="75" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />
                            <line x1="0" y1="30" x2="600" y2="30" stroke="rgba(255,255,255,0.03)" stroke-dasharray="4,4" />

                            <path d="{area_pts}" fill="url(#chartGrad)" />
                            <path d="{glow_pts}" fill="none" stroke="#6366f1" stroke-width="3.5" stroke-linecap="round" />
                        """
                        
                        # Add interactive dots using native CSS tooltip
                        for idx, val in enumerate(monthly_revenue):
                            cx = 20 + idx * 93.3
                            cy = 210 - (val / max_rev) * 160
                            # NiceGUI / standard browser CSS: we can inject style block into the SVG or use standard CSS hover
                            svg_html += f"""
                            <g class="cursor-pointer group">
                              <circle cx="{cx}" cy="{cy}" r="6" fill="#030712" stroke="#6366f1" stroke-width="2" />
                              <circle cx="{cx}" cy="{cy}" r="3" fill="#6366f1" />
                              <style>
                                .group:hover .tooltip-bg {{ opacity: 1; }}
                                .group:hover .tooltip-txt {{ opacity: 1; }}
                              </style>
                              <rect x="{cx - 30}" y="{cy - 30}" width="60" height="20" rx="4" fill="rgba(15,23,42,0.95)" stroke="rgba(255,255,255,0.1)" stroke-width="1" class="tooltip-bg" style="opacity:0; transition: opacity 0.2s;" />
                              <text x="{cx}" y="{cy - 17}" fill="#ffffff" font-size="9" text-anchor="middle" class="tooltip-txt font-mono" style="opacity:0; transition: opacity 0.2s; font-weight: bold;">
                                ${(val / 1000):.1f}k
                              </text>
                            </g>
                            """
                            
                        svg_html += f"""
                          </svg>
                          <div class="absolute bottom-1 left-0 right-0 flex justify-between px-4 text-[10px] font-mono text-slate-500">
                            {" ".join(f"<span>{m}</span>" for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"])}
                          </div>
                        </div>
                        """
                        ui.html(svg_html).classes('w-full')

                    # Recent Transactions Card
                    with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} text-left'):
                        with ui.element('div').classes('flex justify-between items-center mb-4'):
                            with ui.element('div').classes('text-left'):
                                ui.label('Recent Ledger Operations').classes(f'font-display font-bold text-sm {text_color}')
                                ui.label('Latest synchronized ledger database rows').classes('text-[10px] font-mono text-slate-500')
                            
                            inspect_btn = ui.button(on_click=lambda: self.set_active_tab('sales')).classes(
                                'text-xs text-indigo-400 font-semibold hover:underline p-0 min-h-0'
                            ).props('flat dense').style('text-transform: none !important;')
                            with inspect_btn:
                                with ui.element('div').classes('flex items-center gap-1'):
                                    ui.label('Inspect Ledger')
                                    ui.html(get_icon('arrow-right', 'h-3 w-3 text-indigo-400'))

                        # Recent Sales Table
                        recent_sales = sorted(self.sales, key=lambda x: x["saleDate"], reverse=True)[:5]
                        table_html = f"""
                        <div class="overflow-x-auto w-full">
                          <table class="w-full text-left border-collapse">
                            <thead>
                              <tr class="border-b border-white/5 text-[10px] font-mono text-slate-500 uppercase">
                                <th class="py-3 px-2">Ledger ID</th>
                                <th class="py-3 px-2">Enterprise Client</th>
                                <th class="py-3 px-2">Asset Package</th>
                                <th class="py-3 px-2">Total revenue</th>
                                <th class="py-3 px-2">Date</th>
                                <th class="py-3 px-2 text-right">Yield Status</th>
                              </tr>
                            </thead>
                            <tbody class="divide-y divide-white/5 text-xs">
                        """
                        for sale in recent_sales:
                            table_html += f"""
                              <tr class="hover:bg-white/5 transition-colors">
                                <td class="py-3 px-2 font-mono text-indigo-400">{sale["id"]}</td>
                                <td class="py-3 px-2 font-semibold text-slate-200">{sale["customerName"]}</td>
                                <td class="py-3 px-2 text-slate-400 truncate max-w-[150px]">{sale["productName"]}</td>
                                <td class="py-3 px-2 font-semibold font-mono">${sale["totalRevenue"]:,}</td>
                                <td class="py-3 px-2 text-slate-500 font-mono">{sale["saleDate"]}</td>
                                <td class="py-3 px-2 text-right">
                                  <span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-mono bg-emerald-500/10 text-emerald-400 font-semibold">
                                    SYNCHRONIZED
                                  </span>
                                </td>
                              </tr>
                            """
                        table_html += """
                            </tbody>
                          </table>
                        </div>
                        """
                        ui.html(table_html).classes('w-full')

                # Right side
                with ui.element('div').classes('lg:col-span-4 space-y-6'):
                    # AI Panel
                    self.ai_summary_container = ui.element('div')
                    with self.ai_summary_container:
                        self.render_ai_summary_panel(is_dark)

                    # Quick actions panel
                    with ui.element('div').classes(f'p-5 rounded-2xl border text-left {card_bg}'):
                        ui.label('Command Actions Workspace').classes(f'font-display font-bold text-sm mb-4 {text_color}')
                        with ui.element('div').classes('space-y-3'):
                            
                            # Action 1
                            act1 = ui.button(on_click=lambda: self.set_active_tab('churn')).classes(
                                'w-full p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/20 transition-all text-xs font-medium text-left p-0 min-h-0'
                            ).style('text-transform: none !important; font-weight: normal; height: auto;')
                            with act1:
                                with ui.element('div').classes('flex items-center justify-between w-full px-3 py-1.5'):
                                    with ui.element('div').classes('flex items-center gap-3'):
                                        with ui.element('div').classes('h-7 w-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center shrink-0'):
                                            ui.html(get_icon('zap', 'h-3.5 w-3.5 text-indigo-400'))
                                        with ui.element('div').classes('text-left'):
                                            ui.label('Initiate Churn Diagnostic').classes('block font-semibold text-slate-200')
                                            ui.label('Calibrate Random Forest Churn').classes('text-[10px] text-slate-500 font-mono')
                                    ui.html(get_icon('arrow-right', 'h-4 w-4 text-slate-500'))

                            # Action 2
                            act2 = ui.button(on_click=lambda: self.set_active_tab('forecasting')).classes(
                                'w-full p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/20 transition-all text-xs font-medium text-left p-0 min-h-0'
                            ).style('text-transform: none !important; font-weight: normal; height: auto;')
                            with act2:
                                with ui.element('div').classes('flex items-center justify-between w-full px-3 py-1.5'):
                                    with ui.element('div').classes('flex items-center gap-3'):
                                        with ui.element('div').classes('h-7 w-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center shrink-0'):
                                            ui.html(get_icon('activity', 'h-3.5 w-3.5 text-indigo-400'))
                                        with ui.element('div').classes('text-left'):
                                            ui.label('Synthesize Sales Forecast').classes('block font-semibold text-slate-200')
                                            ui.label('Project 12-month growth confidence').classes('text-[10px] text-slate-500 font-mono')
                                    ui.html(get_icon('arrow-right', 'h-4 w-4 text-slate-500'))

                            # Action 3
                            act3 = ui.button(on_click=lambda: self.set_active_tab('reports')).classes(
                                'w-full p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/20 transition-all text-xs font-medium text-left p-0 min-h-0'
                            ).style('text-transform: none !important; font-weight: normal; height: auto;')
                            with act3:
                                with ui.element('div').classes('flex items-center justify-between w-full px-3 py-1.5'):
                                    with ui.element('div').classes('flex items-center gap-3'):
                                        with ui.element('div').classes('h-7 w-7 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center shrink-0'):
                                            ui.html(get_icon('file-text', 'h-3.5 w-3.5 text-emerald-400'))
                                        with ui.element('div').classes('text-left'):
                                            ui.label('Download Operational Ledger').classes('block font-semibold text-slate-200')
                                            ui.label('Generate Excel/CSV packages').classes('text-[10px] text-slate-500 font-mono')
                                    ui.html(get_icon('arrow-right', 'h-4 w-4 text-slate-500'))
