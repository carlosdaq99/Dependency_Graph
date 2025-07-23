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
            /* Light theme variables (default) */
            --bg-primary: #f8f9fa;
            --bg-secondary: #ffffff;
            --bg-container: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --text-primary: #333333;
            --text-secondary: #666666;
            --text-muted: #888888;
            --border-color: #e9ecef;
            --border-color-hover: #dee2e6;
            --shadow-light: rgba(0,0,0,0.1);
            --shadow-medium: rgba(0,0,0,0.2);
            --shadow-heavy: rgba(0,0,0,0.3);
            --accent-color: #ff6600;
            --accent-color-hover: #e55a00;
            --graph-bg: #ffffff;
            --node-stroke: #333333;
            --link-color: #666666;
            --control-bg: #ffffff;
            --control-border: #e9ecef;
            --button-bg: #f8f9fa;
            --button-hover: #e9ecef;
            --input-bg: #ffffff;
            --input-border: #ced4da;
            
            /* Color definitions */
            --accent-color: #ff6600;       /* Orange for direct connections */
            --path-color: #3b82f6;         /* Blue for path connections */
            --text-primary: #24292f;       /* Main text color for light theme */
            --text-secondary: #656d76;     /* Secondary text color */
            --bg-primary: #ffffff;         /* Main background */
            --bg-secondary: #f6f8fa;       /* Secondary background */
            --bg-tertiary: #f6f8fa;        /* Cards, panels */
            --border-color: #d0d7de;       /* General borders */
            --hotspot-color: #ff4444;      /* Performance hotspot indicator */
            
            /* Unified transparency settings for dimmed elements */
            --dimmed-opacity: 0.05;
            --dimmed-link-opacity: 0.15;
            --dimmed-text-opacity: 0.1;  /* Increased for better text visibility */
        }

        [data-theme="dark"] {
            /* Professional Dark Theme - Modern & Clean */
            
            /* Primary background colors using sophisticated grays */
            --bg-primary: #092748;          /* Deep charcoal for main background */
            --bg-secondary: #98c3d8;        /* Slightly lighter for panels */
            --bg-container: linear-gradient(135deg, #125566 0%, #2e7f91 100%);  /* Subtle professional gradient */
            
            /* Text colors with proper contrast hierarchy */
            --text-primary: #000000;        /* Soft white for primary text - easier on eyes */
            --text-secondary: #1c1c1e;      /* Muted gray for secondary text */
            --text-muted: #50555b;          /* Subtle gray for less important text */
            
            /* Border and structural colors */
            --border-color: #30363d;        /* Professional border gray */
            --border-color-hover: #484f58;  /* Lighter on hover */
            
            /* Shadow system using deep blues instead of pure black */
            --shadow-light: rgba(16, 22, 35, 0.3);   /* Subtle depth */
            --shadow-medium: rgba(16, 22, 35, 0.5);  /* Medium depth */
            --shadow-heavy: rgba(16, 22, 35, 0.7);   /* Strong depth */
            
            /* Accent colors - professional blue palette */
            --accent-color: #58a6ff;        /* Modern blue accent */
            --accent-color-hover: #79b8ff;  /* Lighter blue on hover */
            
            /* Graph-specific colors */
            --graph-bg: #092748;           /* Consistent with main background */
            --node-stroke: #58a6ff;        /* Blue stroke for better visibility */
            --link-color: #dae0e8;         /* Muted gray for links */
            
            /* Color definitions */
            --accent-color: #ff6600;       /* Orange for direct connections */
            --path-color: #3b82f6;         /* Blue for path connections */
            --text-primary: #f0f6fc;       /* Light text for dark theme */
            --text-secondary: #7d8590;     /* Secondary text */
            --bg-primary: #0d1117;         /* Main background */
            --bg-secondary: #161b22;       /* Secondary background */
            --bg-tertiary: #21262d;        /* Cards, panels */
            --border-color: #30363d;       /* General borders */
            --hotspot-color: #ff4444;      /* Performance hotspot indicator */
            
            /* Control panel styling */
            --control-bg: #1d5b69;         /* Slightly different from main for distinction */
            --control-border: #30363d;     /* Consistent border */
            --button-bg: #6abfd5;          /* Button background */
            --button-hover: #6abfd5;       /* Button hover state */
            --input-bg: #85bfd2;           /* Input field background */
            --input-border: #30363d;       /* Input field border */
            
            /* Unified transparency settings remain the same for dark theme */
            --dimmed-opacity: 0.05;
            --dimmed-link-opacity: 0.15;
            --dimmed-text-opacity: 0.1;  /* Increased for better text visibility */
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
