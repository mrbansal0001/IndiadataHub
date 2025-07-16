# Comparison Layout Module
# Contains the layout for the comparison tab with all 6 cards

from dash import dcc, html

def create_comparison_layout(COLORS, ATTRIBUTE_CATEGORIES):
    """Create the beautiful Comparison tab layout with 6 cards in 3x2 grid"""
    return html.Div([
        
        # Comparison Analysis Header
        html.Div([
            html.Div([
                html.Span("⚖️", style={
                    'fontSize': '1.5rem',
                    'marginRight': '1rem',
                    'padding': '10px',
                    'background': COLORS['gradient_1'],
                    'borderRadius': '10px',
                    'color': 'white'
                }),
                html.H3("State Comparison Analysis", style={'margin': 0, 'color': 'white'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem'}),
            
            html.P("Compare multiple states across different demographic indicators", 
                   style={'color': 'rgba(255,255,255,0.8)', 'margin': '0', 'fontSize': '1rem'})
            
        ], style={
            'background': COLORS['gradient_2'],
            'padding': '2rem',
            'borderRadius': '16px',
            'margin': '1.5rem',
            'boxShadow': '0 10px 30px rgba(240, 147, 251, 0.3)'
        }),
        
        # 3x2 Grid Layout for 6 Cards
        html.Div([
            
            # ROW 1: Cards 1 & 2
            html.Div([
                
                # Card 1: Multi-State Selector & Controls
                html.Div([
                    html.Div([
                        html.Span("🎛️", style={
                            'fontSize': '1.5rem',
                            'marginRight': '1rem',
                            'padding': '10px',
                            'background': COLORS['gradient_3'],
                            'borderRadius': '10px',
                            'color': 'white'
                        }),
                        html.H3("Comparison Controls", style={'margin': 0, 'color': COLORS['dark']})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                    
                    html.Div([
                        # Multi-state selector
                        html.Div([
                            html.Label("🗺️ Select States to Compare (2-5 states):", style={
                                'fontSize': '0.9rem',
                                'fontWeight': '600',
                                'color': '#4a5568',
                                'marginBottom': '0.5rem',
                                'display': 'block'
                            }),
                            dcc.Dropdown(
                                id="comparison-states-dropdown",
                                options=[],  # Will be populated by callback
                                multi=True,
                                placeholder="Choose 2-5 states to compare...",
                                style={'marginBottom': '1rem'}
                            )
                        ]),
                        
                        # Category selector
                        html.Div([
                            html.Label("📊 Select Category:", style={
                                'fontSize': '0.9rem',
                                'fontWeight': '600',
                                'color': '#4a5568',
                                'marginBottom': '0.5rem',
                                'display': 'block'
                            }),
                            dcc.Dropdown(
                                id="comparison-category-dropdown",
                                options=[{"label": k, "value": k} for k in ATTRIBUTE_CATEGORIES.keys()],
                                placeholder="Choose a demographic category...",
                                style={'marginBottom': '1rem'}
                            )
                        ]),
                        
                        # Attribute selector
                        html.Div([
                            html.Label("📈 Select Attribute:", style={
                                'fontSize': '0.9rem',
                                'fontWeight': '600',
                                'color': '#4a5568',
                                'marginBottom': '0.5rem',
                                'display': 'block'
                            }),
                            dcc.Dropdown(
                                id="comparison-attribute-dropdown",
                                placeholder="First select a category...",
                                style={'marginBottom': '1rem'}
                            )
                        ]),
                        
                        # Comparison type toggle
                        html.Div([
                            html.Label("⚖️ Comparison Type:", style={
                                'fontSize': '0.9rem',
                                'fontWeight': '600',
                                'color': '#4a5568',
                                'marginBottom': '0.5rem',
                                'display': 'block'
                            }),
                            dcc.RadioItems(
                                id="comparison-type-radio",
                                options=[
                                    {"label": " Absolute Values", "value": "absolute"},
                                    {"label": " Relative to National Average", "value": "relative"}
                                ],
                                value="absolute",
                                style={'display': 'flex', 'flexDirection': 'column', 'gap': '0.5rem'},
                                inputStyle={'marginRight': '0.5rem'}
                            )
                        ])
                        
                    ], style={'background': 'white', 'borderRadius': '12px', 'padding': '1.5rem', 'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.1)'})
                    
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'height': '500px'}),
                
                # Card 2: Side-by-Side Bar Comparison
                html.Div([
                    html.Div([
                        html.Span("📊", style={
                            'fontSize': '1.5rem',
                            'marginRight': '1rem',
                            'padding': '10px',
                            'background': COLORS['gradient_4'],
                            'borderRadius': '10px',
                            'color': 'white'
                        }),
                        html.H3("State Comparison Chart", style={'margin': 0, 'color': COLORS['dark']})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                    
                    html.Div([
                        dcc.Graph(
                            id="comparison-bar-chart",
                            style={'height': '400px'},
                            config={'displayModeBar': False}
                        )
                    ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
                    
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'height': '500px'}),
                
            ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '1rem', 'marginBottom': '3rem'}),
            
            # ROW 2: Cards 3 & 4
            html.Div([
                
                # Card 3: Multi-Dimensional Radar Chart
                html.Div([
                    html.Div([
                        html.Span("🕸️", style={
                            'fontSize': '1.5rem',
                            'marginRight': '1rem',
                            'padding': '10px',
                            'background': COLORS['gradient_5'],
                            'borderRadius': '10px',
                            'color': 'white'
                        }),
                        html.H3("Multi-Dimensional Radar", style={'margin': 0, 'color': COLORS['dark']})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                    
                    html.Div([
                        dcc.Graph(
                            id="comparison-radar-chart",
                            style={'height': '400px'},
                            config={'displayModeBar': False}
                        )
                    ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
                    
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'height': '500px'}),
                
                # Card 4: Performance Gap Analysis
                html.Div([
                    html.Div([
                        html.Span("📈", style={
                            'fontSize': '1.5rem',
                            'marginRight': '1rem',
                            'padding': '10px',
                            'background': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                            'borderRadius': '10px',
                            'color': 'white'
                        }),
                        html.H3("Performance Gap Analysis", style={'margin': 0, 'color': COLORS['dark']})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                    
                    html.Div([
                        dcc.Graph(
                            id="comparison-gap-chart",
                            style={'height': '400px'},
                            config={'displayModeBar': False}
                        )
                    ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
                    
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'height': '500px'}),
                
            ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '1rem', 'marginBottom': '3rem'}),
            
            # ROW 3: Cards 5 & 6 (Placeholders for now)
            html.Div([
                
                # Card 5: Comparison Data Table
                html.Div([
                    html.Div([
                        html.Span("📋", style={
                            'fontSize': '1.5rem',
                            'marginRight': '1rem',
                            'padding': '10px',
                            'background': 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
                            'borderRadius': '10px',
                            'color': 'white'
                        }),
                        html.H3("Comparison Data Table", style={'margin': 0, 'color': COLORS['dark']})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                    
                    html.Div([
                        dcc.Graph(
                            id="comparison-table-chart",
                            style={'height': '400px'},
                            config={'displayModeBar': False}
                        )
                    ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
                    
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'height': '500px'}),
                
                # Card 6: AI Insights & Recommendations
                html.Div([
                    html.Div([
                        html.Span("💡", style={
                            'fontSize': '1.5rem',
                            'marginRight': '1rem',
                            'padding': '10px',
                            'background': 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
                            'borderRadius': '10px',
                            'color': 'white'
                        }),
                        html.H3("AI Insights & Recommendations", style={'margin': 0, 'color': COLORS['dark']})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                    
                    html.Div([
                        html.Div(id="comparison-insights-content", style={
                            'background': 'white', 
                            'borderRadius': '16px', 
                            'padding': '1.5rem', 
                            'margin': '1rem 0', 
                            'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)',
                            'minHeight': '350px'
                        })
                    ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
                    
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'height': '500px'}),
                
            ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '1rem'}),
            
        ], style={'padding': '1rem'}),
        
    ])
