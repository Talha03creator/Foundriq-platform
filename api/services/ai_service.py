import json
import re
import random
from api.config import OPENAI_API_KEY

# ---------------------------------------------------------------------------
# AI Service – Business Analysis & Strategy Generation
# ---------------------------------------------------------------------------
# Uses OpenAI API when available, falls back to intelligent mock data
# for demo purposes when the API key is invalid or unreachable.
# ---------------------------------------------------------------------------

try:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except Exception:
    client = None

ANALYSIS_PROMPT = """You are FoundrIQ, an expert AI business analyst. Analyze the following business idea and return a JSON object with EXACTLY this structure (no extra text, no markdown, just valid JSON):

{{
  "validation_score": <integer 0-100>,
  "competition_score": <integer 0-100>,
  "risk_level": "<Low|Medium|High>",
  "swot": {{
    "strengths": ["<strength1>", "<strength2>", "<strength3>"],
    "weaknesses": ["<weakness1>", "<weakness2>", "<weakness3>"],
    "opportunities": ["<opportunity1>", "<opportunity2>", "<opportunity3>"],
    "threats": ["<threat1>", "<threat2>", "<threat3>"]
  }},
  "revenue_forecast": {{
    "month_1": <number>,
    "month_2": <number>,
    "month_3": <number>,
    "month_4": <number>,
    "month_5": <number>,
    "month_6": <number>,
    "month_7": <number>,
    "month_8": <number>,
    "month_9": <number>,
    "month_10": <number>,
    "month_11": <number>,
    "month_12": <number>,
    "currency": "USD"
  }},
  "break_even": {{
    "months_to_break_even": <integer>,
    "initial_investment": <number>,
    "monthly_costs": <number>,
    "monthly_revenue_at_break_even": <number>
  }},
  "strategy_steps": [
    {{
      "step": 1,
      "title": "<step title>",
      "description": "<detailed description>",
      "timeline": "<e.g. Week 1-2>",
      "priority": "<High|Medium|Low>"
    }}
  ],
  "pricing_optimization": "<brief pricing recommendation>",
  "growth_roadmap": "<brief growth roadmap paragraph>",
  "investment_efficiency": "<brief investment efficiency suggestion>"
}}

Business Idea: {business_idea}
Target Market: {target_market}
Budget: ${budget}
Pricing Model: {pricing_model}
Competitors: {competitors}

Return ONLY the JSON object, nothing else."""


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try extracting from code block
    match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    # Try finding first { ... } block
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {}


def _generate_mock_analysis(business_idea: str, target_market: str, budget: float,
                            pricing_model: str, competitors: str) -> dict:
    """Generate intelligent mock analysis for demo/fallback."""
    validation = random.randint(60, 92)
    competition = random.randint(35, 80)
    risk = "Low" if validation > 80 else ("High" if validation < 50 else "Medium")
    base_rev = budget * 0.15 if budget else 5000

    return {
        "validation_score": validation,
        "competition_score": competition,
        "risk_level": risk,
        "swot": {
            "strengths": [
                f"Innovative approach to {target_market or 'the market'}",
                "Strong value proposition with clear differentiation",
                f"Scalable {pricing_model or 'business'} model"
            ],
            "weaknesses": [
                "New entrant with limited brand recognition",
                f"Budget of ${budget or 'N/A'} may limit initial marketing reach",
                "Requires customer education on value proposition"
            ],
            "opportunities": [
                f"Growing demand in {target_market or 'target'} segment",
                "Digital-first strategy enables rapid market penetration",
                "Partnership opportunities with complementary services"
            ],
            "threats": [
                f"Established competitors: {competitors or 'various players'}",
                "Market volatility and economic uncertainty",
                "Rapid technology changes could impact product relevance"
            ]
        },
        "revenue_forecast": {
            "month_1": round(base_rev * 0.3),
            "month_2": round(base_rev * 0.5),
            "month_3": round(base_rev * 0.7),
            "month_4": round(base_rev * 0.9),
            "month_5": round(base_rev * 1.1),
            "month_6": round(base_rev * 1.4),
            "month_7": round(base_rev * 1.7),
            "month_8": round(base_rev * 2.0),
            "month_9": round(base_rev * 2.4),
            "month_10": round(base_rev * 2.8),
            "month_11": round(base_rev * 3.3),
            "month_12": round(base_rev * 3.8),
            "currency": "USD"
        },
        "break_even": {
            "months_to_break_even": random.randint(4, 9),
            "initial_investment": budget or 50000,
            "monthly_costs": round((budget or 50000) * 0.08),
            "monthly_revenue_at_break_even": round((budget or 50000) * 0.12)
        },
        "strategy_steps": [
            {"step": 1, "title": "Market Research & Validation", "description": f"Conduct deep-dive research into {target_market or 'target market'} to validate demand and identify ideal customer profiles.", "timeline": "Week 1-2", "priority": "High"},
            {"step": 2, "title": "MVP Development", "description": f"Build minimum viable product focusing on core value proposition of {business_idea[:80] if business_idea else 'the solution'}.", "timeline": "Week 3-6", "priority": "High"},
            {"step": 3, "title": "Beta Launch & Feedback", "description": "Launch to a small group of early adopters, collect feedback, and iterate on the product.", "timeline": "Week 7-8", "priority": "High"},
            {"step": 4, "title": "Marketing & Growth", "description": "Implement digital marketing strategy including content marketing, SEO, and targeted advertising.", "timeline": "Week 9-12", "priority": "Medium"},
            {"step": 5, "title": "Scale & Optimize", "description": f"Optimize {pricing_model or 'pricing'} strategy, expand to new channels, and build strategic partnerships.", "timeline": "Month 4-6", "priority": "Medium"},
            {"step": 6, "title": "Series Funding Preparation", "description": "Prepare pitch deck, financial projections, and growth metrics for investor meetings.", "timeline": "Month 6-9", "priority": "Low"}
        ],
        "pricing_optimization": f"Consider a tiered {pricing_model or 'pricing'} model with a freemium entry point to maximize user acquisition while maintaining premium revenue from power users.",
        "growth_roadmap": f"Phase 1 (M1-3): Establish product-market fit in {target_market or 'primary market'}. Phase 2 (M4-6): Scale user acquisition through content marketing and partnerships. Phase 3 (M7-12): Expand to adjacent markets and introduce enterprise features.",
        "investment_efficiency": f"With a budget of ${budget or 50000}, allocate 40% to product development, 30% to marketing, 20% to operations, and 10% as reserve. Focus on organic growth channels to maximize ROI."
    }


async def analyze_business(business_idea: str, target_market: str, budget: float,
                           pricing_model: str, competitors: str) -> dict:
    """Run full AI business analysis. Falls back to mock data if API fails."""
    if client:
        try:
            prompt = ANALYSIS_PROMPT.format(
                business_idea=business_idea,
                target_market=target_market,
                budget=budget or 50000,
                pricing_model=pricing_model or "Not specified",
                competitors=competitors or "Not specified"
            )
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7,
            )
            text = response.choices[0].message.content.strip()
            data = _extract_json(text)
            if data and "validation_score" in data:
                return data
        except Exception as e:
            print(f"[FoundrIQ AI] OpenAI API error: {e}")

    # Fallback to mock
    return _generate_mock_analysis(business_idea, target_market, budget, pricing_model, competitors)


async def generate_strategy(business_idea: str, target_market: str) -> dict:
    """Generate a focused strategy document."""
    if client:
        try:
            prompt = f"""Generate a detailed business execution strategy for:
Business: {business_idea}
Market: {target_market}

Return a JSON object with:
{{
  "execution_plan": [
    {{"phase": 1, "name": "<phase name>", "duration": "<timeframe>", "tasks": ["<task1>", "<task2>"], "kpis": ["<kpi1>", "<kpi2>"]}}
  ],
  "investment_tips": ["<tip1>", "<tip2>"],
  "pricing_strategy": "<detailed pricing strategy>",
  "growth_milestones": [{{"month": 3, "milestone": "<description>", "target_metric": "<metric>"}}]
}}
Return ONLY valid JSON."""
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.7,
            )
            data = _extract_json(response.choices[0].message.content.strip())
            if data:
                return data
        except Exception:
            pass

    return {
        "execution_plan": [
            {"phase": 1, "name": "Foundation", "duration": "Month 1-2", "tasks": ["Market research", "MVP design", "Initial team setup"], "kpis": ["Customer interviews completed", "MVP wireframe approved"]},
            {"phase": 2, "name": "Launch", "duration": "Month 3-4", "tasks": ["MVP development", "Beta testing", "Marketing setup"], "kpis": ["100 beta users", "NPS > 40"]},
            {"phase": 3, "name": "Growth", "duration": "Month 5-8", "tasks": ["Scale marketing", "Feature expansion", "Partnerships"], "kpis": ["1000 active users", "MRR > $10K"]},
            {"phase": 4, "name": "Scale", "duration": "Month 9-12", "tasks": ["Enterprise features", "International expansion", "Funding round"], "kpis": ["5000 active users", "Series A ready"]}
        ],
        "investment_tips": [
            "Focus 60% of budget on product development in the first 3 months",
            "Use content marketing for organic growth before paid acquisition",
            "Build referral programs to reduce customer acquisition cost"
        ],
        "pricing_strategy": "Implement a value-based pricing model with 3 tiers. Free tier for user acquisition, Professional tier at $29/month for core features, and Enterprise tier at $99/month with premium support and analytics.",
        "growth_milestones": [
            {"month": 3, "milestone": "Product-Market Fit Achieved", "target_metric": "40% retention rate"},
            {"month": 6, "milestone": "Revenue Breakeven", "target_metric": "MRR covers operating costs"},
            {"month": 9, "milestone": "Growth Inflection Point", "target_metric": "20% MoM growth"},
            {"month": 12, "milestone": "Scale Ready", "target_metric": "Predictable unit economics"}
        ]
    }

