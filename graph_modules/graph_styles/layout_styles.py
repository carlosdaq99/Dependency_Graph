"""
Layout Styles Module
===================

Layout-specific CSS including node styling, controls, animations, and responsive design.
Contains component layouts, interactive elements, and visual effects.
"""


def get_layout_styles_css() -> str:
    """
    Get CSS for layout-specific styles including nodes, controls, and animations.

    Returns:
        str: CSS code for layout styling and interactive components
    """
    return """
        /* Enhanced node styles with theme support */
        .node-rect {
            stroke: var(--node-stroke);
            stroke-width: 1.5;
            rx: 8;
            ry: 8;
            filter: drop-shadow(2px 2px 4px var(--shadow-medium));
            transition: all 0.2s ease;
        }
        
        .node-rect:hover {
            stroke-width: 2.5;
            filter: drop-shadow(3px 3px 8px var(--shadow-heavy));
        }
        
        .node-rect.highlighted {
            stroke: var(--accent-color);
            stroke-width: 3;
            filter: drop-shadow(0 0 12px var(--accent-color));
        }
        
        .node-rect.path-highlighted {
            stroke: var(--path-color);  /* Blue for path highlighting */
            stroke-width: 2.5;
            filter: drop-shadow(0 0 8px var(--path-color));
        }
        
        .node-rect.dimmed {
            opacity: var(--dimmed-opacity);
        }
        
        /* Force-directed circle node styles */
        .node-circle {
            stroke: var(--node-stroke);
            stroke-width: 1.5;
            filter: drop-shadow(2px 2px 4px var(--shadow-medium));
            transition: all 0.2s ease;
            /* Note: fill is set dynamically via d.color attribute */
        }
        
        .node-circle:hover {
            stroke-width: 2.5;
            filter: drop-shadow(3px 3px 8px var(--shadow-heavy));
        }
        
        .node-circle.highlighted {
            stroke: var(--accent-color);
            stroke-width: 3;
            filter: drop-shadow(0 0 12px var(--accent-color));
        }
        
        .node-circle.path-highlighted {
            stroke: var(--path-color);  /* Blue for path highlighting */
            stroke-width: 2.5;
            filter: drop-shadow(0 0 8px var(--path-color));
        }
        
        .node-circle.performance-hotspot {
            stroke: var(--hotspot-color);
            stroke-width: 3;
            filter: drop-shadow(0 0 10px var(--hotspot-color));
        }
        
        .node-rect.performance-hotspot {
            stroke: var(--hotspot-color);
            stroke-width: 3;
            filter: drop-shadow(0 0 10px var(--hotspot-color));
        }
        
        /* Performance hotspot warning icon */
        .performance-warning-icon {
            font-family: 'Arial Unicode MS', sans-serif;
            font-size: 12px;
            fill: var(--hotspot-color);
            text-anchor: middle;
            pointer-events: none;
        }
        
        .node-circle.dimmed {
            opacity: var(--dimmed-opacity);
        }
        
        .node-circle.hotspot {
            stroke: #ff3333;
            stroke-width: 2;
        }
        
        .node-rect.hotspot {
            stroke: #ff3333;
            stroke-width: 2;
        }
        
        /* Enhanced link styles with theme support */
        .link {
            fill: none;
            stroke: var(--link-color);
            stroke-width: 1.5;
            opacity: 0.8;
            transition: all 0.3s ease;
        }
        
        .link:hover {
            stroke-width: 2.5;
            opacity: 1;
        }
        
        .link.highlighted {
            stroke: var(--accent-color);  /* Orange for direct connections */
            stroke-width: 3;
            opacity: 1;
        }
        
        .link.path-highlighted {
            stroke: var(--path-color);  /* Blue for path highlighting */
            stroke-width: 2.5;
            opacity: 0.9;
        }
        
        .link.mixed-highlighted {
            stroke: var(--mixed-edge-color, #9c27b0);  /* Purple for mixed orange/blue edges */
            stroke-width: 2.8;
            opacity: 0.95;
        }
        
                /* Enhanced dimming styles - consolidated and prioritized */
        .link.dimmed {
            opacity: var(--dimmed-link-opacity) !important;
            transition: opacity 0.3s ease !important;
        }
        
        .node.dimmed {
            opacity: var(--dimmed-opacity) !important;
            transition: opacity 0.3s ease !important;
        }
        
        .node-label.dimmed {
            opacity: var(--dimmed-text-opacity) !important;
            transition: opacity 0.3s ease !important;
        }
        
        /* Mixed-category edge styles */
        .link.mixed-highlighted {
            stroke: var(--mixed-edge-color, #9c27b0) !important;  /* Purple for mixed edges */
            stroke-width: 2.8 !important;
            opacity: 0.95 !important;
        }
        
        .link.hidden {
            display: none;
        }
        
        .link.test-related {
            stroke-dasharray: 4,4;
        }
        
        /* Enhanced text styles with theme support */
        .node-label {
            font-size: 11px;
            font-weight: 600;
            text-anchor: middle;
            pointer-events: none;
            fill: var(--text-primary);
            transition: fill 0.3s ease;
        }

        .node-label.dimmed {
            opacity: var(--dimmed-text-opacity);
        }
        
        .folder-label-text {
            font-size: 9px;
            text-anchor: middle;
            pointer-events: none;
            fill: var(--text-secondary);
            font-style: italic;
            transition: fill 0.3s ease;
        }
        
        /* Control panel component styles */
        .folder-item {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            margin: 4px 0;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .folder-item:hover {
            background: #e3f2fd;
            border-color: #90caf9;
        }
        
        .folder-checkbox {
            font-size: 16px;
            margin-right: 10px;
            user-select: none;
        }
        
        .folder-color {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            margin-right: 10px;
            border: 1px solid #dee2e6;
        }
        
        .folder-label {
            flex: 1;
            font-size: 13px;
            font-weight: 500;
        }
        
        .folder-count {
            font-weight: normal;
            color: #6c757d;
            font-size: 11px;
        }
        
        .test-count {
            font-weight: normal;
            color: #fd7e14;
            font-size: 11px;
        }
        
        .reset-button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.2s ease;
            width: 100%;
        }
        
        .reset-button:hover {
            background: #0056b3;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .stat-item {
            background: white;
            padding: 8px;
            border-radius: 4px;
            text-align: center;
            border: 1px solid #dee2e6;
        }
        
        .stat-value {
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
        }
        
        .stat-label {
            font-size: 11px;
            color: #6c757d;
            text-transform: uppercase;
        }
        
        /* Tooltip styles */
        .tooltip {
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 10px;
            border-radius: 6px;
            pointer-events: none;
            font-size: 12px;
            max-width: 300px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        
        .importance-indicator {
            position: absolute;
            top: -8px;
            right: -8px;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #ffc107;
            border: 2px solid white;
            display: none;
        }
        
        .importance-indicator.high {
            display: block;
            background: #dc3545;
        }
        
        .importance-indicator.medium {
            display: block;
            background: #fd7e14;
        }
        
        .importance-indicator.low {
            display: block;
            background: #ffc107;
        }
        
        /* Layout toggle styles */
        .layout-toggle {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            margin-bottom: 15px;
        }
        
        .layout-toggle-label {
            font-size: 13px;
            font-weight: 500;
            color: #495057;
        }
        
        .toggle-switch {
            position: relative;
            width: 50px;
            height: 24px;
            background-color: #ccc;
            border-radius: 12px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .toggle-switch.active {
            background-color: #007bff;
        }
        
        .toggle-slider {
            position: absolute;
            top: 2px;
            left: 2px;
            width: 20px;
            height: 20px;
            background-color: white;
            border-radius: 50%;
            transition: transform 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .toggle-switch.active .toggle-slider {
            transform: translateX(26px);
        }
        
        .layout-mode-indicator {
            font-size: 11px;
            color: #6c757d;
            margin-top: 5px;
        }
        
        /* GitHub link styles with theme support */
        .github-link {
            position: absolute;
            bottom: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            text-decoration: none;
            color: var(--text-primary);
            font-size: 12px;
            transition: all 0.2s ease;
            z-index: 1000;
        }
        
        .github-link:hover {
            background: var(--button-hover);
            border-color: var(--border-color-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow-medium);
        }
        
        .github-icon {
            width: 16px;
            height: 16px;
            fill: currentColor;
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
        
        /* Animation effects for better user experience */
        .fade-in {
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .slide-in {
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
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
            
            .theme-toggle {
                top: 10px;
                right: 10px;
                padding: 6px 12px;
                font-size: 12px;
            }
            
            .github-link {
                bottom: 10px;
                right: 10px;
                padding: 6px 10px;
                font-size: 11px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .layout-toggle {
                padding: 10px;
            }
            
            .folder-item {
                padding: 6px 10px;
            }
        }
        
        @media (max-width: 480px) {
            .controls {
                height: 250px;
                padding: 15px;
            }
            
            .section {
                padding: 12px;
                margin-bottom: 20px;
            }
            
            .section h3 {
                font-size: 12px;
                margin-bottom: 10px;
            }
            
            .folder-label {
                font-size: 12px;
            }
            
            .folder-count, .test-count {
                font-size: 10px;
            }
            
            .stat-value {
                font-size: 16px;
            }
            
            .stat-label {
                font-size: 10px;
            }
        }
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {
            .node-rect, .node-circle {
                stroke-width: 2;
            }
            
            .link {
                stroke-width: 2;
            }
            
            .folder-item {
                border-width: 2px;
            }
            
            .section {
                border-width: 2px;
            }
        }
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
            
            .loading::after {
                animation: none;
            }
        }
    """
