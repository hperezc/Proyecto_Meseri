from dash import Input, Output, callback, dash_table, State
import plotly.graph_objects as go
import plotly.express as px
from .calculations import (
    calculate_meseri_score,
    get_construction_weight,
    get_situation_weight,
    get_process_weight,
    get_concentration_weight,
    get_propagability_weight,
    get_destructibility_weight,
    get_protection_weight
)
import pandas as pd
from datetime import datetime
import numpy as np
from dash import html
import base64
import io
from flask import current_app
import dash
import dash_core_components as dcc
from .risk_categories import get_epm_risk_level
import traceback

def init_callbacks(app, db, Infraestructura):
    @app.callback(
        Output('central-filter', 'options'),
        Input('interval-component', 'n_intervals')
    )
    def update_central_options(n):
        with current_app.app_context():
            try:
                infraestructuras = Infraestructura.query.with_entities(
                    Infraestructura.central).distinct().all()
                centrales = [{'label': 'Todas', 'value': 'all'}]  # Opción "Todas"
                centrales.extend([
                    {'label': central[0], 'value': central[0]} 
                    for central in infraestructuras if central[0]
                ])
                return centrales
            except Exception as e:
                print(f"Debug - Error in update_central_options: {str(e)}")
                return []

    @app.callback(
        Output('infra-filter', 'options'),
        [Input('central-filter', 'value')]
    )
    def update_infra_options(selected_centrales):
        with current_app.app_context():
            try:
                query = Infraestructura.query
                
                if selected_centrales and selected_centrales != 'all':
                    if isinstance(selected_centrales, list):
                        query = query.filter(Infraestructura.central.in_(selected_centrales))
                    else:
                        query = query.filter(Infraestructura.central == selected_centrales)
                
                infraestructuras = query.with_entities(
                    Infraestructura.nombre).distinct().all()
                
                options = [{'label': 'Todas', 'value': 'all'}]
                options.extend([
                    {'label': infra[0], 'value': infra[0]} 
                    for infra in infraestructuras if infra[0]
                ])
                return options
            except Exception as e:
                print(f"Debug - Error in update_infra_options: {str(e)}")
                return []

    @app.callback(
        [Output('gauge-chart', 'figure'),
         Output('factors-pie-chart', 'figure'),
         Output('heatmap-chart', 'figure'),
         Output('comparison-chart', 'figure'),
         Output('results-table', 'children'),
         Output('total-infra', 'children'),
         Output('riesgo-promedio', 'children'),
         Output('mayor-riesgo', 'children'),
         Output('menor-riesgo', 'children')],
        [Input('central-filter', 'value'),
         Input('infra-filter', 'value'),
         Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(selected_centrales, selected_infras, start_date, end_date, n):
        with current_app.app_context():
            try:
                print(f"Debug - Selected centrales: {selected_centrales}")
                print(f"Debug - Selected infras: {selected_infras}")
                
                # Consulta base
                query = Infraestructura.query
                
                # Filtro de centrales
                if selected_centrales and selected_centrales != 'all':
                    if isinstance(selected_centrales, list) and 'all' not in selected_centrales:
                        query = query.filter(Infraestructura.central.in_(selected_centrales))
                    elif isinstance(selected_centrales, str) and selected_centrales != 'all':
                        query = query.filter(Infraestructura.central == selected_centrales)
                
                # Filtro de infraestructuras
                if selected_infras and selected_infras != 'all':
                    if isinstance(selected_infras, list) and 'all' not in selected_infras:
                        query = query.filter(Infraestructura.nombre.in_(selected_infras))
                    elif isinstance(selected_infras, str) and selected_infras != 'all':
                        query = query.filter(Infraestructura.nombre == selected_infras)
                
                # Si no hay selección en los filtros o se selecciona 'all', 
                # se mostrarán todos los registros
                if not selected_centrales or not selected_infras:
                    query = Infraestructura.query
                
                # Ejecutar la consulta
                infraestructuras = query.all()
                print(f"Debug - Number of infrastructures found: {len(infraestructuras)}")
                
                if not infraestructuras:
                    return [go.Figure()] * 4 + ["Sin datos disponibles"] + ["0"] * 4
                
                # Procesar resultados
                resultados = []
                for infra in infraestructuras:
                    try:
                        data = infra.to_dict()
                        print(f"Debug - Processing infrastructure: {data['nombre']} from {data['central']}")
                        score = calculate_meseri_score(data)
                        resultados.append({
                            'nombre': data['nombre'],
                            'central': data['central'],
                            'fecha': data['fecha'],
                            'p': score['p'],
                            'nivel_riesgo': score['risk_level'],
                            'x': score['x'],
                            'y': score['y']
                        })
                    except Exception as e:
                        print(f"Error processing infrastructure {infra.id}: {e}")
                        continue
                
                df = pd.DataFrame(resultados)
                print(f"Debug - Final DataFrame shape: {df.shape}")
                print(f"Debug - Unique centrales in DataFrame: {df['central'].unique()}")
                
                if df.empty:
                    return [go.Figure()] * 4 + ["Sin datos disponibles"] + ["0"] * 4
                
                # Calcular métricas
                total_infra = len(df)
                riesgo_promedio = f"{df['p'].mean():.2f}"
                mayor_riesgo = df.loc[df['p'].idxmin(), 'nombre'] if not df.empty else "N/A"
                menor_riesgo = df.loc[df['p'].idxmax(), 'nombre'] if not df.empty else "N/A"
                
                # Crear gráficos
                gauge = create_gauge_chart(df)
                pie = create_pie_chart(df)
                heatmap = create_heatmap(df)
                comparison = create_comparison_chart(df)
                table = create_table(df)
                
                return (gauge, pie, heatmap, comparison, table,
                        str(total_infra), riesgo_promedio, mayor_riesgo, menor_riesgo)
                
            except Exception as e:
                print(f"Debug - Error in update_dashboard: {str(e)}")
                print(f"Debug - Traceback: {traceback.format_exc()}")
                empty_fig = go.Figure()
                empty_fig.add_annotation(
                    text="Error al cargar los datos",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
                return [empty_fig] * 4 + ["Error"] + ["0"] * 4

    @app.callback(
        Output('upload-output', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def import_excel(contents, filename):
        if contents is None:
            return html.Div('No se ha seleccionado ningún archivo')
        
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            if 'xlsx' in filename:
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return html.Div('Por favor, sube un archivo Excel (.xlsx)')
            
            # Procesar y guardar datos
            for _, row in df.iterrows():
                nueva_infra = Infraestructura(**row.to_dict())
                db.session.add(nueva_infra)
            db.session.commit()
            
            return html.Div(f'Archivo {filename} importado correctamente')
            
        except Exception as e:
            return html.Div(f'Error al procesar el archivo: {str(e)}')

    @app.callback(
        Output('download-dataframe-xlsx', 'data'),
        Input('export-button', 'n_clicks'),
        [State('central-filter', 'value'),
         State('infra-filter', 'value'),
         State('date-range', 'start_date'),
         State('date-range', 'end_date')],
        prevent_initial_call=True
    )
    def export_dashboard_data(n_clicks, selected_centrales, selected_infras, start_date, end_date):
        if n_clicks is None:
            return None
        
        with current_app.app_context():
            try:
                query = Infraestructura.query
                
                # Aplicar filtros
                if selected_centrales and selected_centrales != 'all':
                    if isinstance(selected_centrales, list) and 'all' not in selected_centrales:
                        query = query.filter(Infraestructura.central.in_(selected_centrales))
                
                infraestructuras = query.all()
                
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Hoja de resumen
                    resumen_data = []
                    for infra in infraestructuras:
                        data = infra.to_dict()
                        score = calculate_meseri_score(data)
                        resumen_data.append({
                            'Central': data['central'],
                            'Infraestructura': data['nombre'],
                            'Fecha': data['fecha'],
                            'Factores Agravantes (X)': score['x'],
                            'Factores Protectores (Y)': score['y'],
                            'Valoración Final (P)': score['p'],
                            'Nivel de Riesgo Meseri': score['risk_level'],
                            'Categoría de Riesgo EPM': get_epm_risk_level(score['p'])
                        })
                    
                    df_resumen = pd.DataFrame(resumen_data)
                    df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                    
                    # Hojas individuales para cada infraestructura
                    for infra in infraestructuras:
                        data = infra.to_dict()
                        score = calculate_meseri_score(data)
                        
                        parametros = {
                            'Parámetro': [],
                            'Valor': [],
                            'Peso': []
                        }
                        
                        # Construcción
                        parametros['Parámetro'].extend(['Número de Pisos', 'Superficie Mayor Sector', 
                                                      'Resistencia al Fuego', 'Falsos Techos'])
                        parametros['Valor'].extend([data['numero_pisos'], data['superficie_mayor_sector'],
                                                 data['resistencia_fuego'], data['falsos_techos']])
                        parametros['Peso'].extend([
                            get_construction_weight('numero_pisos', data['numero_pisos']),
                            get_construction_weight('superficie_mayor_sector', data['superficie_mayor_sector']),
                            get_construction_weight('resistencia_fuego', data['resistencia_fuego']),
                            get_construction_weight('falsos_techos', data['falsos_techos'])
                        ])
                        
                        # Situación
                        parametros['Parámetro'].extend(['Distancia Bomberos', 'Accesibilidad Edificio'])
                        parametros['Valor'].extend([data['distancia_bomberos'], data['accesibilidad_edificio']])
                        parametros['Peso'].extend([
                            get_situation_weight('distancia_bomberos', data['distancia_bomberos']),
                            get_situation_weight('accesibilidad_edificio', data['accesibilidad_edificio'])
                        ])
                        
                        # Procesos
                        parametros['Parámetro'].extend(['Peligro de Activación', 'Carga de Fuego', 'Combustibilidad',
                                                      'Orden y Limpieza', 'Almacenamiento en Altura'])
                        parametros['Valor'].extend([data['peligro_activacion'], data['carga_fuego'],
                                                 data['combustibilidad'], data['orden_limpieza'],
                                                 data['almacenamiento_altura']])
                        parametros['Peso'].extend([
                            get_process_weight('peligro_activacion', data['peligro_activacion']),
                            get_process_weight('carga_fuego', data['carga_fuego']),
                            get_process_weight('combustibilidad', data['combustibilidad']),
                            get_process_weight('orden_limpieza', data['orden_limpieza']),
                            get_process_weight('almacenamiento_altura', data['almacenamiento_altura'])
                        ])
                        
                        # Concentración
                        parametros['Parámetro'].extend(['Concentración de Valores'])
                        parametros['Valor'].extend([data['concentracion_valores']])
                        parametros['Peso'].extend([
                            get_concentration_weight('concentracion_valores', data['concentracion_valores'])
                        ])
                        
                        # Propagabilidad
                        parametros['Parámetro'].extend(['Propagabilidad Vertical', 'Propagabilidad Horizontal'])
                        parametros['Valor'].extend([data['propagabilidad_vertical'], data['propagabilidad_horizontal']])
                        parametros['Peso'].extend([
                            get_propagability_weight('propagabilidad_vertical', data['propagabilidad_vertical']),
                            get_propagability_weight('propagabilidad_horizontal', data['propagabilidad_horizontal'])
                        ])
                        
                        # Destructibilidad
                        parametros['Parámetro'].extend(['Por Calor', 'Por Humo', 'Por Corrosión', 'Por Agua'])
                        parametros['Valor'].extend([data['por_calor'], data['por_humo'], 
                                                 data['por_corrosion'], data['por_agua']])
                        parametros['Peso'].extend([
                            get_destructibility_weight('por_calor', data['por_calor']),
                            get_destructibility_weight('por_humo', data['por_humo']),
                            get_destructibility_weight('por_corrosion', data['por_corrosion']),
                            get_destructibility_weight('por_agua', data['por_agua'])
                        ])
                        
                        # Protección
                        parametros['Parámetro'].extend([
                            'Extintores Portátiles', 'Bocas de Incendio', 'Hidrantes Exteriores',
                            'Detección Automática', 'Rociadores Automáticos', 
                            'Equipos Primera Intervención', 'Equipos Segunda Intervención',
                            'Planes de Emergencia'
                        ])
                        parametros['Valor'].extend([
                            data['extintores_portatiles'], data['bocas_incendio'],
                            data['hidrantes_exteriores'], data['deteccion_automatica'],
                            data['rociadores_automaticos'], data['equipos_primera_intervencion'],
                            data['equipos_segunda_intervencion'], data['planes_emergencia']
                        ])
                        parametros['Peso'].extend([
                            get_protection_weight('extintores_portatiles', data['extintores_portatiles']),
                            get_protection_weight('bocas_incendio', data['bocas_incendio']),
                            get_protection_weight('hidrantes_exteriores', data['hidrantes_exteriores']),
                            get_protection_weight('deteccion_automatica', data['deteccion_automatica']),
                            get_protection_weight('rociadores_automaticos', data['rociadores_automaticos']),
                            get_protection_weight('equipos_primera_intervencion', data['equipos_primera_intervencion']),
                            get_protection_weight('equipos_segunda_intervencion', data['equipos_segunda_intervencion']),
                            get_protection_weight('planes_emergencia', data['planes_emergencia'])
                        ])
                        
                        # Agregar totales
                        parametros['Parámetro'].extend([
                            'Total Factores Agravantes (X)', 
                            'Total Factores Protectores (Y)',
                            'Valoración Final (P)', 
                            'Nivel de Riesgo Meseri',
                            'Categoría de Riesgo EPM'
                        ])
                        parametros['Valor'].extend([
                            score['x'], 
                            score['y'], 
                            score['p'], 
                            score['risk_level'],
                            get_epm_risk_level(score['p'])
                        ])
                        parametros['Peso'].extend(['-', '-', '-', '-', '-'])
                        
                        df_infra = pd.DataFrame(parametros)
                        sheet_name = f"{data['central']}_{data['nombre']}"[:31]
                        df_infra.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                output.seek(0)
                return dcc.send_bytes(output.getvalue(), 
                                    f"registros_meseri_{datetime.now().strftime('%Y%m%d')}.xlsx")
                
            except Exception as e:
                print(f"Error en export_dashboard_data: {str(e)}")
                return None

def create_gauge_chart(df):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=df['p'].mean(),
        title={'text': "Nivel de Riesgo Promedio"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 3], 'color': "red", 'name': "Riesgo Muy Alto"},
                {'range': [3, 5], 'color': "orange", 'name': "Riesgo Alto"},
                {'range': [5, 8], 'color': "yellow", 'name': "Riesgo Medio"},
                {'range': [8, 10], 'color': "green", 'name': "Riesgo Bajo"}
            ]
        }
    ))
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Roboto"
        )
    )
    return fig

def create_pie_chart(df):
    fig = px.pie(
        names=df['nivel_riesgo'].value_counts().index,
        values=df['nivel_riesgo'].value_counts().values,
        title="Distribución de Niveles de Riesgo por Categoría",
        color_discrete_map={
            'Riesgo Muy Alto': 'red',
            'Riesgo Alto': 'orange',
            'Riesgo Medio': 'yellow',
            'Riesgo Bajo': 'green'
        }
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                     "Cantidad: %{value}<br>" +
                     "Porcentaje: %{percent:.1%}<extra></extra>"
    )
    return fig

def create_heatmap(df):
    # Agrupar por central y calcular promedios de factores
    heatmap_data = df.groupby('central').agg({
        'x': 'mean',  # Factores agravantes
        'y': 'mean',  # Factores protectores
        'p': 'mean'   # Valoración final
    }).round(2)
    
    return go.Figure(data=go.Heatmap(
        z=[heatmap_data['x'], heatmap_data['y'], heatmap_data['p']],
        x=heatmap_data.index,
        y=['Factores Agravantes', 'Factores Protectores', 'Valoración Final'],
        colorscale='RdYlGn',
        reversescale=True
    ))

def create_comparison_chart(df):
    # Crear gráfico de barras comparativo entre centrales
    fig = go.Figure()
    
    centrales = df['central'].unique()
    
    fig.add_trace(go.Bar(
        name='Valoración de Riesgo (P)',
        x=centrales,
        y=[df[df['central'] == central]['p'].mean() for central in centrales],
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        name='Factores Agravantes (X)',
        x=centrales,
        y=[df[df['central'] == central]['x'].mean() for central in centrales],
        marker_color='red'
    ))
    
    fig.add_trace(go.Bar(
        name='Factores Protectores (Y)',
        x=centrales,
        y=[df[df['central'] == central]['y'].mean() for central in centrales],
        marker_color='green'
    ))
    
    fig.update_layout(
        title="Comparativa entre Centrales",
        barmode='group',
        yaxis_title="Valor",
        xaxis_title="Central"
    )
    
    return fig

def create_table(df):
    df['epm_risk_level'] = df['p'].apply(get_epm_risk_level)
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {"name": "Infraestructura", "id": "nombre"},
            {"name": "Central", "id": "central"},
            {"name": "Fecha", "id": "fecha"},
            {"name": "Valor P", "id": "p"},
            {"name": "Nivel Riesgo MESERI", "id": "nivel_riesgo"},
            {"name": "Nivel Riesgo EPM", "id": "epm_risk_level"}
        ],
        style_data_conditional=[
            {
                'if': {'column_id': 'epm_risk_level', 'filter_query': '{epm_risk_level} = "Aceptable"'},
                'backgroundColor': '#28a745',
                'color': 'white'
            },
            {
                'if': {'column_id': 'epm_risk_level', 'filter_query': '{epm_risk_level} = "Tolerable"'},
                'backgroundColor': '#ffc107',
                'color': 'black'
            },
            {
                'if': {'column_id': 'epm_risk_level', 'filter_query': '{epm_risk_level} = "Alto"'},
                'backgroundColor': '#fd7e14',
                'color': 'white'
            },
            {
                'if': {'column_id': 'epm_risk_level', 'filter_query': '{epm_risk_level} = "Extremo"'},
                'backgroundColor': '#dc3545',
                'color': 'white'
            }
        ],
        style_header={
            'backgroundColor': '#1e3d59',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        page_size=10,
        sort_action='native',
        filter_action='native',
        style_table={'overflowX': 'auto'}
    )