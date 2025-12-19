from flask import Flask, request, render_template_string
import base64
from generators import generate_random_identity, get_psu_html, render_image

app = Flask(__name__)

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IdentityGen Dashboard</title>
    
    <!-- Font Awesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            /* PALETA PLOMO-PLATA ELEGANTE */
            --bg-primary: #1a1d25;       /* Negro suave azulado */
            --bg-secondary: #21252e;     /* Plomo oscuro */
            --bg-tertiary: #14161c;      /* Negro profundo pero no extremo */
            --bg-card: #252932;          /* Card plomo azulado */
            --bg-card-hover: #2d323d;    /* Card hover plomo claro */
            --sidebar-bg: #181b22;       /* Sidebar plomo oscuro */

            /* Bordes Plateados Sutiles */
            --border: rgba(139, 148, 168, 0.08);
            --border-light: rgba(148, 163, 184, 0.14);
            --border-bright: rgba(176, 190, 212, 0.22);

            /* Texto Plata y Plomo */
            --text-primary: #e2e8f0;     /* Plata brillante */
            --text-secondary: #b4bdd0;   /* Plata media */
            --text-muted: #8b93a7;       /* Plomo claro */
            --text-dim: #6b7280;         /* Plomo medio */

            /* Acento Azul Plateado */
            --accent: #5b8def;           /* Azul plata vibrante */
            --accent-dark: #4a76d6;      /* Azul plata oscuro */
            --accent-light: #7ca8f5;     /* Azul plata claro */
            --accent-bg: rgba(91, 141, 239, 0.1);
            --accent-glow: rgba(91, 141, 239, 0.25);

            /* Estados */
            --green: #4ade80;
            --green-glow: rgba(74, 222, 128, 0.2);
            --yellow: #fbbf24;
            --red: #f87171;
            --cyan: #22d3ee;

            /* Sombras Suaves pero Profundas */
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.5);
            --shadow-md: 0 3px 10px rgba(0, 0, 0, 0.6);
            --shadow-lg: 0 8px 20px rgba(0, 0, 0, 0.7);
            --shadow-xl: 0 16px 32px rgba(0, 0, 0, 0.75);

            /* Brillos Plateados */
            --shine-top: inset 0 1px 0 rgba(226, 232, 240, 0.06);
            --shine-bottom: inset 0 -1px 0 rgba(0, 0, 0, 0.3);

            /* Gradientes */
            --gradient-silver: linear-gradient(135deg, rgba(226, 232, 240, 0.04), rgba(139, 147, 168, 0.02));
            --gradient-card: linear-gradient(180deg, rgba(255, 255, 255, 0.03), transparent);
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            line-height: 1.5;
            font-size: 14px;
        }

        /* Gradiente sutil */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.03), transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        .app-container {
            display: flex;
            min-height: 100vh;
            position: relative;
            z-index: 1;
        }

        /* ========== SIDEBAR ========== */
        .sidebar {
            width: 240px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            z-index: 1000;
            box-shadow: 4px 0 16px rgba(0, 0, 0, 0.8);
        }

        .logo-section {
            padding: 20px 16px;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--accent), var(--accent-dark));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4), var(--shine-top);
        }

        .logo-text {
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.3px;
        }

        .nav-menu {
            flex: 1;
            padding: 16px 10px;
            overflow-y: auto;
        }

        .nav-menu::-webkit-scrollbar { width: 3px; }
        .nav-menu::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 2px; }

        .nav-section {
            margin-bottom: 24px;
        }

        .nav-section-title {
            font-size: 9px;
            text-transform: uppercase;
            color: var(--text-dim);
            font-weight: 700;
            letter-spacing: 1px;
            padding: 0 10px 8px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
            margin-bottom: 3px;
            font-size: 13px;
            font-weight: 500;
            position: relative;
        }

        .nav-item i {
            width: 18px;
            text-align: center;
            font-size: 14px;
        }

        .nav-item:hover {
            background: rgba(255, 255, 255, 0.04);
            color: var(--text-primary);
            transform: translateX(2px);
        }

        .nav-item.active {
            background: var(--accent-bg);
            color: white;
            font-weight: 600;
            box-shadow: var(--shadow-sm);
        }

        .nav-item.active::before {
            content: '';
            position: absolute;
            left: 0; top: 50%;
            transform: translateY(-50%);
            width: 2px; height: 16px;
            background: var(--accent);
            border-radius: 0 2px 2px 0;
        }

        .nav-item .badge {
            margin-left: auto;
            background: var(--accent);
            color: white;
            font-size: 8px;
            padding: 2px 6px;
            border-radius: 8px;
            font-weight: 700;
        }

        .sidebar-footer {
            padding: 12px;
            border-top: 1px solid var(--border);
            background: rgba(0, 0, 0, 0.2);
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 8px;
            transition: all 0.2s;
            cursor: pointer;
        }

        .user-profile:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--border-light);
        }

        .user-avatar {
            width: 32px; height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-dark));
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 12px;
            box-shadow: var(--shadow-sm);
        }

        .user-info h4 {
            font-size: 12px;
            font-weight: 600;
        }

        .user-info p {
            font-size: 10px;
            color: var(--text-muted);
        }

        .version-badge {
            text-align: center;
            padding: 10px;
            font-size: 9px;
            color: var(--text-dim);
        }

        /* ========== MAIN CONTENT ========== */
        .main-content {
            flex: 1;
            margin-left: 240px;
        }

        /* Top Bar */
        .top-bar {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        }

        .top-bar h2 {
            font-size: 15px;
            font-weight: 700;
        }

        .top-bar-actions {
            display: flex;
            gap: 8px;
        }

        .icon-btn {
            width: 34px; height: 34px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
            box-shadow: var(--shine-top);
        }

        .icon-btn:hover {
            background: var(--bg-card-hover);
            color: var(--text-primary);
            border-color: var(--border-light);
            transform: translateY(-1px);
        }

        .icon-btn .notification-dot {
            position: absolute;
            top: 6px; right: 6px;
            width: 5px; height: 5px;
            background: var(--red);
            border-radius: 50%;
            border: 1px solid var(--bg-card);
        }

        /* Content Area */
        .content-area {
            padding: 24px 28px;
        }

        /* Breadcrumbs */
        .breadcrumbs {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 16px;
            font-size: 12px;
            color: var(--text-muted);
        }

        .breadcrumbs a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.2s;
        }

        .breadcrumbs a:hover { color: var(--text-primary); }
        .breadcrumbs .separator { color: var(--text-dim); }
        .breadcrumbs .current { color: var(--text-primary); font-weight: 600; }

        /* Page Header */
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
        }

        .page-title {
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        }

        .page-subtitle {
            color: var(--text-secondary);
            font-size: 13px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.1);
            color: var(--green);
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .status-dot {
            width: 5px; height: 5px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 6px var(--green);
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 18px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-md), var(--shine-top);
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(226, 232, 240, 0.2), transparent);
        }

        .stat-card::after {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 50% 0%, var(--accent-glow), transparent 70%);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .stat-card:hover {
            border-color: var(--border-bright);
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg), 0 0 20px var(--accent-glow), var(--shine-top);
        }

        .stat-card:hover::after {
            opacity: 1;
        }

        .stat-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }

        .stat-label i {
            font-size: 12px;
            color: var(--accent-light);
            filter: drop-shadow(0 0 4px var(--accent-glow));
        }

        .stat-value {
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 4px;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            z-index: 1;
        }

        .stat-change {
            font-size: 11px;
            color: var(--green);
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            position: relative;
            z-index: 1;
        }

        /* Success Alert */
        .alert {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-left: 3px solid var(--green);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s;
            box-shadow: var(--shadow-sm);
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .alert i {
            color: var(--green);
            font-size: 16px;
        }

        .alert-content h4 {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 2px;
        }

        .alert-content p {
            font-size: 11px;
            color: var(--text-secondary);
        }

        /* Tabs con 3D */
        .tabs-container {
            display: flex;
            gap: 6px;
            margin-bottom: 24px;
            background: var(--bg-secondary);
            padding: 5px;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow-md), var(--shine-bottom);
        }

        .tab-btn {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 10px 18px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .tab-btn i { font-size: 13px; }

        .tab-btn:hover:not(.disabled) {
            background: rgba(255, 255, 255, 0.04);
            color: var(--text-primary);
        }

        .tab-btn.active {
            background: var(--bg-card);
            color: white;
            box-shadow: var(--shadow-sm), var(--shine-top);
        }

        .tab-btn.disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }

        .tab-content.active { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cards con 3D FUERTE */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 14px;
            padding: 24px;
            box-shadow: var(--shadow-lg), var(--shine-top);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        /* Brillo 3D superior */
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        }

        /* Sombra 3D inferior */
        .card::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,0,0,0.3), transparent);
        }

        .card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-xl), var(--shine-top);
            border-color: var(--border-bright);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .card-title {
            font-size: 15px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-title i { color: var(--accent); }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 50px 24px;
        }

        .empty-icon {
            width: 90px; height: 90px;
            margin: 0 auto 20px;
            background: var(--accent-bg);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(99, 102, 241, 0.2);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2), var(--shine-top);
        }

        .empty-icon i {
            font-size: 38px;
            color: var(--accent);
        }

        .empty-state h3 {
            font-size: 20px;
            margin-bottom: 8px;
            font-weight: 700;
        }

        .empty-state p {
            color: var(--text-secondary);
            margin-bottom: 24px;
            max-width: 420px;
            margin-left: auto;
            margin-right: auto;
            font-size: 13px;
        }

        .keyboard-hint {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 10px;
            color: var(--text-dim);
            margin-top: 14px;
        }

        .kbd {
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            padding: 2px 7px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 9px;
            box-shadow: var(--shine-top);
        }

        /* Buttons con 3D */
        .btn {
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            text-decoration: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-dark));
            color: white;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4), var(--shine-top);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        .btn-secondary {
            background: var(--bg-card-hover);
            color: var(--text-primary);
            border: 1px solid var(--border-light);
            box-shadow: var(--shine-top);
        }

        .btn-secondary:hover {
            border-color: var(--border-bright);
            background: rgba(255, 255, 255, 0.08);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }

        .spinner {
            width: 12px; height: 12px;
            border: 2px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        /* Data Grid */
        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 14px;
            margin-bottom: 20px;
        }

        .data-field {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            transition: all 0.2s;
            box-shadow: var(--shine-top);
        }

        .data-field:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--border-light);
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm), var(--shine-top);
        }

        .field-label {
            font-size: 9px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 7px;
            display: flex;
            align-items: center;
            gap: 5px;
            font-weight: 600;
        }

        .field-label i { color: var(--text-dim); }

        .field-value-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
        }

        .field-value {
            font-family: 'SF Mono', Consolas, monospace;
            font-size: 12px;
            font-weight: 600;
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .copy-btn {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 5px 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 10px;
        }

        .copy-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-primary);
            transform: scale(1.05);
        }

        .copy-btn.copied {
            background: rgba(16, 185, 129, 0.2);
            border-color: var(--green);
            color: var(--green);
        }

        /* Preview CENTRADO con 3D */
        .preview-container {
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
            text-align: center;
        }

        .preview-label {
            font-size: 11px;
            color: var(--text-secondary);
            margin-bottom: 14px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-weight: 600;
        }

        .preview-img {
            max-width: 100%;
            max-height: 480px;
            border-radius: 12px;
            border: 1px solid var(--border-light);
            box-shadow: var(--shadow-xl), var(--shine-top);
            transition: transform 0.3s;
        }

        .preview-img:hover {
            transform: scale(1.02);
        }

        .coming-soon {
            font-size: 9px;
            color: var(--yellow);
            background: rgba(245, 158, 11, 0.15);
            padding: 2px 7px;
            border-radius: 8px;
            font-weight: 700;
            border: 1px solid rgba(245, 158, 11, 0.25);
        }

        /* Footer */
        .content-footer {
            margin-top: 32px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 11px;
            color: var(--text-dim);
        }

        .content-footer a {
            color: var(--accent);
            text-decoration: none;
        }

        .content-footer a:hover { text-decoration: underline; }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar { width: 60px; }
            .sidebar .logo-text,
            .sidebar .nav-item span,
            .sidebar .nav-section-title,
            .sidebar .user-info,
            .version-badge { display: none; }
            .sidebar .nav-item { justify-content: center; }
            .main-content { margin-left: 60px; }
            .top-bar { padding: 10px 16px; }
            .content-area { padding: 16px; }
            .page-header { flex-direction: column; gap: 10px; }
            .tabs-container { flex-direction: column; }
            .data-grid, .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

<div class="app-container">
    <!-- SIDEBAR -->
    <aside class="sidebar">
        <div class="logo-section">
            <div class="logo">
                <div class="logo-icon">
                    <i class="fa-solid fa-fingerprint"></i>
                </div>
                <span class="logo-text">IdentityGen</span>
            </div>
        </div>
        
        <nav class="nav-menu">
            <div class="nav-section">
                <div class="nav-section-title">MAIN</div>
                <a href="/" class="nav-item active">
                    <i class="fa-solid fa-house"></i>
                    <span>Dashboard</span>
                </a>
                <div class="nav-item">
                    <i class="fa-solid fa-clock-rotate-left"></i>
                    <span>History</span>
                    <span class="badge">Soon</span>
                </div>
            </div>

            <div class="nav-section">
                <div class="nav-section-title">GENERATORS</div>
                <a href="/" class="nav-item active">
                    <i class="fa-solid fa-graduation-cap"></i>
                    <span>PSU Identity</span>
                </a>
                <div class="nav-item">
                    <i class="fa-solid fa-brain"></i>
                    <span>AI Generator</span>
                    <span class="badge">Soon</span>
                </div>
                <div class="nav-item">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                    <span>Perxfef</span>
                    <span class="badge">Soon</span>
                </div>
            </div>

            <div class="nav-section">
                <div class="nav-section-title">SETTINGS</div>
                <div class="nav-item">
                    <i class="fa-solid fa-sliders"></i>
                    <span>Preferences</span>
                </div>
                <div class="nav-item">
                    <i class="fa-solid fa-circle-question"></i>
                    <span>Help</span>
                </div>
            </div>
        </nav>

        <div class="sidebar-footer">
            <div class="user-profile">
                <div class="user-avatar">U</div>
                <div class="user-info">
                    <h4>User</h4>
                    <p>Premium</p>
                </div>
            </div>
        </div>

        <div class="version-badge">v1.0.0-beta</div>
    </aside>

    <!-- MAIN -->
    <main class="main-content">
        <!-- Top Bar -->
        <div class="top-bar">
            <h2>IdentityGen Dashboard</h2>
            <div class="top-bar-actions">
                <div class="icon-btn" title="Notifications">
                    <i class="fa-solid fa-bell"></i>
                    <span class="notification-dot"></span>
                </div>
                <div class="icon-btn" title="Settings">
                    <i class="fa-solid fa-gear"></i>
                </div>
            </div>
        </div>

        <!-- Content Area -->
        <div class="content-area">
            <!-- Breadcrumbs -->
            <nav class="breadcrumbs">
                <a href="/"><i class="fa-solid fa-house"></i></a>
                <span class="separator">/</span>
                <a href="/">Dashboard</a>
                <span class="separator">/</span>
                <span class="current">PSU Generator</span>
            </nav>

            <!-- Page Header -->
            <div class="page-header">
                <div>
                    <h1 class="page-title">Identity Generator</h1>
                    <p class="page-subtitle">Create synthetic identities for testing purposes</p>
                </div>
                <div class="status-pill">
                    <span class="status-dot"></span>
                    System Online
                </div>
            </div>

            <!-- Stats -->
            {% if generated %}
            

            <div class="alert">
                <i class="fa-solid fa-circle-check"></i>
                <div class="alert-content">
                    <h4>Identity Generated Successfully</h4>
                    <p>Your PSU student identity has been created and is ready for download.</p>
                </div>
            </div>
            {% endif %}

            <!-- TABS -->
            <div class="tabs-container">
                <button class="tab-btn active" onclick="switchTab(event, 'psu')">
                    <i class="fa-solid fa-graduation-cap"></i>
                    PSU Generator
                </button>
                <button class="tab-btn disabled">
                    <i class="fa-solid fa-brain"></i>
                    AI Generator
                    <span class="coming-soon">Soon</span>
                </button>
                <button class="tab-btn disabled">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                    Perxfef
                    <span class="coming-soon">Soon</span>
                </button>
            </div>

            <!-- TAB: PSU -->
            <div id="tab-psu" class="tab-content active">
                {% if not generated %}
                <div class="card">
                    <div class="empty-state">
                        <div class="empty-icon">
                            <i class="fa-solid fa-bolt"></i>
                        </div>
                        <h3>Generate PSU Identity</h3>
                        <p>Create a complete Penn State student profile with documentation for testing verification systems.</p>
                        <form action="/generate" method="POST" onsubmit="handleGenerate(this)">
                            <button type="submit" class="btn btn-primary" id="gen-btn">
                                <i class="fa-solid fa-sparkles"></i>
                                <span id="btn-text">Generate Identity</span>
                                <span id="btn-loader" class="spinner" style="display:none;"></span>
                            </button>
                        </form>
                        <div class="keyboard-hint">
                            Press <span class="kbd">Ctrl</span> + <span class="kbd">G</span> to generate
                        </div>
                    </div>
                </div>
                {% else %}
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">
                            <i class="fa-solid fa-id-card"></i>
                            Generated Identity Details
                        </div>
                        <form action="/generate" method="POST" onsubmit="handleGenerate(this)" style="margin:0;">
                            <button type="submit" class="btn btn-secondary" id="regen-btn">
                                <i class="fa-solid fa-arrows-rotate"></i>
                                <span id="regen-text">Regenerate</span>
                                <span id="regen-loader" class="spinner" style="display:none;"></span>
                            </button>
                        </form>
                    </div>

                    <div class="data-grid">
                        <div class="data-field">
                            <span class="field-label"><i class="fa-solid fa-user"></i> Full Name</span>
                            <div class="field-value-row">
                                <span class="field-value">{{ name }}</span>
                                <button class="copy-btn" onclick="copyText('{{ name }}', this)">
                                    <i class="fa-solid fa-copy"></i>
                                </button>
                            </div>
                        </div>

                        <div class="data-field">
                            <span class="field-label"><i class="fa-solid fa-envelope"></i> Email</span>
                            <div class="field-value-row">
                                <span class="field-value">{{ email }}</span>
                                <button class="copy-btn" onclick="copyText('{{ email }}', this)">
                                    <i class="fa-solid fa-copy"></i>
                                </button>
                            </div>
                        </div>

                        <div class="data-field">
                            <span class="field-label"><i class="fa-solid fa-id-badge"></i> Student ID</span>
                            <div class="field-value-row">
                                <span class="field-value">{{ psu_id }}</span>
                                <button class="copy-btn" onclick="copyText('{{ psu_id }}', this)">
                                    <i class="fa-solid fa-copy"></i>
                                </button>
                            </div>
                        </div>

                        <div class="data-field">
                            <span class="field-label"><i class="fa-solid fa-book-open"></i> Program</span>
                            <div class="field-value-row">
                                <span class="field-value">{{ major }}</span>
                                <button class="copy-btn" onclick="copyText('{{ major }}', this)">
                                    <i class="fa-solid fa-copy"></i>
                                </button>
                            </div>
                        </div>

                        <div class="data-field" style="grid-column: 1 / -1;">
                            <span class="field-label"><i class="fa-solid fa-building-columns"></i> University</span>
                            <div class="field-value-row">
                                <span class="field-value">{{ uni_name }}</span>
                                <button class="copy-btn" onclick="copyText('{{ uni_name }}', this)">
                                    <i class="fa-solid fa-copy"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                    <a href="data:image/png;base64,{{ img_b64 }}" download="{{ filename }}" class="btn btn-primary" style="width:100%;">
                        <i class="fa-solid fa-download"></i>
                        Download Official Document ({{ filename }})
                    </a>

                    <div class="preview-container">
                        <span class="preview-label">
                            <i class="fa-solid fa-image"></i>
                            Document Preview
                        </span>
                        <br>
                        <img src="data:image/png;base64,{{ img_b64 }}" class="preview-img" alt="Document">
                    </div>
                </div>
                {% endif %}
            </div>

            <!-- TAB: AI -->
            <div id="tab-ai" class="tab-content">
                <div class="card">
                    <div class="empty-state">
                        <div class="empty-icon">
                            <i class="fa-solid fa-brain"></i>
                        </div>
                        <h3>AI Generator Coming Soon</h3>
                        <p>Advanced AI-powered identity generation with machine learning capabilities.</p>
                    </div>
                </div>
            </div>

            <!-- TAB: Perxfef -->
            <div id="tab-perxfef" class="tab-content">
                <div class="card">
                    <div class="empty-state">
                        <div class="empty-icon">
                            <i class="fa-solid fa-wand-magic-sparkles"></i>
                        </div>
                        <h3>Perxfef Module Coming Soon</h3>
                        <p>This advanced feature is currently in development.</p>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="content-footer">
                IdentityGen v1.0.0-beta &nbsp;•&nbsp; Made with <i class="fa-solid fa-heart" style="color:var(--red);"></i> for testing &nbsp;•&nbsp; 
                <a href="#">Documentation</a> &nbsp;•&nbsp; 
                <a href="#">Support</a>
            </div>
        </div>
    </main>
</div>

<script>
    function switchTab(event, tab) {
        if (event.target.closest('.disabled')) return;
        
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        event.currentTarget.classList.add('active');
        document.getElementById('tab-' + tab).classList.add('active');
    }

    function copyText(text, btn) {
        navigator.clipboard.writeText(text).then(() => {
            const icon = btn.querySelector('i');
            icon.className = 'fa-solid fa-check';
            btn.classList.add('copied');
            
            setTimeout(() => {
                icon.className = 'fa-solid fa-copy';
                btn.classList.remove('copied');
            }, 2000);
        });
    }

    function handleGenerate(form) {
        const btn = form.querySelector('button');
        const textSpan = btn.querySelector('span[id$="-text"]');
        const loaderSpan = btn.querySelector('span[id$="-loader"]');
        
        btn.disabled = true;
        if (textSpan) textSpan.style.display = 'none';
        if (loaderSpan) loaderSpan.style.display = 'inline-block';
    }

    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
            e.preventDefault();
            const genBtn = document.getElementById('gen-btn');
            if (genBtn && !genBtn.disabled) {
                genBtn.click();
            }
        }
    });
</script>

</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(DASHBOARD_TEMPLATE, generated=False)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        identity = generate_random_identity()
        html, psu_id, major, uni_name = get_psu_html(identity)
        img_bytes = render_image(html)
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        clean_filename = f"{identity['first_name']}-{identity['last_name']}.png"

        return render_template_string(
            DASHBOARD_TEMPLATE,
            generated=True,
            name=identity['full_name'],
            email=identity['email'],
            psu_id=psu_id,
            major=major,
            uni_name=uni_name,
            img_b64=img_b64,
            filename=clean_filename
        )
    except Exception as e:
        return f"<div style='background:#1c1c24;color:#e8e8ec;padding:60px;text-align:center;'><h2>Error</h2><p>{e}</p><a href='/' style='color:#6366f1'>← Back</a></div>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
