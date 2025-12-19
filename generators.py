import random
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- DATOS (Sin cambios) ---
ROOTS = {
    'prefixes': ['Al', 'Bri', 'Car', 'Dan', 'El', 'Fer', 'Gar', 'Har', 'Jes', 'Kar', 
                'Lar', 'Mar', 'Nor', 'Par', 'Quin', 'Ros', 'Sar', 'Tar', 'Val', 'Wil'],
    'suffixes': ['ton', 'son', 'man', 'ley', 'field', 'ford', 'wood', 'stone', 'worth', 'berg'],
    'names': ['Alex', 'Bern', 'Crist', 'Dav', 'Edw', 'Fred', 'Greg', 'Henr', 'Ivan', 'John']
}

def generate_random_identity():
    first = random.choice(ROOTS['names']) + random.choice(['an', 'en', 'on'])
    last = random.choice(ROOTS['prefixes']) + random.choice(ROOTS['suffixes'])
    first = first.capitalize()
    last = last.capitalize()
    
    num = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{num}@psu.edu"
    
    return {
        'first_name': first,
        'last_name': last,
        'full_name': f"{first} {last}",
        'email': email
    }

def generate_psu_id():
    return f"9{random.randint(10000000, 99999999)}"

# --- GENERACIÓN DE HTML (ESTILO CLEAN LIONPATH) ---
def get_psu_html(identity):
    psu_id = generate_psu_id()
    name = identity['full_name']
    # Fecha exacta como en la referencia (MM/DD/YYYY, HH:MM:SS AM/PM)
    date_str = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')
    
    majors = ['Software Engineering (BS)', 'Computer Science (BS)', 'Data Science (BS)', 'Business Administration (BS)']
    major = random.choice(majors)

    # Nombre oficial para el footer
    uni_name_footer = "Pennsylvania State University-World Campus"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            /* Reset y Fuentes */
            :root {{ --psu-blue: #1E407C; --bg-gray: #f0f0f0; --text: #333; --border: #ddd; }}
            body {{ 
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; 
                background: #e6e6e6; 
                margin: 0; 
                padding: 40px; 
                display: flex; 
                justify-content: center; 
            }}
            
            /* Hoja de Papel Principal */
            .viewport {{ 
                width: 1100px; 
                background: #fff; 
                min-height: 800px; 
                box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
            }}

            /* Header Azul Oscuro */
            .header {{ 
                background: var(--psu-blue); 
                color: white; 
                height: 60px;
                padding: 0 30px; 
                display: flex; 
                align-items: center; 
                justify-content: space-between; 
            }}
            
            .brand {{ display: flex; align-items: center; height: 100%; }}
            .psu-logo {{ 
                font-family: "Georgia", serif; 
                font-weight: bold; 
                font-size: 22px; 
                letter-spacing: 0.5px;
                padding-right: 15px;
                margin-right: 15px;
                border-right: 1px solid rgba(255,255,255,0.3);
                height: 24px;
                line-height: 24px;
                display: block;
            }}
            .sys-name {{ font-size: 18px; font-weight: 300; opacity: 0.9; }}
            
            .user-menu {{ font-size: 13px; font-weight: 500; }}
            
            /* Barra de Navegación Gris */
            .nav {{ 
                background: #f8f8f8; 
                border-bottom: 1px solid #ccc; 
                padding: 0 30px; 
                display: flex; 
                gap: 25px; 
                font-size: 13px; 
                color: #555; 
                height: 45px;
                align-items: center;
            }}
            .nav-item {{ cursor: pointer; height: 100%; display: flex; align-items: center; }}
            .nav-item.active {{ 
                color: var(--psu-blue); 
                font-weight: bold; 
                border-bottom: 3px solid var(--psu-blue); 
                box-sizing: border-box;
            }}

            /* Contenido Principal */
            .content {{ padding: 30px; }}
            
            /* Título y Semestre */
            .page-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                margin-bottom: 20px;
                border-bottom: 1px solid #eee;
                padding-bottom: 15px;
            }}
            .page-title {{ 
                font-size: 24px; 
                color: var(--psu-blue); 
                margin: 0; 
                font-weight: bold;
            }}
            .term-info {{ font-size: 14px; color: #444; }}

            /* Tarjeta de Información del Estudiante */
            .student-card {{ 
                background: #fbfbfb; 
                border: 1px solid #e0e0e0; 
                padding: 15px 20px; 
                display: grid; 
                grid-template-columns: 2fr 1.5fr 3fr 2fr; 
                gap: 20px; 
                margin-bottom: 10px; 
            }}
            
            .field-group {{ display: flex; flex-direction: column; }}
            .field-label {{ 
                font-size: 10px; 
                color: #777; 
                text-transform: uppercase; 
                margin-bottom: 4px; 
                font-weight: 600;
            }}
            .field-value {{ 
                font-size: 14px; 
                font-weight: bold; 
                color: #222; 
            }}
            
            /* Status Enrolled (Sin emoji, fondo verde claro) */
            .status-box {{
                background-color: #e6fffa;
                border: 1px solid #b2f5ea;
                color: #007a5e;
                padding: 4px 10px;
                font-weight: bold;
                font-size: 13px;
                display: inline-block;
                border-radius: 2px;
            }}
            /* Check cuadrado verde simulado con CSS si se quiere, o simple texto */
            .status-check {{
                display: inline-block;
                width: 10px; height: 10px;
                background: #007a5e;
                margin-right: 5px;
                vertical-align: middle;
                position: relative;
            }}
            /* Check mark blanco dentro del cuadrado */
            .status-check::after {{
                content: '';
                position: absolute;
                left: 3px; top: 1px;
                width: 3px; height: 6px;
                border: solid white;
                border-width: 0 2px 2px 0;
                transform: rotate(45deg);
            }}

            /* Fecha de reporte alineada a la derecha */
            .report-date {{
                text-align: right;
                font-size: 11px;
                color: #666;
                margin-bottom: 5px;
            }}

            /* Tabla de Clases */
            table {{ 
                width: 100%; 
                border-collapse: collapse; 
                font-size: 13px; 
            }}
            
            thead tr {{ background-color: #eee; }}
            th {{ 
                text-align: left; 
                padding: 10px; 
                color: #444; 
                font-weight: bold; 
                border-bottom: 2px solid #ccc;
            }}
            
            td {{ 
                padding: 15px 10px; 
                border-bottom: 1px solid #eee; 
                color: #333;
                vertical-align: top;
            }}
            
            .course-code {{ 
                color: var(--psu-blue); 
                font-weight: bold; 
            }}

            /* Footer Copyright */
            .footer {{ 
                margin-top: 50px; 
                text-align: center; 
                font-size: 11px; 
                color: #777; 
                border-top: 1px solid #ddd; 
                padding-top: 15px; 
                line-height: 1.5;
            }}

        </style>
    </head>
    <body>
        <div class="viewport">
            <!-- Header -->
            <div class="header">
                <div class="brand">
                    <span class="psu-logo">PennState</span>
                    <span class="sys-name">LionPATH</span>
                </div>
                <div class="user-menu">
                    Welcome, <strong>{name}</strong> &nbsp;|&nbsp; Sign Out
                </div>
            </div>

            <!-- Navegación -->
            <div class="nav">
                <div class="nav-item">Student Home</div>
                <div class="nav-item active">My Class Schedule</div>
                <div class="nav-item">Academics</div>
                <div class="nav-item">Finances</div>
                <div class="nav-item">Campus Life</div>
            </div>

            <!-- Contenido -->
            <div class="content">
                <div class="page-header">
                    <h1 class="page-title">My Class Schedule</h1>
                    <div class="term-info">Term: <strong>Fall 2025</strong> (Aug 25 - Dec 12)</div>
                </div>

                <div class="student-card">
                    <div class="field-group">
                        <span class="field-label">Student Name</span>
                        <span class="field-value">{name}</span>
                    </div>
                    <div class="field-group">
                        <span class="field-label">PSU ID</span>
                        <span class="field-value">{psu_id}</span>
                    </div>
                    <div class="field-group">
                        <span class="field-label">Academic Program</span>
                        <span class="field-value">{major}</span>
                    </div>
                    <div class="field-group">
                        <span class="field-label">Enrollment Status</span>
                        <div>
                            <span class="status-box">
                                <span class="status-check"></span> Enrolled
                            </span>
                        </div>
                    </div>
                </div>

                <div class="report-date">
                    Data retrieved: {date_str}
                </div>

                <table>
                    <thead>
                        <tr>
                            <th style="width:10%">Class Nbr</th>
                            <th style="width:12%">Course</th>
                            <th style="width:30%">Title</th>
                            <th style="width:25%">Days & Times</th>
                            <th style="width:15%">Room</th>
                            <th style="width:8%">Units</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>14920</td><td class="course-code">CMPSC 465</td><td>Data Structures and Algorithms</td><td>MoWeFr 10:10AM - 11:00AM</td><td>Willard 062</td><td>3.00</td></tr>
                        <tr><td>18233</td><td class="course-code">MATH 230</td><td>Calculus and Vector Analysis</td><td>TuTh 1:35PM - 2:50PM</td><td>Thomas 102</td><td>4.00</td></tr>
                        <tr><td>20491</td><td class="course-code">CMPSC 473</td><td>Operating Systems Design</td><td>MoWe 2:30PM - 3:45PM</td><td>Westgate E201</td><td>3.00</td></tr>
                        <tr><td>11029</td><td class="course-code">ENGL 202C</td><td>Technical Writing</td><td>Fr 1:25PM - 2:15PM</td><td>Boucke 304</td><td>3.00</td></tr>
                        <tr><td>15502</td><td class="course-code">STAT 318</td><td>Elementary Probability</td><td>TuTh 9:05AM - 10:20AM</td><td>Osmond 112</td><td>3.00</td></tr>
                    </tbody>
                </table>

                <div class="footer">
                    &copy; 2025 <b>{uni_name_footer}</b>. All rights reserved.<br>
                    LionPATH is the student information system for Penn State.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html, psu_id, major, uni_name_footer

def render_image(html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Viewport ligeramente más ancho para coincidir con la referencia
        page = browser.new_page(viewport={'width': 1200, 'height': 950})
        page.set_content(html_content, wait_until='networkidle')
        screenshot_bytes = page.screenshot(type='png')
        browser.close()
        return screenshot_bytes

