//chest exercises

document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".chestPress").style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".pushups").style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".chestflies").style.display = "none";
    }
});

benchPress.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".chestPress").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".chestPress").scrollIntoView({ 
        behavior: 'smooth' 
    });
});


pushup.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".pushups").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".pushups").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

chestFlies.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".chestFlies").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".chestFlies").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

chestDips.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".chestDips").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".chestDips").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

backBtnChest.addEventListener("click", async () => {
    // Show right2 and hide right1
        document.querySelector(".gallery-area").style.display = "block";
        document.querySelector(".gallery-area").scrollIntoView({ 
            behavior: 'smooth' 
        });
        
        document.querySelector(".chestPress").style.display = "none";
    })



