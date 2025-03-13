from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
import os
from pathlib import Path
from functools import wraps
from dotenv import load_dotenv
from dash import Dash
from dashboard.layout import create_layout
from dashboard.callbacks import init_callbacks
import dash_bootstrap_components as dbc

load_dotenv()

# Asegurarse que el directorio instance existe
instance_path = Path(__file__).parent / "instance"
instance_path.mkdir(exist_ok=True)

app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://hperezc97:geoHCP97@mysql-hperezc97.alwaysdata.net/hperezc97_meseribd')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

# Configuración de la clave secreta para las sesiones
app.secret_key = os.getenv('SECRET_KEY', 'd978422048d1ad28cf337105b9dc5bad')

# Credenciales de administrador (en producción, esto debería estar en una base de datos)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'epmcrcsa'  # En producción, usar hash en lugar de texto plano

# Decorador de autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] == ADMIN_USERNAME and 
            request.form['password'] == ADMIN_PASSWORD):
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        error = 'Credenciales inválidas'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# Definir el modelo primero
class Infraestructura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    central = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Factores de construcción
    numero_pisos = db.Column(db.String(20))
    altura_edificio = db.Column(db.String(20))
    superficie_mayor_sector = db.Column(db.String(20))
    resistencia_fuego = db.Column(db.String(50))
    falsos_techos = db.Column(db.String(50))
    
    # Factores de situación
    distancia_bomberos = db.Column(db.String(20))
    tiempo_llegada = db.Column(db.String(20))
    accesibilidad_edificio = db.Column(db.String(50))
    
    # Factores de proceso
    peligro_activacion = db.Column(db.String(20))
    carga_fuego = db.Column(db.String(20))
    combustibilidad = db.Column(db.String(20))
    orden_limpieza = db.Column(db.String(20))
    almacenamiento_altura = db.Column(db.String(20))
    
    # Factores de valor económico
    concentracion_valores = db.Column(db.String(20))
    
    # Factores de destructibilidad
    por_calor = db.Column(db.String(20))
    por_humo = db.Column(db.String(20))
    por_corrosion = db.Column(db.String(20))
    por_agua = db.Column(db.String(20))
    
    # Factores de propagabilidad
    propagabilidad_horizontal = db.Column(db.String(20))
    propagabilidad_vertical = db.Column(db.String(20))
    
    # Instalaciones de Protección Contra Incendios
    deteccion_automatica = db.Column(db.String(50))
    rociadores_automaticos = db.Column(db.String(50))
    extintores_portatiles = db.Column(db.String(50))
    bocas_incendio = db.Column(db.String(50))
    hidrantes_exteriores = db.Column(db.String(50))
    
    # Organización
    equipos_primera_intervencion = db.Column(db.String(50))
    equipos_segunda_intervencion = db.Column(db.String(50))
    planes_emergencia = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'central': self.central,
            'nombre': self.nombre,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M'),
            'numero_pisos': self.numero_pisos,
            'superficie_mayor_sector': self.superficie_mayor_sector,
            'resistencia_fuego': self.resistencia_fuego,
            'falsos_techos': self.falsos_techos,
            'distancia_bomberos': self.distancia_bomberos,
            'tiempo_llegada': self.tiempo_llegada,
            'accesibilidad_edificio': self.accesibilidad_edificio,
            'peligro_activacion': self.peligro_activacion,
            'carga_fuego': self.carga_fuego,
            'combustibilidad': self.combustibilidad,
            'orden_limpieza': self.orden_limpieza,
            'almacenamiento_altura': self.almacenamiento_altura,
            'concentracion_valores': self.concentracion_valores,
            'por_calor': self.por_calor,
            'por_humo': self.por_humo,
            'por_corrosion': self.por_corrosion,
            'por_agua': self.por_agua,
            'propagabilidad_horizontal': self.propagabilidad_horizontal,
            'propagabilidad_vertical': self.propagabilidad_vertical,
            'deteccion_automatica': self.deteccion_automatica,
            'rociadores_automaticos': self.rociadores_automaticos,
            'extintores_portatiles': self.extintores_portatiles,
            'bocas_incendio': self.bocas_incendio,
            'hidrantes_exteriores': self.hidrantes_exteriores,
            'equipos_primera_intervencion': self.equipos_primera_intervencion,
            'equipos_segunda_intervencion': self.equipos_segunda_intervencion,
            'planes_emergencia': self.planes_emergencia
        }

def validar_datos(datos):
    campos_requeridos = [
        'central', 'nombre', 'numero_pisos', 'superficie_mayor_sector',
        'resistencia_fuego', 'falsos_techos', 'distancia_bomberos',
        'tiempo_llegada', 'accesibilidad_edificio'
    ]
    
    for campo in campos_requeridos:
        if campo not in datos or not datos[campo]:
            return False, f"El campo {campo} es requerido"
    return True, None

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos'
            }), 400
        
        valido, mensaje = validar_datos(datos)
        if not valido:
            return jsonify({
                'success': False,
                'error': mensaje
            }), 400
        
        datos_limpios = {k: v.strip() if isinstance(v, str) else v 
                        for k, v in datos.items()}
        
        nueva_infra = Infraestructura(**datos_limpios)
        db.session.add(nueva_infra)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Datos guardados correctamente',
            'id': nueva_infra.id
        })
        
    except json.JSONDecodeError:
        return jsonify({
            'success': False,
            'error': 'Datos JSON inválidos'
        }), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error en la base de datos: ' + str(e)
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    try:
        infraestructuras = Infraestructura.query.order_by(
            Infraestructura.fecha.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'data': [infra.to_dict() for infra in infraestructuras]
        })
        
    except SQLAlchemyError as e:
        return jsonify({
            'success': False,
            'error': 'Error en la base de datos: ' + str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/ver_datos')
def ver_datos():
    infraestructuras = Infraestructura.query.all()
    return render_template('ver_datos.html', infraestructuras=infraestructuras)

@app.route('/admin')
@login_required
def admin_panel():
    try:
        # Obtener todos los registros ordenados por fecha descendente
        infraestructuras = Infraestructura.query.order_by(Infraestructura.fecha.desc()).all()
        return render_template('admin.html', infraestructuras=infraestructuras)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/exportar_excel', methods=['POST'])
@login_required
def exportar_excel():
    try:
        selected_ids = request.form.getlist('selected_ids[]')
        print("IDs seleccionados:", selected_ids)  # Para debugging
        
        if not selected_ids:
            return jsonify({'success': False, 'error': 'No se seleccionaron registros'})
        
        registros = Infraestructura.query.filter(Infraestructura.id.in_(selected_ids)).all()
        
        if not registros:
            return jsonify({'success': False, 'error': 'No se encontraron registros'})
            
        import pandas as pd
        from io import BytesIO
        
        data = [reg.to_dict() for reg in registros]
        df = pd.DataFrame(data)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Registros', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='registros_meseri.xlsx'
        )
        
    except Exception as e:
        print("Error en exportar_excel:", str(e))  # Para debugging
        return jsonify({'success': False, 'error': str(e)})

@app.route('/obtener_registro/<int:id>')
@login_required
def obtener_registro(id):
    try:
        registro = Infraestructura.query.get(id)
        if registro:
            return jsonify({
                'success': True,
                'registro': registro.to_dict()
            })
        return jsonify({
            'success': False,
            'error': 'Registro no encontrado'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/editar_registro/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_registro(id):
    registro = Infraestructura.query.get_or_404(id)
    if request.method == 'POST':
        try:
            datos = request.get_json()
            if not datos:
                return jsonify({
                    'success': False,
                    'error': 'No se recibieron datos'
                }), 400
            
            # Lista de todos los campos que necesitamos manejar
            campos_formulario = [
                'central', 'nombre', 'numero_pisos', 'superficie_mayor_sector',
                'resistencia_fuego', 'falsos_techos', 'distancia_bomberos',
                'tiempo_llegada', 'accesibilidad_edificio', 'peligro_activacion',
                'carga_fuego', 'combustibilidad', 'orden_limpieza',
                'almacenamiento_altura', 'concentracion_valores', 'por_calor',
                'por_humo', 'por_corrosion', 'por_agua', 'propagabilidad_horizontal',
                'propagabilidad_vertical', 'deteccion_automatica',
                'rociadores_automaticos', 'extintores_portatiles', 'bocas_incendio',
                'hidrantes_exteriores', 'equipos_primera_intervencion',
                'equipos_segunda_intervencion', 'planes_emergencia'
            ]
            
            # Actualizar cada campo si existe en los datos recibidos
            for campo in campos_formulario:
                if campo in datos:
                    setattr(registro, campo, datos[campo])
            
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Registro actualizado correctamente'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Para GET request, asegurarse de que todos los campos estén disponibles
    registro_dict = registro.to_dict()
    return render_template('editar_registro.html', registro=registro)

@app.route('/eliminar_registro/<int:id>', methods=['DELETE'])
@login_required
def eliminar_registro(id):
    try:
        registro = Infraestructura.query.get_or_404(id)
        db.session.delete(registro)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Registro eliminado correctamente'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Función para inicializar la base de datos
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Base de datos creada exitosamente")
            return True
        except Exception as e:
            print(f"Error al crear la base de datos: {str(e)}")
            return False

def test_db_connection():
    with app.app_context():
        try:
            # Intenta realizar una consulta simple
            Infraestructura.query.first()
            print("Conexión a la base de datos exitosa")
            return True
        except Exception as e:
            print(f"Error al conectar con la base de datos: {str(e)}")
            return False

def init_dashboard(server):
    with server.app_context():
        dash_app = Dash(
            __name__,
            server=server,
            url_base_pathname='/dashboard/',
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        
        index_string = '''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            {%metas%}
            <title>Dashboard MESERI</title>
            {%css%}
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="/static/css/styles.css">
            <style>
                .dash-container {
                    padding: 2rem 1rem;
                    background-color: #f8f9fa;
                }
                .card {
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .card-header {
                    border-radius: 10px 10px 0 0 !important;
                }
                .dash-dropdown {
                    border-radius: 5px;
                }
                .DateInput_input {
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="dash-container">
                {%app_entry%}
            </div>
            {%config%}
            {%scripts%}
            {%renderer%}
        </body>
        </html>
        '''
        
        dash_app.index_string = index_string
        dash_app.layout = create_layout()
        init_callbacks(dash_app, db, Infraestructura)
        
        return dash_app

# Agregar después de crear la app Flask
dash_app = init_dashboard(app)

@app.route('/debug_data')
def debug_data():
    infraestructuras = Infraestructura.query.all()
    data = []
    for infra in infraestructuras:
        data.append({
            'id': infra.id,
            'central': infra.central,
            'nombre': infra.nombre,
            'fecha': infra.fecha.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    test_db_connection()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))