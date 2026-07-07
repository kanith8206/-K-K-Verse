from nicegui import ui
from src.components.Icons import get_icon
from src.data import BUSINESS_SCORE_COMPONENTS
from src.services.ai import fetch_copilot_logic

class AICopilot:
    def __init__(self, kpis, counts, theme: str):
        self.kpis = kpis
        self.counts = counts
        self.theme = theme

        self.messages = [
            {
                "role": "assistant",
                "content": f"Welcome, Chief Business Intelligence Officer Alexander Vance. I am your specialized **KKVerse AI Cognitive Copilot**.\n\nI have locked onto your live corporate database context:\n- **Client base**: {self.counts['customersCount']} active accounts\n- **Ledger Invoices**: {self.counts['salesCount']} records\n- **Catalog items**: {self.counts['productsCount']} products\n- **Gross Yield**: ${self.kpis.totalRevenue:,}\n\nAsk me any strategic question, or type e.g., `Which accounts represent our highest churn exposure?` or `Project Q3 revenue paths based on XGBoost`."
            }
        ]
        
        self.user_input_val = ""
        self.loading = False

        # References
        self.messages_container = None
        self.scroll_area = None
        self.input_field = None

    def set_user_input(self, text: str):
        self.user_input_val = text
        if self.input_field:
            self.input_field.value = text

    async def handle_send_message(self):
        if not self.user_input_val.strip() or self.loading:
            return

        user_msg = self.user_input_val
        self.user_input_val = ""
        if self.input_field:
            self.input_field.value = ""

        # Append user message
        self.messages.append({"role": "user", "content": user_msg})
        self.render_new_message(self.messages[-1])
        
        self.loading = True
        self.render_loading_bubble(True)

        try:
            # Prepare history list
            history = [{"role": m["role"], "content": m["content"]} for m in self.messages[1:-1]]
            
            # Direct python call to shared service
            response_data = await fetch_copilot_logic(
                message=user_msg,
                history_list=history,
                context_data={
                    "customersCount": self.counts["customersCount"],
                    "salesCount": self.counts["salesCount"],
                    "productsCount": self.counts["productsCount"],
                    "totalRevenue": self.kpis.totalRevenue,
                    "totalProfit": self.kpis.totalProfit
                }
            )

            self.messages.append({
                "role": "assistant",
                "content": response_data.get("text", ""),
                "isSimulated": response_data.get("isSimulated", False)
            })

            # Remove loading indicator
            self.render_loading_bubble(False)
            self.render_new_message(self.messages[-1])

        except Exception as error:
            print("Copilot communication error:", error)
            self.render_loading_bubble(False)
            self.messages.append({
                "role": "assistant",
                "content": "### System Connection Fault\n\nUnable to bridge connection to Gemini AI. Check your internet connection or try again."
            })
            self.render_new_message(self.messages[-1])
        finally:
            self.loading = False

    def render_new_message(self, msg):
        if not self.messages_container:
            return
        
        is_user = msg["role"] == "user"
        is_dark = self.theme == 'dark'
        
        with self.messages_container:
            align_class = 'ml-auto flex-row-reverse' if is_user else ''
            avatar_bg = 'bg-violet-500/20 text-violet-300' if is_user else 'bg-indigo-500/15 text-indigo-400 border border-indigo-500/10'
            bubble_bg = 'bg-violet-950/15 border-violet-500/20 text-slate-100 rounded-tr-none' if is_user else 'bg-slate-950/40 border-white/5 text-slate-300 rounded-tl-none' if is_dark else 'bg-white border-slate-200 text-slate-700 rounded-tl-none shadow-sm'

            with ui.element('div').classes(f'flex gap-3 text-xs leading-relaxed text-left max-w-[85%] {align_class}'):
                # Avatar
                with ui.element('div').classes(f'h-8 w-8 rounded-lg shrink-0 flex items-center justify-center {avatar_bg}'):
                    ui.html(get_icon('cpu' if is_user else 'bot', 'h-4 w-4'))
                
                # Bubble Content
                with ui.element('div').classes(f'p-4 rounded-xl border relative text-left {bubble_bg}'):
                    # Use ui.markdown for perfect formatting
                    ui.markdown(msg["content"]).classes('font-sans text-xs text-left')
                    
                    if msg.get("isSimulated"):
                        ui.label('Local Inference Node').classes('text-[9px] font-mono text-slate-500 uppercase mt-3 block border-t border-white/5 pt-2 text-left')

        if self.scroll_area:
            self.scroll_area.scroll_to(percent=1.0)

    def render_loading_bubble(self, show: bool):
        if not self.messages_container:
            return
            
        # Clear previous loading elements if any
        if not show:
            # We refresh the messages container, or we can just pop the last child element
            # But the simplest is to rebuild from the self.messages list since it is quick!
            self.messages_container.clear()
            for m in self.messages:
                self.render_new_message(m)
            return

        with self.messages_container:
            with ui.element('div').classes('flex gap-3 text-xs max-w-[85%]').name('loading_bubble'):
                with ui.element('div').classes('h-8 w-8 rounded-lg shrink-0 flex items-center justify-center bg-indigo-500/15 text-indigo-400 border border-indigo-500/10'):
                    ui.html(get_icon('bot', 'h-4 w-4 animate-spin'))
                with ui.element('div').classes('p-4 rounded-xl border bg-slate-950/40 border-white/5 text-slate-500 rounded-tl-none'):
                    ui.label('Consulting multi-dimensional metrics...').classes('font-mono animate-pulse text-xs')
                    
        if self.scroll_area:
            self.scroll_area.scroll_to(percent=1.0)

    def render(self):
        is_dark = self.theme == 'dark'
        card_bg = 'bg-[#0F172A] border-slate-800 shadow-lg' if is_dark else 'bg-white border-slate-200 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        text_color = 'text-white' if is_dark else 'text-slate-900'

        quick_prompts = [
            "Analyze client retention exposure.",
            "Recommend gross profit margin optimizations.",
            "Draft a Q3 expansion strategy proposal."
        ]

        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full text-left'):
                with ui.element('div').classes('text-left'):
                    ui.label('AI Copilot Workspace').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Engage our contextual LLM neural bridge to explore data schemas, ask queries, and compute health scores.').classes('text-xs text-slate-500')

            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Chat Panel
                with ui.element('div').classes('lg:col-span-8 flex flex-col h-[600px] rounded-2xl border overflow-hidden relative z-10 bg-[#0F172A] border-slate-800 shadow-lg'):
                    # Chat Header
                    with ui.element('div').classes('p-4 border-b border-white/5 flex items-center justify-between bg-slate-950/20 w-full'):
                        with ui.element('div').classes('flex items-center gap-2.5 text-left'):
                            ui.html(get_icon('bot', 'h-5 w-5 text-indigo-400'))
                            with ui.element('div'):
                                ui.label('Contextual Cog-Bridge v4').classes('block text-xs font-semibold text-slate-200')
                                ui.label('Active models: Gemini 3.5 Flash').classes('block text-[10px] font-mono text-slate-500')
                        ui.element('div').classes('h-2 w-2 rounded-full bg-emerald-400 animate-pulse')

                    # Messages Scroll Area
                    self.scroll_area = ui.scroll_area().classes('flex-1 p-5')
                    with self.scroll_area:
                        self.messages_container = ui.element('div').classes('space-y-4 w-full text-left')
                        # Render initial messages
                        for m in self.messages:
                            self.render_new_message(m)

                    # Chat Input Bar
                    with ui.element('div').classes('p-4 border-t border-white/5 bg-slate-950/20 w-full'):
                        # Quick Prompts Row
                        with ui.element('div').classes('flex flex-wrap gap-2 mb-3'):
                            for qp in quick_prompts:
                                ui.button(qp, on_click=lambda q=qp: self.set_user_input(q)).classes(
                                    'px-2.5 py-1 rounded bg-white/5 hover:bg-white/10 border border-white/5 text-[10px] text-slate-400 hover:text-white font-mono p-0 min-h-0'
                                ).style('text-transform: none !important; height: auto; line-height: 1.2;')

                        # Main Input Form
                        with ui.element('div').classes('flex gap-2 w-full'):
                            self.input_field = ui.input(
                                placeholder='Ask Copilot: recommended expansion steps...',
                                on_change=lambda e: setattr(self, 'user_input_val', e.value)
                            ).classes('flex-1 text-xs bg-slate-900 border-slate-800 rounded-lg text-white dark').props('dense filled')
                            
                            # Bind Enter key to send message
                            self.input_field.on('keydown.enter', self.handle_send_message)

                            ui.button(on_click=self.handle_send_message).classes(
                                'px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white flex items-center justify-center transition-all active:scale-95 shrink-0 font-semibold p-0 min-h-0'
                            ).style('height: 38px; width: 38px;').add_slot('default', get_icon('send', 'h-4 w-4 text-white'))

                # Right Panel: Corporate Health Score
                with ui.element('div').classes('lg:col-span-4 space-y-6 text-left'):
                    with ui.element('div').classes(f'p-5 rounded-2xl border text-left {card_bg}'):
                        with ui.element('div').classes('flex items-center gap-2.5 mb-4 pb-3 border-b border-white/5'):
                            ui.html(get_icon('gauge', 'h-4 w-4 text-indigo-400'))
                            ui.label('Strategic Corporate Health Score').classes(f'font-display font-bold text-sm {text_color}')

                        # Large Index Box
                        with ui.element('div').classes('text-center py-6 border border-white/5 rounded-2xl bg-white/5 mb-6 relative overflow-hidden'):
                            ui.label('KKVERSE VALUE INDEX').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest block mb-1')
                            ui.html(f'<h3 class="text-4xl font-extrabold font-display text-indigo-400">89.2 <span class="text-xs font-semibold text-slate-400">/ 100</span></h3>')
                            ui.label('✓ AAA EXCELLENT INVESTMENT GRADE').classes('text-[10px] font-mono text-emerald-400 font-bold block mt-1')

                        # Score Components
                        with ui.element('div').classes('space-y-4'):
                            for comp in BUSINESS_SCORE_COMPONENTS:
                                with ui.element('div').classes('space-y-1.5 text-left'):
                                    with ui.element('div').classes('flex justify-between text-xs font-semibold'):
                                        ui.label(comp["name"]).classes('text-slate-200')
                                        ui.label(f'{comp["score"]}%').classes('font-mono text-indigo-400')
                                    with ui.element('div').classes('h-1 rounded-full bg-slate-800 overflow-hidden'):
                                        ui.element('div').classes('bg-indigo-500 h-full').style(f'width: {comp["score"]}%;')
                                    ui.label(comp["description"]).classes('text-[9px] text-slate-500 leading-tight block')
