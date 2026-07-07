from nicegui import ui
import json
import datetime
import hashlib
import asyncio
from src.components.Icons import get_icon

class InteractiveReports:
    def __init__(self, sales, theme: str):
        self.sales = sales
        self.theme = theme

        self.download_format = 'excel' # excel, csv, json
        self.report_type = 'ledger' # regional, ledger, customers
        self.compiling = False
        self.compiled_report = None

        # References
        self.main_container = None

    async def handle_generate_report(self):
        self.compiling = True
        self.refresh()
        await asyncio.sleep(0.8)
        self.compiling = False

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Hash creation for mock integrity
        hash_seed = f"KKVERSE-REPORT-{self.report_type}-{now_str}"
        sha_hash = hashlib.sha256(hash_seed.encode()).hexdigest()[:16]

        if self.report_type == 'ledger':
            records = [{
                "ID": s["id"],
                "Customer": s["customerName"],
                "Product": s["productName"],
                "TotalRevenue": s["totalRevenue"],
                "Date": s["saleDate"],
                "Rep": s["salesRep"]
            } for s in self.sales]

            self.compiled_report = {
                "name": "Synchronized Ledger Export",
                "linesCount": len(records),
                "generatedAt": now_str,
                "hash": f"SHA256: {sha_hash}...",
                "records": records
            }
        elif self.report_type == 'regional':
            # Aggregate by region
            regional_map = {}
            for s in self.sales:
                reg = s["region"]
                if reg not in regional_map:
                    regional_map[reg] = {"revenue": 0, "count": 0}
                regional_map[reg]["revenue"] += s["totalRevenue"]
                regional_map[reg]["count"] += 1

            records = [{
                "Region": region,
                "TotalRevenue": val["revenue"],
                "TransactionCount": val["count"],
                "MeanTicket": round(val["revenue"] / val["count"]) if val["count"] > 0 else 0
            } for region, val in regional_map.items()]

            self.compiled_report = {
                "name": "Regional Density Distributions",
                "linesCount": len(records),
                "generatedAt": now_str,
                "hash": f"SHA256: {sha_hash}...",
                "records": records
            }
        else:
            # Customers map
            cust_map = {}
            for s in self.sales:
                cust = s["customerName"]
                if cust not in cust_map:
                    cust_map[cust] = {"revenue": 0, "count": 0}
                cust_map[cust]["revenue"] += s["totalRevenue"]
                cust_map[cust]["count"] += 1

            records = [{
                "ClientEntity": cust,
                "AccumulatedRevenue": val["revenue"],
                "InvoiceCount": val["count"]
            } for cust, val in cust_map.items()]

            self.compiled_report = {
                "name": "Client Account Gross Yield Matrix",
                "linesCount": len(records),
                "generatedAt": now_str,
                "hash": f"SHA256: {sha_hash}...",
                "records": records
            }

        self.refresh()

    def handle_trigger_download(self):
        if not self.compiled_report or not self.compiled_report.get("records"):
            return

        payload_str = ""
        extension = "txt"

        if self.download_format == 'json':
            payload_str = json.dumps(self.compiled_report["records"], indent=2)
            extension = "json"
        elif self.download_format == 'csv':
            headers = ",".join(self.compiled_report["records"][0].keys())
            rows = [",".join(str(val) for val in r.values()) for r in self.compiled_report["records"]]
            payload_str = "\n".join([headers] + rows)
            extension = "csv"
        else:
            # Excel simulation format
            headers = "\t".join(self.compiled_report["records"][0].keys())
            rows = ["\t".join(str(val) for val in r.values()) for r in self.compiled_report["records"]]
            payload_str = (
                "KKVERSE AI ADVANCED EXCEL PACKAGES DATASET\n\n"
                f"Report Name: {self.compiled_report['name']}\n"
                f"Generated: {self.compiled_report['generatedAt']}\n"
                f"Integrity Check: {self.compiled_report['hash']}\n\n"
                f"{headers}\n" + "\n".join(rows)
            )
            extension = "xls"

        # NiceGUI byte trigger download
        ui.download(
            payload_str.encode('utf-8'),
            filename=f"kkverse_{self.report_type}_export.{extension}"
        )

    def set_report_type(self, rtype: str):
        self.report_type = rtype
        self.refresh()

    def set_download_format(self, fmt: str):
        self.download_format = fmt
        self.refresh()

    def refresh(self):
        if self.main_container:
            self.main_container.refresh()

    @ui.refreshable
    def render_content(self):
        is_dark = self.theme == 'dark'
        card_bg = 'bg-slate-900/40 border-white/5 shadow-lg' if is_dark else 'bg-white border-slate-200 shadow-sm'
        sub_text_class = 'text-slate-400' if is_dark else 'text-slate-600'
        text_color = 'text-white' if is_dark else 'text-slate-900'

        with ui.element('div').classes('space-y-6 w-full text-left'):
            
            # Header
            with ui.element('div').classes('flex flex-col md:flex-row md:items-center justify-between gap-4 w-full text-left'):
                with ui.element('div'):
                    ui.label('Interactive Reports Workspace').classes(f'font-display text-2xl font-bold tracking-tight {text_color}')
                    ui.label('Compile analytical ledgers, configure target export profiles, and download system backups.').classes('text-xs text-slate-500')

            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-12 gap-6 w-full'):
                
                # Left Parameter Controls
                with ui.element('div').classes('lg:col-span-5 space-y-6 text-left'):
                    with ui.element('div').classes(f'p-5 rounded-2xl border {card_bg}'):
                        ui.label('Report Parameters').classes(f'font-display font-bold text-sm mb-4 pb-2 border-b border-white/5 {text_color}')

                        with ui.element('div').classes('space-y-4'):
                            # Aggregate Targets Selection
                            with ui.element('div').classes('space-y-1.5 text-left'):
                                ui.label('Aggregate Targets').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block')
                                with ui.element('div').classes('space-y-2'):
                                    for item_id, item_title, item_desc in [
                                        ('ledger', 'Ledger Invoices Audit', 'Direct raw ledger rows with transactional rep metadata.'),
                                        ('regional', 'Regional Density Distribution', 'Summarized regional matrix groupings.'),
                                        ('customers', 'Client Account Valuation Matrix', 'Enterprise accounts lifetime purchase valuations.')
                                    ]:
                                        is_sel = self.report_type == item_id
                                        
                                        btn_style = 'bg-cyan-500/10 border-cyan-500/30' if is_sel else 'bg-white/5 border-white/5 hover:bg-white/10'
                                        title_style = 'text-cyan-400' if is_sel else 'text-slate-200'
                                        
                                        btn_sel = ui.button(on_click=lambda i=item_id: self.set_report_type(i)).classes(
                                            f'w-full p-3 rounded-xl border text-left transition-all p-0 min-h-0 {btn_style}'
                                        ).style('text-transform: none !important; height: auto; display: block; line-height: 1.2;')
                                        with btn_sel:
                                            with ui.element('div').classes('px-3 py-1.5 text-left'):
                                                ui.label(item_title).classes(f'block font-semibold text-xs {title_style}')
                                                ui.label(item_desc).classes('block text-[10px] text-slate-500 mt-0.5')

                            # Export File Package Format
                            with ui.element('div').classes('space-y-1.5 text-left'):
                                ui.label('Export File Package Format').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block')
                                with ui.element('div').classes('grid grid-cols-3 gap-2'):
                                    for f_id, f_lbl in [('excel', 'Excel Workbook'), ('csv', 'CSV Comma Delimited'), ('json', 'JSON Payload')]:
                                        is_sel = self.download_format == f_id
                                        btn_style = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/20' if is_sel else 'bg-white/5 border-white/5 hover:bg-white/10 text-slate-400'
                                        
                                        f_btn = ui.button(f_lbl.upper(), on_click=lambda f=f_id: self.set_download_format(f)).classes(
                                            f'py-2 px-1 rounded-lg text-[10px] font-mono font-bold transition-all border p-0 min-h-0 {btn_style}'
                                        ).style('text-transform: none !important; height: 32px;')

                            # Compile Button
                            btn_comp = ui.button(on_click=self.handle_generate_report).classes(
                                'w-full py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-semibold text-xs transition-all shadow-lg shadow-cyan-500/15 p-0 min-h-0'
                            ).style('text-transform: none !important; height: 38px;')
                            with btn_comp:
                                with ui.element('div').classes('flex items-center gap-2 justify-center px-4'):
                                    ui.html(get_icon('refresh-cw', f'h-4 w-4 text-white {"animate-spin" if self.compiling else ""}'))
                                    ui.label('Assembling Ledger Rowsets...' if self.compiling else 'Compile Operational Dataset')

                # Right Compiled visualizer preview
                with ui.element('div').classes('lg:col-span-7 space-y-6 text-left'):
                    if self.compiled_report:
                        with ui.element('div').classes(f'p-5 rounded-2xl border flex flex-col justify-between h-full {card_bg}'):
                            with ui.element('div').classes('w-full'):
                                with ui.element('div').classes('flex justify-between items-start mb-4 pb-2 border-b border-white/5 w-full'):
                                    with ui.element('div').classes('text-left'):
                                        ui.label(self.compiled_report["name"]).classes('font-display font-bold text-sm text-cyan-400')
                                        ui.label(f'Generated at: {self.compiled_report["generatedAt"]}').classes('text-[10px] font-mono text-slate-500 block')

                                    dl_btn = ui.button(on_click=self.handle_trigger_download).classes(
                                        'px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-mono font-bold text-[10px] p-0 min-h-0 flex items-center gap-1.5'
                                    ).style('text-transform: none !important; height: 32px;')
                                    with dl_btn:
                                        with ui.element('div').classes('flex items-center gap-1 px-3'):
                                            ui.html(get_icon('download', 'h-3.5 w-3.5 text-slate-950'))
                                            ui.label(f'EXPORT .{self.download_format.upper()}')

                                # Simulated stats metadata
                                with ui.element('div').classes('grid grid-cols-2 gap-4 p-3.5 rounded-xl bg-white/5 border border-white/5 mb-4 text-[11px] font-mono text-slate-400 w-full text-left'):
                                    with ui.element('div'):
                                        ui.label('RECORD COUNT').classes('text-slate-500 block mb-0.5')
                                        ui.label(f'{self.compiled_report["linesCount"]} items').classes('font-bold text-slate-100')
                                    with ui.element('div'):
                                        ui.label('METADATA INTEGRITY SIGN').classes('text-slate-500 block mb-0.5')
                                        ui.label(self.compiled_report["hash"]).classes('font-bold text-slate-100 truncate block')

                                # Preview box
                                ui.label('RAW PARSED PREVIEW').classes('text-[10px] font-mono text-slate-500 uppercase tracking-widest font-bold block mb-2')
                                
                                # Format preview text
                                preview_records = self.compiled_report["records"][:4]
                                if self.download_format == 'json':
                                    preview_str = json.dumps(preview_records, indent=2)
                                elif self.download_format == 'csv':
                                    headers = ",".join(self.compiled_report["records"][0].keys())
                                    rows = [",".join(str(val) for val in r.values()) for r in preview_records]
                                    preview_str = "\n".join([headers] + rows) + "\n..."
                                else:
                                    headers = "\t".join(self.compiled_report["records"][0].keys())
                                    rows = ["\t".join(str(val) for val in r.values()) for r in preview_records]
                                    preview_str = "\n".join([headers] + rows) + "\n..."

                                with ui.element('div').classes('p-4 rounded-xl bg-slate-950 font-mono text-[10px] leading-relaxed text-slate-400 overflow-x-auto max-h-60 overflow-y-auto w-full text-left'):
                                    ui.html(f'<pre class="whitespace-pre">{preview_str}</pre>')

                            with ui.element('div').classes('p-3 bg-cyan-950/20 border border-cyan-500/10 rounded-xl text-[11px] text-slate-450 leading-normal mt-4 text-left w-full'):
                                ui.label('✓ SIGNATURE VALIDATED').classes('font-bold text-cyan-400 block mb-0.5')
                                ui.label('This export package complies with standard regulatory corporate ledger parameters. Safe to download.')

                    else:
                        with ui.element('div').classes(f'p-12 rounded-2xl border flex flex-col items-center justify-center text-center space-y-4 h-full {card_bg} w-full'):
                            ui.html(get_icon('file-text', 'h-12 w-12 text-slate-600 animate-pulse'))
                            with ui.element('div'):
                                ui.label('Operational Report Empty').classes('font-display font-bold text-sm text-slate-300')
                                ui.label('Configure target aggregate report parameters on the left and trigger compilation to view data package contents.').classes('text-[11px] text-slate-500 max-w-sm mt-1 block')

    def render(self):
        self.main_container = ui.element('div').classes('w-full')
        with self.main_container:
            self.render_content()
