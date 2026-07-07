from nicegui import ui
from src.components.Icons import get_icon
from src.data import INITIAL_USER

class Sidebar:
    def __init__(self, active_tab: str, set_active_tab, theme: str, set_theme, on_logout):
        self.active_tab = active_tab
        self.set_active_tab = set_active_tab
        self.theme = theme
        self.set_theme = set_theme
        self.on_logout = on_logout
        
        self.collapsed = False
        self.show_notifications = False
        self.search_query = ''

        # Reference to elements for redrawing
        self.container = None
        self.search_dialog = None
        self.notifications_dialog = None
        
        self.navigation_items = [
            {"id": "dashboard", "label": "Executive Dashboard", "icon": "bar-chart-3", "category": "CORE"},
            {"id": "sales", "label": "Sales Analytics", "icon": "trending-up", "category": "INTELLIGENCE"},
            {"id": "customers", "label": "Customer Analytics", "icon": "users", "category": "INTELLIGENCE"},
            {"id": "churn", "label": "Churn Prediction Lab", "icon": "cpu", "category": "PREDICTIVE"}, # using cpu for brain
            {"id": "forecasting", "label": "Sales Forecasting", "icon": "activity", "category": "PREDICTIVE"},
            {"id": "inventory", "label": "Warehouse Intelligence", "icon": "database", "category": "LOGISTICS"},
            {"id": "copilot", "label": "AI Copilot Workspace", "icon": "sparkles", "category": "COGNITIVE"},
            {"id": "reports", "label": "Reporting Center", "icon": "file-text", "category": "COMPLIANCE"},
            {"id": "settings", "label": "Workspace Settings", "icon": "sliders-horizontal", "category": "SYSTEM"} # using sliders for settings
        ]

        self.demo_notifications = [
            {"id": 1, "text": "XGBoost forecasting model calibrated successfully.", "time": "4m ago", "unread": True},
            {"id": 2, "text": "APAC region low-stock warning: Gateway Module v4.", "time": "1h ago", "unread": True},
            {"id": 3, "text": "Client Globex Inc. registered Activity Drift decrease of -14%.", "time": "4h ago", "unread": False}
        ]

    def toggle_collapse(self):
        self.collapsed = not self.collapsed
        self.refresh()

    def select_tab(self, tab_id: str):
        self.active_tab = tab_id
        self.set_active_tab(tab_id)
        self.refresh()

    def toggle_theme(self):
        new_theme = 'light' if self.theme == 'dark' else 'dark'
        self.theme = new_theme
        self.set_theme(new_theme)
        self.refresh()

    def open_search(self):
        if self.search_dialog:
            self.search_dialog.open()

    def open_notifications(self):
        if self.notifications_dialog:
            self.notifications_dialog.open()

    def refresh(self):
        if self.container:
            self.container.clear()
            with self.container:
                self.build_sidebar()

    def build_sidebar(self):
        is_dark = self.theme == 'dark'
        width_class = 'w-20' if self.collapsed else 'w-72'
        bg_class = 'bg-[#0F172A] border-slate-800' if is_dark else 'bg-white border-slate-200 shadow-sm'
        border_color = 'border-slate-800' if is_dark else 'border-slate-100'

        with ui.element('aside').classes(f'h-[calc(100vh-24px)] sticky top-3 left-3 z-30 flex flex-col rounded-2xl border transition-all duration-300 shadow-xl {width_class} {bg_class}'):
            
            # Header
            with ui.element('div').classes(f'p-4 border-b flex items-center justify-between relative {border_color}'):
                with ui.element('div').classes('flex items-center gap-3 overflow-hidden text-left'):
                    with ui.element('div').classes('h-10 w-10 shrink-0 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/20'):
                        ui.html(get_icon('sparkles', 'h-5 w-5 text-white'))
                    if not self.collapsed:
                        with ui.element('div').classes('text-left'):
                            ui.label('KKVerse AI').classes('font-display font-bold text-base tracking-tight bg-gradient-to-r from-white via-indigo-300 to-indigo-400 bg-clip-text text-transparent block')
                            ui.label('v4.1 ENTERPRISE').classes('text-[9px] font-mono text-slate-500 tracking-wider block')

                # Collapse Button
                btn_border = 'bg-[#0f172a] border-slate-800 text-slate-400 hover:text-white' if is_dark else 'bg-white border-slate-200 text-slate-500 hover:text-slate-900'
                collapse_btn = ui.button(on_click=self.toggle_collapse).classes(
                    f'absolute top-1/2 -right-3 -translate-y-1/2 h-6 w-6 rounded-full border flex items-center justify-center transition-colors {btn_border} p-0 min-h-0'
                ).props('flat dense')
                with collapse_btn:
                    icon_name = 'arrow-right' if self.collapsed else 'arrow-right' # simple fallback or get_icon
                    ui.html(get_icon('arrow-right' if self.collapsed else 'arrow-right', 'h-3 w-3'))

            # Search bar trigger
            with ui.element('div').classes('px-3 py-4'):
                search_btn = ui.button(on_click=self.open_search).classes(
                    'w-full py-2 px-3 rounded-xl border text-left flex items-center justify-between text-xs transition-all p-0 min-h-0'
                ).style('text-transform: none !important; font-weight: normal;')
                
                search_bg = 'bg-slate-800/50 border-slate-700/50 hover:border-slate-600 text-slate-400' if is_dark else 'bg-slate-100 border-slate-200 hover:border-slate-300 text-slate-500'
                search_btn.classes(search_bg)
                
                with search_btn:
                    with ui.element('div').classes('flex items-center gap-2 pl-3'):
                        ui.html(get_icon('search', 'h-3.5 w-3.5 text-slate-500'))
                        if not self.collapsed:
                            ui.label('Global search...')
                    if not self.collapsed:
                        with ui.element('div').classes('flex items-center gap-1 opacity-60 pr-3'):
                            ui.html(get_icon('terminal', 'h-3 w-3 text-slate-500'))
                            ui.label('K').classes('text-[10px] font-mono')

            # Nav menu
            with ui.element('nav').classes('flex-1 overflow-y-auto px-3 py-2 space-y-6 text-left'):
                for category in ['CORE', 'INTELLIGENCE', 'PREDICTIVE', 'LOGISTICS', 'COGNITIVE', 'COMPLIANCE', 'SYSTEM']:
                    category_items = [item for item in self.navigation_items if item["category"] == category]
                    if not category_items:
                        continue

                    with ui.element('div').classes('space-y-1'):
                        if not self.collapsed:
                            ui.label(category).classes('text-[10px] font-mono font-bold text-slate-500 tracking-widest block px-3 mb-1 uppercase')
                        
                        for item in category_items:
                            is_active = self.active_tab == item["id"]
                            
                            nav_btn = ui.button(on_click=lambda i=item: self.select_tab(i["id"])).classes(
                                'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium tracking-wide transition-all p-0 min-h-0 text-left'
                            ).style('text-transform: none !important; font-weight: normal;')
                            
                            if is_active:
                                active_styles = 'bg-indigo-500/15 border-l-2 border-indigo-500 text-indigo-300' if is_dark else 'bg-indigo-50 border-l-2 border-indigo-600 text-indigo-700 font-semibold'
                                nav_btn.classes(active_styles)
                            else:
                                inactive_styles = 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/50' if is_dark else 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                                nav_btn.classes(inactive_styles)

                            with nav_btn:
                                icon_color = 'text-indigo-400' if is_active else 'text-slate-500'
                                with ui.element('div').classes('flex items-center gap-3 pl-3 py-1.5'):
                                    ui.html(get_icon(item["icon"], f'h-4 w-4 shrink-0 {icon_color}'))
                                    if not self.collapsed:
                                        ui.label(item["label"]).classes('truncate')

            # Footer profile
            with ui.element('div').classes(f'p-3 border-t {border_color} space-y-4'):
                with ui.element('div').classes('flex items-center gap-3 px-2 py-1 overflow-hidden text-left'):
                    ui.image(INITIAL_USER["avatar"]).classes('h-9 w-9 rounded-xl border border-white/10 shrink-0 object-cover object-top')
                    if not self.collapsed:
                        with ui.element('div').classes('text-left min-w-0 flex-1'):
                            ui.label(INITIAL_USER["name"]).classes('block text-xs font-semibold text-slate-200 truncate' if is_dark else 'block text-xs font-semibold text-slate-800 truncate')
                            ui.label(INITIAL_USER["role"].split(' ')[0]).classes('block text-[10px] font-mono text-slate-500 truncate uppercase tracking-tight')

                # Utilities buttons row
                util_bg = 'bg-white/5' if is_dark else 'bg-slate-100'
                with ui.element('div').classes(f'flex items-center justify-between gap-1 p-1 rounded-xl {util_bg}'):
                    
                    # Theme toggle
                    theme_hover = 'hover:bg-white/5' if is_dark else 'hover:bg-slate-200'
                    theme_btn = ui.button(on_click=self.toggle_theme).classes(f'flex-1 py-1.5 rounded-lg flex justify-center text-slate-400 hover:text-white transition-all p-0 min-h-0 {theme_hover}').props('flat dense')
                    with theme_btn:
                        ui.html(get_icon('zap' if is_dark else 'sparkles', 'h-4 w-4 text-indigo-400')) # simple visuals for theme

                    # Notifications trigger
                    notif_btn = ui.button(on_click=self.open_notifications).classes(f'flex-1 py-1.5 rounded-lg flex justify-center text-slate-400 hover:text-white transition-all relative p-0 min-h-0 {theme_hover}').props('flat dense')
                    with notif_btn:
                        ui.html(get_icon('terminal', 'h-4 w-4 text-slate-400')) # representation for alerts
                        # indicator dot
                        ui.element('div').classes('absolute top-1.5 right-4 h-1.5 w-1.5 rounded-full bg-indigo-500 ring-2 ring-slate-900')

                    # Logout
                    logout_btn = ui.button(on_click=self.on_logout).classes(f'flex-1 py-1.5 rounded-lg flex justify-center text-slate-400 hover:text-red-400 transition-all p-0 min-h-0 {theme_hover}').props('flat dense')
                    with logout_btn:
                        ui.html(get_icon('log-out', 'h-4 w-4 text-slate-400'))

    def render(self):
        is_dark = self.theme == 'dark'
        card_class = 'bg-slate-950/95 border-white/10 text-slate-100 backdrop-blur-md shadow-2xl' if is_dark else 'bg-white border-slate-200 text-slate-900 shadow-xl'
        
        # Search dialog setup
        self.search_dialog = ui.dialog()
        with self.search_dialog:
            with ui.card().classes(f'w-full max-w-xl p-0 overflow-hidden {card_class}'):
                with ui.element('div').classes('p-4 flex items-center gap-3 border-b border-white/5'):
                    ui.html(get_icon('search', 'h-5 w-5 text-slate-400 shrink-0'))
                    search_input = ui.input(placeholder='Search workspaces...').classes('w-full bg-transparent border-none text-slate-100 focus:outline-none focus:ring-0').props('dark borderless')
                    
                    esc_btn = ui.button('ESC', on_click=self.search_dialog.close).classes('px-2 py-1 rounded bg-white/5 hover:bg-white/10 border border-white/5 text-[10px] font-mono text-slate-400 p-0 min-h-0').props('flat dense')
                
                # Navigate options inside search
                with ui.element('div').classes('p-4 space-y-2 text-left'):
                    ui.label('Navigation Commands').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-2')
                    for item in self.navigation_items:
                        nav_opt = ui.button(on_click=lambda i=item: [self.select_tab(i["id"]), self.search_dialog.close()]).classes(
                            'w-full p-3 rounded-xl flex items-center justify-between text-xs font-medium hover:bg-white/5 text-slate-300 hover:text-white text-left p-0 min-h-0'
                        ).style('text-transform: none !important;')
                        with nav_opt:
                            with ui.element('div').classes('flex items-center gap-3 pl-3'):
                                ui.html(get_icon(item["icon"], 'h-4 w-4 text-indigo-400 shrink-0'))
                                ui.label(item["label"])
                            with ui.element('div').classes('flex items-center gap-1 text-[10px] font-mono text-slate-500 pr-3'):
                                ui.label('Jump to Workspace')
                                ui.html(get_icon('arrow-right', 'h-3 w-3'))

        # Notifications dialog setup
        self.notifications_dialog = ui.dialog()
        with self.notifications_dialog:
            with ui.card().classes(f'w-80 p-5 rounded-2xl border shadow-2xl text-left {card_class}'):
                with ui.element('div').classes('flex justify-between items-center mb-4 pb-2 border-b border-white/5'):
                    ui.label('Enterprise Notifications').classes('font-display font-bold text-sm tracking-tight')
                    close_notif = ui.button(on_click=self.notifications_dialog.close).classes('text-slate-500 hover:text-slate-300 p-0 min-h-0').props('flat dense')
                    with close_notif:
                        ui.html(get_icon('log-out', 'h-4 w-4')) # small close representation

                with ui.element('div').classes('space-y-3'):
                    for notif in self.demo_notifications:
                        with ui.element('div').classes('p-3 rounded-xl bg-white/5 border border-white/5 flex gap-2 text-left'):
                            with ui.element('div').classes('pt-0.5'):
                                dot_color = 'bg-indigo-500' if notif["unread"] else 'bg-slate-600'
                                ui.element('div').classes(f'h-2 w-2 rounded-full {dot_color}')
                            with ui.element('div'):
                                ui.label(notif["text"]).classes('text-xs text-slate-200 leading-tight')
                                ui.label(notif["time"]).classes('text-[10px] font-mono text-slate-500 mt-1 block')

        # Sidebar core container
        self.container = ui.element('div').classes('h-full')
        with self.container:
            self.build_sidebar()
