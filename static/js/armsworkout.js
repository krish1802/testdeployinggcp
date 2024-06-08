//arms exercises

//bicep curls
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".bicepCurls").style.display = "none";
    }
});

bicepCurls.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".bicepCurls").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".bicepCurls").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//hammer curls
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".hammerCurls").style.display = "none";
    }
});

hammerCurls.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".hammerCurls").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".hammerCurls").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//preacher curls
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".preacherCurls").style.display = "none";
    }
});

preacherCurls.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".preacherCurls").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".preacherCurls").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//tricep pushdown
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".tricepPushdown").style.display = "none";
    }
});

tricepPushdown.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".tricepPushdown").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".tricepPushdown").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//tricep rope pushdown
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".tricepRopePushdown").style.display = "none";
    }
});

tricepRopePushdown.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".tricepRopePushdown").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".tricepRopePushdown").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//bench tricep dips
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".benchTricepDips").style.display = "none";
    }
});

benchTricepDips.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".benchTricepDips").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".benchTricepDips").scrollIntoView({ 
        behavior: 'smooth' 
    });
});

//backward wrist curls
document.addEventListener("DOMContentLoaded", function() {
    // Check if the page is being refreshed
    if (performance.navigation.type === 1) {
        // Hide the .chestPress div
        document.querySelector(".backwardWristCurls").style.display = "none";
    }
});

backwardWristCurls.addEventListener("click", async () => {
    // Show right2 and hide right1
    document.querySelector(".backwardWristCurls").style.display = "block";
    document.querySelector(".gallery-area").style.display = "none";

    // Scroll to a specific element
    document.querySelector(".backwardWristCurls").scrollIntoView({ 
        behavior: 'smooth' 
    });
});