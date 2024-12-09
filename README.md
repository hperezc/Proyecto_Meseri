# MESERI Dashboard - Fire Risk Assessment System

[English](#english) | [Español](#español)

![Dashboard Preview](static/img/dashboard-preview.png)

# Español

## Sistema de Evaluación de Riesgo de Incendio MESERI

### 📋 Descripción
Dashboard interactivo desarrollado para la Cruz Roja Colombiana (Seccional Antioquia) y EPM (Empresas Públicas de Medellín) que implementa el método MESERI (Método Simplificado de Evaluación del Riesgo de Incendio) para evaluar y visualizar riesgos de incendio en diferentes infraestructuras.

### ✨ Características Principales
- 📊 Evaluación de riesgo mediante metodología MESERI
- 📈 Visualización de datos en tiempo real
- 🔄 Sistema de clasificación dual (MESERI y EPM)
- 📱 Interfaz responsiva y amigable
- 🔒 Sistema de autenticación para administradores
- 📥 Exportación de datos a Excel
- 🔍 Filtros avanzados por central e infraestructura
- 📅 Filtros por rango de fechas

### 🛠️ Tecnologías Utilizadas
- Python 3.8+
- Flask (Framework web)
- Dash (Visualización de datos)
- Plotly (Gráficos interactivos)
- SQLAlchemy (ORM)
- Pandas (Análisis de datos)
- Bootstrap 5 (Frontend)
- SQLite (Base de datos)

### ⚙️ Instalación

1. Clonar el repositorio:
git clone https://github.com/hperezc/Proyecto_Meseri.git

2. Crear y activar entorno virtual:
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

3. Instalar dependencias:
pip install -r requirements.txt

4. Configurar variables de entorno

5. Inicializar la base de datos

6. Ejecutar la aplicación


### 📱 Uso
1. Acceder a `http://localhost:5000`
2. Iniciar sesión con credenciales de administrador
3. Usar los filtros para seleccionar centrales e infraestructuras
4. Visualizar datos en gráficos interactivos:
   - Gauge de nivel de probabilidad promedio
   - Distribución de niveles de probabilidad
   - Mapa de calor de factores
   - Comparativa entre centrales
5. Exportar resultados en formato Excel

### 📄 Licencia
© 2024 Héctor Camilo Pérez Contreras. Todos los derechos reservados.

---

# English

## MESERI Fire Risk Assessment Dashboard

### 📋 Description
Interactive dashboard developed for EPM (Empresas Públicas de Medellín) that implements the MESERI method (Simplified Method of Fire Risk Assessment) to evaluate and visualize fire risks across different infrastructures.

### ✨ Key Features
- 📊 Risk assessment using MESERI methodology
- 📈 Real-time data visualization
- 🔄 Dual classification system (MESERI and EPM)
- 📱 Responsive and user-friendly interface
- 🔒 Administrator authentication system
- 📥 Excel data export
- 🔍 Advanced filtering by plant and infrastructure
- 📅 Date range filtering

### 🛠️ Technologies Used
- Python 3.8+
- Flask (Web framework)
- Dash (Data visualization)
- Plotly (Interactive charts)
- SQLAlchemy (ORM)
- Pandas (Data analysis)
- Bootstrap 5 (Frontend)
- SQLite (Database)

### ⚙️ Installation

1. Clone the repository:
git clone https://github.com/hperezc/Proyecto_Meseri.git

2. Create and activate virtual environment:
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Configure environment variables
 
5. Initialize database

6. Run the application

### 📱 Usage
1. Access `http://localhost:5000`
2. Login with administrator credentials
3. Use filters to select plants and infrastructures
4. View data in interactive charts:
   - Average probability level gauge
   - Probability levels distribution
   - Factors heatmap
   - Plant comparison
5. Export results in Excel format

### 📄 License
© 2024 Héctor Camilo Pérez Contreras. All rights reserved.

---

### 📞 Contact
- LinkedIn: [Héctor Camilo Pérez Contreras](https://www.linkedin.com/in/hector-camilo-perez-contreras-a971551a1/)
- Email: hectorcperez21@gmail.com
- GitHub: [@hperezc](https://github.com/hperezc)
