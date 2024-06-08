//shoulder exercises

//lateral raises
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".lateralRaises").style.display = "none";
    }
});

lateralRaises.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".lateralRaises").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".lateralRaises").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//front raises
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".frontRaises").style.display = "none";
    }
});

frontRaises.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".frontRaises").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".frontRaises").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//arnold shoulder press
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".arnoldShoulderPress").style.display = "none";
    }
});

arnoldShoulderPress.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".arnoldShoulderPress").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".arnoldShoulderPress").scrollIntoView({ 
        behavior: 'smooth' 
    });
});