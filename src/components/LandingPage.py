from nicegui import ui
import random
from src.components.Icons import get_icon

class LandingPage:
    def __init__(self, on_start, theme: str):
        self.on_start = on_start
        self.theme = theme
        self.live_revenue = 14589200
        self.revenue_label = None

    def update_revenue(self):
        self.live_revenue += random.randint(3, 17)
        if self.revenue_label:
            self.revenue_label.text = f"${self.live_revenue:,}"

    def render(self):
        # Timer to tick revenue
        ui.timer(2.0, self.update_revenue)

        is_dark = self.theme == 'dark'
        bg_class = 'bg-[#030712] text-slate-100' if is_dark else 'bg-slate-50 text-slate-900'
        border_class = 'border-white/5 bg-[#030712]/60' if is_dark else 'border-slate-200 bg-white/60'
        card_class = 'bg-slate-900/40 border-white/5 text-slate-100 backdrop-blur-lg' if is_dark else 'bg-white border-slate-200 text-slate-900 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'

        with ui.element('div').classes(f'min-h-screen relative overflow-hidden font-sans transition-colors duration-500 {bg_class}'):
            # Ambient Background Orbs
            with ui.element('div').classes('absolute inset-0 pointer-events-none overflow-hidden'):
                ui.element('div').classes('absolute -top-[30%] -left-[20%] w-[70vw] h-[70vw] rounded-full bg-cyan-500/10 blur-[120px]')
                ui.element('div').classes('absolute -bottom-[20%] -right-[10%] w-[60vw] h-[60vw] rounded-full bg-violet-500/10 blur-[130px]')
                ui.element('div').classes('absolute top-[40%] left-[40%] w-[40vw] h-[40vw] rounded-full bg-emerald-500/5 blur-[100px]')

            # Header
            with ui.element('header').classes(f'sticky top-0 z-50 px-6 py-4 backdrop-blur-md border-b transition-colors duration-300 {border_class}'):
                with ui.element('div').classes('max-w-7xl mx-auto flex justify-between items-center'):
                    # Logo
                    with ui.element('div').classes('flex items-center gap-3'):
                        with ui.element('div').classes('h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20'):
                            ui.html(get_icon('sparkles', 'h-5 w-5 text-white'))
                        with ui.element('div'):
                            ui.label('KKVerse AI').classes('font-display font-bold text-xl tracking-tight bg-gradient-to-r from-white via-cyan-400 to-violet-500 bg-clip-text text-transparent')
                            ui.label('BI PLATFORM').classes('text-[9px] block font-mono text-cyan-400 tracking-widest uppercase')

                    # Action bar
                    with ui.element('div').classes('flex items-center gap-6'):
                        with ui.element('span').classes('font-mono text-xs hidden md:inline-block'):
                            ui.label('LIVE GLOBAL REVENUE: ').classes('text-slate-400')
                            self.revenue_label = ui.label(f"${self.live_revenue:,}").classes('text-cyan-400 font-semibold glow-text-cyan')
                        
                        btn = ui.button(on_click=self.on_start).classes(
                            'px-5 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-505 text-white text-xs font-semibold tracking-wide shadow-lg shadow-cyan-500/15 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]'
                        ).style('text-transform: none !important;')
                        with btn:
                            with ui.element('div').classes('flex items-center gap-2'):
                                ui.label('Access Command Center')
                                ui.html(get_icon('arrow-right', 'h-3.5 w-3.5 text-white'))

            # Hero Section
            with ui.element('main').classes('max-w-7xl mx-auto px-6 pt-16 pb-24 relative z-10'):
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-12 items-center'):
                    
                    # Left Column
                    with ui.element('div').classes('lg:col-span-7 flex flex-col items-start text-left'):
                        badge_bg = 'bg-white/5 border-white/10 text-cyan-400' if is_dark else 'bg-slate-100 border-slate-200 text-cyan-600'
                        with ui.element('div').classes(f'px-3 py-1 rounded-full text-[11px] font-mono mb-6 border flex items-center gap-2 {badge_bg}'):
                            ui.html(get_icon('bot', 'h-3.5 w-3.5'))
                            ui.label('GENERATIVE BUSINESS INTELLIGENCE IS HERE')

                        with ui.element('h1').classes('font-display text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight leading-[1.1] mb-6'):
                            ui.label('One Platform. ').classes('text-white' if is_dark else 'text-slate-900')
                            ui.label('Infinite Intelligence.').classes('bg-gradient-to-r from-cyan-400 via-emerald-400 to-violet-500 bg-clip-text text-transparent')

                        ui.label(
                            'KKVerse AI integrates enterprise databases, advanced machine learning prediction engines, and secure Gemini generative analysis into a single, unified executive cockpit. Forecast revenue, defend customer churn, and orchestrate warehouse inventory flow in real-time.'
                        ).classes(f'text-base md:text-lg mb-8 max-w-xl leading-relaxed {sub_text_class}')

                        with ui.element('div').classes('flex flex-col sm:flex-row gap-4 w-full sm:w-auto'):
                            launch_btn = ui.button(on_click=self.on_start).classes(
                                'px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-505 text-white font-semibold text-sm shadow-xl shadow-cyan-500/25 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]'
                            ).style('text-transform: none !important;')
                            with launch_btn:
                                with ui.element('div').classes('flex items-center gap-2'):
                                    ui.label('Launch Enterprise Dashboard')
                                    ui.html(get_icon('arrow-right', 'h-4 w-4 text-white'))
                            
                            explore_border = 'border-white/10 hover:border-white/20 hover:bg-white/5' if is_dark else 'border-slate-300 hover:bg-slate-100'
                            ui.link('Explore Technology', '#features').classes(
                                f'px-8 py-4 rounded-xl font-semibold text-sm border text-center transition-all duration-300 {explore_border} text-slate-300' if is_dark else f'px-8 py-4 rounded-xl font-semibold text-sm border text-center transition-all duration-300 {explore_border} text-slate-700'
                            ).style('text-decoration: none;')

                        # Trust metrics
                        with ui.element('div').classes('grid grid-cols-3 gap-8 mt-12 pt-8 border-t border-white/5 w-full'):
                            with ui.element('div'):
                                ui.label('99.4%').classes('block font-display text-2xl sm:text-3xl font-bold bg-gradient-to-r from-white to-cyan-400 bg-clip-text text-transparent')
                                ui.label('Churn Defense Accuracy').classes('text-[10px] sm:text-xs text-slate-500 uppercase tracking-widest font-mono')
                            with ui.element('div'):
                                ui.label('< 2s').classes('block font-display text-2xl sm:text-3xl font-bold bg-gradient-to-r from-white to-emerald-400 bg-clip-text text-transparent')
                                ui.label('Insight Latency').classes('text-[10px] sm:text-xs text-slate-500 uppercase tracking-widest font-mono')
                            with ui.element('div'):
                                ui.label('$4.2B').classes('block font-display text-2xl sm:text-3xl font-bold bg-gradient-to-r from-white to-violet-400 bg-clip-text text-transparent')
                                ui.label('Volume Analyzed').classes('text-[10px] sm:text-xs text-slate-500 uppercase tracking-widest font-mono')

                    # Right Column (Interactive Glass Mockup)
                    with ui.element('div').classes('lg:col-span-5 relative'):
                        # Halo back
                        ui.element('div').classes('absolute -inset-1 rounded-2xl bg-gradient-to-tr from-cyan-500/10 to-violet-500/15 blur-lg -z-10')
                        
                        # Card container
                        with ui.element('div').classes(f'p-6 rounded-2xl border {card_class} relative overflow-hidden shadow-2xl'):
                            with ui.element('div').classes('flex items-center justify-between mb-6 border-b border-white/5 pb-4'):
                                with ui.element('div').classes('flex items-center gap-2'):
                                    ui.element('div').classes('h-3 w-3 rounded-full bg-red-500/80')
                                    ui.element('div').classes('h-3 w-3 rounded-full bg-yellow-500/80')
                                    ui.element('div').classes('h-3 w-3 rounded-full bg-green-500/80')
                                ui.label('kkverse-bi-model-v4.1').classes('text-[10px] font-mono text-slate-500')

                            # Content
                            with ui.element('div').classes('space-y-4'):
                                # KPI 1
                                with ui.element('div').classes('p-4 rounded-xl bg-white/5 border border-white/5 text-left'):
                                    with ui.element('div').classes('flex justify-between items-center mb-1'):
                                        ui.label('FORECAST ACCURACY').classes('text-[11px] font-mono text-slate-400')
                                        ui.label('XGBoost Optimized').classes('text-xs font-mono text-cyan-400 font-bold')
                                    with ui.element('div').classes('h-2 rounded-full bg-slate-800 overflow-hidden relative'):
                                        ui.element('div').classes('absolute top-0 left-0 h-full bg-gradient-to-r from-cyan-400 to-violet-500 rounded-full w-[94.8%]')
                                    with ui.element('div').classes('flex justify-between items-center mt-2 text-[10px] font-mono text-slate-500'):
                                        ui.label('Baseline: 82.1%')
                                        ui.label('Active Model: 94.8%')

                                # KPI 2
                                with ui.element('div').classes('p-4 rounded-xl bg-white/5 border border-white/5 text-left'):
                                    with ui.element('div').classes('flex justify-between items-center mb-2'):
                                        ui.label('CHURN ESCAPE PROBABILITY').classes('text-[11px] font-mono text-slate-400')
                                        ui.label('Safe Zone').classes('text-xs font-mono text-emerald-400 font-bold')
                                    with ui.element('div').classes('flex items-end gap-1.5 h-12 pt-2'):
                                        for val in [30, 45, 55, 40, 60, 75, 85, 92, 94]:
                                            ui.element('div').classes('flex-1 bg-gradient-to-t from-emerald-500 to-cyan-400 rounded-t-sm').style(f'height: {val}%;')

                                # Recommendation Banner
                                with ui.element('div').classes('p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/10 flex items-center gap-3 text-left'):
                                    with ui.element('div').classes('h-8 w-8 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-400 shrink-0'):
                                        ui.html(get_icon('bot', 'h-4 w-4 text-cyan-400'))
                                    with ui.element('div'):
                                        ui.label('COPILOT RECOMMENDATION').classes('block text-[11px] font-mono text-cyan-400')
                                        ui.label('Reorder support hardware. Stock level below safety index of 15 units.').classes('text-xs text-slate-300 block leading-tight')

            # Features Section
            features_bg = 'border-t border-white/5 bg-[#030712]/30' if is_dark else 'border-t border-slate-200 bg-slate-100/50'
            with ui.element('section').classes(f'py-20 {features_bg}').style('scroll-behavior: smooth;'):
                ui.element('div').style('scroll-margin-top: 100px;').props('id=features')
                with ui.element('div').classes('max-w-7xl mx-auto px-6'):
                    with ui.element('div').classes('text-center max-w-2xl mx-auto mb-16'):
                        ui.label('Enterprise Grade Business Cockpit').classes('font-display text-3xl font-bold mb-4 tracking-tight text-white' if is_dark else 'font-display text-3xl font-bold mb-4 tracking-tight text-slate-900')
                        ui.label('Every single operational tool you need is fully engineered and tightly integrated.').classes(f'text-sm {sub_text_class}')

                    # Grid
                    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
                        self.render_feature_card('BarChart3', 'Executive Command Center', 'Visualizes total revenue, net profits, and client health vectors in a customizable high-end command panel.', is_dark)
                        self.render_feature_card('bot', 'AI Copilot & Summarizer', 'Uses active Gemini models to analyze performance data, identify critical operational risks, and recommend action items.', is_dark)
                        self.render_feature_card('trending-up', 'Customer Churn Laboratory', 'Choose Logistic Regression, Random Forest, or XGBoost algorithms to predict churn probability and test retention thresholds.', is_dark)
                        self.render_feature_card('database', 'Full Database Integration', 'Fully integrated data collection allowing instant CRUD updates for Customers, Products, and stock levels.', is_dark)
                        self.render_feature_card('users', 'Loyalty & Journey Analytics', 'Tracks customer segmentation matrices, historical lifetime values, and retention statuses with visual charts.', is_dark)
                        self.render_feature_card('shield-check', 'Automated Executive Reporting', 'Instantly export raw dashboard data arrays into CSV/Excel tables, or launch high-contrast print-ready report frames.', is_dark)

            # Footer
            footer_border = 'border-t border-white/5 bg-[#030712]' if is_dark else 'border-t border-slate-200 bg-white'
            with ui.element('footer').classes(f'py-12 px-6 {footer_border}'):
                with ui.element('div').classes('max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6'):
                    with ui.element('div').classes('flex items-center gap-3'):
                        ui.html(get_icon('sparkles', 'h-5 w-5 text-cyan-400'))
                        ui.label('KKVerse AI Global Solutions Inc.').classes('font-display font-bold text-sm text-slate-400')
                    with ui.element('div').classes('flex gap-6 text-xs text-slate-500 font-mono'):
                        ui.label('v4.1 Enterprise Secure Node')
                        ui.label('© 2026 KKVerse. All Rights Reserved.')

    def render_feature_card(self, icon_name: str, title: str, desc: str, is_dark: bool):
        card_bg = 'bg-white/5 border-white/5' if is_dark else 'bg-white border-slate-200 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        with ui.element('div').classes(f'p-6 rounded-xl border {card_bg} text-left'):
            with ui.element('div').classes('h-10 w-10 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center mb-4'):
                ui.html(get_icon(icon_name.lower(), 'h-5 w-5 text-cyan-400'))
            ui.label(title).classes('font-display font-semibold text-lg mb-2 text-white' if is_dark else 'font-display font-semibold text-lg mb-2 text-slate-900')
            ui.label(desc).classes(f'text-xs leading-relaxed {sub_text_class}')
