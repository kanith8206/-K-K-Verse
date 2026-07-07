from nicegui import ui
import copy
import datetime
from src.components.LandingPage import LandingPage
from src.components.AuthPage import AuthPage
from src.components.Sidebar import Sidebar
from src.components.Dashboard import Dashboard
from src.components.SalesAnalytics import SalesAnalytics
from src.components.CustomerAnalytics import CustomerAnalytics
from src.components.ChurnPrediction import ChurnPrediction
from src.components.SalesForecasting import SalesForecasting
from src.components.InventoryAnalytics import InventoryAnalytics
from src.components.AICopilot import AICopilot
from src.components.InteractiveReports import InteractiveReports

from src.data import INITIAL_SALES, INITIAL_CUSTOMERS, INITIAL_PRODUCTS

class AppState:
    def __init__(self):
        self.is_authenticated = False
        self.active_tab = 'landing' # landing, auth, dashboard, sales, customers, churn, forecasting, inventory, copilot, reports, settings
        self.theme = 'dark'

        # Client-specific mock DB session copy
        self.sales = copy.deepcopy(INITIAL_SALES)
        self.customers = copy.deepcopy(INITIAL_CUSTOMERS)
        self.products = copy.deepcopy(INITIAL_PRODUCTS)

        # References
        self.layout_container = None

    def set_active_tab(self, tab: str):
        self.active_tab = tab
        self.refresh()

    def set_theme(self, theme: str):
        self.theme = theme
        self.refresh()

    def handle_login_success(self, user_info):
        self.is_authenticated = True
        self.active_tab = 'dashboard'
        self.refresh()

    def handle_logout(self):
        self.is_authenticated = False
        self.active_tab = 'landing'
        self.refresh()

    # CRUD database helper functions
    def handle_add_customer(self, new_cust):
        self.customers.insert(0, new_cust)
        self.refresh()

    def handle_add_product(self, new_prod):
        self.products.insert(0, new_prod)
        self.refresh()

    def handle_update_stock(self, prod_id: str, new_stock: int):
        for p in self.products:
            if p["id"] == prod_id:
                p["stock"] = new_stock
                p["status"] = 'Out of Stock' if new_stock == 0 else 'Low Stock' if new_stock <= p["minStockThreshold"] else 'In Stock'
                break
        self.refresh()

    def handle_add_sale(self, new_sale):
        self.sales.insert(0, new_sale)

        # Deduct product stock
        for p in self.products:
            if p["id"] == new_sale["productId"]:
                remaining = max(0, p["stock"] - new_sale["quantity"])
                p["stock"] = remaining
                p["status"] = 'Out of Stock' if remaining == 0 else 'Low Stock' if remaining <= p["minStockThreshold"] else 'In Stock'
                break

        # Update customer spend data
        for c in self.customers:
            if c["id"] == new_sale["customerId"]:
                c["monthlySpend"] += (new_sale["totalRevenue"] / 12.0)
                c["clv"] += new_sale["totalRevenue"]
                c["lastActive"] = datetime.date.today().strftime("%Y-%m-%d")
                break
        
        self.refresh()

    def refresh(self):
        if self.layout_container:
            self.layout_container.refresh()

    @ui.refreshable
    def render_layout(self):
        is_dark = self.theme == 'dark'
        bg_class = 'bg-[#0B0F19] text-slate-100' if is_dark else 'bg-slate-50 text-slate-900'
        text_color = 'text-white' if is_dark else 'text-slate-900'

        # Math aggregates computed on current mutable state
        total_rev = sum(s["totalRevenue"] for s in self.sales)
        total_cost = sum(s["totalCost"] for s in self.sales)
        total_profit = total_rev - total_cost
        
        # Pydantic or dict shape helper
        class BusinessKPIsObj:
            def __init__(self, rev, profit, margin, customers_cnt, products_cnt, churn_cnt):
                self.totalRevenue = rev
                self.totalProfit = profit
                self.profitMargin = margin
                self.totalCustomers = customers_cnt
                self.activeProductsCount = products_cnt
                self.churnRiskCount = churn_cnt

        kpi_data = BusinessKPIsObj(
            rev=total_rev,
            profit=total_profit,
            margin=round((total_profit / total_rev) * 100, 1) if total_rev > 0 else 0.0,
            customers_cnt=len(self.customers),
            products_cnt=len(self.products),
            churn_cnt=len([c for c in self.customers if c["retentionScore"] < 75])
        )

        with ui.element('div').classes(f'min-h-screen w-full flex flex-col relative overflow-hidden transition-colors duration-500 {bg_class}'):
            
            # Mesh Glow Orbs Background
            with ui.element('div').classes('absolute inset-0 pointer-events-none z-0 overflow-hidden'):
                ui.element('div').classes('absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-indigo-500/5 blur-[120px]')
                ui.element('div').classes('absolute bottom-[-10%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-indigo-600/5 blur-[120px]')

            # App wrapper
            with ui.element('div').classes('flex-1 flex relative z-10 w-full'):
                
                # Render Sidebar if authenticated and not on landing page
                if self.is_authenticated and self.active_tab not in ['landing', 'auth']:
                    sidebar_view = Sidebar(
                        active_tab=self.active_tab,
                        set_active_tab=self.set_active_tab,
                        theme=self.theme,
                        set_theme=self.set_theme,
                        on_logout=self.handle_logout
                    )
                    sidebar_view.render()

                # Content Panel
                with ui.element('main').classes('flex-1 flex flex-col p-4 md:p-8 max-w-7xl mx-auto w-full relative overflow-y-auto'):
                    
                    if self.active_tab == 'landing':
                        landing = LandingPage(
                            on_start=lambda: self.set_active_tab('auth'),
                            theme=self.theme
                        )
                        landing.render()

                    elif self.active_tab == 'auth':
                        with ui.element('div').classes('flex-1 flex items-center justify-center'):
                            auth = AuthPage(
                                on_login=self.handle_login_success,
                                theme=self.theme
                            )
                            auth.render()

                    elif self.is_authenticated:
                        with ui.element('div').classes('flex-1 space-y-6 w-full'):
                            
                            if self.active_tab == 'dashboard':
                                dashboard = Dashboard(
                                    sales=self.sales,
                                    customers=self.customers,
                                    products=self.products,
                                    theme=self.theme,
                                    set_active_tab=self.set_active_tab
                                )
                                dashboard.render()

                            elif self.active_tab == 'sales':
                                sales_view = SalesAnalytics(
                                    sales=self.sales,
                                    products=self.products,
                                    customers=self.customers,
                                    theme=self.theme,
                                    on_add_sale=self.handle_add_sale
                                )
                                sales_view.render()

                            elif self.active_tab == 'customers':
                                cust_view = CustomerAnalytics(
                                    customers=self.customers,
                                    theme=self.theme,
                                    on_add_customer=self.handle_add_customer
                                )
                                cust_view.render()

                            elif self.active_tab == 'churn':
                                churn_view = ChurnPrediction(
                                    customers=self.customers,
                                    theme=self.theme
                                )
                                churn_view.render()

                            elif self.active_tab == 'forecasting':
                                forecast_view = SalesForecasting(
                                    sales=self.sales,
                                    theme=self.theme
                                )
                                forecast_view.render()

                            elif self.active_tab == 'inventory':
                                inv_view = InventoryAnalytics(
                                    products=self.products,
                                    theme=self.theme,
                                    on_add_product=self.handle_add_product,
                                    on_update_stock=self.handle_update_stock
                                )
                                inv_view.render()

                            elif self.active_tab == 'copilot':
                                copilot_view = AICopilot(
                                    kpis=kpi_data,
                                    counts={
                                        "customersCount": len(self.customers),
                                        "salesCount": len(self.sales),
                                        "productsCount": len(self.products)
                                    },
                                    theme=self.theme
                                )
                                copilot_view.render()

                            elif self.active_tab == 'reports':
                                reports_view = InteractiveReports(
                                    sales=self.sales,
                                    theme=self.theme
                                )
                                reports_view.render()
                                
                            elif self.active_tab == 'settings':
                                # Simple settings dashboard details
                                with ui.element('div').classes('text-left space-y-4'):
                                    ui.label('Workspace Settings').classes(f'font-display text-2xl font-bold {text_color}')
                                    ui.label('Configure environment keys and active system telemetry nodes.').classes('text-xs text-slate-500')
                                    with ui.element('div').classes('p-5 rounded-2xl border border-white/5 bg-slate-900/40 text-left space-y-4 max-w-lg'):
                                        ui.label('System Telemetry Secrets').classes('text-xs font-mono text-slate-400 font-bold uppercase block')
                                        ui.input(
                                            label='GEMINI_API_KEY', 
                                            value='••••••••••••••••••••••••••••••••'
                                        ).classes('w-full dark text-xs').props('dense filled')
                                        ui.label('Verify that your API keys are added in the environment variables block or secrets panel of the project to allow live neural queries.').classes('text-[11px] text-slate-500 leading-normal block')

            # Global Footer
            with ui.element('footer').classes('py-4 text-center text-[10px] font-mono text-slate-500 border-t border-white/5 relative z-10 w-full'):
                ui.label('KKVERSE AI PLATFORM v2.5.0 • COGNITIVE BUSINESS INTELLIGENCE PLATFORM • SECURE TLS SHA256 ENCRYPTION')

    def render(self):
        self.layout_container = ui.element('div').classes('w-full')
        with self.layout_container:
            self.render_layout()
