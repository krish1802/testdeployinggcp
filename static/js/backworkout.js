//back exercises

//latPulldown
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".latPulldown").style.display = "none";
    }
});

latPulldown.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".latPulldown").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".latPulldown").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//deadLift
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".deadlift").style.display = "none";
    }
});

deadlift.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".deadlift").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".deadlift").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//t Bar Rows
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".tBarRows").style.display = "none";
    }
});

tBarRows.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".tBarRows").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".tBarRows").scrollIntoView({ 
        behavior: 'smooth' 
    });
});


//bent over rows
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".bentOverRows").style.display = "none";
    }
});

bentOverRows.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".bentOverRows").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".bentOverRows").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//dumbell rows
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".dumbellRows").style.display = "none";
    }
});

dumbellRows.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".dumbellRows").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".dumbellRows").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//cable rows
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".cableRows").style.display = "none";
    }
});

cableRows.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".cableRows").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".cableRows").scrollIntoView({ 
        behavior: 'smooth' 
    });
});
