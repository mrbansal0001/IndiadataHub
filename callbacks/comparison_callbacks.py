# ===========================================
# COMPARISON CALLBACKS
# ===========================================

from dash import Input, Output, callback_context
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config.settings import COLORS, FONT_FAMILY, ATTRIBUTE_CATEGORIES
from data.loader import load_state_data, get_state_data

def register_comparison_callbacks(app):
    """Register all comparison-related callbacks"""
    
    # Load state data for comparison
    try:
        load_result = load_state_data()
        if load_result:
            state_data = get_state_data()
            if state_data is not None and not state_data.empty:
                # Create state-level aggregated data for comparison
                comparison_state_data = state_data.groupby('State name').mean().reset_index()
            else:
                raise Exception("State data is empty or None")
        else:
            raise Exception("Failed to load state data")
    except Exception as e:
        print(f"Error loading state data for comparison: {e}")
        state_data = None
        comparison_state_data = None
    
    def get_short_label(column_name):
        """Convert long column names to short, readable labels"""
        clean_name = column_name.replace('_pct', '').replace('%', '').strip()
        
        label_map = {
            'Male_Literate': 'Male Literacy',
            'Female_Literate': 'Female Literacy',
            'Male_Workers': 'Male Employment',
            'Female_Workers': 'Female Employment',
            'Rural_Households': 'Rural Areas',
            'Urban_Households': 'Urban Areas',
            'LPG_or_PNG_Households': 'LPG/PNG Access',
            'Housholds_with_Electric_Lighting': 'Electricity',
            'Households_with_Internet': 'Internet',
            'Households_with_Computer': 'Computer',
        }
        
        return label_map.get(clean_name, clean_name.replace('_', ' ').title())

    # Populate comparison states dropdown
    @app.callback(
        Output('comparison-states-dropdown', 'options'),
        [Input('tab-content', 'children')]
    )
    def update_comparison_states_dropdown(_):
        """Populate states dropdown for comparison analysis"""
        if state_data is None:
            return []
        try:
            available_states = sorted(state_data['State name'].unique())
            return [{"label": state, "value": state} for state in available_states]
        except Exception as e:
            print(f"Error loading states for comparison: {e}")
            return []

    # Update comparison attribute dropdown based on category
    @app.callback(
        Output('comparison-attribute-dropdown', 'options'),
        [Input('comparison-category-dropdown', 'value')]
    )
    def update_comparison_attribute_dropdown(selected_category):
        """Update attribute dropdown for comparison based on selected category"""
        if not selected_category or state_data is None:
            return []
        
        # Get attributes from the selected category
        attributes = ATTRIBUTE_CATEGORIES.get(selected_category, [])
        
        # Convert from district format (_%) to state format (_pct) and filter available columns
        available_attributes = []
        for attr in attributes:
            if attr.endswith('_%'):
                state_attr = attr.replace('_%', '_pct')
                if state_attr in state_data.columns:
                    available_attributes.append(state_attr)
            elif attr + '_pct' in state_data.columns:
                available_attributes.append(attr + '_pct')
        
        return [{"label": get_short_label(attr), "value": attr} for attr in available_attributes]

    # Main comparison bar chart callback
    @app.callback(
        Output('comparison-bar-chart', 'figure'),
        [Input('comparison-states-dropdown', 'value'),
         Input('comparison-attribute-dropdown', 'value'),
         Input('comparison-type-radio', 'value')]
    )
    def update_comparison_bar_chart(selected_states, selected_attribute, comparison_type):
        """Create beautiful side-by-side state comparison bar chart"""
        
        # Show placeholder if no states or attribute selected
        if not selected_states or not selected_attribute or len(selected_states) < 2 or comparison_state_data is None:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="📊 State Comparison - Select 2+ states and an attribute",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#64748b",
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                annotations=[
                    dict(
                        text="🎯 Choose 2-5 states and a demographic attribute for beautiful comparison!",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=16, color="#94a3b8"),
                        showarrow=False
                    )
                ]
            )
            return placeholder_fig
        
        try:
            # Use the clean state-level aggregated data for comparison
            comparison_data = comparison_state_data[comparison_state_data['State name'].isin(selected_states)].copy()
            
            # Check if selected attribute exists
            if selected_attribute not in comparison_data.columns:
                raise ValueError(f"Attribute '{selected_attribute}' not found in state data")
            
            # Remove any rows with missing data
            comparison_data = comparison_data[['State name', selected_attribute]].dropna()
            
            if comparison_data.empty:
                raise ValueError("No data available for selected states and attribute")
            
            # Calculate national average for relative comparison
            national_avg = comparison_state_data[selected_attribute].mean()
            
            if comparison_type == "relative":
                # Show relative to national average
                comparison_data['comparison_value'] = ((comparison_data[selected_attribute] - national_avg) / national_avg) * 100
                y_values = comparison_data['comparison_value']
                y_title = f"% Difference from National Average ({national_avg:.1f}%)"
                hover_template = "<b>%{x}</b><br>" + \
                               f"{get_short_label(selected_attribute)}: %{{customdata:.1f}}%<br>" + \
                               "Difference: %{y:.1f}%<br>" + \
                               "<extra></extra>"
                customdata = comparison_data[selected_attribute]
                
                # Create color gradient based on relative performance
                colors = []
                for val in y_values:
                    if val > 15:
                        colors.append('#10b981')  # Strong positive - Green
                    elif val > 5:
                        colors.append('#34d399')  # Moderate positive - Light green
                    elif val > -5:
                        colors.append('#fbbf24')  # Near average - Yellow
                    elif val > -15:
                        colors.append('#f97316')  # Moderate negative - Orange
                    else:
                        colors.append('#ef4444')  # Strong negative - Red
                        
            else:
                # Show absolute values
                y_values = comparison_data[selected_attribute]
                y_title = f"{get_short_label(selected_attribute)} (%)"
                hover_template = "<b>%{x}</b><br>" + \
                               f"{get_short_label(selected_attribute)}: %{{y:.1f}}%<br>" + \
                               "<extra></extra>"
                customdata = None
                
                # Create color gradient based on performance ranking
                max_val = y_values.max()
                min_val = y_values.min()
                colors = []
                for val in y_values:
                    normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0.5
                    if normalized > 0.8:
                        colors.append('#10b981')  # Top performer - Green
                    elif normalized > 0.6:
                        colors.append('#34d399')  # Good - Light green
                    elif normalized > 0.4:
                        colors.append('#fbbf24')  # Average - Yellow
                    elif normalized > 0.2:
                        colors.append('#f97316')  # Below average - Orange
                    else:
                        colors.append('#ef4444')  # Low performer - Red
            
            # Create beautiful horizontal bar chart
            fig = go.Figure(data=[
                go.Bar(
                    y=comparison_data['State name'],
                    x=y_values,
                    orientation='h',
                    marker=dict(
                        color=colors,
                        line=dict(color='rgba(255,255,255,0.8)', width=2)
                    ),
                    hovertemplate=hover_template,
                    customdata=customdata,
                    text=[f"{val:.1f}%" for val in y_values],
                    textposition='outside',
                    textfont=dict(size=12, color='#374151', weight='bold')
                )
            ])
            
            # Beautiful styling for comparison chart
            fig.update_layout(
                title=f"📊 State Comparison: {get_short_label(selected_attribute)}",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=400,
                margin=dict(l=120, r=50, t=60, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                xaxis=dict(
                    title=y_title,
                    title_font_size=14,
                    title_font_weight="bold",
                    title_font_color="#4a5568",
                    tickfont=dict(size=11, color="#6b7280"),
                    gridcolor="rgba(203,213,225,0.5)",
                    gridwidth=1,
                    showgrid=True,
                    zeroline=True,
                    zerolinecolor="rgba(107,114,128,0.5)",
                    zerolinewidth=2
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=11, color="#374151"),
                    showgrid=False,
                    categoryorder='total ascending'
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="rgba(0,0,0,0.1)",
                    font_size=12,
                    font_family=FONT_FAMILY
                )
            )
            
            # Add reference line for relative comparison
            if comparison_type == "relative":
                fig.add_vline(
                    x=0, 
                    line_dash="dash", 
                    line_color="rgba(107,114,128,0.5)",
                    annotation_text="National Average",
                    annotation_position="top"
                )
            
            return fig
            
        except Exception as e:
            print(f"Error in comparison bar chart: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title="❌ Error loading comparison chart",
                title_x=0.5,
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[
                    dict(
                        text=f"Error: {str(e)[:50]}...",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=14, color="#ef4444"),
                        showarrow=False
                    )
                ]
            )
            return error_fig

    # Multi-dimensional radar chart callback
    @app.callback(
        Output('comparison-radar-chart', 'figure'),
        [Input('comparison-states-dropdown', 'value'),
         Input('comparison-category-dropdown', 'value')]
    )
    def update_comparison_radar_chart(selected_states, selected_category):
        """Create multi-dimensional radar chart comparing states across all attributes in a category"""
        
        # Show placeholder if insufficient selection
        if not selected_states or not selected_category or len(selected_states) < 2 or comparison_state_data is None:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="🕸️ Multi-Dimensional Radar - Select 2+ states and a category",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#64748b",
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                annotations=[
                    dict(
                        text="🎯 Choose 2-5 states and a category for multi-dimensional comparison!",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=16, color="#94a3b8"),
                        showarrow=False
                    )
                ]
            )
            return placeholder_fig
        
        try:
            # Get attributes from the selected category
            attributes = ATTRIBUTE_CATEGORIES.get(selected_category, [])
            
            if not attributes:
                raise ValueError(f"No attributes found for category '{selected_category}'")
            
            # Convert from district format (_%) to state format (_pct) and filter available columns
            available_attributes = []
            for attr in attributes:
                if attr.endswith('_%'):
                    state_attr = attr.replace('_%', '_pct')
                    if state_attr in comparison_state_data.columns:
                        available_attributes.append(state_attr)
                elif attr + '_pct' in comparison_state_data.columns:
                    available_attributes.append(attr + '_pct')
            
            if len(available_attributes) < 3:
                raise ValueError(f"Need at least 3 attributes for radar chart. Found {len(available_attributes)} in {selected_category}")
            
            # Filter data for selected states
            radar_data = comparison_state_data[comparison_state_data['State name'].isin(selected_states)].copy()
            
            if radar_data.empty:
                raise ValueError("No data available for selected states")
            
            # Create radar chart
            fig = go.Figure()
            
            # Color palette for states
            state_colors = [
                '#3b82f6',  # Blue
                '#ef4444',  # Red  
                '#10b981',  # Green
                '#f59e0b',  # Amber
                '#8b5cf6',  # Purple
            ]
            
            # Add trace for each state
            for idx, (_, state_row) in enumerate(radar_data.iterrows()):
                state_name = state_row['State name']
                
                # Get values for all available attributes
                values = []
                labels = []
                hover_texts = []
                
                for attr in available_attributes:
                    if pd.notna(state_row[attr]):
                        values.append(state_row[attr])
                        labels.append(get_short_label(attr))
                        hover_texts.append(f"{get_short_label(attr)}: {state_row[attr]:.1f}%")
                
                # Close the radar chart by repeating first value
                if values:
                    values.append(values[0])
                    labels.append(labels[0])
                    hover_texts.append(hover_texts[0])
                
                # Add radar trace
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    fillcolor=f"rgba({hex_to_rgb(state_colors[idx % len(state_colors)])}, 0.1)",
                    line=dict(
                        color=state_colors[idx % len(state_colors)],
                        width=3
                    ),
                    marker=dict(
                        color=state_colors[idx % len(state_colors)],
                        size=8,
                        line=dict(color='white', width=2)
                    ),
                    name=state_name,
                    hovertemplate="<b>%{fullData.name}</b><br>" + 
                                "<br>".join([f"{labels[i]}: {values[i]:.1f}%" for i in range(len(values)-1)]) +
                                "<extra></extra>",
                    showlegend=True
                ))
            
            # Beautiful radar chart styling
            fig.update_layout(
                title=f"🕸️ Multi-Dimensional Comparison: {selected_category}",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                polar=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    radialaxis=dict(
                        visible=True,
                        range=[0, max([max(comparison_state_data[attr].fillna(0)) for attr in available_attributes]) * 1.1],
                        tickfont=dict(size=10, color="#6b7280"),
                        gridcolor="rgba(203,213,225,0.5)",
                        gridwidth=1,
                        linecolor="rgba(203,213,225,0.7)",
                        linewidth=1
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=11, color="#374151", weight='bold'),
                        linecolor="rgba(203,213,225,0.7)",
                        linewidth=1,
                        gridcolor="rgba(203,213,225,0.3)"
                    )
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="rgba(203,213,225,0.5)",
                    borderwidth=1,
                    font=dict(size=11, color="#374151")
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="rgba(0,0,0,0.1)",
                    font_size=12,
                    font_family=FONT_FAMILY
                )
            )
            
            return fig
            
        except Exception as e:
            print(f"Error in radar chart: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title="❌ Error loading radar chart",
                title_x=0.5,
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                annotations=[
                    dict(
                        text=f"Error: {str(e)[:80]}...",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=14, color="#ef4444"),
                        showarrow=False
                    )
                ]
            )
            return error_fig

    # Placeholder callbacks for Cards 5-6
    
    @app.callback(
        Output('comparison-gap-chart', 'figure'),
        [Input('comparison-states-dropdown', 'value'),
         Input('comparison-attribute-dropdown', 'value')]
    )
    def update_comparison_gap_chart(selected_states, selected_attribute):
        """Placeholder for gap analysis - Cards 3 & 4 coming next!"""
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="📈 Performance Gap Analysis - Cards 3 & 4 Coming Next!",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="🎯 Cards 3 & 4 implementation in progress...",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig

    print("✅ Comparison callbacks registered successfully!")

def hex_to_rgb(hex_color):
    """Convert hex color to RGB string for rgba usage"""
    hex_color = hex_color.lstrip('#')
    return ','.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))
