import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import data_processor
import skill_grouper

st.set_page_config(page_title="Skill Extractor & Analyzer Dashboard", layout="wide")
st.title("Skill Extractor & Analyzer Dashboard")

# Layout Configuration
st.sidebar.header("Configuration")
threshold = st.sidebar.slider("Skill Frequency Threshold", min_value=1, max_value=20, value=3)

@st.cache_data
def load_data():
    return data_processor.process_logs("activity_log.csv")

skill_counts = load_data()
grouped_data = skill_grouper.group_skills(skill_counts, threshold)

general_skills = grouped_data['general_skills']
merged_skills = grouped_data['merged_skills']

total_xp = sum([g['experience_points'] for g in general_skills])
total_gen = len(general_skills)
total_specific = sum([len(g['specific_skills']) for g in general_skills])

# KPIs
st.markdown("### Experience Points Overview")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Experience Points", total_xp)
kpi2.metric("General Skills Detected", total_gen)
kpi3.metric("Specific Skills Above Threshold", total_specific)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Experience Points Distribution")
    df_bar = pd.DataFrame([{
        "General Skill": g["skill"],
        "Experience Points": g["experience_points"]
    } for g in general_skills])
    
    if not df_bar.empty:
        df_bar = df_bar.sort_values(by="Experience Points", ascending=False)
        fig_bar = px.bar(df_bar, x="Experience Points", y="General Skill", orientation='h', color="General Skill")
        st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("### Skill Hierarchy (Treemap)")
    tree_data = []
    for g in general_skills:
        cat = g["skill"]
        cat_total = g["experience_points"]
        specifics_xp = 0
        for s in g["specific_skills"]:
            cap_s = s.capitalize()
            count = skill_counts.get(s, 0)
            tree_data.append({"Category": cat, "Skill": cap_s, "Points": count})
            specifics_xp += count
            
        remainder = cat_total - specifics_xp
        if remainder > 0:
            tree_data.append({"Category": cat, "Skill": "Direct Mentions / Merged", "Points": remainder})
            
    if tree_data:
        df_tree = pd.DataFrame(tree_data)
        fig_tree = px.treemap(df_tree, path=["Category", "Skill"], values="Points", 
                              color="Category", title="Hierarchy Treemap")
        fig_tree.update_layout(margin=dict(t=30, l=0, r=0, b=0))
        st.plotly_chart(fig_tree, use_container_width=True)

st.markdown("### Network Graph of Skill Relationships")
# Build networkx graph
G = nx.Graph()
for g in general_skills:
    cat = g["skill"]
    G.add_node(cat, size=20, color='red')
    for s in g["specific_skills"]:
        cap_s = s.capitalize()
        G.add_node(cap_s, size=10, color='blue')
        G.add_edge(cat, cap_s)

if len(G.nodes) > 0:
    pos = nx.spring_layout(G, seed=42)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.0, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    for node in G.nodes():
        node_x.append(pos[node][0])
        node_y.append(pos[node][1])
        node_text.append(node)
        node_size.append(G.nodes[node].get('size', 10))
        node_color.append(G.nodes[node].get('color', 'blue'))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2))

    fig_net = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    st.plotly_chart(fig_net, use_container_width=True)
else:
    st.info("No skills to display in the network graph.")

col3, col4 = st.columns(2)

with col3:
    st.markdown("### Merged Skills Mapping Data")
    if merged_skills:
        st.json({"merged_skills": merged_skills})
    else:
        st.write("No skills were merged into parents at this threshold.")

with col4:
    st.markdown("### Final Skill Hierarchy Object")
    if general_skills:
        st.json({"general_skills": general_skills})
    else:
        st.write("No general skills found.")
