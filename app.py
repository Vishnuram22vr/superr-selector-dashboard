"""
SupeRR Selector Season 2 — Rajasthan Royals IPL 2027 Auction Analytics
Phase 6: Executive Analytics Dashboard
Framework: Streamlit + Plotly + Pandas
Theme: Rajasthan Royals Pink & Royal Blue
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RR SupeRR Selector 2027 | Executive Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Rajasthan Royals CSS
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #0A1128;
        color: #F8FAFC;
    }
    
    /* Headers & Text */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1C2541 0%, #151D36 100%);
        border: 1px solid #2A3859;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        margin-bottom: 15px;
    }
    .metric-card-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .metric-card-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .metric-card-subtitle {
        font-size: 0.8rem;
        color: #E73895;
        font-weight: 600;
        margin-top: 4px;
    }
    
    /* RR Pink Highlights */
    .rr-pink-text {
        color: #E73895 !important;
        font-weight: 700;
    }
    .rr-blue-text {
        color: #38BDF8 !important;
        font-weight: 700;
    }
    .rr-gold-text {
        color: #FBBF24 !important;
        font-weight: 700;
    }
    
    /* Badges & Tags */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-pink {
        background-color: rgba(231, 56, 149, 0.2);
        color: #FF66B2;
        border: 1px solid #E73895;
    }
    .badge-blue {
        background-color: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid #0284C7;
    }
    .badge-gold {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid #D97706;
    }
    .badge-red {
        background-color: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid #DC2626;
    }
    .badge-green {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid #059669;
    }
    
    /* Governance Disclaimer Banner */
    .disclaimer-banner {
        background: rgba(30, 41, 59, 0.8);
        border-left: 4px solid #E73895;
        padding: 12px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
        font-size: 0.85rem;
        color: #CBD5E1;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA LOADERS (CACHED)
# -----------------------------------------------------------------------------
@st.cache_data
def load_all_datasets():
    """Loads all approved Phase 4 & Phase 5 datasets with zero recalculation."""
    squad_df = pd.read_csv('phase5_rr_proposed_analytical_squad.csv')
    shortlist_df = pd.read_csv('phase5_rr_shortlist_by_archetype.csv')
    ar_df = pd.read_csv('phase5_rr_all_rounders_balance.csv')
    watchlist_df = pd.read_csv('phase5_rr_emerging_talent_watchlist.csv')
    dossier_df = pd.read_csv('phase5_rr_target_dossiers.csv')
    comp_df = pd.read_csv('phase4_player_comparison.csv')
    val_results = pd.read_csv('phase5_validation_results.csv')
    return squad_df, shortlist_df, ar_df, watchlist_df, dossier_df, comp_df, val_results

try:
    squad_df, shortlist_df, ar_df, watchlist_df, dossier_df, comp_df, val_results = load_all_datasets()
except Exception as e:
    st.error(f"Error loading Phase 5 datasets: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & SEARCH
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 15px 0;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #E73895; letter-spacing: -1px;">
                Supe<span style="color: #38BDF8;">RR</span> Selector
            </div>
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.15em; color: #94A3B8; font-weight: 600;">
                Rajasthan Royals IPL 2027 Analytics
            </div>
            <div style="margin-top: 8px;">
                <span class="badge badge-pink">Phase 6 Engine</span>
                <span class="badge badge-blue">10/10 Audited</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Radio
    nav_selection = st.radio(
        "Navigation Menu",
        [
            "🏛️ Executive Overview",
            "⚡ Pressure Performance & APR",
            "🎯 Tactical Role Shortlists",
            "⚖️ All-Rounder Evaluation",
            "👑 Proposed RR Squad (25 Players)",
            "🌟 Emerging Talent Watchlist",
            "📋 Player Target Dossiers",
            "⚔️ Player Comparison Tool",
            "📖 Metrics & Methodology Glossary"
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Quick Player Lookup in Sidebar
    st.markdown("### 🔍 Global Player Search")
    all_player_names = sorted(comp_df['player_name'].unique().tolist())
    search_query = st.selectbox(
        "Select / Search Player by Name:",
        options=["-- Quick Search Player --"] + all_player_names,
        index=0
    )
    
    if search_query != "-- Quick Search Player --":
        p_row = comp_df[comp_df['player_name'] == search_query].iloc[0]
        st.markdown(f"""
            <div style="background: #1C2541; padding: 12px; border-radius: 8px; border: 1px solid #3A506B; margin-top: 10px;">
                <div style="font-weight: 700; color: #E73895;">{p_row['player_name']} <span style="color: #94A3B8; font-size: 0.8rem;">(ID: {p_row['player_id']})</span></div>
                <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 4px;">Role: <b>{p_row['assigned_role']}</b></div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Bat APR: <b>{p_row['batting_auction_index']:.1f}</b> ({p_row['bat_confidence_tier']})</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Bowl APR: <b>{p_row['bowling_auction_index']:.1f}</b> ({p_row['bowl_confidence_tier']})</div>
                <div style="font-size: 0.8rem; color: #FBBF24; margin-top: 4px;">Valuation: <b>{p_row['rr_auction_tier']}</b></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Official Governance Notice
    st.markdown("""
        <div style="font-size: 0.72rem; color: #64748B; line-height: 1.4;">
            <b>Analytical Governance:</b><br>
            All evaluations stem strictly from audited Phase 1–5 models. Does not invent auction purse, retention choices, or confirmed player availability.
        </div>
    """, unsafe_allow_html=True)


# Top Governance Banner for all views
st.markdown("""
    <div class="disclaimer-banner">
        <b>Rajasthan Royals IPL 2027 Auction Analytics Suite:</b> Management decision support dashboard built on audited Phase 5 squad construction datasets. Zero subjective adjustments or recalculations. Player IDs preserved as primary keys.
    </div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. SECTION A: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if nav_selection == "🏛️ Executive Overview":
    st.markdown("## 🏛️ Executive Recruitment Overview")
    st.markdown("High-level strategic briefing and squad construction architecture for Rajasthan Royals ahead of the IPL 2027 Mega-Auction.")
    
    # Top KPI Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-title">Total Evaluated</div>
                <div class="metric-card-value">958</div>
                <div class="metric-card-subtitle">888 Bat / 647 Bowl</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-title">Proposed RR Squad</div>
                <div class="metric-card-value">25</div>
                <div class="metric-card-subtitle">100% Unique Player IDs</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-title">Tactical Roles</div>
                <div class="metric-card-value">7 Units</div>
                <div class="metric-card-subtitle">6 Phase + 1 All-Rounder</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-title">Role Candidates</div>
                <div class="metric-card-value">879</div>
                <div class="metric-card-subtitle">Conjunctive Gate Filtered</div>
            </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-card-title">Emerging Watchlist</div>
                <div class="metric-card-value">67</div>
                <div class="metric-card-subtitle">Developmental Prospects</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Breakdown of Squad & Architecture
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        st.markdown("### 👑 25-Player Squad Composition by Category")
        category_counts = squad_df['squad_category'].value_counts().reset_index()
        category_counts.columns = ['Squad Category', 'Player Count']
        
        fig_cat = px.bar(
            category_counts,
            x='Squad Category',
            y='Player Count',
            color='Squad Category',
            text='Player Count',
            color_discrete_sequence=['#E73895', '#38BDF8', '#F59E0B', '#10B981', '#A855F7', '#EC4899', '#6366F1'],
            title="Squad Distribution across 7 Tactical Roles"
        )
        fig_cat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            showlegend=False,
            height=320,
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_right:
        st.markdown("### 🎯 Valuation Tier & Pathway Breakdown")
        tier_counts = squad_df['rr_auction_valuation_tier'].value_counts().reset_index()
        tier_counts.columns = ['Valuation Tier', 'Player Count']
        
        fig_tier = px.pie(
            tier_counts,
            values='Player Count',
            names='Valuation Tier',
            hole=0.45,
            color='Valuation Tier',
            color_discrete_map={
                'Tier 1: Priority RR Auction Target': '#E73895',
                'Tier 2: Core Squad Target': '#38BDF8',
                'Tier 3: Tactical / Backup Option': '#F59E0B',
                'Tier 4: Speculative / High-Risk': '#EF4444'
            },
            title="Squad Valuation Tier Distribution"
        )
        fig_tier.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            height=320,
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_tier, use_container_width=True)

    st.markdown("---")

    # Strategic Findings & Recruitment Pillars
    st.markdown("### 🏆 Core Strategic Recruitment Findings for Rajasthan Royals")
    
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
            <div style="background: #1C2541; padding: 18px; border-radius: 10px; border-left: 4px solid #E73895; margin-bottom: 12px;">
                <h4 style="color: #E73895; margin-top: 0;">1. Powerplay Firepower & Speculative Hedge</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0;">
                    <b>Ishan Kishan</b> (1262 PP BF, 106 p-BF, CRSS 85.72) and <b>Rohit Sharma</b> (1084 PP BF, 59 p-BF, CRSS 81.66) form an established, high-volume opening foundation. 
                    <b>Priyansh Arya</b> is explicitly recruited under the <i>Emerging / Speculative Pathway</i> (387 PP BF, 14 p-BF, CRSS 79.48). With an unverified pressure sample, he provides developmental upside without jeopardizing primary squad stability.
                </p>
            </div>
            
            <div style="background: #1C2541; padding: 18px; border-radius: 10px; border-left: 4px solid #38BDF8; margin-bottom: 12px;">
                <h4 style="color: #38BDF8; margin-top: 0;">2. Elite Middle-Order Anchors & Acceleration</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0;">
                    <b>Suryakumar Yadav</b> (CRSS 88.83, 457 p-BF) leads the middle-order, flanked by high-efficiency options <b>Mark Chapman</b> (CRSS 87.75), <b>Sameer Rizvi</b> (CRSS 86.63), and <b>Rishabh Pant</b> (CRSS 86.30), providing multi-phase versatility and left-right balance.
                </p>
            </div>
            
            <div style="background: #1C2541; padding: 18px; border-radius: 10px; border-left: 4px solid #10B981; margin-bottom: 12px;">
                <h4 style="color: #10B981; margin-top: 0;">3. Ice-Veined Death-Overs Finishing</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0;">
                    <b>Ashutosh Sharma</b> (CRSS 91.90, shrunk death SR 172.10) provides youthful finishing aggression alongside battle-tested legends <b>Dinesh Karthik</b> (CRSS 91.27) and <b>MS Dhoni</b> (CRSS 90.93), guaranteeing high strike rates in high-leverage closing overs.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
            <div style="background: #1C2541; padding: 18px; border-radius: 10px; border-left: 4px solid #F59E0B; margin-bottom: 12px;">
                <h4 style="color: #F59E0B; margin-top: 0;">4. Dual-Gated All-Rounder Discipline</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0;">
                    Dual 50:50 balance indices are strictly computed for players meeting both pressure sample thresholds: <b>Mohammad Nawaz</b> (CRSS 84.69) and <b>Sikandar Raza</b> (CRSS 83.72). 
                    <b>Naman Dhir</b> and <b>Nitish Rana</b> have insufficient pressure bowling samples (<18 LB), gating their balance index to NaN and preventing RR from over-valuing them as frontline bowlers.
                </p>
            </div>
            
            <div style="background: #1C2541; padding: 18px; border-radius: 10px; border-left: 4px solid #A855F7; margin-bottom: 12px;">
                <h4 style="color: #A855F7; margin-top: 0;">5. Phase-Specific Bowling Firepower</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0;">
                    <b>Powerplay:</b> Mohammed Shami (CRSS 84.87) & Shaheen Afridi (CRSS 84.61) provide early wicket-taking threat.<br>
                    <b>Middle Overs:</b> Sufiyan Muqeem (CRSS 95.77), Iftikhar Ahmed (CRSS 94.21), and Qais Ahmad (CRSS 93.47) enforce middle-phase chokehold.<br>
                    <b>Death Overs:</b> Mohammad Amir, Zawar Farid, Kane Richardson, and Zahoor Khan provide tactical yorker/death execution.
                </p>
            </div>
            
            <div style="background: #1C2541; padding: 18px; border-radius: 10px; border-left: 4px solid #EC4899; margin-bottom: 12px;">
                <h4 style="color: #EC4899; margin-top: 0;">6. Strict Empirical Bayes Shrinkage</h4>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0;">
                    Small sample sizes are shrunk aggressively toward population priors ($K_{bat}=50, K_{bowl}=36$). This mathematically protects RR from overpaying for noisy, low-volume anomalies.
                </p>
            </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. SECTION B: PRESSURE PERFORMANCE & APR
# -----------------------------------------------------------------------------
elif nav_selection == "⚡ Pressure Performance & APR":
    st.markdown("## ⚡ Pressure Performance Analytics & Auction Priority Rating")
    st.markdown("Audited evaluation of player resilience under pressure situations (rules B1–B5 for batting and P1–P4 for bowling), comparing pressure performance against baseline conditions.")

    tab1, tab2, tab3 = st.tabs(["🔥 Top 10 Pressure Batters", "🎯 Top 10 Pressure Bowlers", "📊 Pressure vs Normal Delta Distributions"])

    with tab1:
        st.markdown("### Top 10 Batters by Batting Auction Priority Rating (APR)")
        st.caption("Filtered for qualified batters with at least 20 pressure balls faced. Shrunk strike rate incorporates Empirical Bayes shrinkage toward the population prior (140.23).")
        
        top_bat = comp_df[comp_df['p_balls_faced'] >= 20].sort_values(
            by='batting_auction_index', ascending=False
        ).head(10)[['player_id', 'player_name', 'p_balls_faced', 'norm_balls_faced', 'p_strike_rate', 'norm_strike_rate', 'sr_delta', 'shrunk_p_strike_rate', 'bat_confidence_tier', 'batting_auction_index', 'rr_auction_tier']]
        
        # Display Plotly Bar Chart
        fig_top_bat = px.bar(
            top_bat,
            x='player_name',
            y='batting_auction_index',
            color='shrunk_p_strike_rate',
            text='shrunk_p_strike_rate',
            color_continuous_scale='Reds',
            labels={'batting_auction_index': 'Batting APR (0-100)', 'shrunk_p_strike_rate': 'Shrunk P-SR', 'player_name': 'Player'},
            title="Top 10 Batting APR Leaders (with Shrunk Pressure Strike Rate)"
        )
        fig_top_bat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            height=340
        )
        st.plotly_chart(fig_top_bat, use_container_width=True)
        
        # Formatted Data Table
        st.dataframe(
            top_bat.style.format({
                'p_balls_faced': '{:.0f}',
                'norm_balls_faced': '{:.0f}',
                'p_strike_rate': '{:.2f}',
                'norm_strike_rate': '{:.2f}',
                'sr_delta': '{:+.2f}',
                'shrunk_p_strike_rate': '{:.2f}',
                'batting_auction_index': '{:.2f}'
            }),
            use_container_width=True
        )

    with tab2:
        st.markdown("### Top 10 Bowlers by Bowling Auction Priority Rating (APR)")
        st.caption("Filtered for qualified bowlers with at least 18 pressure legal balls. Shrunk economy incorporates Empirical Bayes shrinkage toward the population prior (8.88).")
        
        top_bowl = comp_df[comp_df['p_legal_balls'] >= 18].sort_values(
            by='bowling_auction_index', ascending=False
        ).head(10)[['player_id', 'player_name', 'p_legal_balls', 'norm_legal_balls', 'p_economy', 'norm_economy', 'econ_delta', 'shrunk_p_economy', 'bowl_confidence_tier', 'bowling_auction_index', 'rr_auction_tier']]
        
        # Display Plotly Bar Chart
        fig_top_bowl = px.bar(
            top_bowl,
            x='player_name',
            y='bowling_auction_index',
            color='shrunk_p_economy',
            text='shrunk_p_economy',
            color_continuous_scale='Blues_r',
            labels={'bowling_auction_index': 'Bowling APR (0-100)', 'shrunk_p_economy': 'Shrunk P-Econ', 'player_name': 'Player'},
            title="Top 10 Bowling APR Leaders (with Shrunk Pressure Economy Rate)"
        )
        fig_top_bowl.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            height=340
        )
        st.plotly_chart(fig_top_bowl, use_container_width=True)
        
        # Formatted Data Table
        st.dataframe(
            top_bowl.style.format({
                'p_legal_balls': '{:.0f}',
                'norm_legal_balls': '{:.0f}',
                'p_economy': '{:.2f}',
                'norm_economy': '{:.2f}',
                'econ_delta': '{:+.2f}',
                'shrunk_p_economy': '{:.2f}',
                'bowling_auction_index': '{:.2f}'
            }),
            use_container_width=True
        )

    with tab3:
        st.markdown("### 📈 Comparative Distributions: Normal vs Pressure Performance")
        
        c_left, c_right = st.columns(2)
        
        with c_left:
            st.markdown("#### Batting Strike Rate: Normal vs Pressure")
            valid_bat_comp = comp_df[comp_df['p_balls_faced'] >= 20].copy()
            fig_scat_bat = px.scatter(
                valid_bat_comp,
                x='norm_strike_rate',
                y='p_strike_rate',
                color='bat_confidence_tier',
                size='p_balls_faced',
                hover_data=['player_name', 'sr_delta', 'batting_auction_index'],
                color_discrete_map={
                    'High (100+)': '#10B981',
                    'Medium (50-99)': '#38BDF8',
                    'Low (20-49)': '#F59E0B',
                    'Insufficient (<20)': '#EF4444'
                },
                labels={'norm_strike_rate': 'Normal Strike Rate', 'p_strike_rate': 'Pressure Strike Rate'},
                title="Batting Resilience: Above Line = Outperforms Under Pressure"
            )
            # Add y=x line
            fig_scat_bat.add_shape(type='line', x0=80, y0=80, x1=220, y1=220, line=dict(color='#E73895', dash='dash'))
            fig_scat_bat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=380)
            st.plotly_chart(fig_scat_bat, use_container_width=True)

        with c_right:
            st.markdown("#### Bowling Economy: Normal vs Pressure")
            valid_bowl_comp = comp_df[comp_df['p_legal_balls'] >= 18].copy()
            fig_scat_bowl = px.scatter(
                valid_bowl_comp,
                x='norm_economy',
                y='p_economy',
                color='bowl_confidence_tier',
                size='p_legal_balls',
                hover_data=['player_name', 'econ_delta', 'bowling_auction_index'],
                color_discrete_map={
                    'High (75+)': '#10B981',
                    'Medium (36-74)': '#38BDF8',
                    'Low (18-35)': '#F59E0B',
                    'Insufficient (<18)': '#EF4444'
                },
                labels={'norm_economy': 'Normal Economy', 'p_economy': 'Pressure Economy'},
                title="Bowling Resilience: Below Line = Clamps Down Under Pressure"
            )
            # Add y=x line
            fig_scat_bowl.add_shape(type='line', x0=4, y0=4, x1=14, y1=14, line=dict(color='#E73895', dash='dash'))
            fig_scat_bowl.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=380)
            st.plotly_chart(fig_scat_bowl, use_container_width=True)


# -----------------------------------------------------------------------------
# 6. SECTION C: ROLE-BASED RECRUITMENT SHORTLISTS
# -----------------------------------------------------------------------------
elif nav_selection == "🎯 Tactical Role Shortlists":
    st.markdown("## 🎯 Role-Based Recruitment Shortlists")
    st.markdown(r"Audited shortlists filtered strictly by conjunctive volume gates: Tactical-phase volume **AND** pressure-sample volume **AND** $\ge 3$ distinct matches. Ranked by Composite Role Suitability Score (CRSS).")

    # Archetype selector
    archetypes = [
        "Powerplay Batters",
        "Middle-Order Batters",
        "Death-Overs Finishers",
        "Powerplay Bowlers",
        "Middle-Overs Bowlers",
        "Death-Overs Bowlers"
    ]
    
    col_arch, col_conf, col_mat = st.columns([1.5, 1, 1])
    with col_arch:
        selected_arch = st.selectbox("Select Tactical Archetype:", archetypes, index=0)
    with col_conf:
        conf_filter = st.multiselect(
            "Confidence Tier Filter:",
            options=["High (100+)", "High (75+)", "Medium (50-99)", "Medium (36-74)", "Low (20-49)", "Low (18-35)"],
            default=["High (100+)", "High (75+)", "Medium (50-99)", "Medium (36-74)"]
        )
    with col_mat:
        min_matches = st.slider("Min Distinct Matches:", min_value=3, max_value=100, value=5, step=1)

    # Filter shortlist
    filtered_sl = shortlist_df[
        (shortlist_df['tactical_archetype'] == selected_arch) &
        (shortlist_df['distinct_matches_played'] >= min_matches)
    ]
    if conf_filter:
        filtered_sl = filtered_sl[filtered_sl['confidence_tier'].isin(conf_filter)]

    st.markdown(f"**Found {len(filtered_sl)} qualified candidates** matching criteria for **{selected_arch}**:")

    # Top candidates chart
    top_arch_chart = filtered_sl.sort_values(by='composite_role_suitability_score', ascending=False).head(15)
    if not top_arch_chart.empty:
        fig_arch = px.bar(
            top_arch_chart,
            x='player_name',
            y='composite_role_suitability_score',
            color='confidence_tier',
            text='composite_role_suitability_score',
            labels={'composite_role_suitability_score': 'CRSS (0-100)', 'player_name': 'Candidate'},
            title=f"Top 15 {selected_arch} by Composite Role Suitability Score (CRSS)"
        )
        fig_arch.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=330)
        st.plotly_chart(fig_arch, use_container_width=True)

    # Display Candidates Table
    display_cols = [
        'player_id', 'player_name', 'distinct_matches_played', 'phase_balls', 
        'pressure_sample_size', 'confidence_tier', 'phase_exposure_share', 
        'phase_specific_metric', 'stored_apr', 'composite_role_suitability_score', 'rr_auction_valuation_tier'
    ]
    st.dataframe(
        filtered_sl[display_cols].sort_values(by='composite_role_suitability_score', ascending=False).style.format({
            'distinct_matches_played': '{:.0f}',
            'phase_balls': '{:.0f}',
            'pressure_sample_size': '{:.0f}',
            'phase_exposure_share': '{:.1%}',
            'phase_specific_metric': '{:.2f}',
            'stored_apr': '{:.2f}',
            'composite_role_suitability_score': '{:.2f}'
        }),
        use_container_width=True
    )


# -----------------------------------------------------------------------------
# 7. SECTION D: ALL-ROUNDER EVALUATION
# -----------------------------------------------------------------------------
elif nav_selection == "⚖️ All-Rounder Evaluation":
    st.markdown("## ⚖️ All-Rounder Evaluation & Dual-Gating Matrix")
    st.markdown(r"Exhaustive evaluation of all 958 players across the audited 4-tier taxonomy. A composite 50:50 balance index is computed **exclusively** for players satisfying dual-discipline pressure sample criteria ($N_{\text{p\_bf}} \ge 20$ AND $N_{\text{p\_lb}} \ge 18$).")

    # Taxonomy Count Cards
    ar_counts = ar_df['all_rounder_category'].value_counts()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Genuine All-Rounders</div>
                <div class="metric-card-value">{ar_counts.get('Genuine All-Rounder', 0)}</div>
                <div class="metric-card-subtitle">Both Disciplines >= 250 Balls</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Batting All-Rounders</div>
                <div class="metric-card-value">{ar_counts.get('Batting All-Rounder', 0)}</div>
                <div class="metric-card-subtitle">Bat >= 250, Bowl >= 90 Balls</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Bowling All-Rounders</div>
                <div class="metric-card-value">{ar_counts.get('Bowling All-Rounder', 0)}</div>
                <div class="metric-card-subtitle">Bowl >= 250, Bat >= 80 Balls</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Dual Eligible for Balance</div>
                <div class="metric-card-value">{(ar_df['dual_gating_status'] == 'Eligible Dual Profile').sum()}</div>
                <div class="metric-card-subtitle">p-Bat >= 20 & p-Bowl >= 18</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # All-Rounder Scatter Plot: Batting APR vs Bowling APR
    st.markdown("### 🎯 All-Rounder Quadrant Analysis: Batting APR vs Bowling APR")
    st.caption("Players with dual gating status 'Eligible Dual Profile' qualify for the balanced 50:50 composite index. Single-discipline profiles are strictly gated to specialist valuation.")
    
    ar_plot_df = ar_df[ar_df['all_rounder_category'] != 'Unclassified / Specialist'].copy()
    
    fig_ar = px.scatter(
        ar_plot_df,
        x='stored_bowling_apr',
        y='stored_batting_apr',
        color='dual_gating_status',
        size='distinct_matches_played',
        hover_data=['player_name', 'all_rounder_category', 'gated_balance_index', 'career_balls_faced', 'career_legal_balls'],
        color_discrete_map={
            'Eligible Dual Profile': '#10B981',
            'Ineligible Dual Sample (<20 bat or <18 bowl pressure balls)': '#EF4444'
        },
        labels={'stored_bowling_apr': 'Bowling APR (0-100)', 'stored_batting_apr': 'Batting APR (0-100)'},
        title="All-Rounder Quadrants: High Batting & High Bowling Priority"
    )
    # Add 50-50 quadrant lines
    fig_ar.add_hline(y=50, line=dict(color='#94A3B8', dash='dash'))
    fig_ar.add_vline(x=50, line=dict(color='#94A3B8', dash='dash'))
    fig_ar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=400)
    st.plotly_chart(fig_ar, use_container_width=True)

    # Filterable All-Rounders Table
    st.markdown("### 📋 All-Rounder Candidate Registry")
    selected_ar_cat = st.multiselect(
        "Filter by Taxonomy Category:",
        options=ar_df['all_rounder_category'].unique().tolist(),
        default=['Genuine All-Rounder', 'Batting All-Rounder', 'Bowling All-Rounder']
    )
    
    filtered_ar = ar_df[ar_df['all_rounder_category'].isin(selected_ar_cat)]
    st.dataframe(
        filtered_ar[[
            'player_id', 'player_name', 'all_rounder_category', 'distinct_matches_played',
            'career_balls_faced', 'career_legal_balls', 'pressure_balls_faced', 'pressure_legal_balls',
            'stored_batting_apr', 'stored_bowling_apr', 'gated_balance_index', 'dual_gating_status', 'rr_auction_tier'
        ]].sort_values(by='gated_balance_index', ascending=False, na_position='last').style.format({
            'career_balls_faced': '{:.0f}',
            'career_legal_balls': '{:.0f}',
            'pressure_balls_faced': '{:.0f}',
            'pressure_legal_balls': '{:.0f}',
            'stored_batting_apr': '{:.2f}',
            'stored_bowling_apr': '{:.2f}',
            'gated_balance_index': lambda x: f"{x:.2f}" if pd.notnull(x) else "Gated (NaN)"
        }),
        use_container_width=True
    )



# -----------------------------------------------------------------------------
# 8. SECTION E: PROPOSED RAJASTHAN ROYALS SQUAD
# -----------------------------------------------------------------------------
elif nav_selection == "👑 Proposed RR Squad (25 Players)":

    st.markdown("## 👑 Proposed Rajasthan Royals IPL 2027 Squad (25 Players)")
    st.markdown(
        "The official analytical squad recommendation comprising "
        "**exactly 25 unique player IDs** across seven tactical squad categories. "
        "Fully audited for volume, sample risk, and qualification pathways."
    )

    # Category quick-filter
    cat_options = ["All 25 Players"] + squad_df['squad_category'].unique().tolist()

    filter_sq_cat = st.selectbox(
        "Filter Squad by Tactical Category:",
        cat_options,
        index=0
    )

    display_squad = (
        squad_df
        if filter_sq_cat == "All 25 Players"
        else squad_df[squad_df['squad_category'] == filter_sq_cat]
    )

    # Squad Table
    st.markdown(f"**Displaying {len(display_squad)} Players:**")

    def safe_float_format(value):
        if pd.isna(value):
            return "—"

        try:
            return f"{float(value):.2f}"
        except (ValueError, TypeError):
            return str(value)

    squad_display = display_squad[[
        'squad_slot_number',
        'player_id',
        'player_name',
        'squad_category',
        'primary_squad_role',
        'qualification_pathway',
        'distinct_matches_played',
        'tactical_phase_balls',
        'pressure_sample_size',
        'confidence_tier',
        'phase_metric_value',
        'phase_metric_name',
        'shrunk_pressure_metric',
        'stored_apr',
        'composite_role_suitability_score',
        'rr_auction_valuation_tier',
        'sample_risk_interpretation'
    ]].sort_values(by='squad_slot_number')

    st.dataframe(
        squad_display.style.format({
            'phase_metric_value': safe_float_format,
            'shrunk_pressure_metric': safe_float_format,
            'stored_apr': safe_float_format,
            'composite_role_suitability_score': safe_float_format
        }),
        use_container_width=True
    )

    st.markdown("---")

    # Highlight on Speculative & Single-Discipline Exceptions
    st.markdown("### ⚠️ Audited Exceptions & Management Risk Flags")

    e1, e2 = st.columns(2)

    with e1:
        st.markdown("""
            <div style="background: #1C2541; padding: 16px; border-radius: 10px; border-left: 4px solid #EF4444;">
                <h4 style="color: #EF4444; margin-top: 0;">Priyansh Arya (Slot 3 — Powerplay Batter)</h4>
                <div style="font-size: 0.85rem; color: #CBD5E1;">
                    <b>Pathway:</b> Emerging / Speculative Pathway Exception<br>
                    <b>Tactical Phase Volume:</b> 387 Balls Faced (PP SR 192.99)<br>
                    <b>Pressure Sample Size:</b> 14 Balls Faced (<20 Threshold)<br>
                    <b>Valuation Tier:</b> Tier 4: Speculative / High-Risk<br>
                    <b>Management Directive:</b> Acquired strictly as a high-upside developmental asset. Must not be budgeted or counted upon as a guaranteed primary tournament starter.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown("""
            <div style="background: #1C2541; padding: 16px; border-radius: 10px; border-left: 4px solid #F59E0B;">
                <h4 style="color: #F59E0B; margin-top: 0;">Naman Dhir (Slot 11) & Nitish Rana (Slot 12)</h4>
                <div style="font-size: 0.85rem; color: #CBD5E1;">
                    <b>Pathway:</b> Single-Discipline All-Rounder (Career Volume Qualified)<br>
                    <b>Bowling Pressure Sample:</b> Dhir (6 LB), Rana (11 LB) (<18 Threshold)<br>
                    <b>Dual Gating Consequence:</b> 50:50 Balance Index = NaN<br>
                    <b>Valuation Tier:</b> Tier 2/3 Specialist Execution<br>
                    <b>Management Directive:</b> Value and deploy purely as batting specialists with incidental part-time spin utility. Do NOT treat as frontline 4-over bowling options.
                </div>
            </div>
        """, unsafe_allow_html=True)



# -----------------------------------------------------------------------------
# 9. SECTION F: EMERGING TALENT WATCHLIST
# -----------------------------------------------------------------------------
elif nav_selection == "🌟 Emerging Talent Watchlist":
    st.markdown("## 🌟 Emerging Talent Watchlist (67 Candidates)")
    st.markdown("High-upside developmental prospects identified through extreme phase volume or efficiency. **Strictly disjoint from the primary shortlist** (zero overlap).")

    st.markdown("""
        <div style="background: #1C2541; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #F59E0B; margin-bottom: 16px; font-size: 0.85rem; color: #CBD5E1;">
            <b>Developmental Recruitment Notice:</b> These 67 prospects exhibit intriguing domestic or phase flashes but possess small pressure sample sizes (<20 bat or <18 bowl) or limited multi-match exposure. They represent cost-effective developmental / net-bowler / replacement targets.
        </div>
    """, unsafe_allow_html=True)

    # Watchlist Archetype Breakdown
    wl_arch_counts = watchlist_df['tactical_archetype'].value_counts().reset_index()
    wl_arch_counts.columns = ['Tactical Archetype', 'Prospect Count']
    
    fig_wl = px.bar(
        wl_arch_counts,
        x='Tactical Archetype',
        y='Prospect Count',
        color='Tactical Archetype',
        text='Prospect Count',
        title="Emerging Talent Pool by Tactical Archetype"
    )
    fig_wl.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=300, showlegend=False)
    st.plotly_chart(fig_wl, use_container_width=True)

    # Table of Watchlist
    st.dataframe(
        watchlist_df[[
            'player_id', 'player_name', 'tactical_archetype', 'distinct_matches_played',
            'phase_balls', 'pressure_sample_size', 'confidence_tier', 'phase_exposure_share',
            'phase_specific_metric', 'composite_role_suitability_score', 'rr_auction_valuation_tier'
        ]].sort_values(by='composite_role_suitability_score', ascending=False).style.format({
            'distinct_matches_played': '{:.0f}',
            'phase_balls': '{:.0f}',
            'pressure_sample_size': '{:.0f}',
            'phase_exposure_share': '{:.1%}',
            'phase_specific_metric': '{:.2f}',
            'composite_role_suitability_score': '{:.2f}'
        }),
        use_container_width=True
    )


# -----------------------------------------------------------------------------
# 10. SECTION G: PLAYER TARGET DOSSIERS
# -----------------------------------------------------------------------------
elif nav_selection == "📋 Player Target Dossiers":
    st.markdown("## 📋 Priority Target Dossiers (Top 30 Candidates)")
    st.markdown("Multi-format scouting breakdowns across **IPL**, **Other Domestic T20**, and **International T20I** competitions, incorporating score uncertainty flags and valuation bands.")

    # Dossier Player Selector
    dossier_players = dossier_df['player_name'].tolist()
    selected_target = st.selectbox("Select Priority Target Dossier to Inspect:", dossier_players, index=0)
    
    target_data = dossier_df[dossier_df['player_name'] == selected_target].iloc[0]
    
    # Target Header Cards
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1C2541 0%, #151D36 100%); padding: 20px; border-radius: 12px; border: 1px solid #3A506B; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="color: #FFFFFF; margin: 0;">{target_data['player_name']} <span style="font-size: 1rem; color: #94A3B8;">(ID: {target_data['player_id']})</span></h2>
                    <div style="margin-top: 6px;">
                        <span class="badge badge-pink">{target_data['assigned_role']}</span>
                        <span class="badge badge-blue">{target_data['distinct_matches_played']} Distinct Matches</span>
                        <span class="badge badge-gold">{target_data['rr_auction_valuation_tier']}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.85rem; color: #94A3B8;">BATTING / BOWLING APR</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #38BDF8;">{target_data['batting_auction_index']:.1f} <span style="color: #94A3B8; font-size: 1.2rem;">/</span> {target_data['bowling_auction_index']:.1f}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3-Way Format Breakdown Cards
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Indian Premier League (IPL)</div>
                <div class="metric-card-value">{target_data['ipl_batting_sr']} <span style="font-size: 0.9rem; color: #94A3B8;">SR</span></div>
                <div class="metric-card-subtitle">Bowling Econ: {target_data['ipl_bowling_econ']} | Exp: {'✅ Yes' if target_data['has_ipl_experience'] else '❌ No'}</div>
            </div>
        """, unsafe_allow_html=True)
    with f_col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Other Domestic T20</div>
                <div class="metric-card-value">{target_data['other_dom_batting_sr']} <span style="font-size: 0.9rem; color: #94A3B8;">SR</span></div>
                <div class="metric-card-subtitle">Bowling Econ: {target_data['other_dom_bowling_econ']} | Exp: {'✅ Yes' if target_data['has_other_domestic_experience'] else '❌ No'}</div>
            </div>
        """, unsafe_allow_html=True)
    with f_col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">International T20I</div>
                <div class="metric-card-value">{target_data['t20i_batting_sr']} <span style="font-size: 0.9rem; color: #94A3B8;">SR</span></div>
                <div class="metric-card-subtitle">Bowling Econ: {target_data['t20i_bowling_econ']} | Exp: {'✅ Yes' if target_data['has_t20i_experience'] else '❌ No'}</div>
            </div>
        """, unsafe_allow_html=True)

    # Score Uncertainty & Sample Metrics
    st.markdown("### 📊 Pressure Metric Accounting & Score Uncertainty")
    u1, u2, u3, u4 = st.columns(4)
    with u1:
        st.metric("Pressure Balls Faced", f"{target_data['p_balls_faced']:.0f} BF", f"Total: {target_data['total_balls_faced']:.0f} BF")
    with u2:
        st.metric("Shrunk Pressure SR", f"{target_data['shrunk_p_strike_rate']:.2f}", f"Uncertainty: {target_data['bat_score_uncertainty_share']}")
    with u3:
        st.metric("Pressure Legal Balls", f"{target_data['p_legal_balls']:.0f} LB", f"Total: {target_data['total_legal_balls']:.0f} LB")
    with u4:
        st.metric("Shrunk Pressure Econ", f"{target_data['shrunk_p_economy']:.2f}", f"Uncertainty: {target_data['bowl_score_uncertainty_share']}")

    st.markdown("---")
    
    # Full Top 30 Registry Table
    st.markdown("### 📋 Complete Top 30 Dossier Summary Table")
    st.dataframe(
        dossier_df[[
            'player_id', 'player_name', 'assigned_role', 'distinct_matches_played',
            'has_ipl_experience', 'has_other_domestic_experience', 'has_t20i_experience',
            'p_balls_faced', 'shrunk_p_strike_rate', 'p_legal_balls', 'shrunk_p_economy',
            'batting_auction_index', 'bowling_auction_index', 'rr_auction_valuation_tier'
        ]].style.format({
            'distinct_matches_played': '{:.0f}',
            'p_balls_faced': '{:.0f}',
            'shrunk_p_strike_rate': '{:.2f}',
            'p_legal_balls': '{:.0f}',
            'shrunk_p_economy': '{:.2f}',
            'batting_auction_index': '{:.2f}',
            'bowling_auction_index': '{:.2f}'
        }),
        use_container_width=True
    )


# -----------------------------------------------------------------------------
# 11. SECTION H: SIDE-BY-SIDE PLAYER COMPARISON TOOL
# -----------------------------------------------------------------------------
elif nav_selection == "⚔️ Player Comparison Tool":
    st.markdown("## ⚔️ Head-to-Head Player Comparison Engine")
    st.markdown("Compare any two players side-by-side across career volume, pressure sample size, empirical Bayes metrics, confidence tiers, and auction valuation tiers.")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        player_a_name = st.selectbox("Select Player A:", options=all_player_names, index=all_player_names.index("Ishan Kishan") if "Ishan Kishan" in all_player_names else 0)
    with col_p2:
        player_b_name = st.selectbox("Select Player B:", options=all_player_names, index=all_player_names.index("Rohit Sharma") if "Rohit Sharma" in all_player_names else 1)

    pA = comp_df[comp_df['player_name'] == player_a_name].iloc[0]
    pB = comp_df[comp_df['player_name'] == player_b_name].iloc[0]

    # Side-by-Side Comparison Columns
    col_card_A, col_card_B = st.columns(2)
    
    with col_card_A:
        st.markdown(f"""
            <div style="background: #1C2541; padding: 20px; border-radius: 12px; border-top: 4px solid #E73895;">
                <h3 style="color: #E73895; margin: 0;">{pA['player_name']} <span style="font-size: 0.85rem; color: #94A3B8;">(ID: {pA['player_id']})</span></h3>
                <div style="font-size: 0.85rem; color: #38BDF8; font-weight: 600; margin-top: 4px;">Role: {pA['assigned_role']}</div>
                <div style="margin-top: 10px;">
                    <span class="badge badge-pink">Bat APR: {pA['batting_auction_index']:.1f}</span>
                    <span class="badge badge-blue">Bowl APR: {pA['bowling_auction_index']:.1f}</span>
                    <span class="badge badge-gold">{pA['rr_auction_tier']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_card_B:
        st.markdown(f"""
            <div style="background: #1C2541; padding: 20px; border-radius: 12px; border-top: 4px solid #38BDF8;">
                <h3 style="color: #38BDF8; margin: 0;">{pB['player_name']} <span style="font-size: 0.85rem; color: #94A3B8;">(ID: {pB['player_id']})</span></h3>
                <div style="font-size: 0.85rem; color: #E73895; font-weight: 600; margin-top: 4px;">Role: {pB['assigned_role']}</div>
                <div style="margin-top: 10px;">
                    <span class="badge badge-blue">Bat APR: {pB['batting_auction_index']:.1f}</span>
                    <span class="badge badge-pink">Bowl APR: {pB['bowling_auction_index']:.1f}</span>
                    <span class="badge badge-gold">{pB['rr_auction_tier']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed Metric Comparison Table
    st.markdown("### 📊 Side-by-Side Metric Decomposition")
    
    comp_metrics = [
        ("Discipline / Role", pA['assigned_role'], pB['assigned_role']),
        ("Batting Confidence Tier", pA['bat_confidence_tier'], pB['bat_confidence_tier']),
        ("Pressure Balls Faced", f"{pA['p_balls_faced']:.0f} BF", f"{pB['p_balls_faced']:.0f} BF"),
        ("Normal Balls Faced", f"{pA['norm_balls_faced']:.0f} BF", f"{pB['norm_balls_faced']:.0f} BF"),
        ("Pressure Strike Rate", f"{pA['p_strike_rate']:.2f}", f"{pB['p_strike_rate']:.2f}"),
        ("Normal Strike Rate", f"{pA['norm_strike_rate']:.2f}", f"{pB['norm_strike_rate']:.2f}"),
        ("Strike Rate Delta (P - N)", f"{pA['sr_delta']:+.2f}", f"{pB['sr_delta']:+.2f}"),
        ("Shrunk Pressure Strike Rate", f"{pA['shrunk_p_strike_rate']:.2f}", f"{pB['shrunk_p_strike_rate']:.2f}"),
        ("Batting Auction Index (APR)", f"{pA['batting_auction_index']:.2f}", f"{pB['batting_auction_index']:.2f}"),
        ("Bowling Confidence Tier", pA['bowl_confidence_tier'], pB['bowl_confidence_tier']),
        ("Pressure Legal Balls", f"{pA['p_legal_balls']:.0f} LB", f"{pB['p_legal_balls']:.0f} LB"),
        ("Normal Legal Balls", f"{pA['norm_legal_balls']:.0f} LB", f"{pB['norm_legal_balls']:.0f} LB"),
        ("Pressure Economy Rate", f"{pA['p_economy']:.2f}" if pd.notnull(pA['p_economy']) else "N/A", f"{pB['p_economy']:.2f}" if pd.notnull(pB['p_economy']) else "N/A"),
        ("Normal Economy Rate", f"{pA['norm_economy']:.2f}" if pd.notnull(pA['norm_economy']) else "N/A", f"{pB['norm_economy']:.2f}" if pd.notnull(pB['norm_economy']) else "N/A"),
        ("Economy Delta (P - N)", f"{pA['econ_delta']:+.2f}" if pd.notnull(pA['econ_delta']) else "N/A", f"{pB['econ_delta']:+.2f}" if pd.notnull(pB['econ_delta']) else "N/A"),
        ("Shrunk Pressure Economy", f"{pA['shrunk_p_economy']:.2f}" if pd.notnull(pA['shrunk_p_economy']) else "N/A", f"{pB['shrunk_p_economy']:.2f}" if pd.notnull(pB['shrunk_p_economy']) else "N/A"),
        ("Bowling Auction Index (APR)", f"{pA['bowling_auction_index']:.2f}", f"{pB['bowling_auction_index']:.2f}"),
        ("Final Auction Valuation Tier", pA['rr_auction_tier'], pB['rr_auction_tier'])
    ]
    
    df_compare = pd.DataFrame(comp_metrics, columns=["Evaluation Metric", f"Player A: {player_a_name}", f"Player B: {player_b_name}"])
    st.table(df_compare)

    # Comparison Radar / Bar Chart
    radar_categories = ['Bat APR', 'Bowl APR', 'Shrunk P-SR (Norm)', 'Shrunk P-Econ (Norm)']
    
    # Normalized scores for visualization
    val_a_bat_sr = min(max((pA['shrunk_p_strike_rate'] - 100) / 100 * 100, 0), 100) if pd.notnull(pA['shrunk_p_strike_rate']) else 0
    val_b_bat_sr = min(max((pB['shrunk_p_strike_rate'] - 100) / 100 * 100, 0), 100) if pd.notnull(pB['shrunk_p_strike_rate']) else 0
    
    val_a_bowl_ec = min(max((12 - pA['shrunk_p_economy']) / 6 * 100, 0), 100) if pd.notnull(pA['shrunk_p_economy']) else 0
    val_b_bowl_ec = min(max((12 - pB['shrunk_p_economy']) / 6 * 100, 0), 100) if pd.notnull(pB['shrunk_p_economy']) else 0
    
    fig_comp_bar = go.Figure()
    fig_comp_bar.add_trace(go.Bar(
        x=radar_categories,
        y=[pA['batting_auction_index'], pA['bowling_auction_index'], val_a_bat_sr, val_a_bowl_ec],
        name=player_a_name,
        marker_color='#E73895'
    ))
    fig_comp_bar.add_trace(go.Bar(
        x=radar_categories,
        y=[pB['batting_auction_index'], pB['bowling_auction_index'], val_b_bat_sr, val_b_bowl_ec],
        name=player_b_name,
        marker_color='#38BDF8'
    ))
    fig_comp_bar.update_layout(
        barmode='group',
        title="Comparative Priority Index & Efficiency Profile",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC'),
        height=350
    )
    st.plotly_chart(fig_comp_bar, use_container_width=True)


# -----------------------------------------------------------------------------
# 12. SECTION I: METRICS & METHODOLOGY GLOSSARY
# -----------------------------------------------------------------------------
elif nav_selection == "📖 Metrics & Methodology Glossary":
    st.markdown("## 📖 Metrics & Analytical Methodology Glossary")
    st.markdown("Complete mathematical documentation of the audited metrics, pressure classification rules, and shrinkage formulations.")

    with st.expander("⚡ Phase 3 Pressure Classification Rules (B1–B5 & P1–P4)", expanded=True):
        st.markdown(r"""
            **Batting Pressure Rules (B1–B5):**
            - **B1 (Death Overs Leverage):** Match Phase = Death Overs (Overs 16–20) AND Required Run Rate $\ge 9.0$ (2nd innings) OR Current Run Rate $< 7.5$ (1st innings).
            - **B2 (Collapse Management):** Wickets Fallen $\ge 3$ within the first 6 overs (Powerplay collapse).
            - **B3 (Chasing Escalation):** 2nd Innings, Balls Remaining $< 36$ AND Required Run Rate $\ge 10.0$.
            - **B4 (Wicket Cascade):** 2 wickets lost in the preceding 12 legal deliveries.
            - **B5 (High-Leverage Match Context):** Tournament knockout/playoff matches or final-over finishes (Balls remaining $\le 6$, margin $\le 12$ runs).
            
            **Bowling Pressure Rules (P1–P4):**
            - **P1 (Powerplay Restriction Defense):** Overs 1–6 with fielding restrictions active.
            - **P2 (Death Overs Defense):** Overs 16–20 with batting team accelerating.
            - **P3 (Defending Low Totals):** Defending target $< 150$ with opposition Required Run Rate $< 7.5$.
            - **P4 (High Boundary Concession Recovery):** Bowling immediately after conceding consecutive boundaries in the over.
        """)

    with st.expander("📉 Empirical Bayes Shrinkage Formulations", expanded=False):
        st.markdown(r"""
            To prevent small sample distortion, player metrics are shrunk toward empirical population priors:
            
            $$\text{Shrunk Metric} = w_i \cdot \bar{x}_i + (1 - w_i) \cdot \mu_{\text{prior}}$$
            
            Where the shrinkage weight $w_i$ is governed by discipline-specific constants ($K_{bat}=50, K_{bowl}=36$):
            
            $$w_{bat, i} = \frac{N_{p\_bf, i}}{N_{p\_bf, i} + 50}, \quad w_{bowl, i} = \frac{N_{p\_lb, i}}{N_{p\_lb, i} + 36}$$
            
            - **Batting Population Prior ($\mu_{bat}$):** 140.23 Strike Rate
            - **Bowling Population Prior ($\mu_{bowl}$):** 8.88 Economy Rate
        """)

    with st.expander("🎯 Composite Role Suitability Score (CRSS) Formulation", expanded=False):
        st.markdown(r"""
            The CRSS (0–100) measures candidate suitability for a specific tactical phase:
            
            $$\text{CRSS} = 0.40 \cdot \text{APR}_{\text{stored}} + 0.35 \cdot \text{Metric}_{\text{phase, norm}} + 0.25 \cdot \text{Exposure}_{\text{phase, norm}}$$
            
            - **$\text{APR}_{\text{stored}}$:** Pre-computed Auction Priority Rating (incorporating confidence).
            - **$\text{Metric}_{\text{phase, norm}}$:** Normalized phase-specific metric (Powerplay/Middle/Death SR for batters; Economy for bowlers).
            - **$\text{Exposure}_{\text{phase, norm}}$:** Share of player's total deliveries bowled/faced within that specific match phase.
        """)

    with st.expander("⚖️ All-Rounder 50:50 Dual-Gating Formulation", expanded=False):
        st.markdown(r"""
            Dual-discipline balance evaluation requires verified samples in both disciplines:
            
            $$\text{Balance Index} = \begin{cases} 
            0.50 \cdot \text{APR}_{bat} + 0.50 \cdot \text{APR}_{bowl} & \text{if } N_{p\_bf} \ge 20 \text{ AND } N_{p\_lb} \ge 18 \\ 
            \text{NaN} & \text{otherwise (Gated to Single-Discipline)}
            \end{cases}$$
            
            This mathematical gate prevents Rajasthan Royals from valuing part-time bowlers as frontline bowling all-rounders.
        """)
