// Test our dual-layout implementation
console.log("Testing dual-layout functionality...");

// Check if functions are properly exposed
if (typeof switchToLayout === 'function') {
    console.log("✅ switchToLayout function is available");
} else {
    console.log("❌ switchToLayout function is NOT available");
}

if (typeof calculateCircleRadius === 'function') {
    console.log("✅ calculateCircleRadius function is available");
} else {
    console.log("❌ calculateCircleRadius function is NOT available");
}

// Test the circle radius calculation
try {
    const testNode = { importance: 0.8 };
    const radius = calculateCircleRadius(testNode);
    console.log(`🔍 Circle radius for importance 0.8: ${radius}px`);
} catch (error) {
    console.log("❌ Error testing calculateCircleRadius:", error);
}

// Test layout switching
try {
    switchToLayout("force");
    console.log("✅ Successfully switched to force layout");
    
    setTimeout(() => {
        switchToLayout("hierarchical");
        console.log("✅ Successfully switched back to hierarchical layout");
    }, 2000);
} catch (error) {
    console.log("❌ Error testing layout switching:", error);
}
