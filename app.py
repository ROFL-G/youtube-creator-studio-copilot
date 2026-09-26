import os
import sys
import socket
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gradio as gr

# ==============================================================================
# 1. NETWORK & PORT BINDING RESOLVER
# ==============================================================================
def find_available_port(preferred_ports=[7860, 8080, 8501, 9000]):
    for p in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    for _ in range(25):
        p = random.randint(8100, 9500)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    return 7860

# ==============================================================================
# 2. VECTOR RAG POLICY RETRIEVAL ENGINE
# ==============================================================================
YOUTUBE_SOP_KNOWLEDGE_BASE = [
    {
        "id": "SOP-CID-001",
        "topic": "Content ID Automated Match & Claim Dispute Workflow",
        "content": (
            "Content ID claims are automated fingerprint matches from sound recordings, melodies, or video segments. "
            "A claim is non-punitive and impacts monetization or regional availability only, not channel standing. "
            "Creators have 30 days to file an initial dispute. Claimants have 30 days to review, release, or uphold the claim. "
            "If an appeal is rejected, the claimant may issue a formal DMCA copyright takedown resulting in a strike."
        )
    },
    {
        "id": "SOP-ESC-002",
        "topic": "AdSense Monetization Escrow Policy",
        "content": (
            "During a Content ID claim dispute, ad revenue is held in an AdSense Escrow account if the creator disputes "
            "the claim within 5 days of the initial notification. If disputed after 5 days, all accrued pre-dispute revenue "
            "is transferred to the copyright owner, and escrow applies only to revenue generated after the dispute date."
        )
    },
    {
        "id": "SOP-REM-003",
        "topic": "YouTube Studio In-Editor Audio & Visual Remediation",
        "content": (
            "Creators can clear Content ID claims immediately without filing a dispute using Studio Editor tools: "
            "1. Erase/Mute Audio: Mutes only the flagged audio segment or all audio during that timestamp. "
            "2. Replace Song: Swaps claimed audio with a track from YouTube Audio Library. "
            "3. Trim Segment: Removes the claimed timestamp range entirely. The claim releases once processing finishes."
        )
    },
    {
        "id": "SOP-ADF-004",
        "topic": "Advertiser-Friendly Guidelines (Yellow Dollar Icon) Triage",
        "content": (
            "Yellow dollar icons denote limited or no ads due to Advertiser-Friendly Guideline violations: "
            "focal profanity in the first 7 to 30 seconds, adult themes, sensitive current events, or graphic content. "
            "Creators in good standing in the YouTube Partner Program (YPP) with high-velocity uploads (>100 views in 7 days) "
            "can request an expedited manual human review directly in YouTube Studio."
        )
    },
    {
        "id": "SOP-LIC-005",
        "topic": "Third-Party Commercial Music Licensing & Whitelist Tokens",
        "content": (
            "Commercial music subscription providers (Epidemic Sound, Artlist, Envato Elements, AudioJungle) "
            "issue digital license tokens. If a partner publisher triggers an automated claim, creators must provide "
            "the active license order ID or channel safelist CID. Support systems can trigger automated partner clearing."
        )
    },
    {
        "id": "SOP-STR-006",
        "topic": "DMCA Copyright Strike vs. Content ID Claim Distinction",
        "content": (
            "A Content ID claim does not penalize your channel. A Copyright Strike is a legal DMCA notice resulting in a "
            "channel penalty (3 strikes in 90 days = channel termination). Filing a DMCA Counter-Notification is a legal "
            "procedure with federal court disclosure. Never file a counter-notice without verified legal authorization or fair use."
        )
    },
    {
        "id": "SOP-AI-007",
        "topic": "Altered or Synthetic Content & AI Disclosure Mandate",
        "content": (
            "YouTube requires creators to disclose realistic altered or synthetic content, including AI-generated voices, "
            "deepfakes, and synthesized footage. Failure to disclose triggers video removal, demonetization, or platform penalties. "
            "Attaching standard C2PA metadata and checking the 'Altered Content' label resolves automated synthetic flags."
        )
    },
    {
        "id": "SOP-REU-008",
        "topic": "Reused Content & Inauthentic Mass Production Policy",
        "content": (
            "Monetization is suspended when channels upload content with minimal or no original commentary or narrative value. "
            "To resolve reused content demonetization, creators must submit a 5-minute video appeal detailing their original "
            "editing workflow, voiceover recording setup, and project files, or modify their channel catalog within 30 days."
        )
    }
]

sop_corpus = [doc["topic"] + " " + doc["content"] for doc in YOUTUBE_SOP_KNOWLEDGE_BASE]
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
sop_tfidf_matrix = tfidf_vectorizer.fit_transform(sop_corpus)

def retrieve_youtube_sop(query: str, top_k=2):
    query_vec = tfidf_vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, sop_tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [{"sop": YOUTUBE_SOP_KNOWLEDGE_BASE[idx], "score": float(similarities[idx])} for idx in top_indices]

# ==============================================================================
# 3. SIMULATED YOUTUBE STUDIO CMS & RIGHTS MANAGEMENT TOOLS
# ==============================================================================
SIMULATED_STUDIO_CMS_DB = {
    "VID-YT-88201": {
        "channel_name": "TechPulse Reviews",
        "channel_tier": "YPP Partner (520K subs)",
        "title": "Top Tech Gadgets of 2026 - Ultimate Guide",
        "views_24h": 142000,
        "restriction": "Content ID Claim (Monetization Sharing)",
        "claimant": "Universal Music Group / Epidemic Whitelist Sync",
        "asset_type": "Sound Recording (14s intro audio)",
        "matched_timestamps": "00:00 - 00:14",
        "license_token_attached": "EPIDEMIC-SUB-2026-X89",
        "dispute_age_days": 1
    },
    "VID-YT-91304": {
        "channel_name": "GameCraft Cinema",
        "channel_tier": "YPP Partner (1.2M subs)",
        "title": "Cyberpunk 2077 Sequel - In-Depth Lore Breakdown",
        "views_24h": 320000,
        "restriction": "Yellow Dollar Icon (Limited Ads)",
        "claimant": "Automated Content Classifier",
        "asset_type": "Advertiser-Friendly Ad Suitability",
        "matched_timestamps": "00:02 - 00:06 (High Profanity)",
        "license_token_attached": "None",
        "dispute_age_days": 0
    },
    "VID-YT-77402": {
        "channel_name": "Global Beat Beats",
        "channel_tier": "YPP Partner (85K subs)",
        "title": "Summer Beach Lo-Fi Chill Beats Mix 2026",
        "views_24h": 41000,
        "restriction": "Content ID Claim (Blocked in 2 Territories)",
        "claimant": "Sony Music Entertainment Japan",
        "asset_type": "Melody Composition Match",
        "matched_timestamps": "14:20 - 15:45",
        "license_token_attached": "None",
        "dispute_age_days": 7
    },
    "VID-YT-66110": {
        "channel_name": "Indie Film Spotlight",
        "channel_tier": "Standard Creator (24K subs)",
        "title": "Analyzing the Cinematography of Sci-Fi Classics",
        "views_24h": 12000,
        "restriction": "Content ID Claim (Revenue Claimed)",
        "claimant": "Warner Bros. Entertainment",
        "asset_type": "Audiovisual Clip (Movie Segment)",
        "matched_timestamps": "03:10 - 04:30",
        "license_token_attached": "FAIR-USE-CRITIQUE-TRANSFORMATIVE",
        "dispute_age_days": 2
    },
    "VID-YT-55301": {
        "channel_name": "Soundscape Audio",
        "channel_tier": "YPP Partner (310K subs)",
        "title": "Relaxing Rain and Thunder Ambience 8 Hours",
        "views_24h": 85000,
        "restriction": "Content ID Claim (False Positive Nature Audio)",
        "claimant": "Rumblefish Rights Administration",
        "asset_type": "Sound Recording (Thunder FX)",
        "matched_timestamps": "01:12:00 - 01:15:30",
        "license_token_attached": "PUBLIC-DOMAIN-COMMONS-CC0",
        "dispute_age_days": 0
    },
    "VID-YT-44219": {
        "channel_name": "Viral Reacts TV",
        "channel_tier": "YPP Partner (980K subs)",
        "title": "Reacting to the Craziest Stunts of 2026",
        "views_24h": 610000,
        "restriction": "DMCA Copyright Takedown (Strike 1 Pending Appeal)",
        "claimant": "RedBull Media House Legal",
        "asset_type": "Full Uncut Broadcast Restream",
        "matched_timestamps": "10:15 - 18:40",
        "license_token_attached": "None",
        "dispute_age_days": 4
    },
    "VID-YT-33108": {
        "channel_name": "Future Voices AI",
        "channel_tier": "YPP Partner (190K subs)",
        "title": "Celebrity Voice Simulation Experiment",
        "views_24h": 220000,
        "restriction": "Synthetic Content Disclosure Flag",
        "claimant": "Automated SynthID / C2PA Inspector",
        "asset_type": "Synthesized AI Voice Audio",
        "matched_timestamps": "01:10 - 02:45",
        "license_token_attached": "AI-SYNTH-DISCLOSURE-PENDING",
        "dispute_age_days": 1
    },
    "VID-YT-22091": {
        "channel_name": "Daily Clip Compilation Hub",
        "channel_tier": "YPP Monetization Suspended",
        "title": "Best Viral Moments Compilation #44",
        "views_24h": 95000,
        "restriction": "Channel Reused Content Demonetization",
        "claimant": "YouTube Policy Review Team",
        "asset_type": "Mass Unedited Viral Video Compilation",
        "matched_timestamps": "Full Video Duration",
        "license_token_attached": "None",
        "dispute_age_days": 3
    }
}

def tool_inspect_content_id_match(video_id: str):
    if video_id not in SIMULATED_STUDIO_CMS_DB:
        return {"status": "ERROR", "message": f"Video ID {video_id} not found."}
    meta = SIMULATED_STUDIO_CMS_DB[video_id]
    return {"status": "SUCCESS", "video_id": video_id, **meta}

def tool_evaluate_monetization_escrow(video_id: str):
    meta = SIMULATED_STUDIO_CMS_DB.get(video_id, {})
    dispute_age = meta.get("dispute_age_days", 0)
    if dispute_age <= 5:
        return {
            "escrow_status": "ESCROW_PRESERVED",
            "views_24h": meta.get("views_24h", 0),
            "policy": "Dispute filed within 5-day window. 100% of accrued ad revenue held in AdSense Escrow."
        }
    return {
        "escrow_status": "ESCROW_FORFEITED",
        "views_24h": meta.get("views_24h", 0),
        "policy": "Disputed after 5-day window. Pre-dispute ad revenue released to claimant."
    }

def tool_verify_fair_use_and_license(license_token: str):
    if any(k in license_token for k in ["EPIDEMIC", "ENVATO", "ARTLIST", "PUBLIC-DOMAIN"]):
        return {"validation": "VERIFIED_COMMERCIAL_OR_PD", "automated_clearance": True, "strike_risk": "0%"}
    elif "FAIR-USE" in license_token:
        return {"validation": "TRANSFORMATIVE_CRITIQUE", "automated_clearance": False, "strike_risk": "Moderate"}
    elif "AI-SYNTH" in license_token:
        return {"validation": "SYNTHETIC_AI_DISCLOSURE_ELIGIBLE", "automated_clearance": True, "strike_risk": "0%"}
    return {"validation": "NO_VALID_LICENSE", "automated_clearance": False, "strike_risk": "High"}

def tool_execute_studio_remediation(action_type: str, video_id: str, parameters: dict):
    if action_type == "AUTO_CLEAR_WHITELIST":
        return {"execution": "COMPLETED", "action": "Partner Whitelist API Call", "result": f"Claim released on video {video_id}. Ad revenue escrow restored."}
    elif action_type == "STAGE_STUDIO_AUDIO_MUTE":
        return {"execution": "STAGED", "action": "Studio In-Editor Audio Mute", "result": f"Flagged audio segment ({parameters.get('segment')}) queued for muting."}
    elif action_type == "SUBMIT_YELLOW_ICON_MANUAL_REVIEW":
        return {"execution": "SUBMITTED", "action": "YPP Ad Suitability Review Queue", "result": f"Video {video_id} expedited to human ad specialist."}
    elif action_type == "APPLY_AI_DISCLOSURE_LABEL":
        return {"execution": "COMPLETED", "action": "Studio Metadata Patch", "result": f"Altered Content disclosure badge added to {video_id}. Monetization restored."}
    elif action_type == "ESCALATE_LEGAL_COPYRIGHT_TEAM":
        return {"execution": "ESCALATED", "action": "YouTube Copyright Operations Queue", "result": f"Escalated to Legal & Fair Use review team."}
    return {"execution": "FAILED", "reason": "Unknown remediation action."}

# ==============================================================================
# 4. REACT AGENT ORCHESTRATION LOOP
# ==============================================================================
def run_youtube_rights_copilot(video_id: str, creator_query: str, remediation_override: str):
    trace = [
        f"🔍 [Perception]: Ingested request for Video ID: {video_id}",
        f"📝 [Perception]: Creator Issue Query: '{creator_query}'",
        f"⚙️ [Perception]: Support Routing Mode: '{remediation_override}'"
    ]
    
    cms = tool_inspect_content_id_match(video_id)
    if cms.get("status") == "ERROR":
        return (
            "### ❌ Error Encountered\nVideo was not found in the Studio CMS registry.",
            "\n".join(trace),
            "N/A",
            "Please verify the Video ID."
        )

    trace.append(f"⚙️ [Action 1: CMS Inspection]: Restriction: '{cms['restriction']}', Claimant: '{cms['claimant']}'.")

    # Domain RAG retrieval
    sops = retrieve_youtube_sop(f"{cms['restriction']} {cms['asset_type']} {creator_query}", top_k=1)
    top_sop = sops[0]["sop"]
    trace.append(f"📚 [Action 2: Domain Vector RAG]: Grounded Policy [{top_sop['id']}]: '{top_sop['topic']}'.")

    # Escrow and license evaluations
    escrow = tool_evaluate_monetization_escrow(video_id)
    trace.append(f"💳 [Action 3: AdSense Escrow]: {escrow['escrow_status']} - {escrow['policy']}")

    license_eval = tool_verify_fair_use_and_license(cms["license_token_attached"])
    trace.append(f"🛡️ [Action 4: License Verification]: Status: '{license_eval['validation']}' (Strike Risk: {license_eval['strike_risk']})")

    # Autonomous remediation execution
    if remediation_override == "Force Manual Human Review Escalation":
        action_type = "ESCALATE_LEGAL_COPYRIGHT_TEAM"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {})
        trace.append(f"⚠️ [Override Action]: Forced manual escalation triggered.")
        work_order = f"### 📋 MINTO WORK ORDER: MANUAL SPECIALIST DISPATCH\n- **Verdict:** Human intervention requested via operator override.\n- **Action:** {remedy_result['result']}\n- **Telemetry:** {escrow['views_24h']:,} 24h views."
        creator_guidance = f"Your case for video **{cms['title']}** has been escalated directly to a Senior YouTube Support Specialist for manual investigation."
    elif remediation_override == "Force Studio Audio Mute / Replace":
        action_type = "STAGE_STUDIO_AUDIO_MUTE"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {"segment": cms["matched_timestamps"]})
        trace.append(f"⚙️ [Override Action]: Staged Studio In-Editor Audio Mute.")
        work_order = f"### 📋 MINTO WORK ORDER: IN-STUDIO REMEDIATION APPLIED\n- **Verdict:** Manual mute trigger initiated.\n- **Action:** {remedy_result['result']}"
        creator_guidance = f"We have prepared the YouTube Studio Editor to mute the audio at `{cms['matched_timestamps']}`. Once processing completes, all restrictions will be lifted."
    elif "AI-SYNTH" in cms["license_token_attached"]:
        action_type = "APPLY_AI_DISCLOSURE_LABEL"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {})
        trace.append(f"🤖 [Action 5]: Synthetic Content label applied to resolve SynthID flag.")
        work_order = f"### 📋 MINTO WORK ORDER: AI DISCLOSURE COMPLIANCE\n- **Verdict:** Flagged for synthetic voice without disclosure.\n- **Action:** {remedy_result['result']}"
        creator_guidance = f"Your video was flagged for synthetic voice usage. We updated your video metadata with YouTube's **Altered Content** badge, resolving the restriction."
    elif license_eval["automated_clearance"]:
        action_type = "AUTO_CLEAR_WHITELIST"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {})
        trace.append(f"⚙️ [Action 5]: Verified commercial license token identified. Executed {action_type}.")
        work_order = f"### 📋 MINTO WORK ORDER: AUTOMATED CLAIM CLEARANCE\n- **Verdict:** Valid commercial license confirmed (`{cms['license_token_attached']}`).\n- **Action:** {remedy_result['result']}\n- **Escrow:** {escrow['escrow_status']}."
        creator_guidance = f"Good news! We validated your commercial license token (`{cms['license_token_attached']}`). The claim from **{cms['claimant']}** has been released with zero revenue loss."
    elif "Yellow Dollar" in cms["restriction"]:
        action_type = "SUBMIT_YELLOW_ICON_MANUAL_REVIEW"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {})
        trace.append(f"⚙️ [Action 5]: Ad-suitability demonetization detected. Expedited for review.")
        work_order = f"### 📋 MINTO WORK ORDER: ADVERTISER-FRIENDLY REVIEW DISPATCH\n- **Verdict:** Flagged language at `{cms['matched_timestamps']}`.\n- **Action:** {remedy_result['result']} (High view velocity: {escrow['views_24h']:,} views/24h)."
        creator_guidance = f"Your video was flagged for limited ads at `{cms['matched_timestamps']}`. With over 100,000 views today, it has been expedited to a human ad specialist (ETA: 4–12 hours)."
    elif "DMCA" in cms["restriction"]:
        action_type = "ESCALATE_LEGAL_COPYRIGHT_TEAM"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {})
        trace.append(f"⚖️ [Action 5]: Formal DMCA strike pending. Escalated to Legal Operations.")
        work_order = f"### 📋 MINTO WORK ORDER: LEGAL TAKEDOWN ESCALATION\n- **Verdict:** Formal DMCA takedown issued by {cms['claimant']}.\n- **Warning:** Do not advise submitting counter-notification without verified court standing."
        creator_guidance = f"Your video received a formal DMCA copyright takedown notice from **{cms['claimant']}**. Contact the claimant directly to request a retraction to protect your channel from strikes."
    elif "Reused Content" in cms["restriction"]:
        action_type = "ESCALATE_LEGAL_COPYRIGHT_TEAM"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {})
        trace.append(f"🛑 [Action 5]: Reused content demonetization flagged. Staged appeal workflow.")
        work_order = f"### 📋 MINTO WORK ORDER: REUSED CONTENT APPEAL\n- **Verdict:** Channel demonetized under inauthentic/reused content policy.\n- **Recommended Fix:** Prepare 5-minute video appeal detailing editing timeline and voiceover projects."
        creator_guidance = f"Your channel was flagged under the Reused Content policy. You can submit a 5-minute video appeal in YouTube Studio demonstrating your recording and editing process."
    else:
        action_type = "STAGE_STUDIO_AUDIO_MUTE"
        remedy_result = tool_execute_studio_remediation(action_type, video_id, {"segment": cms["matched_timestamps"]})
        trace.append(f"✂️ [Action 5]: Claim is past 5-day escrow window. Staged in-editor audio mute.")
        work_order = f"### 📋 MINTO WORK ORDER: STUDIO IN-EDITOR REMEDIATION STAGED\n- **Verdict:** Content ID claim past 5-day escrow window (`{cms['matched_timestamps']}`).\n- **Action:** {remedy_result['result']}"
        creator_guidance = f"This claim is older than 5 days, so filing a dispute will not recover past revenue. We recommend using YouTube Studio Editor to mute or replace that segment to lift the block."

    sop_text = f"**[{top_sop['id']}] {top_sop['topic']}**\n\n{top_sop['content']}"
    return work_order, "\n".join(trace), sop_text, creator_guidance

# ==============================================================================
# 5. GRADIO OPERATIONS COCKPIT UI
# ==============================================================================
PRESET_SCENARIOS = {
    "1. Epidemic Sound License Sync (Instant Whitelist Release)": (
        "VID-YT-88201",
        "I purchased an Epidemic Sound commercial license for my intro, but UMG still claimed it! How do I clear this?",
        "TechPulse Reviews (YPP Partner - 520K subs)"
    ),
    "2. Demonetization Yellow Dollar Icon (Profanity Fast-Track Triage)": (
        "VID-YT-91304",
        "My new video got 300k views today but has a yellow dollar icon! Can I get an urgent manual human review?",
        "GameCraft Cinema (YPP Partner - 1.2M subs)"
    ),
    "3. Lo-Fi Melody Composition Claim (>5 Days / Escrow Forfeited)": (
        "VID-YT-77402",
        "This song has been blocked in Japan for a week. Can I dispute it now and keep my ad revenue?",
        "Global Beat Beats (YPP Partner - 85K subs)"
    ),
    "4. Fair Use Transformative Critique (Active AdSense Escrow)": (
        "VID-YT-66110",
        "Warner Bros claimed my 1-minute critique clip. Will disputing this give my channel a copyright strike?",
        "Indie Film Spotlight (Standard Creator - 24K subs)"
    ),
    "5. Public Domain Nature Thunder FX Claimed (Automated Release)": (
        "VID-YT-55301",
        "A distributor claimed thunder sounds in my 8-hour storm video. Thunder is public domain! Please clear this.",
        "Soundscape Audio (YPP Partner - 310K subs)"
    ),
    "6. High-Severity DMCA Legal Takedown (RedBull Broadcast Restream)": (
        "VID-YT-44219",
        "I received a Copyright Strike for restreaming a stunt broadcast. Can your AI cancel the strike?",
        "Viral Reacts TV (YPP Partner - 980K subs)"
    ),
    "7. Synthetic Content AI Voice Flag (SynthID / C2PA Disclosure)": (
        "VID-YT-33108",
        "My experiment video has a restriction saying 'Altered synthetic audio not disclosed'. How do I fix this?",
        "Future Voices AI (YPP Partner - 190K subs)"
    ),
    "8. Reused Content Channel Demonetization (Mass Compilation)": (
        "VID-YT-22091",
        "My entire channel monetization was turned off for 'Reused Content'. What evidence do I submit for appeal?",
        "Daily Clip Compilation Hub (YPP Suspended)"
    )
}

DEFAULT_PRESET_KEY = list(PRESET_SCENARIOS.keys())[0]

def update_incident_fields(preset_key):
    if preset_key in PRESET_SCENARIOS:
        vid_id, query, channel_info = PRESET_SCENARIOS[preset_key]
        return vid_id, query, channel_info
    return "", "", ""

custom_css = """
.container { max-width: 1200px; margin: auto; }
.output-box { border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); }
"""

with gr.Blocks(title="YouTube Studio Agentic Copilot", theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# 🔴 YouTube Creator Studio & Rights Operations Agentic Copilot")
    gr.Markdown("Autonomous dispute diagnostics, AdSense revenue escrow preservation, and grounded SOP retrieval.")

    with gr.Row():
        with gr.Column(scale=4):
            gr.Markdown("### ⚙️ Studio Triage & Ticket Injection")
            scenario_dropdown = gr.Dropdown(
                choices=list(PRESET_SCENARIOS.keys()),
                value=DEFAULT_PRESET_KEY,
                label="Choose an Incident Preset"
            )
            channel_badge = gr.Textbox(
                label="Channel & Tier Context",
                value=PRESET_SCENARIOS[DEFAULT_PRESET_KEY][2],
                interactive=False
            )
            video_id_input = gr.Textbox(
                label="Target Video ID",
                value=PRESET_SCENARIOS[DEFAULT_PRESET_KEY][0]
            )
            creator_query_input = gr.Textbox(
                label="Creator Support Query / In-Studio Restriction Ticket",
                lines=4,
                value=PRESET_SCENARIOS[DEFAULT_PRESET_KEY][1]
            )
            remediation_override_dropdown = gr.Dropdown(
                choices=[
                    "Auto-Detect Optimal Action (Autonomous ReAct)",
                    "Force Manual Human Review Escalation",
                    "Force Studio Audio Mute / Replace"
                ],
                value="Auto-Detect Optimal Action (Autonomous ReAct)",
                label="Support Routing Override"
            )
            run_btn = gr.Button("🚀 Run Autonomous Agent Triage", variant="primary")

        with gr.Column(scale=6):
            with gr.Tabs():
                with gr.TabItem("📋 Partner Support Work Order"):
                    work_order_output = gr.Markdown()
                with gr.TabItem("💬 In-Studio Creator Guidance"):
                    creator_guidance_output = gr.Textbox(label="Customer-Ready Empathetic Studio Response", lines=6)
                with gr.TabItem("🧠 ReAct Agent Diagnostic Trace"):
                    thought_trace_output = gr.Textbox(label="Perception-Thought-Action Execution Log", lines=12)
                with gr.TabItem("📖 Grounded YouTube Policy SOP"):
                    sop_output = gr.Markdown()

    # Dynamic interactions
    scenario_dropdown.change(
        fn=update_incident_fields,
        inputs=[scenario_dropdown],
        outputs=[video_id_input, creator_query_input, channel_badge]
    )

    run_btn.click(
        fn=run_youtube_rights_copilot,
        inputs=[video_id_input, creator_query_input, remediation_override_dropdown],
        outputs=[work_order_output, thought_trace_output, sop_output, creator_guidance_output]
    )

# ==============================================================================
# 6. APPLICATION ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    is_colab = "google.colab" in sys.modules
    env_port = os.environ.get("PORT")

    if env_port:
        port = int(env_port)
        host = "0.0.0.0"
        share = False
    elif is_colab:
        port = find_available_port()
        host = "127.0.0.1"
        share = True
    else:
        port = find_available_port()
        host = "127.0.0.1"
        share = False

    print(f"🚀 Launching YouTube Copilot on http://{host}:{port}")
    demo.launch(
        server_name=host,
        server_port=port,
        inbrowser=True,
        share=share
    )
