from nicegui import ui
import datetime
import random
from src.components.Icons import get_icon

class SalesAnalytics:
    def __init__(self, sales, products, theme: str, on_add_sale, customers):
        self.sales = sales
        self.products = products
        self.theme = theme
        self.on_add_sale = on_add_sale
        self.customers = customers

        self.selected_region = 'All'
        self.search_query = ''
        
        # CRUD modal states
        self.form_customer = ''
        self.form_product = ''
        self.form_quantity = 1
        self.form_sales_rep = 'Elena Rostova'

        # Reference elements for refreshing
        self.main_container = None
        self.add_sale_dialog = None

    def handle_submit_sale(self):
        if not self.form_customer or not self.form_product:
            return

        chosen_cust = next((c for c in self.customers if c["id"] == self.form_customer), None)
        chosen_prod = next((p for p in self.products if p["id"] == self.form_product), None)
        if not chosen_cust or not chosen_prod:
            return

        rev = chosen_prod["price"] * self.form_quantity
        cost = chosen_prod["cost"] * self.form_quantity

        # Create new sale dict matching types.py Pydantic structure
        new_sale_obj = {
            "id": f"SALE-0{len(self.sales) + 1}",
            "customerId": chosen_cust["id"],
            "customerName": chosen_cust["name"],
            "productId": chosen_prod["id"],
            "productName": chosen_prod["name"],
            "quantity": self.form_quantity,
            "totalRevenue": rev,
            "totalCost": cost,
            "profit": rev - cost,
            "saleDate": datetime.date.today().strftime("%Y-%m-%d"),
            "region": random.choice(['North America', 'Europe', 'APAC', 'LATAM']),
            "salesRep": self.form_sales_rep
        }

        self.on_add_sale(new_sale_obj)
        self.add_sale_dialog.close()
        
        # Reset form states
        self.form_customer = ''
        self.form_product = ''
        self.form_quantity = 1
        self.refresh()

    def filter_sales(self):
        q = self.search_query.lower()
        res = []
        for s in self.sales:
            matches_region = self.selected_region == 'All' or s["region"] == self.selected_region
            matches_search = q in s["customerName"].lower() or q in s["productName"].lower()
            if matches_region and matches_search:
                res.append(s)
        return res

    def set_region(self, region: str):
        self.selected_region = region
        self.refresh()

    def refresh(self):
        if self.main_container:
            self.main_container.refresh()

    @ui.refreshable
    def render_content(self):
        is_dark = self.theme == 'dark'
        card_bg = 'bg-[#0F172A] border-slate-800 shadow-lg' if is_dark else 'bg-white border-slate-200 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        text_color = 'text-white' if is_dark else 'text-slate-900'

        filtered = self.filter_sales()

        # KPIs
        total_rev = sum(s["totalRevenue"] for s in filtered)
        total_cost = sum(s["totalCost"] for s in filtered)
        total_profit = total_rev - total_cost
        avg_order_value = int(total_rev / len(filtered)) if len(filtered) > 0 else 0
        profit_margin = f"{((total_profit / total_rev) * 100):.1f}" if total_rev > 0 else "0"

        # Category Breakdown
        category_summary = {}
        for s in filtered:
            prod = next((p for p in self.products if p["id"] == s["productId"]), None)
            cat = prod["category"] if prod else "Software License"
            category_summary[cat] = category_summary.get(cat, 0.0) + s["totalRevenue"]
        total_cat_revenue = sum(category_summary.values())

        # Regional Breakdown
        regional_summary = {}
        for s in filtered:
            reg = s["region"]
            regional_summary[reg] = regional_summary.get(reg, 0.0) + s["totalRevenue"]
        total_reg_revenue = sum(regional_summary.values())

        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full'):
                with ui.element('div'):
                    ui.label('Sales Analytics Intelligence').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Corporate revenue flow tracking, regional distributions, and active ledger logs.').classes('text-xs text-slate-500')
                
                btn_add = ui.button('Add New Sales Ledger Row', on_click=self.add_sale_dialog.open).classes(
                    'px-4 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-xs tracking-wide shadow-lg shadow-indigo-500/15 hover:bg-indigo-700 hover:scale-[1.02] active:scale-[0.98]'
                ).style('text-transform: none !important;')

            # Filters bar
            with ui.element('div').classes(f'p-4 rounded-xl border flex flex-col md:flex-row items-center justify-between gap-4 {card_bg} w-full'):
                
                # Search Input
                with ui.element('div').classes('relative w-full md:w-80'):
                    search_input = ui.input(
                        placeholder='Search transactions or assets...',
                        value=self.search_query,
                        on_change=lambda e: [setattr(self, 'search_query', e.value), self.refresh()]
                    ).classes('w-full text-xs text-white border-slate-800 focus:border-indigo-500').props('dark filled dense').style('border-radius: 8px;')
                    search_input.add_slot('prepend', get_icon('search', 'h-4 w-4 text-slate-500'))

                # Regional tabs
                with ui.element('div').classes('flex items-center gap-3 w-full md:w-auto justify-end'):
                    with ui.element('div').classes('flex items-center gap-1.5 text-xs text-slate-400'):
                        ui.html(get_icon('filter', 'h-3.5 w-3.5 text-slate-400'))
                        ui.label('Region:')
                    
                    with ui.element('div').classes('flex bg-white/5 p-1 rounded-lg border border-white/5 text-xs font-mono'):
                        for reg in ['All', 'North America', 'Europe', 'APAC', 'LATAM']:
                            is_sel = self.selected_region == reg
                            short_lbl = 'ALL' if reg == 'All' else reg.split(' ')[0].upper()
                            
                            reg_btn = ui.button(short_lbl, on_click=lambda r=reg: self.set_region(r)).classes('px-3 py-1 rounded-md transition-all p-0 min-h-0').style('text-transform: none !important; font-size: 10px;')
                            if is_sel:
                                reg_btn.classes('bg-indigo-500/20 text-indigo-300 font-semibold')
                            else:
                                reg_btn.classes('text-slate-400 hover:text-white')

            # Stats Cards Row
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-5 w-full'):
                # 1
                with ui.element('div').classes(f'p-4 rounded-xl border {card_bg}'):
                    ui.label('Target Yield Velocity').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                    ui.label(f"${total_rev:,}").classes(f'text-xl font-bold font-display {text_color}')
                    ui.label('Selected Scope Gross').classes('text-[10px] font-mono text-indigo-400 mt-1 block')
                # 2
                with ui.element('div').classes(f'p-4 rounded-xl border {card_bg}'):
                    ui.label('Profit Aggregate').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                    ui.label(f"${total_profit:,}").classes('text-xl font-bold font-display text-emerald-400')
                    ui.label(f'Margin: {profit_margin}% | Peak Yield').classes('text-[10px] font-mono text-slate-400 mt-1 block')
                # 3
                with ui.element('div').classes(f'p-4 rounded-xl border {card_bg}'):
                    ui.label('Average Contract Ticket').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                    ui.label(f"${avg_order_value:,}").classes(f'text-xl font-bold font-display {text_color}')
                    ui.label('Per synchronized ledger line').classes('text-[10px] font-mono text-indigo-400 mt-1 block')

            # Split charts row
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Categories Card
                with ui.element('div').classes(f'lg:col-span-6 p-5 rounded-2xl border {card_bg} text-left'):
                    ui.label('Asset Category Revenue Contribution').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                    ui.label('Percentage share of total gross revenue bookings').classes('text-[10px] font-mono text-slate-500 mb-6')
                    
                    with ui.element('div').classes('space-y-4'):
                        for cat, rev in category_summary.items():
                            pct = (rev / total_cat_revenue) * 100 if total_cat_revenue > 0 else 0
                            with ui.element('div').classes('space-y-1.5'):
                                with ui.element('div').classes('flex justify-between items-center text-xs'):
                                    ui.label(cat).classes('font-semibold text-slate-300')
                                    ui.label(f"${int(rev):,} ({pct:.1f}%)").classes('font-mono text-indigo-400 font-bold')
                                with ui.element('div').classes('h-2 rounded-full bg-slate-800 overflow-hidden relative'):
                                    ui.element('div').classes('absolute top-0 left-0 h-full rounded-full bg-indigo-600').style(f'width: {pct}%;')

                # Regions Card
                with ui.element('div').classes(f'lg:col-span-6 p-5 rounded-2xl border {card_bg} text-left'):
                    ui.label('Global Regional Matrices').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                    ui.label('Aggregate transactions density across territory bounds').classes('text-[10px] font-mono text-slate-500 mb-6')
                    
                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        for region in ['North America', 'Europe', 'APAC', 'LATAM']:
                            rev = regional_summary.get(region, 0.0)
                            pct = (rev / total_reg_revenue) * 100 if total_reg_revenue > 0 else 0
                            
                            sub_card_bg = 'bg-[#1E293B] border-slate-700/60 hover:border-indigo-500/20' if is_dark else 'bg-slate-50 border-slate-100 hover:border-indigo-200'
                            with ui.element('div').classes(f'p-4 rounded-xl border transition-all text-left {sub_card_bg}'):
                                with ui.element('div').classes('flex items-center gap-2 mb-2 text-slate-400'):
                                    ui.html(get_icon('globe', 'h-4 w-4 text-indigo-400'))
                                    ui.label(region).classes('text-[11px] font-mono uppercase font-bold tracking-wider')
                                ui.label(f"${int(rev):,}").classes(f'text-lg font-bold font-display tracking-tight {text_color}')
                                with ui.element('div').classes('w-full bg-slate-850 h-1 rounded-full mt-2 overflow-hidden'):
                                    ui.element('div').classes('bg-indigo-500 h-full').style(f'width: {pct}%;')
                                ui.label(f'{pct:.1f}% density index').classes('text-[9px] font-mono text-slate-500 block mt-1.5')

            # Table Card
            with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} w-full text-left'):
                ui.label('Asset Operational Ledger Rows').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                ui.label(f'Total filtered ledger lines count: {len(filtered)}').classes('text-[10px] font-mono text-slate-500 mb-4')

                table_html = """
                <div class="overflow-x-auto w-full">
                  <table class="w-full border-collapse text-left">
                    <thead>
                      <tr class="border-b border-white/5 text-[10px] font-mono text-slate-500 uppercase">
                        <th class="py-2.5 px-3">Transaction ID</th>
                        <th class="py-2.5 px-3">Client Entity</th>
                        <th class="py-2.5 px-3">Product Name</th>
                        <th class="py-2.5 px-3">Qty</th>
                        <th class="py-2.5 px-3">Total Cost</th>
                        <th class="py-2.5 px-3">Total Revenue</th>
                        <th class="py-2.5 px-3">Net Profit</th>
                        <th class="py-2.5 px-3">Rep</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-xs">
                """
                for sale in filtered:
                    table_html += f"""
                      <tr class="hover:bg-white/5 transition-colors">
                        <td class="py-3 px-3 font-mono text-indigo-400">{sale["id"]}</td>
                        <td class="py-3 px-3 font-semibold text-slate-200">{sale["customerName"]}</td>
                        <td class="py-3 px-3 text-slate-400">{sale["productName"]}</td>
                        <td class="py-3 px-3 font-mono">{sale["quantity"]}</td>
                        <td class="py-3 px-3 font-mono text-slate-500">${sale["totalCost"]:,}</td>
                        <td class="py-3 px-3 font-mono font-semibold">${sale["totalRevenue"]:,}</td>
                        <td class="py-3 px-3 font-mono text-emerald-400 font-bold">${sale["profit"]:,}</td>
                        <td class="py-3 px-3 text-slate-400 text-[11px] font-semibold">{sale["salesRep"]}</td>
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

        # Add Sale Dialog definition
        self.add_sale_dialog = ui.dialog()
        with self.add_sale_dialog:
            with ui.card().classes(f'w-full max-w-lg p-6 {card_class} text-left'):
                ui.label('Add Sales Transaction Ledger').classes('font-display font-bold text-lg mb-1')
                ui.label('Log manual corporate invoice or license allocation instantly into the synchronized DB.').classes('text-[11px] text-slate-500 mb-6')

                with ui.element('div').classes('space-y-4 w-full'):
                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Customer selection
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Select Client').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            # NiceGUI dropdown
                            cust_sel = ui.select(
                                {c["id"]: c["name"] for c in self.customers},
                                label='Client',
                                on_change=lambda e: setattr(self, 'form_customer', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')
                            
                        # Product selection
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Select Product Asset').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            prod_sel = ui.select(
                                {p["id"]: f'{p["name"]} (${p["price"]})' for p in self.products},
                                label='Product',
                                on_change=lambda e: setattr(self, 'form_product', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Quantity
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Quantity Seats').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            qty_input = ui.number(
                                value=self.form_quantity,
                                min=1,
                                format='%.0f',
                                on_change=lambda e: setattr(self, 'form_quantity', int(e.value or 1))
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                        # Sales rep
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Allocated Sales Rep').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            rep_input = ui.input(
                                value=self.form_sales_rep,
                                on_change=lambda e: setattr(self, 'form_sales_rep', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    # Actions row
                    with ui.element('div').classes('flex justify-end gap-3 pt-4 border-t border-white/5 w-full'):
                        ui.button('Cancel', on_click=self.add_sale_dialog.close).classes(
                            'px-4 py-2 rounded-lg text-xs font-semibold bg-white/5 border border-white/5 hover:bg-white/10 text-slate-450'
                        ).style('text-transform: none !important;')
                        
                        ui.button('Synchronize DB Row', on_click=self.handle_submit_sale).classes(
                            'px-4 py-2 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white'
                        ).style('text-transform: none !important;')

        # Render container
        self.main_container = ui.element('div').classes('w-full')
        with self.main_container:
            self.render_content()
