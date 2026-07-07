import os
import json
from google import genai
from google.genai import types

# Simulated insights in case Gemini key is missing
SIMULATED_INSIGHTS = {
    "executiveSummary": "KKVerse AI platform diagnostics show optimized growth vectors with potential churn risks in APAC and Europe. Software licenses (SaaS Tier A & Cloud Database Nodes) are yielding a high profit margin of 77.2%, compensating for hardware warehouse overheads. Recent sales highlight an active enterprise lifecycle with Stark Industries and Acme Corporation leading expansion margins.",
    "opportunities": [
        {
            "title": "Consolidated APAC Support Node",
            "description": "APAC accounts for 24% of enterprise spend but scores lowest on retention metrics. Deploying a dedicated regional Customer Success cluster can mitigate high-risk warning status on key accounts.",
            "impact": "High"
        },
        {
            "title": "Quantum Hardware Seat Upgrades",
            "description": "Quantum BI Gateway Server v4 is in high demand (Low Stock Alert). Upsell physical server clients to cloud-native database subscriptions for a recurring 82% margin boost.",
            "impact": "High"
        },
        {
            "title": "Automated Ticket Renewal Cycles",
            "description": "Convert support-level SLA customers to automatic annual licensing packages to secure long-term active cashflow.",
            "impact": "Medium"
        }
    ],
    "risks": [
        {
            "title": "High Churn Alert: Globex & Hooli",
            "description": "Globex and Hooli show declining product activity profiles and critical tenure expiration zones, threatening up to $24,800 in monthly recurring spend.",
            "severity": "Critical"
        },
        {
            "title": "Warehouse Stock Scarcity",
            "description": "Gateway Server stock levels have fallen below safety limits. Inability to fulfill impending enterprise contracts may delay revenue realization by 4-6 weeks.",
            "severity": "High"
        },
        {
            "title": "Support SLA Dilution",
            "description": "Support response latency on high-complexity tickets has trended upward by 14% due to peak consulting assignments.",
            "severity": "Medium"
        }
    ],
    "businessScore": 89
}

ai_client = None

def get_ai_client():
    global ai_client
    if not ai_client:
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "MY_GEMINI_API_KEY":
            ai_client = genai.Client(
                api_key=key,
                http_options={"headers": {"User-Agent": "aistudio-build"}}
            )
    return ai_client

async def fetch_insights_logic(kpis, customer_summary, product_summary):
    try:
        client = get_ai_client()
        if not client:
            res = SIMULATED_INSIGHTS.copy()
            res.update({
                "isSimulated": True,
                "message": "Demo Mode: Running on high-fidelity local AI modeling. Add your real GEMINI_API_KEY in the Secrets panel to unlock live generative insights."
            })
            return res

        prompt = f"""You are the Principal AI Business Analyst for KKVerse AI. Analyze the following current business state and generate structural enterprise intelligence.
    
    METRICS REPORT:
    - Total Revenue: ${kpis.get('totalRevenue')}
    - Total Profit: ${kpis.get('totalProfit')} (Margin: {kpis.get('profitMargin')}%)
    - Active Client Count: {kpis.get('totalCustomers')}
    - Warehouse Assets in Low Stock: {product_summary.get('lowStockCount')}
    - Active Customer segments: {json.dumps(customer_summary)}
    
    Format your response EXACTLY as a JSON object matching this schema:
    {{
      "executiveSummary": "A concise, high-impact paragraph summarizing the operational health, key performance drivers, and recommendations for the CEO.",
      "opportunities": [
        {{ "title": "Opportunity Name", "description": "Specific action-oriented tactical advice.", "impact": "High" | "Medium" | "Low" }}
      ],
      "risks": [
        {{ "title": "Risk Name", "description": "Details about active operational exposure or churn threat.", "severity": "Critical" | "High" | "Medium" }}
      ],
      "businessScore": 88
    }}
    
    Make the summary extremely specific, realistic, and insightful. Return ONLY valid JSON, with no markdown code blocks or wrapper text outside the raw JSON."""

        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        text = (response.text or "").strip()
        parsed_data = json.loads(text)
        parsed_data["isSimulated"] = False
        return parsed_data
    except Exception as error:
        print("Gemini API Error in fetch_insights_logic:", error)
        res = SIMULATED_INSIGHTS.copy()
        res.update({
            "isSimulated": True,
            "errorMessage": str(error)
        })
        return res

async def fetch_copilot_logic(message, history_list, context_data):
    try:
        client = get_ai_client()
        
        system_prompt = f"""You are KKVerse AI Copilot, a brilliant, helpful enterprise strategist, machine learning scientist, and BI architect. 
You have direct context of the active company database:
- Customer count: {context_data.get('customersCount')}
- Active Sales Records: {context_data.get('salesCount')}
- Catalog Products: {context_data.get('productsCount')}
- Active Revenue: ${context_data.get('totalRevenue')}
- Active Profit: ${context_data.get('totalProfit')}

Respond in beautiful, concise Markdown with highly actionable, professional insights. Use bullet points, bold key terms, and high-impact layouts. Keep explanations precise and CEO-focused."""

        if not client:
            # Elegant simulator response
            lowercase_msg = message.lower()
            response_text = "### KKVerse Copilot *[Simulation Node]*\n\n"
            if "churn" in lowercase_msg or "retention" in lowercase_msg:
                response_text += "Globex Industries and Hooli Inc are our highest-priority retention risks right now. \n\n**Action Items:**\n- **Initiate Executive Outreach**: Assign John Vance to schedule a health audit with Globex's ops team before their contract expires.\n- **Pricing Model Realignment**: Offer Hooli Inc a consolidated SaaS Tier A pricing tier to defend against license contraction."
            elif "revenue" in lowercase_msg or "forecast" in lowercase_msg or "sales" in lowercase_msg:
                total_rev = context_data.get('totalRevenue', 1) or 1
                total_profit = context_data.get('totalProfit', 0) or 0
                margin = (total_profit / total_rev) * 100 if total_rev else 80.0
                response_text += f"Current revenue stands at **${total_rev:,}** with a strong profit margin of **{margin:.1f}%**. \n\nOur XGBoost predictive model indicates a **6.4% quarter-on-quarter growth vector** for Q3, primarily driven by SaaS upgrades and cloud subscription expansion. Keep warehouse assets (Quantum BI Gateway Servers) stocked to prevent fulfillment friction."
            else:
                response_text += "Welcome, CBIO Alexander Vance. I am ready to analyze KKVerse's dataset. Ask me about:\n- **Customer Churn Exposure**: Risks surrounding high-value clients.\n- **Revenue Optimization**: Strategies to expand our net profit margins beyond current limits.\n- **Warehouse Inventory Squeeze**: Recommendations for replenishing low-stock servers.\n\n*Note: Connect your live GEMINI_API_KEY in the Secrets panel to activate full contextual reasoning capabilities.*"
            
            return {"text": response_text, "isSimulated": True}

        formatted_history = []
        for msg in history_list:
            # check if dict or object
            msg_role = msg.get("role") if isinstance(msg, dict) else msg.role
            msg_content = msg.get("content") if isinstance(msg, dict) else msg.content
            role = "user" if msg_role == "user" else "model"
            formatted_history.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg_content)]
                )
            )

        full_message = f"CURRENT WORKSPACE METRICS: Revenue ${context_data.get('totalRevenue')}, Profit ${context_data.get('totalProfit')}, Customers {context_data.get('customersCount')}.\n\nUSER QUESTION: {message}"

        formatted_history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=full_message)]
            )
        )

        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=formatted_history,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            )
        )
        return {"text": response.text, "isSimulated": False}
    except Exception as error:
        print("Gemini API Error in fetch_copilot_logic:", error)
        return {
            "text": f"### Copilot System Notice\n\nWe encountered an issue connecting to the live neural network: `{str(error)}`.\n\nFalling back to our high-fidelity, client-side intelligence system. Please verify that your API key is correctly entered under the **Secrets panel** or retry shortly.",
            "isSimulated": True
        }
