import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import datetime, timedelta
from flask import url_for



def create_layout():
    # Estilos consistentes para todas las tarjetas
    card_style = {
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'border': 'none',
        'border-radius': '10px',
        'margin-bottom': '20px'
    }

    card_header_style = {
        'background-color': '#1e3d59',
        'color': 'white',
        'border-radius': '10px 10px 0 0',
        'padding': '15px 20px'
    }

    graph_style = {
        'background-color': 'white',
        'padding': '15px',
        'border-radius': '0 0 10px 10px'
    }

    section_icon_style = {'marginRight': '10px'}

    return dbc.Container([
        # Header con logos
        dbc.Row([
            dbc.Col(
                html.H1("Dashboard MESERI",
                       className="text-center mb-0 header-title",
                       style={
                           'color': '#1e3d59',
                           'font-weight': 'bold',
                           'text-transform': 'uppercase',
                           'letter-spacing': '2px'
                       }),
                width=12,
                className="d-flex align-items-center justify-content-center"
            ),
            dbc.Col(
                [
                    html.Img(src="/static/img/logo-cruz-roja.png", height="60px", className="header-logo")
                ],
                width=12,
                className="d-flex align-items-center justify-content-center mt-3"
            ),
        ], className="mb-4 header"),

        dcc.Interval(
            id='interval-component',
            interval=30*1000,
            n_intervals=0
        ),
        
        # Filtros con tooltip
        dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        html.H4("Filtros y Controles", className="mb-0 d-inline"),
                        html.Span([
                            html.I(
                                className="fas fa-info-circle ms-2",
                                id="filters-info",
                                style={
                                    'color': 'white',
                                    'cursor': 'pointer',
                                    'fontSize': '1.1rem'
                                }
                            ),
                        ])
                    ], width=12),
                ]),
            ], style=card_header_style),
            dbc.Tooltip(
                "Utilice estos controles para filtrar la información mostrada en el dashboard",
                target="filters-info",
                placement="top",
                style={
                    'backgroundColor': 'white',
                    'color': '#1e3d59',
                    'fontSize': '0.9rem',
                    'padding': '8px 12px',
                    'borderRadius': '4px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                }
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Central", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='central-filter',
                            multi=True,
                            className="mb-3",
                            style={
                                'zIndex': 1000
                            }
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Infraestructura", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='infra-filter',
                            multi=True,
                            className="mb-3",
                            style={
                                'zIndex': 999
                            }
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Rango de Fechas", className="fw-bold mb-2"),
                        dcc.DatePickerRange(
                            id='date-range',
                            start_date=None,
                            end_date=None,
                            className="mb-3"
                        )
                    ], md=4)
                ], className="g-3")
            ], style={'background-color': 'white'})
        ], style={**card_style, 'zIndex': 1}),
        
        # Resumen Ejecutivo con tooltip mejorado
        dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        html.H4("Resumen Ejecutivo", className="mb-0 d-inline me-2"),
                        html.I(
                            className="fas fa-info-circle",
                            id="summary-info",
                            style={'cursor': 'pointer', 'color': 'white'}
                        ),
                    ], width=12),
                ]),
                dbc.Tooltip(
                    [
                        html.P("Métricas clave del análisis de riesgo MESERI:", className="mb-2"),
                        html.Ul([
                            html.Li("Total de infraestructuras evaluadas"),
                            html.Li("Promedio general de riesgo"),
                            html.Li("Infraestructuras con mayor y menor riesgo")
                        ], className="mb-0")
                    ],
                    target="summary-info",
                    placement="right"
                )
            ], style=card_header_style),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4("Total Infraestructuras", className="text-center"),
                        html.H2(id='total-infra', className="text-center")
                    ], width=3),
                    dbc.Col([
                        html.H4("Riesgo Promedio", className="text-center"),
                        html.H2(id='riesgo-promedio', className="text-center")
                    ], width=3),
                    dbc.Col([
                        html.H4("Mayor Riesgo", className="text-center"),
                        html.H2(id='mayor-riesgo', className="text-center")
                    ], width=3),
                    dbc.Col([
                        html.H4("Menor Riesgo", className="text-center"),
                        html.H2(id='menor-riesgo', className="text-center")
                    ], width=3)
                ])
            ])
        ], className="mb-4"),
        
        # Gráficos Principales con tooltips
        dbc.Row([
            # Indicador de Riesgo Global
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.H4("Indicador de Riesgo Global", className="mb-0"), width=11),
                            dbc.Col(
                                [
                                    html.I(className="fas fa-info-circle", id="gauge-info"),
                                    dbc.Tooltip(
                                        "Medidor que muestra el nivel de riesgo promedio de todas las instalaciones",
                                        target="gauge-info",
                                        placement="top"
                                    )
                                ],
                                width=1,
                                className="text-end"
                            )
                        ]),
                        style=card_header_style
                    ),
                    dbc.CardBody([
                        dcc.Graph(
                            id='gauge-chart',
                            style={'background-color': 'white'},
                            config={'responsive': True}
                        )
                    ], style={'background-color': 'white'})
                ], style=card_style)
            ], xs=12, sm=12, md=6, className="mb-4"),
            
            # Distribución de Niveles de Riesgo
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.H4("Distribución de Niveles de Riesgo", className="mb-0"), width=11),
                            dbc.Col(
                                [
                                    html.I(className="fas fa-info-circle", id="pie-info"),
                                    dbc.Tooltip(
                                        "Distribución porcentual de los diferentes niveles de riesgo",
                                        target="pie-info",
                                        placement="top"
                                    )
                                ],
                                width=1,
                                className="text-end"
                            )
                        ]),
                        style=card_header_style
                    ),
                    dbc.CardBody([
                        dcc.Graph(
                            id='factors-pie-chart',
                            config={'responsive': True}
                        )
                    ])
                ], className="mb-4")
            ], xs=12, sm=12, md=6)
        ]),
        
        # Análisis Detallado con tooltips
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.H4("Mapa de Calor - Factores de Riesgo", className="mb-0"), width=11),
                            dbc.Col(
                                [
                                    html.I(className="fas fa-info-circle", id="heatmap-info"),
                                    dbc.Tooltip(
                                        "Visualización de la intensidad de los factores de riesgo por infraestructura",
                                        target="heatmap-info",
                                        placement="top"
                                    )
                                ],
                                width=1,
                                className="text-end"
                            )
                        ]),
                        style=card_header_style
                    ),
                    dbc.CardBody([
                        dcc.Graph(id='heatmap-chart')
                    ])
                ], className="mb-4")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.H4("Comparativa entre Centrales", className="mb-0"), width=11),
                            dbc.Col(
                                [
                                    html.I(className="fas fa-info-circle", id="comparison-info"),
                                    dbc.Tooltip(
                                        "Análisis comparativo de riesgos entre diferentes centrales",
                                        target="comparison-info",
                                        placement="top"
                                    )
                                ],
                                width=1,
                                className="text-end"
                            )
                        ]),
                        style=card_header_style
                    ),
                    dbc.CardBody([
                        dcc.Graph(id='comparison-chart')
                    ])
                ], className="mb-4")
            ], width=12)
        ]),
        
        # Tabla de Resultados con tooltip
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col([
                                html.H5("Resultados por Infraestructura"),
                                dbc.Tooltip(
                                    "Detalle completo de los resultados de evaluación por infraestructura",
                                    target="table-info",
                                    placement="top"
                                ),
                                html.I(className="fas fa-info-circle ms-2", id="table-info"),
                            ], width=8),
                            dbc.Col([
                                dbc.Button(
                                    [html.I(className="fas fa-file-excel me-2"), "Exportar Excel"],
                                    id="export-button",
                                    color="success",
                                    className="float-end"
                                ),
                                dcc.Download(id='download-dataframe-xlsx')
                            ], width=4)
                        ])
                    ], style=card_header_style),
                    dbc.CardBody([
                        html.Div(id='results-table')
                    ], style={'background-color': 'white'})
                ], style=card_style)
            ])
        ]),
        
        # Footer modificado
        html.Footer(
            dbc.Container([
                html.Hr(),
                html.P(
                    [
                        "Desarrollado por Héctor Camilo Pérez Contreras © 2024",
                        html.Br(),
                        "Sistema de Evaluación de Riesgo de Incendio MESERI"
                    ],
                    className="text-center text-muted"
                )
            ]),
            className="mt-5"
        ),
        
        html.Div(id='debug-output', style={'margin': '10px', 'padding': '10px', 'border': '1px solid #ccc'})
    ], fluid=True)