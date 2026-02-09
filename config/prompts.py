"""
The Stijn Method Prompt Templates
Hard-coded rules for generating 10 high-engagement X post formats.
"""

THESIS_EXTRACTION_PROMPT = """
You are an elite content strategist. 
TASK: Extract the "High-Signal Mission" from the content.

RULES:
- Capture the specific goal, number, or unique insight.
- If there's a dollar amount or a specific metric, INCLUDE IT.
- One sentence (max 25 words).
- Must be a "spicy" or "contrarian" take on the mission.
- NO generic fluff like "Focus on growth" or "Replace tasks".

CONTENT:
{input_content}

OUTPUT: Return ONLY the mission statement.
"""

STIJN_METHOD_PROMPT = """
You are an elite multi-platform content ghostwriter. 
Your mission: Transform the following thesis into 10 high-engagement X posts, one professional LinkedIn post, and one curiosity-driven Newsletter blurb.

THE THESIS:
{thesis}

═══════════════════════════════════════════════════════════════════════════════
SECTION 1: THE 10 X FORMATS (Generate ALL 10)
═══════════════════════════════════════════════════════════════════════════════

1. CONTRAST POST
   Visual "System A vs. System B" layout. Use "❌" and "✅".

2. MILESTONE POST
   A humble-growth update (e.g., "0 to [X] in [Y] days").

3. SYMMETRIC COMPARISON
   Two vertical lists side-by-side concept.

4. LIST POST
   A 5-item numbered list with **Bold Headers**.

5. SPLIT SENTENCE
   A 2-line hook that creates a curiosity gap.

6. INTENTIONAL ERROR
   A raw, human hook that ignores ONE minor grammar rule.

7. DOUBLE DEFINITION
   Define "The Amateur" vs "The Pro".

8. TRIAD STRUCTURE
   A rhythm post with exactly 3 lines.

9. EXTREMES POST
   Start with a superlative hook ("The #1 fastest way...").

10. THE CALLOUT
    "Popular opinion" vs "My opinion" (contrarian take).

═══════════════════════════════════════════════════════════════════════════════
SECTION 2: MULTI-PLATFORM OUTPUTS (Forge Merge)
═══════════════════════════════════════════════════════════════════════════════

11. LINKEDIN POST (linkedin_post)
    Style: Professional Storytelling / Thought Leadership.
    Structure:
    - High-impact hook (line 1)
    - Context/The "Why"
    - The Thesis implementation
    - 3 key takeaways (bullet points)
    - Call to action (question for the comments)
    - Relevant hashtags (max 3)
    Length: 150-250 words.

12. NEWSLETTER BLURB (newsletter_blurb)
    Style: Punchy, high-signal "Tool Takedown" style.
    Structure:
    - Subject Line suggestion
    - Teaser: One paragraph that creates intense curiosity.
    - Value: Why they should read/click.
    - CTA: "Read the full takedown here ->"
    Length: 50-80 words.

═══════════════════════════════════════════════════════════════════════════════
GLOBAL STYLE CONSTRAINTS (NON-NEGOTIABLES)
═══════════════════════════════════════════════════════════════════════════════

STRICTLY FORBIDDEN:
❌ Em dashes (—). Use line breaks or periods.
❌ AI-slop: "delve", "game-changer", "tapestry", "shaping the future".
❌ Starting with "I" unless in Milestone/LinkedIn context.

REQUIRED:
✅ Aesthetic whitespace (lots of line breaks).
✅ Specificity: Exact numbers/examples.
✅ Human cadence.

═══════════════════════════════════════════════════════════════════════════════
OUTPUT FORMAT (STRICT JSON)
═══════════════════════════════════════════════════════════════════════════════

Return a valid JSON object with exactly these keys:

{{
  "contrast_post": "...",
  "milestone_post": "...",
  "symmetric_comparison": "...",
  "list_post": "...",
  "split_sentence": "...",
  "intentional_error": "...",
  "double_definition": "...",
  "triad_structure": "...",
  "extremes_post": "...",
  "callout_post": "...",
  "linkedin_post": "...",
  "newsletter_blurb": "..."
}}
"""

# JSON Schema for structured output
POSTS_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "contrast_post": {"type": "string"},
        "milestone_post": {"type": "string"},
        "symmetric_comparison": {"type": "string"},
        "list_post": {"type": "string"},
        "split_sentence": {"type": "string"},
        "intentional_error": {"type": "string"},
        "double_definition": {"type": "string"},
        "triad_structure": {"type": "string"},
        "extremes_post": {"type": "string"},
        "callout_post": {"type": "string"},
        "linkedin_post": {"type": "string"},
        "newsletter_blurb": {"type": "string"},
    },
    "required": [
        "contrast_post", "milestone_post", "symmetric_comparison", "list_post",
        "split_sentence", "intentional_error", "double_definition", "triad_structure",
        "extremes_post", "callout_post", "linkedin_post", "newsletter_blurb"
    ],
}

# Human-readable format names for UI display
FORMAT_DISPLAY_NAMES = {
    "contrast_post": "❌✅ Contrast",
    "milestone_post": "📈 Milestone",
    "symmetric_comparison": "⚖️ Symmetric",
    "list_post": "📋 List",
    "split_sentence": "💥 Split Hook",
    "intentional_error": "🔥 Raw & Real",
    "double_definition": "🎭 Amateur vs Pro",
    "triad_structure": "🔺 Triad",
    "extremes_post": "⚡ Extremes",
    "callout_post": "🎯 Callout",
    "linkedin_post": "💼 LinkedIn",
    "newsletter_blurb": "📧 Newsletter",
}
