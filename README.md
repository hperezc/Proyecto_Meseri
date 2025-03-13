# MESERI Dashboard - Sistema de Evaluación de Riesgo de Incendio

[English](#english) | [Español](#español)

![Logo Cruz Roja](static/img/logo-cruz-roja.png)

## Español

### 📋 Descripción

Dashboard interactivo desarrollado para la Cruz Roja Colombiana (Seccional Antioquia) que implementa el método MESERI (Método Simplificado de Evaluación del Riesgo de Incendio) para evaluar y visualizar riesgos de incendio en diferentes infraestructuras.

### 🔥 Sobre la Metodología MESERI

El método MESERI es una metodología de evaluación de riesgo de incendio que considera de forma separada los factores generadores o agravantes del riesgo y los factores reductores o protectores. El método evalúa el riesgo de incendio considerando los siguientes aspectos:

#### Factores de Construcción:
* Número de plantas y altura del edificio
* Superficie del mayor sector de incendio
* Resistencia al fuego de elementos constructivos
* Falsos techos y suelos

#### Factores de Situación:
* Distancia de los bomberos
* Accesibilidad al edificio
* Peligro de activación
* Carga de fuego
* Inflamabilidad de los combustibles

#### Factores de Proceso/Operación:
* Orden y limpieza
* Almacenamiento en altura
* Factor de concentración
* Propagabilidad vertical y horizontal

#### Factores de Valor Económico:
* Concentración de valores

#### Factores de Destructibilidad:
* Por calor, humo, corrosión y agua

### ✨ Características Principales

* 📊 Evaluación de riesgo mediante metodología MESERI
* 📈 Visualización de datos en tiempo real
* 🔄 Sistema de clasificación por niveles de riesgo
* 📱 Interfaz responsiva y amigable
* 🔒 Sistema de autenticación para administradores
* 📥 Exportación de datos a Excel
* 🔍 Filtros avanzados por edificación
* 📅 Filtros por rango de fechas

### 📝 Funcionalidades del Formulario

#### Recolección de Datos
* Información general de la edificación
* Datos del evaluador y fecha de evaluación
* Características constructivas del edificio
* Factores de situación y entorno
* Medidas de protección existentes

#### Cálculos Automáticos
* Coeficiente de protección frente al incendio (P)
* Evaluación cualitativa del riesgo
* Valoración del riesgo de incendio
* Recomendaciones automáticas basadas en resultados

#### Panel de Administración
* Gestión de usuarios y permisos
* Historial de evaluaciones
* Edición y actualización de registros
* Exportación de informes detallados

### 🛠️ Tecnologías Utilizadas

* Python 3.11+
* Flask (Framework web)
* Dash (Visualización de datos)
* Plotly (Gráficos interactivos)
* SQLAlchemy (ORM)
* Pandas (Análisis de datos)
* Bootstrap 5 (Frontend)
* MySQL (Base de datos)

### ⚙️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/hperezc/Proyecto_Meseri.git
cd Proyecto_Meseri
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\\Scripts\\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
* Crear archivo `.env` en la raíz del proyecto con la siguiente estructura:
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=mysql://user:password@host/database_name
FLASK_ENV=development
DEBUG=True
```

5. Ejecutar la aplicación:
```bash
python app.py
```

### 📱 Uso

1. La aplicación estará disponible en:
   * `http://localhost:5000` (o el puerto que hayas configurado)
   * La URL y puerto exactos se mostrarán en la consola al iniciar la aplicación

2. Iniciar sesión con credenciales de administrador
3. Usar los filtros para seleccionar centrales e infraestructuras
4. Visualizar datos en gráficos interactivos:
   * Gauge de nivel de probabilidad promedio
   * Distribución de niveles de probabilidad
   * Mapa de calor de factores
   * Comparativa entre centrales
5. Exportar resultados en formato Excel

### 🌐 Demo en Vivo

Puedes ver una demostración en vivo de la aplicación en:
[https://meseri-app.onrender.com](https://meseri-app.onrender.com)

### 📞 Contacto

* LinkedIn: [Héctor Camilo Pérez Contreras](https://www.linkedin.com/in/hectorcperez21)
* Email: hectorcperez21@gmail.com
* GitHub: [@hperezc](https://github.com/hperezc)

### 📄 Licencia

© 2024 Héctor Camilo Pérez Contreras. Todos los derechos reservados.

---

## English

### 📋 Description

Interactive dashboard developed for the Colombian Red Cross (Antioquia Section) that implements the MESERI method (Simplified Method of Fire Risk Assessment) to evaluate and visualize fire risks across different infrastructures.

### 🔥 About MESERI Methodology

The MESERI method is a fire risk assessment methodology that separately considers risk-generating or aggravating factors and reducing or protective factors. The method evaluates fire risk considering the following aspects:

#### Construction Factors:
* Number of floors and building height
* Largest fire sector area
* Fire resistance of construction elements
* False ceilings and floors

#### Situation Factors:
* Distance from fire station
* Building accessibility
* Activation hazard
* Fire load
* Fuel flammability

#### Process/Operation Factors:
* Order and cleanliness
* Storage height
* Concentration factor
* Vertical and horizontal propagation

#### Economic Value Factors:
* Value concentration

#### Destructibility Factors:
* By heat, smoke, corrosion, and water

### ✨ Key Features

* 📊 Risk assessment using MESERI methodology
* 📈 Real-time data visualization
* 🔄 Risk level classification system
* 📱 Responsive and user-friendly interface
* 🔒 Administrator authentication system
* 📥 Excel data export
* 🔍 Advanced filtering by building
* 📅 Date range filtering

### 📝 Form Functionalities

#### Data Collection
* General building information
* Evaluator data and assessment date
* Building construction characteristics
* Situation and environment factors
* Existing protection measures

#### Automatic Calculations
* Fire protection coefficient (P)
* Qualitative risk assessment
* Fire risk rating
* Automatic recommendations based on results

#### Administration Panel
* User and permission management
* Assessment history
* Record editing and updating
* Detailed report export

### ��️ Technologies Used

* Python 3.11+
* Flask (Web framework)
* Dash (Data visualization)
* Plotly (Interactive charts)
* SQLAlchemy (ORM)
* Pandas (Data analysis)
* Bootstrap 5 (Frontend)
* MySQL (Database)

### ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/hperezc/Proyecto_Meseri.git
cd Proyecto_Meseri
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
* Create a `.env` file in the project root with the following structure:
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=mysql://user:password@host/database_name
FLASK_ENV=development
DEBUG=True
```

5. Run the application:
```bash
python app.py
```

### 📱 Usage

1. The application will be available at:
   * `http://localhost:5000` (or your configured port)
   * The exact URL and port will be displayed in the console when starting the application

2. Login with administrator credentials
3. Use filters to select plants and infrastructures
4. View data in interactive charts:
   * Average probability level gauge
   * Probability levels distribution
   * Factors heatmap
   * Plant comparison
5. Export results in Excel format

### 🌐 Live Demo

You can see a live demonstration of the application at:
[https://meseri-app.onrender.com](https://meseri-app.onrender.com)

### 📞 Contact

* LinkedIn: [Héctor Camilo Pérez Contreras](https://www.linkedin.com/in/hectorcperez21)
* Email: hectorcperez21@gmail.com
* GitHub: [@hperezc](https://github.com/hperezc)

### 📄 License

© 2024 Héctor Camilo Pérez Contreras. All rights reserved.
