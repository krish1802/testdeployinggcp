const video = document.querySelector(".myVideo");
const overlayP = document.querySelector(".overlay");
    

const timestamps = [0, 3, 4, 5, 10, 15, 20];
    
video.addEventListener("timeupdate", () => {
    const currentTime = Math.floor(video.currentTime);
    if (timestamps.includes(currentTime)) {
        overlayP.innerText = "Backbend at " + currentTime + "s";
        overlayP.style.fontSize = "20px";
        overlayP.style.display = "block"; // Show the timestamps
        overlayP.style.color = "red"; // Example text color
        overlayP.style.background="none"; // Example background color
        overlayP.style.padding = "10px"; 
        overlayP.style.borderRadius = "5px"; // Example border radius
    } else {
        overlayP.innerText = "";
    }
});