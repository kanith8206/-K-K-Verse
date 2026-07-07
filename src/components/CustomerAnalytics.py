from nicegui import ui
import datetime
from src.components.Icons import get_icon

class CustomerAnalytics:
    def __init__(self, customers, theme: str, on_add_customer):
        self.customers = customers
        self.theme = theme
        self.on_add_customer = on_add_customer

        self.search_query = ''
        self.selected_segment = 'All'
        self.selected_tier = 'All'

        # Form states for adding customer (CRUD)
        self.form_name = ''
        self.form_email = ''
        self.form_segment = 'Enterprise'
        self.form_tier = 'Platinum'
        self.form_region = 'North America'
        self.form_monthly_spend = 5000

        # Elements reference
        self.main_container = None
        self.add_cust_dialog = None

    def handle_submit_customer(self):
        if not self.form_name or not self.form_email:
            return

        new_cust = {
            "id": f"CUST-0{len(self.customers) + 1}",
            "name": self.form_name,
            "email": self.form_email,
            "segment": self.form_segment,
            "clv": self.form_monthly_spend * 12.0, # Estimation
            "retentionScore": 90.0,
            "loyaltyTier": self.form_tier,
            "region": self.form_region,
            "tenureMonths": 1,
            "monthlySpend": self.form_monthly_spend,
            "lastActive": datetime.date.today().strftime("%Y-%m-%d"),
            "activityTrend": "Stable"
        }

        self.on_add_customer(new_cust)
        self.add_cust_dialog.close()

        # Reset states
        self.form_name = ''
        self.form_email = ''
        self.form_monthly_spend = 5000
        self.refresh()

    def filter_customers(self):
        q = self.search_query.lower()
        res = []
        for c in self.customers:
            matches_search = q in c["name"].lower() or q in c["email"].lower()
            matches_segment = self.selected_segment == 'All' or c["segment"] == self.selected_segment
            matches_tier = self.selected_tier == 'All' or c["loyaltyTier"] == self.selected_tier
            if matches_search and matches_segment and matches_tier:
                res.append(c)
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

        filtered = self.filter_customers()
        active_count = len(filtered)
        
        avg_clv = sum(c["clv"] for c in filtered) / active_count if active_count > 0 else 0.0
        avg_tenure = sum(c["tenureMonths"] for c in filtered) / active_count if active_count > 0 else 0.0

        # Segment ratios
        segments = ['Enterprise', 'Mid-Market', 'SMB']
        segment_counts = {seg: len([c for c in filtered if c["segment"] == seg]) for seg in segments}

        # Render Content
        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full'):
                with ui.element('div'):
                    ui.label('Customer Intelligence Workspace').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Corporate accounts profiles, lifetime value (CLV) distributions, and activity indexes.').classes('text-xs text-slate-500')
                
                ui.button('Register New Customer Account', on_click=self.add_cust_dialog.open).classes(
                    'px-4 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-xs tracking-wide shadow-lg shadow-indigo-500/15 hover:bg-indigo-700 hover:scale-[1.02] active:scale-[0.98]'
                ).style('text-transform: none !important;')

            # Filter Console
            with ui.element('div').classes(f'p-4 rounded-xl border flex flex-col md:flex-row items-center justify-between gap-4 {card_bg} w-full'):
                # Search Input
                with ui.element('div').classes('relative w-full md:w-80'):
                    search_input = ui.input(
                        placeholder='Search account name or email...',
                        value=self.search_query,
                        on_change=lambda e: [setattr(self, 'search_query', e.value), self.refresh()]
                    ).classes('w-full text-xs text-white border-slate-800 focus:border-indigo-500').props('dark filled dense').style('border-radius: 8px;')
                    search_input.add_slot('prepend', get_icon('search', 'h-4 w-4 text-slate-500'))

                # Segment and Loyalty selectors
                with ui.element('div').classes('flex flex-wrap items-center gap-4 text-xs'):
                    with ui.element('div').classes('flex items-center gap-1.5 text-slate-400'):
                        ui.html(get_icon('filter', 'h-3.5 w-3.5 text-slate-400'))
                        ui.label('Filters:')
                    
                    # Segment select dropdown
                    seg_filter = ui.select(
                        {'All': 'All Segments', 'Enterprise': 'Enterprise', 'Mid-Market': 'Mid-Market', 'SMB': 'SMB'},
                        value=self.selected_segment,
                        on_change=lambda e: [setattr(self, 'selected_segment', e.value), self.refresh()]
                    ).classes('text-xs dark bg-slate-900 border-slate-800 rounded').props('dense filled')
                    
                    # Loyalty select dropdown
                    tier_filter = ui.select(
                        {'All': 'All Loyalty Tiers', 'Platinum': 'Platinum', 'Gold': 'Gold', 'Silver': 'Silver', 'Bronze': 'Bronze'},
                        value=self.selected_tier,
                        on_change=lambda e: [setattr(self, 'selected_tier', e.value), self.refresh()]
                    ).classes('text-xs dark bg-slate-900 border-slate-800 rounded').props('dense filled')

            # KPIs Row
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-5 w-full'):
                with ui.element('div').classes(f'p-4 rounded-xl border {card_bg}'):
                    ui.label('Accounts Profile Scope').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                    ui.label(f"{active_count} Account row(s)").classes(f'text-xl font-bold font-display {text_color}')
                    ui.label('Active segment filters applied').classes('text-[10px] font-mono text-indigo-400 mt-1 block')

                with ui.element('div').classes(f'p-4 rounded-xl border {card_bg}'):
                    ui.label('Average Account CLV').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                    ui.label(f"${int(avg_clv):,}").classes(f'text-xl font-bold font-display text-indigo-400')
                    ui.label('Value over billing history').classes('text-[10px] font-mono text-slate-400 mt-1 block')

                with ui.element('div').classes(f'p-4 rounded-xl border {card_bg}'):
                    ui.label('Mean Contract Tenure').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                    ui.label(f"{avg_tenure:.1f} Months").classes(f'text-xl font-bold font-display {text_color}')
                    ui.label('Loyal relationship length').classes('text-[10px] font-mono text-indigo-400 mt-1 block')

            # Split charts row
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Segment Profiles
                with ui.element('div').classes(f'lg:col-span-4 p-5 rounded-2xl border {card_bg} text-left'):
                    ui.label('Client Segment Profiles').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                    ui.label('Aggregate ratios by contractual category').classes('text-[10px] font-mono text-slate-500 mb-6')
                    
                    with ui.element('div').classes('space-y-4'):
                        for seg in segments:
                            count = segment_counts[seg]
                            pct = (count / active_count) * 100 if active_count > 0 else 0
                            with ui.element('div').classes('p-3.5 rounded-xl bg-white/5 border border-white/5'):
                                with ui.element('div').classes('flex justify-between items-center text-xs mb-1'):
                                    ui.label(seg).classes('font-semibold text-slate-300')
                                    ui.label(f"{count} ({pct:.0f}%)").classes('font-mono text-indigo-400 font-bold')
                                with ui.element('div').classes('h-1.5 rounded-full bg-slate-800 overflow-hidden'):
                                    ui.element('div').classes('bg-indigo-500 h-full').style(f'width: {pct}%;')

                # CLV Distribution columns
                with ui.element('div').classes(f'lg:col-span-8 p-5 rounded-2xl border {card_bg} text-left'):
                    ui.label('Estimated Account Lifetime Value Curves').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                    ui.label('Chronological distribution curve of corporate client valuations').classes('text-[10px] font-mono text-slate-500 mb-6')
                    
                    # Columns rendering in NiceGUI (using HTML structures)
                    max_clv = max(c["clv"] for c in self.customers) if self.customers else 1.0
                    col_html = '<div class="h-44 flex items-end gap-3 justify-between pb-2 font-mono w-full">'
                    for cust in filtered:
                        pct = (cust["clv"] / max_clv) * 100
                        # Color coding based on tier
                        if cust["loyaltyTier"] == 'Platinum':
                            grad = 'from-indigo-500 to-indigo-700'
                        elif cust["loyaltyTier"] == 'Gold':
                            grad = 'from-yellow-500 to-yellow-600'
                        elif cust["loyaltyTier"] == 'Silver':
                            grad = 'from-slate-400 to-slate-500'
                        else:
                            grad = 'from-amber-700 to-amber-800'
                            
                        # Custom tooltip
                        col_html += f"""
                        <div class="flex-1 flex flex-col items-center group relative cursor-pointer h-full justify-end">
                          <div class="absolute bottom-full mb-2 bg-slate-950 border border-white/10 px-2 py-1 rounded text-[9px] text-white opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-20 pointer-events-none">
                            {cust["name"]}: ${cust["clv"]:,}
                          </div>
                          <div class="w-full rounded-t-lg bg-gradient-to-t {grad} transition-all duration-300 group-hover:opacity-90" style="height: {pct}%;"></div>
                          <span class="text-[8px] text-slate-500 uppercase mt-2 hidden md:block select-none truncate max-w-[40px]">
                            {cust["name"][:5]}
                          </span>
                        </div>
                        """
                    col_html += '</div>'
                    ui.html(col_html).classes('w-full')

            # Table list
            with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} w-full text-left'):
                ui.label('Chronological Accounts Table').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                ui.label(f'Total active accounts: {len(filtered)}').classes('text-[10px] font-mono text-slate-500 mb-4')

                table_html = """
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-left border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-[10px] font-mono text-slate-500 uppercase">
                        <th class="py-2.5 px-3">Account ID</th>
                        <th class="py-2.5 px-3">Name</th>
                        <th class="py-2.5 px-3">Segment</th>
                        <th class="py-2.5 px-3">Region</th>
                        <th class="py-2.5 px-3">Tenure</th>
                        <th class="py-2.5 px-3">Monthly Spend</th>
                        <th class="py-2.5 px-3">Activity Trend</th>
                        <th class="py-2.5 px-3 text-right">Retention Status</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-xs">
                """
                for cust in filtered:
                    trend_val = cust["activityTrend"]
                    if trend_val == 'Upward':
                        trend_char, trend_color = '▲', 'text-emerald-400'
                    elif trend_val == 'Declining':
                        trend_char, trend_color = '▼', 'text-red-400'
                    else:
                        trend_char, trend_color = '●', 'text-slate-400'

                    score = cust["retentionScore"]
                    if score >= 85:
                        score_bg = 'bg-emerald-500/10 text-emerald-400'
                    elif score >= 60:
                        score_bg = 'bg-yellow-500/10 text-yellow-400'
                    else:
                        score_bg = 'bg-red-500/10 text-red-400'

                    table_html += f"""
                      <tr class="hover:bg-white/5 transition-colors">
                        <td class="py-3 px-3 font-mono text-indigo-400">{cust["id"]}</td>
                        <td class="py-3 px-3">
                          <span class="block font-semibold text-slate-200">{cust["name"]}</span>
                          <span class="text-[10px] text-slate-500 font-mono">{cust["email"]}</span>
                        </td>
                        <td class="py-3 px-3">
                          <span class="inline-block px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-white/5 border border-white/5">
                            {cust["segment"].upper()}
                          </span>
                        </td>
                        <td class="py-3 px-3 font-mono text-slate-400">{cust["region"]}</td>
                        <td class="py-3 px-3 font-mono">{cust["tenureMonths"]} Months</td>
                        <td class="py-3 px-3 font-semibold font-mono">${cust["monthlySpend"]:,}</td>
                        <td class="py-3 px-3">
                          <span class="inline-flex items-center gap-1 text-[10px] font-mono font-bold {trend_color}">
                            {trend_char} {trend_val.upper()}
                          </span>
                        </td>
                        <td class="py-3 px-3 text-right">
                          <span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold {score_bg}">
                            {int(score)}% INDEX
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

    def render(self):
        is_dark = self.theme == 'dark'
        card_class = 'bg-slate-950/95 border-white/10 text-slate-100 backdrop-blur-md shadow-2xl' if is_dark else 'bg-white border-slate-200 text-slate-900 shadow-xl'

        # Modal Registration Dialog
        self.add_cust_dialog = ui.dialog()
        with self.add_cust_dialog:
            with ui.card().classes(f'w-full max-w-md p-6 {card_class} text-left'):
                ui.label('Register Enterprise Client').classes('font-display font-bold text-lg mb-1')
                ui.label('Insert new company records directly into the operational database system.').classes('text-[11px] text-slate-500 mb-6')

                with ui.element('div').classes('space-y-4 w-full text-left'):
                    # Company Name
                    with ui.element('div').classes('space-y-1 text-left'):
                        ui.label('Company Entity Name').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                        name_input = ui.input(
                            placeholder='Acme Global Inc',
                            value=self.form_name,
                            on_change=lambda e: setattr(self, 'form_name', e.value)
                        ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    # Email
                    with ui.element('div').classes('space-y-1 text-left'):
                        ui.label('Billing/Ops Email').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                        email_input = ui.input(
                            placeholder='procurement@acme.com',
                            value=self.form_email,
                            on_change=lambda e: setattr(self, 'form_email', e.value)
                        ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    # Grid options
                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Segment select
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Segment Class').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            seg_select = ui.select(
                                {'Enterprise': 'Enterprise', 'Mid-Market': 'Mid-Market', 'SMB': 'SMB'},
                                value=self.form_segment,
                                on_change=lambda e: setattr(self, 'form_segment', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')
                            
                        # Loyalty tier select
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Loyalty Level').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            tier_select = ui.select(
                                {'Platinum': 'Platinum', 'Gold': 'Gold', 'Silver': 'Silver', 'Bronze': 'Bronze'},
                                value=self.form_tier,
                                on_change=lambda e: setattr(self, 'form_tier', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Region select
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Region Territory').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            reg_select = ui.select(
                                {'North America': 'North America', 'Europe': 'Europe', 'APAC': 'APAC', 'LATAM': 'LATAM'},
                                value=self.form_region,
                                on_change=lambda e: setattr(self, 'form_region', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')
                            
                        # Monthly spend
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Est. Monthly Spend').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            spend_input = ui.number(
                                value=self.form_monthly_spend,
                                min=100,
                                format='%.0f',
                                on_change=lambda e: setattr(self, 'form_monthly_spend', float(e.value or 0))
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    # Actions row
                    with ui.element('div').classes('flex justify-end gap-3 pt-4 border-t border-white/5 w-full'):
                        ui.button('Cancel', on_click=self.add_cust_dialog.close).classes(
                            'px-4 py-2 rounded-lg text-xs font-semibold bg-white/5 border border-white/5 hover:bg-white/10 text-slate-450'
                        ).style('text-transform: none !important;')
                        
                        ui.button('Confirm Account Registration', on_click=self.handle_submit_customer).classes(
                            'px-4 py-2 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white'
                        ).style('text-transform: none !important;')

        # Render Main
        self.main_container = ui.element('div').classes('w-full')
        with self.main_container:
            self.render_content()
