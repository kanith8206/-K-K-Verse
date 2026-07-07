from nicegui import ui
from src.components.Icons import get_icon

class InventoryAnalytics:
    def __init__(self, products, theme: str, on_add_product, on_update_stock):
        self.products = products
        self.theme = theme
        self.on_add_product = on_add_product
        self.on_update_stock = on_update_stock

        self.search_query = ''
        self.selected_category = 'All'

        # Form states for adding product (CRUD)
        self.form_name = ''
        self.form_category = 'Software License'
        self.form_price = 1000
        self.form_cost = 300
        self.form_stock = 100
        self.form_threshold = 15
        self.form_warehouse = 'Cloud Cluster West'

        # References
        self.main_container = None
        self.add_prod_dialog = None

    def handle_submit_product(self):
        if not self.form_name:
            return

        new_prod = {
            "id": f"PROD-0{len(self.products) + 1}",
            "name": self.form_name,
            "category": self.form_category,
            "price": float(self.form_price),
            "cost": float(self.form_cost),
            "stock": int(self.form_stock),
            "minStockThreshold": int(self.form_threshold),
            "warehouseLocation": self.form_warehouse,
            "status": 'Out of Stock' if self.form_stock == 0 else 'Low Stock' if self.form_stock <= self.form_threshold else 'In Stock'
        }

        self.on_add_product(new_prod)
        self.add_prod_dialog.close()

        # Reset states
        self.form_name = ''
        self.form_price = 1000
        self.form_cost = 300
        self.form_stock = 100
        self.form_threshold = 15
        self.refresh()

    def handle_refill_stock(self, prod_id: str):
        prod = next((p for p in self.products if p["id"] == prod_id), None)
        if not prod:
            return
        target = prod["stock"] + 50
        self.on_update_stock(prod_id, target)
        self.refresh()

    def filter_products(self):
        q = self.search_query.lower()
        res = []
        for p in self.products:
            matches_search = q in p["name"].lower() or q in p["warehouseLocation"].lower()
            matches_category = self.selected_category == 'All' or p["category"] == self.selected_category
            if matches_search and matches_category:
                res.append(p)
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

        filtered = self.filter_products()
        low_stock_alerts = [p for p in self.products if p["stock"] <= p["minStockThreshold"]]

        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full'):
                with ui.element('div'):
                    ui.label('Warehouse Intelligence Center').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Logistics stocks tracking, threshold monitoring, and product database row administration.').classes('text-xs text-slate-500')
                
                ui.button('Add Catalog Product Row', on_click=self.add_prod_dialog.open).classes(
                    'px-4 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-xs tracking-wide shadow-lg shadow-indigo-500/15 hover:bg-indigo-700 hover:scale-[1.02] active:scale-[0.98]'
                ).style('text-transform: none !important;')

            # Filter bar
            with ui.element('div').classes(f'p-4 rounded-xl border flex flex-col md:flex-row items-center justify-between gap-4 {card_bg} w-full'):
                # Search Input
                with ui.element('div').classes('relative w-full md:w-80'):
                    search_input = ui.input(
                        placeholder='Search catalog ID or warehouse...',
                        value=self.search_query,
                        on_change=lambda e: [setattr(self, 'search_query', e.value), self.refresh()]
                    ).classes('w-full text-xs text-white border-slate-800 focus:border-indigo-500').props('dark filled dense').style('border-radius: 8px;')
                    search_input.add_slot('prepend', get_icon('search', 'h-4 w-4 text-slate-500'))

                # Category select
                with ui.element('div').classes('flex items-center gap-3 text-xs w-full md:w-auto justify-end'):
                    ui.label('Category:').classes('text-slate-400')
                    cat_select = ui.select(
                        {
                            'All': 'All Categories',
                            'Software License': 'Software License',
                            'Cloud Storage': 'Cloud Storage',
                            'Consulting': 'Consulting',
                            'Hardware': 'Hardware',
                            'Support': 'Support'
                        },
                        value=self.selected_category,
                        on_change=lambda e: [setattr(self, 'selected_category', e.value), self.refresh()]
                    ).classes('text-xs dark bg-slate-900 border-slate-800 rounded').props('dense filled')

            # Alerts box
            if low_stock_alerts:
                alert_names = ", ".join(p["name"] for p in low_stock_alerts)
                with ui.element('div').classes('p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 flex gap-3 text-left w-full'):
                    ui.html(get_icon('alert-triangle', 'h-5 w-5 text-amber-400 shrink-0 mt-0.5 animate-bounce'))
                    with ui.element('div'):
                        ui.label('LOW STOCK CRITICAL WARP ALERTS').classes('font-mono text-[10px] font-bold text-amber-400 uppercase tracking-widest block mb-0.5')
                        ui.label(f"The following {len(low_stock_alerts)} catalog product(s) are below safety margins: {alert_names}. Trigger stock replenishment logs immediately.").classes('text-xs text-slate-300 leading-normal')

            # Main Stock Table Card
            with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg} w-full text-left'):
                ui.label('Stock Portfolio Matrix').classes(f'font-display font-bold text-sm mb-1 {text_color}')
                ui.label(f'Total catalog rows tracked: {len(filtered)}').classes('text-[10px] font-mono text-slate-500 mb-4')

                table_html = """
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-left border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-[10px] font-mono text-slate-500 uppercase">
                        <th class="py-2.5 px-3">Catalog ID</th>
                        <th class="py-2.5 px-3">Name</th>
                        <th class="py-2.5 px-3">Class Category</th>
                        <th class="py-2.5 px-3">Wholesale Cost</th>
                        <th class="py-2.5 px-3">License Price</th>
                        <th class="py-2.5 px-3">Stock count</th>
                        <th class="py-2.5 px-3">Fulfillment Hub</th>
                        <th class="py-2.5 px-3 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-xs">
                """
                for prod in filtered:
                    is_low = prod["stock"] <= prod["minStockThreshold"]
                    is_out = prod["stock"] == 0
                    row_bg = 'bg-amber-500/5' if is_low else ''
                    stock_color = 'text-red-400' if is_out else 'text-amber-400' if is_low else 'text-slate-200'
                    stock_bar_color = 'bg-red-400' if is_out else 'bg-amber-400' if is_low else 'bg-emerald-400'
                    
                    bar_pct = min((prod["stock"] / 100.0) * 100.0, 100.0)

                    btn_lbl = "REFILL (+50)" if (is_low or is_out) else "ADD STOCK"
                    btn_cls = "bg-amber-500 text-slate-950 hover:bg-amber-400" if (is_low or is_out) else "bg-white/5 text-slate-400 hover:text-white hover:bg-white/10"

                    table_html += f"""
                      <tr class="hover:bg-white/5 transition-colors {row_bg}">
                        <td class="py-3 px-3 font-mono text-indigo-400">{prod["id"]}</td>
                        <td class="py-3 px-3 font-semibold text-slate-200">{prod["name"]}</td>
                        <td class="py-3 px-3">
                          <span class="inline-block px-2 py-0.5 rounded text-[10px] font-mono bg-white/5 border border-white/5 uppercase">
                            {prod["category"]}
                          </span>
                        </td>
                        <td class="py-3 px-3 font-mono text-slate-500">${prod["cost"]:,}</td>
                        <td class="py-3 px-3 font-semibold font-mono">${prod["price"]:,}</td>
                        <td class="py-3 px-3">
                          <div class="flex items-center gap-2">
                            <span class="font-mono font-bold {stock_color}">
                              {prod["stock"]:,}
                            </span>
                            <div class="w-16 bg-slate-800 h-1 rounded overflow-hidden">
                              <div style="width: {bar_pct}%;" class="h-full {stock_bar_color}"></div>
                            </div>
                          </div>
                        </td>
                        <td class="py-3 px-3 text-slate-400 font-mono text-[11px]">{prod["warehouseLocation"]}</td>
                        <td class="py-3 px-3 text-right">
                          <button
                            onclick="refillProductStock('{prod["id"]}')"
                            class="px-2.5 py-1 text-[10px] font-mono font-bold rounded active:scale-[0.98] transition-all {btn_cls}"
                          >
                            {btn_lbl}
                          </button>
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

        # Add Product Dialog definition
        self.add_prod_dialog = ui.dialog()
        with self.add_prod_dialog:
            with ui.card().classes(f'w-full max-w-md p-6 {card_class} text-left'):
                ui.label('Add Catalog Product Row').classes('font-display font-bold text-lg mb-1')
                ui.label('Write catalog asset definitions and initial stock pools into the database.').classes('text-[11px] text-slate-500 mb-6')

                with ui.element('div').classes('space-y-4 w-full text-left'):
                    # Product Name
                    with ui.element('div').classes('space-y-1 text-left'):
                        ui.label('Product Asset Name').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                        name_input = ui.input(
                            placeholder='Enterprise Kubernetes Node License',
                            value=self.form_name,
                            on_change=lambda e: setattr(self, 'form_name', e.value)
                        ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Category select
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Class Category').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            cat_select = ui.select(
                                {
                                    'Software License': 'Software License',
                                    'Cloud Storage': 'Cloud Storage',
                                    'Consulting': 'Consulting',
                                    'Hardware': 'Hardware',
                                    'Support': 'Support'
                                },
                                value=self.form_category,
                                on_change=lambda e: setattr(self, 'form_category', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                        # WarehouseLocation
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Fulfillment Node').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            wh_input = ui.input(
                                placeholder='Cloud AWS Central US',
                                value=self.form_warehouse,
                                on_change=lambda e: setattr(self, 'form_warehouse', e.value)
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Price
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('License Price ($)').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            price_input = ui.number(
                                value=self.form_price,
                                min=1,
                                format='%.0f',
                                on_change=lambda e: setattr(self, 'form_price', float(e.value or 0))
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                        # Cost
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Wholesale Cost ($)').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            cost_input = ui.number(
                                value=self.form_cost,
                                min=1,
                                format='%.0f',
                                on_change=lambda e: setattr(self, 'form_cost', float(e.value or 0))
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    with ui.element('div').classes('grid grid-cols-2 gap-4'):
                        # Stock
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Starting Stock').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            stock_input = ui.number(
                                value=self.form_stock,
                                min=0,
                                format='%.0f',
                                on_change=lambda e: setattr(self, 'form_stock', int(e.value or 0))
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                        # Threshold
                        with ui.element('div').classes('space-y-1 text-left'):
                            ui.label('Low Stock Alert Threshold').classes('text-[10px] font-mono text-slate-400 uppercase tracking-widest')
                            thresh_input = ui.number(
                                value=self.form_threshold,
                                min=1,
                                format='%.0f',
                                on_change=lambda e: setattr(self, 'form_threshold', int(e.value or 1))
                            ).classes('w-full text-xs bg-slate-900 border-slate-800 rounded-lg dark').props('dense filled')

                    # Actions row
                    with ui.element('div').classes('flex justify-end gap-3 pt-4 border-t border-white/5 w-full'):
                        ui.button('Cancel', on_click=self.add_prod_dialog.close).classes(
                            'px-4 py-2 rounded-lg text-xs font-semibold bg-white/5 border border-white/5 hover:bg-white/10 text-slate-450'
                        ).style('text-transform: none !important;')
                        
                        ui.button('Write Product Row', on_click=self.handle_submit_product).classes(
                            'px-4 py-2 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white'
                        ).style('text-transform: none !important;')

        # Setup standard NiceGUI JS callbacks for HTML table click integration
        # This resolves the refillProductStock call from within the rendered HTML string!
        ui.on_page_ready(lambda: ui.run_javascript(f"""
            window.refillProductStock = function(prodId) {{
                const target = "{self.on_page_refill_script_link()}";
                // Trigger a python method call via standard NiceGUI event
                // We will attach an event listener or run a script query
                nicegui.run_with_id('{self.main_container.id}', 'refill', {{'id': prodId}});
            }};
        """))

        self.main_container = ui.element('div').classes('w-full')
        # Handle the refill event fired from javascript
        self.main_container.on('refill', lambda msg: self.handle_refill_stock(msg.args['id']))
        with self.main_container:
            self.render_content()

    def on_page_refill_script_link(self):
        return "nicegui_refill_callback"
