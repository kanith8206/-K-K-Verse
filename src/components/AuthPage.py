from nicegui import ui
import asyncio
from src.components.Icons import get_icon

class AuthPage:
    def __init__(self, on_login, theme: str):
        self.on_login = on_login
        self.theme = theme
        self.email = 'kanith770@gmail.com'
        self.password = '••••••••••••'
        self.show_password = False
        self.remember_me = True
        self.error_message = ''
        self.is_loading = False
        
        # Telemetry logs rotating state
        self.active_log_idx = 0
        self.logs = [
            "Secure handshake verified with ledger node-a7",
            "Calibrating Shapley values for churn risk model...",
            "Synthesizing 12-month forward predictive neural path",
            "Active session tokens authenticated via RSA key pair",
            "Synchronized catalog definitions with central warehouse"
        ]

        # UI Element references for dynamic updates
        self.email_input = None
        self.password_input = None
        self.error_container = None
        self.loading_spinner = None
        self.submit_btn = None
        self.log_container = None

    def update_log(self):
        self.active_log_idx = (self.active_log_idx + 1) % len(self.logs)
        if self.log_container:
            self.log_container.clear()
            with self.log_container:
                ui.label(self.logs[self.active_log_idx]).classes('text-slate-400 select-none')

    def handle_quick_login(self, email: str):
        self.email = email
        self.password = 'demo-credentials-validated'
        if self.email_input:
            self.email_input.value = email
        if self.password_input:
            self.password_input.value = 'demo-credentials-validated'

    async def handle_login_submit(self):
        if not self.email or len(self.email) < 5 or '@' not in self.email:
            self.error_message = 'Please enter a valid enterprise email address.'
            self.update_error()
            return

        self.is_loading = True
        self.error_message = ''
        self.update_error()
        self.update_submit_button()

        # Simulate 1.2s delay
        await asyncio.sleep(1.2)

        self.is_loading = False
        self.update_submit_button()

        # Callback on successful authentication
        self.on_login({
            "name": "Alexander Vance" if self.email == "kanith770@gmail.com" else self.email.split('@')[0],
            "email": self.email
        })

    def update_error(self):
        if self.error_container:
            self.error_container.clear()
            if self.error_message:
                with self.error_container:
                    with ui.element('div').classes('p-3.5 rounded-xl bg-red-950/20 border border-red-500/30 text-red-400 text-xs flex items-start gap-2.5 text-left w-full'):
                        ui.html(get_icon('alert-triangle', 'h-4 w-4 shrink-0 mt-0.5 text-red-400'))
                        ui.label(self.error_message)

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        if self.password_input:
            self.password_input.password = not self.show_password
            self.password_input.update()

    def update_submit_button(self):
        if self.submit_btn:
            self.submit_btn.clear()
            with self.submit_btn:
                if self.is_loading:
                    with ui.element('div').classes('flex items-center justify-center gap-2'):
                        ui.spinner(size='xs', color='white')
                        ui.label('Configuring Workspace Decryptors...')
                else:
                    with ui.element('div').classes('flex items-center justify-center gap-2'):
                        ui.html(get_icon('shield-check', 'h-4 w-4 text-white'))
                        ui.label('Authorize System Session')

    def render(self):
        # Timer to rotate logs
        ui.timer(3.5, self.update_log)

        is_dark = self.theme == 'dark'
        bg_class = 'bg-[#030712] text-slate-100' if is_dark else 'bg-slate-50 text-slate-900'
        left_bg_class = 'border-slate-800 bg-slate-950/40' if is_dark else 'border-slate-200 bg-white/40'
        input_class = 'glass-input' if is_dark else 'glass-input-light'

        with ui.element('div').classes(f'min-h-screen w-full flex relative overflow-hidden font-sans transition-colors duration-500 {bg_class}'):
            
            # Glowing backgrounds
            with ui.element('div').classes('absolute inset-0 pointer-events-none overflow-hidden'):
                ui.element('div').classes('absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] rounded-full bg-indigo-500/10 blur-[130px]')
                ui.element('div').classes('absolute bottom-[-15%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-violet-600/10 blur-[130px]')
                if is_dark:
                    ui.element('div').classes('absolute top-[40%] left-[30%] w-[40vw] h-[40vw] rounded-full bg-emerald-500/5 blur-[150px]')

            # LEFT PORTION
            with ui.element('div').classes(f'hidden lg:flex lg:w-[55%] xl:w-[60%] flex-col justify-between p-12 relative overflow-hidden border-r {left_bg_class}'):
                # Grid background pattern
                ui.element('div').classes('absolute inset-0 opacity-[0.03] pointer-events-none').style(
                    "background-image: radial-gradient(circle, #4f46e5 1px, transparent 1.5px); background-size: 24px 24px;"
                )

                # Header
                with ui.element('div').classes('flex items-center gap-3 relative z-10 text-left'):
                    with ui.element('div').classes('h-8 w-8 rounded-xl bg-indigo-600 flex items-center justify-center shadow-md shadow-indigo-500/20'):
                        ui.html(get_icon('sparkles', 'h-4.5 w-4.5 text-white'))
                    with ui.element('div'):
                        ui.label('KKVERSE OPERATIONAL SYSTEM').classes('block text-xs font-bold font-display uppercase tracking-widest text-indigo-400')
                        ui.label('SECURE SEED GATEWAY v4.12').classes('block text-[9px] font-mono text-slate-500')

                # Middle Showcase Info
                with ui.element('div').classes('my-auto relative z-10 max-w-xl text-left'):
                    with ui.element('h1').classes('text-4xl xl:text-5xl font-extrabold font-display tracking-tight leading-tight mb-4'):
                        ui.label('The intelligent console for ')
                        ui.label('cognitive enterprises.').classes('bg-gradient-to-r from-indigo-400 via-violet-400 to-emerald-400 bg-clip-text text-transparent')
                    ui.label('Unlock real-time telemetry, synchronized smart ledgers, neural cash forecasts, and ML customer churn predictions with a single secure signature.').classes('text-sm text-slate-400 leading-relaxed mb-10 max-w-md')

                    # Metrics block
                    metrics_card = 'bg-[#0B0F19]/90 border-slate-800 shadow-2xl' if is_dark else 'bg-white border-slate-200 shadow-md'
                    with ui.element('div').classes(f'p-6 rounded-2xl border text-left space-y-5 {metrics_card}'):
                        with ui.element('div').classes('flex justify-between items-center pb-3 border-b border-slate-800'):
                            with ui.element('div').classes('flex items-center gap-2'):
                                ui.html(get_icon('activity', 'h-4 w-4 text-indigo-400'))
                                ui.label('REAL-TIME INTEGRITY FEED').classes('text-[11px] font-mono tracking-wider font-bold uppercase text-slate-400')
                            with ui.element('div').classes('flex items-center gap-1.5'):
                                ui.element('span').classes('h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping')
                                ui.label('ONLINE').classes('text-[9px] font-mono text-emerald-500 font-bold')

                        # Sparklines
                        with ui.element('div').classes('grid grid-cols-2 gap-4'):
                            with ui.element('div').classes('p-3.5 rounded-xl bg-slate-900/50 border border-slate-850'):
                                ui.label('CONTRACTS HEALTH').classes('text-[9px] font-mono text-slate-500 uppercase tracking-wider block mb-1')
                                with ui.element('div').classes('flex items-baseline gap-1.5'):
                                    ui.label('98.4%').classes('text-lg font-bold font-display text-slate-200')
                                    ui.label('+1.2%').classes('text-[9px] font-mono text-emerald-400 font-bold')
                                ui.html('<svg class="w-full h-5 mt-2 overflow-visible" viewBox="0 0 100 20"><path d="M0,15 L20,13 L40,16 L60,10 L80,12 L100,4" fill="none" stroke="#6366f1" stroke-width="1.5" stroke-linecap="round"/><circle cx="100" cy="4" r="2" fill="#6366f1"/></svg>')

                            with ui.element('div').classes('p-3.5 rounded-xl bg-slate-900/50 border border-slate-850'):
                                ui.label('ESTIMATED GROWTH').classes('text-[9px] font-mono text-slate-500 uppercase tracking-wider block mb-1')
                                with ui.element('div').classes('flex items-baseline gap-1.5'):
                                    ui.label('$4.8M').classes('text-lg font-bold font-display text-slate-200')
                                    ui.label('Q4').classes('text-[9px] font-mono text-indigo-400 font-bold')
                                ui.html('<svg class="w-full h-5 mt-2 overflow-visible" viewBox="0 0 100 20"><path d="M0,18 L20,15 L40,11 L60,14 L80,6 L100,2" fill="none" stroke="#10b981" stroke-width="1.5" stroke-linecap="round"/><circle cx="100" cy="2" r="2" fill="#10b981"/></svg>')

                        # Live Terminal Log rotating
                        with ui.element('div').classes('p-3 rounded-lg bg-slate-950 border border-slate-850 flex items-center gap-2.5'):
                            ui.html(get_icon('terminal', 'h-3.5 w-3.5 text-indigo-400 shrink-0'))
                            self.log_container = ui.element('div').classes('font-mono text-[10px] text-slate-400 w-full')
                            with self.log_container:
                                ui.label(self.logs[self.active_log_idx]).classes('text-slate-400 select-none')

                # Security Footer
                with ui.element('div').classes('flex items-center gap-2.5 text-slate-500 relative z-10'):
                    ui.html(get_icon('shield', 'h-4 w-4 text-slate-400'))
                    ui.label('Secured terminal access point. High-intensity RSA authentication keys enabled.').classes('text-[10px] font-mono uppercase tracking-wider')

            # RIGHT PORTION: LOGIN FORM
            with ui.element('div').classes('w-full lg:w-[45%] xl:w-[40%] flex flex-col justify-between p-6 sm:p-12 relative z-10 bg-inherit'):
                
                # Mobile Header
                with ui.element('div').classes('flex justify-between items-center lg:hidden mb-8'):
                    with ui.element('div').classes('flex items-center gap-2.5'):
                        with ui.element('div').classes('h-7 w-7 rounded-lg bg-indigo-600 flex items-center justify-center'):
                            ui.html(get_icon('sparkles', 'h-4 w-4 text-white'))
                        ui.label('KKVERSE AI').classes('text-[11px] font-display font-bold uppercase tracking-widest text-indigo-500')
                    ui.label('Gatekeeper Secure').classes('text-[9px] font-mono text-slate-500')

                ui.element('div').classes('hidden lg:block h-6')

                # Card Form
                with ui.element('div').classes('my-auto w-full max-w-sm mx-auto'):
                    with ui.element('div').classes('text-left mb-6'):
                        ui.label('System Access Portal').classes('font-display font-extrabold text-2xl tracking-tight text-slate-200')
                        ui.label('Verify your operational workspace identity credentials.').classes('text-xs text-slate-500 mt-1')

                    # Presets Selection
                    with ui.element('div').classes('mb-6 text-left'):
                        ui.label('QUICK ACCESS PRESETS').classes('text-[9px] font-mono text-slate-500 uppercase tracking-widest block mb-2 font-bold')
                        with ui.element('div').classes('grid grid-cols-2 gap-2.5'):
                            
                            # Preset 1
                            preset1_btn = ui.button(on_click=lambda: self.handle_quick_login('kanith770@gmail.com')).classes(
                                'p-2.5 rounded-xl border text-left bg-white/5 border-white/5 hover:bg-white/10 hover:border-white/10 transition-all duration-300 hover:scale-[1.01]'
                            ).style('text-transform: none !important; width: 100%; height: auto;')
                            with preset1_btn:
                                with ui.element('div').classes('flex items-center gap-2'):
                                    with ui.element('div').classes('h-5 w-5 rounded bg-indigo-500/15 text-indigo-400 flex items-center justify-center shrink-0'):
                                        ui.html(get_icon('user', 'h-3 w-3 text-indigo-400'))
                                    with ui.element('div').classes('min-w-0 text-left'):
                                        ui.label('Alexander Vance').classes('block text-[10px] font-bold text-slate-200 truncate')
                                        ui.label('Executive Admin').classes('block text-[8px] font-mono text-slate-500 truncate')

                            # Preset 2
                            preset2_btn = ui.button(on_click=lambda: self.handle_quick_login('guest@kkverse.ai')).classes(
                                'p-2.5 rounded-xl border text-left bg-white/5 border-white/5 hover:bg-white/10 hover:border-white/10 transition-all duration-300 hover:scale-[1.01]'
                            ).style('text-transform: none !important; width: 100%; height: auto;')
                            with preset2_btn:
                                with ui.element('div').classes('flex items-center gap-2'):
                                    with ui.element('div').classes('h-5 w-5 rounded bg-emerald-500/15 text-emerald-400 flex items-center justify-center shrink-0'):
                                        ui.html(get_icon('fingerprint', 'h-3 w-3 text-emerald-400'))
                                    with ui.element('div').classes('min-w-0 text-left'):
                                        ui.label('Guest Auditor').classes('block text-[10px] font-bold text-slate-200 truncate')
                                        ui.label('Standard Profile').classes('block text-[8px] font-mono text-slate-500 truncate')

                    # Error Container
                    self.error_container = ui.element('div').classes('mb-6')

                    # Inputs
                    with ui.element('div').classes('space-y-4 text-left'):
                        
                        # Email Input
                        with ui.element('div').classes('space-y-1.5'):
                            ui.label('ENTERPRISE EMAIL').classes('text-[10px] font-mono text-slate-400 uppercase tracking-wider block')
                            with ui.element('div').classes('relative'):
                                self.email_input = ui.input(
                                    placeholder='name@company.com',
                                    value=self.email,
                                    on_change=lambda e: setattr(self, 'email', e.value)
                                ).classes('w-full text-xs text-white border-slate-800 focus:border-indigo-500').props('dark filled dense').style('border-radius: 8px;')
                                # Add icon inside input via Quasar slot
                                self.email_input.add_slot('prepend', get_icon('user', 'h-4 w-4 text-slate-500'))

                        # Password Input
                        with ui.element('div').classes('space-y-1.5'):
                            with ui.element('div').classes('flex justify-between items-center'):
                                ui.label('ACCESS SECURE KEY').classes('text-[10px] font-mono text-slate-400 uppercase tracking-wider block')
                                ui.link('Forgot Key?', '#reset').classes('text-[9px] font-mono text-indigo-400 hover:underline').style('text-decoration: none;')
                            
                            with ui.element('div').classes('relative'):
                                self.password_input = ui.input(
                                    placeholder='••••••••••••',
                                    value=self.password,
                                    password=True,
                                    on_change=lambda e: setattr(self, 'password', e.value)
                                ).classes('w-full text-xs text-white border-slate-800 focus:border-indigo-500').props('dark filled dense').style('border-radius: 8px;')
                                self.password_input.add_slot('prepend', get_icon('lock', 'h-4 w-4 text-slate-500'))
                                
                                # eye toggle slot at the end
                                eye_btn = ui.button(on_click=self.toggle_password_visibility).classes('bg-transparent border-0 shadow-none text-slate-500 hover:text-slate-300 p-0 min-h-0').props('flat round dense')
                                with eye_btn:
                                    ui.html(get_icon('eye', 'h-4 w-4 text-slate-500'))
                                self.password_input.add_slot('append', eye_btn)

                        # Remember me
                        with ui.element('div').classes('flex items-center justify-between pt-1 text-left'):
                            self.remember_checkbox = ui.checkbox(
                                'Remember active token lock', 
                                value=self.remember_me,
                                on_change=lambda e: setattr(self, 'remember_me', e.value)
                            ).classes('text-[11px] text-slate-400 dark')

                        # Authorize submit button
                        self.submit_btn = ui.button(on_click=self.handle_login_submit).classes(
                            'w-full py-3 mt-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs tracking-wide shadow-lg shadow-indigo-500/15 hover:shadow-indigo-500/20 hover:scale-[1.01] active:scale-[0.99] transition-all duration-300'
                        ).style('text-transform: none !important; height: 48px;')
                        self.update_submit_button()

                    # Footnote
                    with ui.element('div').classes('mt-8 pt-5 border-t border-white/5 text-center text-[9px] text-slate-500 font-mono tracking-wider'):
                        ui.label('SECURED BY KKVERSE HIGH INTEGRITY SYSTEM SHIELD')

                ui.element('div').classes('hidden lg:block h-6')
