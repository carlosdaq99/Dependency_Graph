"""
Base Styles Module
=================

Core CSS styling including theme variables, basic elements, and foundational styles.
Contains theme definitions, variable declarations, and fundamental component styling.
"""


def get_base_styles_css() -> str:
    """
    Get CSS for base styles, themes, and core components.

    Returns:
        str: CSS code for base styling and theme support
    """
    return """
        :root {
            /* ===== Light Theme Variables (Default) ===== */
            --bg-primary: #f8f9fa;           /* Main app background (body, graph area) */
            --bg-secondary: #ffffff;         /* Secondary background (panels, cards) */
            --bg-container: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Graph container background gradient */
            --text-primary: #333333;         /* Primary text color (high contrast) */
            --text-secondary: #666666;       /* Secondary text color (subheadings, less important info) */
            --text-muted: #888888;           /* Muted text color (hints, disabled, less visible) */
            --border-color: #e9ecef;         /* Standard border color for UI elements */
            --border-color-hover: #dee2e6;   /* Border color on hover/focus */
            --shadow-light: rgba(0,0,0,0.1); /* Light shadow for subtle elevation */
            --shadow-medium: rgba(0,0,0,0.2);/* Medium shadow for modals, overlays */
            --shadow-heavy: rgba(0,0,0,0.3); /* Heavy shadow for strong elevation */
            --accent-color: #ff6600;         /* Accent color for buttons, highlights, direct connections */
            --accent-color-hover: #e55a00;   /* Accent color on hover (buttons, links) */
            --graph-bg: #ffffff;             /* Graph SVG background */
            --node-stroke: #333333;          /* Node border color in graph */
            --link-color: #666666;           /* Link/edge color in graph */
            --control-bg: #ffffff;           /* Sidebar/control panel background */
            --control-border: #e9ecef;       /* Sidebar/control panel border */
            --button-bg: #f8f9fa;            /* Button background */
            --button-hover: #e9ecef;         /* Button background on hover */
            --input-bg: #ffffff;             /* Input field background */
            --input-border: #ced4da;         /* Input field border */

            /* ===== Graph/Connection Colors ===== */
            --accent-color: #ff6600;         /* Direct connection edge color (orange) */
            --path-color: #3b82f6;           /* Path connection edge color (blue) */
            --mixed-edge-color: #3b82f6;     /* Mixed edge color (blue, for hybrid connections) */

            /* ===== Text Colors ===== */
            --text-primary: #24292f;         /* Main text color for light theme (body, headings) */
            --text-secondary: #656d76;       /* Secondary text color (subheadings, meta info) */

            /* ===== Background Colors ===== */
            --bg-primary: #ffffff;           /* Main background for app body */
            --bg-secondary: #f6f8fa;         /* Secondary background for panels/cards */
            --bg-tertiary: #f6f8fa;          /* Tertiary background for cards/panels */

            /* ===== Border & Hotspot Colors ===== */
            --border-color: #d0d7de;         /* General border color for UI elements */
            --hotspot-color: #ff4444;        /* Performance hotspot indicator (red) */

            /* ===== Transparency for Dimmed Elements ===== */
            --dimmed-opacity: 0.3;             /* Opacity for dimmed nodes/elements */
            --dimmed-link-opacity: 0.1;        /* Opacity for dimmed links/edges */
            --dimmed-text-opacity: 0.3;       /* Opacity for dimmed text (improved visibility) */
        }

        [data-theme="dark"] {
            /* ===== Dark Theme Variables ===== */
            --graph-bg: #092748;               /* Graph SVG background (matches main background) */
            --node-stroke: #000000;            /* Node border color in graph */
            --link-color: #dae0e8;             /* Link/edge color in graph (muted gray) */

            /* ===== Graph/Connection Colors ===== */
            --accent-color: #ff6600;           /* Direct connection edge color (orange) */
            --path-color: #3b82f6;             /* Path connection edge color (blue) */
            --mixed-edge-color: #3b82f6;     /* Mixed edge color (blue, for hybrid connections) */

            /* ===== Text Colors  ===== */
            --text-primary: #262a2f;           /* Main text color for dark theme (body, headings) */
            --text-secondary: #0c0c0c;         /* Secondary text color (subheadings, meta info) */

            /* ===== Background Colors ===== */
            --input-bg: #85bfd2;               /* Control Panel background (dark mode) */
            --bg-secondary: #d2f6f7c6;           /* Background for panels/cards (dark mode) */
            --bg-primary: #272833;             /* Main background for app body (dark mode) */
            --bg-tertiary: #e123c1;            /* Tertiary background for cards/panels (dark mode) */

            /* ===== Border & Hotspot Colors ===== */
            --border-color: #30363d;           /* General border color for UI elements (dark mode) */
            --hotspot-color: #ffe23c;          /* Performance hotspot indicator (yellow) */

            /* ===== Control Panel & Input Styling ===== */
            --control-bg: #1d5b69;             /* Sidebar/control panel background (dark mode) */
            --control-border: #292f29;         /* Sidebar/control panel border (dark mode) */
            --button-bg: #6abfd5;              /* Button background (dark mode) */
            --button-hover: #6abfd5;           /* Button background on hover (dark mode) */
            --input-border: #b6e1e4;           /* Input field border (dark mode) */

            /* ===== Transparency for Dimmed Elements ===== */
            --dimmed-opacity: 0.3;             /* Opacity for dimmed nodes/elements */
            --dimmed-link-opacity: 0.1;        /* Opacity for dimmed links/edges */
            --dimmed-text-opacity: 0.3;       /* Opacity for dimmed text (improved visibility) */
        }

        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        
        .container {
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        
        .controls {
            width: 400px;  /* Increased width for theme toggle */
            background: var(--control-bg);
            border-right: 2px solid var(--border-color);
            padding: 20px;
            overflow-y: auto;
            box-shadow: 2px 0 8px var(--shadow-light);
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }
        
        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--button-bg);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 14px;
            color: var(--text-primary);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 1000;
        }
        
        .theme-toggle:hover {
            background: var(--button-hover);
            border-color: var(--border-color-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow-medium);
        }
        
        .theme-icon {
            font-size: 16px;
            transition: transform 0.3s ease;
        }
        
        .theme-toggle:hover .theme-icon {
            transform: rotate(180deg);
        }
        
        .graph-container {
            flex: 1;
            position: relative;
            background: var(--bg-container);
            transition: background 0.3s ease;
        }
        
        #graph {
            width: 100%;
            height: 100%;
            background: var(--graph-bg);
            cursor: grab;
            transition: background-color 0.3s ease;
        }
        
        #graph:active {
            cursor: grabbing;
        }

        /* Control panel styles with theme support */
        .section {
            margin-bottom: 25px;
            padding: 15px;
            background: var(--bg-secondary);
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .section h3 {
            margin: 0 0 15px 0;
            color: var(--text-primary);
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: color 0.3s ease;
        }

        /* Accessibility improvements */
        .folder-item:focus {
            outline: 2px solid #007bff;
            outline-offset: 2px;
        }
        
        .toggle-switch:focus {
            outline: 2px solid #007bff;
            outline-offset: 2px;
        }
        
        /* Loading states */
        .loading {
            opacity: 0.5;
            pointer-events: none;
        }
        
        .loading::after {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            margin: -10px 0 0 -10px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
            
            .controls {
                width: 100%;
                height: 300px;
                order: 2;
            }
            
            .graph-container {
                height: calc(100vh - 300px);
                order: 1;
            }
        }
    """
