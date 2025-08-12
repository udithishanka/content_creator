"""Content creation pipeline using CrewAI.

This script defines agents and tasks for a high-level content
creation workflow:
1. Trend Detection
2. Planning
3. Research & Fact-Checking
4. Outline
5. Drafting
6. Editing & SEO
7. Media Generation
8. Assembly
9. Compliance
10. Publish/Schedule
11. Analytics Feedback
"""

from crewai import Agent, Task, Crew

# Agent definitions
trend_detector = Agent(
    name="Trend Detector Agent",
    role="Finds and ranks trending topics",
    goal="Ingest social signals and output ranked trend candidates",
    backstory=(
        "Scans X/Twitter, Reddit, YouTube, Google Trends and niche RSS feeds "
        "to surface timely, relevant topics."
    ),
)

planner = Agent(
    name="Planner Agent",
    role="Creates content plans aligned with brand goals",
    goal="Turn a top trend into an actionable content plan",
    backstory=(
        "Understands the audience persona, brand style and calendar to craft "
        "titles and channel choices."
    ),
)

researcher = Agent(
    name="Researcher Agent",
    role="Gathers facts and sources",
    goal="Collect verifiable information for the planned content",
    backstory=(
        "Uses web search and internal knowledge to build a bundle of sources "
        "with citations."
    ),
)

fact_checker = Agent(
    name="Fact-Checker Agent",
    role="Validates claims and flags risks",
    goal="Ensure the research bundle and draft contain accurate information",
    backstory="Performs secondary verification and contradiction detection.",
)

outliner = Agent(
    name="Outliner Agent",
    role="Structures articles and scripts",
    goal="Transform research into an outline for blog and video",
    backstory="Applies channel-specific templates for clarity and flow.",
)

writer = Agent(
    name="Writer Agent",
    role="Produces long-form drafts",
    goal="Write a brand-aligned article with SEO keywords",
    backstory="Mimics the house tone and embeds citation anchors.",
)

editor = Agent(
    name="Editor/SEO Agent",
    role="Polishes drafts for style and search",
    goal="Improve grammar, readability and metadata",
    backstory="Optimizes content, injects schema.org JSON-LD and prepares meta tags.",
)

scriptwriter = Agent(
    name="Scriptwriter Agent",
    role="Crafts short-form video scripts",
    goal="Produce hooks and beats for 9:16 videos",
    backstory="Uses formulas like AIDA to keep viewers engaged.",
)

media_gen = Agent(
    name="Media Generation Agent",
    role="Produces multimedia assets",
    goal="Generate images, B-roll, voiceover and captions",
    backstory="Pluggable tools like SDXL, stock search and TTS build the asset pack.",
)

assembler = Agent(
    name="Video Assembler Agent",
    role="Composes final short video",
    goal="Lay out assets on a timeline to render a 9:16 short",
    backstory="Uses FFmpeg/Remotion style presets for quick assembly.",
)

qa_agent = Agent(
    name="Compliance/Brand QA Agent",
    role="Checks safety and tone",
    goal="Verify no PII, plagiarism or off-brand terms remain",
    backstory="Final gatekeeper before publishing.",
)

publisher = Agent(
    name="Publisher/Scheduler Agent",
    role="Posts content to platforms",
    goal="Schedule the blog and short across channels",
    backstory="Interfaces with WordPress, YouTube Shorts and social schedulers.",
)

analytics = Agent(
    name="Analytics Agent",
    role="Monitors performance",
    goal="Report metrics back to the planning loop",
    backstory="Feeds CTR and watch-time into future trend detection.",
)

# Task definitions
trend_task = Task(
    description="Ingest and rank trending topics across social sources",
    expected_output="TrendCandidates[] with confidence and angle suggestions",
    agent=trend_detector,
)

plan_task = Task(
    description="Create a content plan for the top trend including title options, angle and channels",
    expected_output="ContentPlan with target persona and distribution channels",
    agent=planner,
)

research_task = Task(
    description="Gather facts, quotes and links with citations based on the content plan",
    expected_output="ResearchBundle containing sourced information",
    agent=researcher,
)

fact_check_task = Task(
    description="Verify research and highlight any risky claims",
    expected_output="VerifiedClaims and RiskFlags",
    agent=fact_checker,
)

outline_task = Task(
    description="Turn the plan and verified claims into both article and video outlines",
    expected_output="ArticleOutline and VideoScriptOutline",
    agent=outliner,
)

write_task = Task(
    description="Draft the article following the outline and style guide",
    expected_output="DraftArticle.md with citation anchors",
    agent=writer,
)

edit_task = Task(
    description="Edit the draft for grammar, readability and SEO; output final article and metadata",
    expected_output="FinalArticle.md plus meta tags",
    agent=editor,
)

script_task = Task(
    description="Write a short-form video script based on the video outline and key findings",
    expected_output="ShortsScript.txt with beats and CTA",
    agent=scriptwriter,
)

media_task = Task(
    description="Generate required multimedia assets from article highlights and script",
    expected_output="images, b-roll, voiceover.wav and captions.srt",
    agent=media_gen,
)

assemble_task = Task(
    description="Assemble the short video using the script and assets",
    expected_output="shorts.mp4 and thumbnail.png",
    agent=assembler,
)

qa_task = Task(
    description="Run compliance and brand checks on the article and video",
    expected_output="pass/fail report with fixes if needed",
    agent=qa_agent,
)

publish_task = Task(
    description="Publish or schedule approved assets to the blog and social channels",
    expected_output="Platform post IDs or schedule confirmations",
    agent=publisher,
)

analytics_task = Task(
    description="Collect performance metrics and feed insights back to the trend detector",
    expected_output="PerformanceReport linking to planning data",
    agent=analytics,
)

crew = Crew(
    agents=[
        trend_detector,
        planner,
        researcher,
        fact_checker,
        outliner,
        writer,
        editor,
        scriptwriter,
        media_gen,
        assembler,
        qa_agent,
        publisher,
        analytics,
    ],
    tasks=[
        trend_task,
        plan_task,
        research_task,
        fact_check_task,
        outline_task,
        write_task,
        edit_task,
        script_task,
        media_task,
        assemble_task,
        qa_task,
        publish_task,
        analytics_task,
    ],
)

if __name__ == "__main__":
    # Kicking off the crew will require valid LLM credentials.
    # The call is guarded so importing this module does not execute the workflow.
    crew.kickoff()
