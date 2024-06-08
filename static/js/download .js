const video = document.getElementById("myVideo");
const timestampsDiv = document.getElementById("timestamps");

// Define your timestamps in seconds
const timestamps = [0, 10, 20, 30];

video.addEventListener("timeupdate", () => {
  const currentTime = Math.floor(video.currentTime);
  if (timestamps.includes(currentTime)) {
    timestampsDiv.innerText = `Timestamp: ${currentTime} seconds`;
    timestampsDiv.style.display = "block"; // Show the timestamps
    timestampsDiv.style.color = "red"; // Example text color
    timestampsDiv.style.backgroundColor = "black"; // Example background color
    timestampsDiv.style.padding = "10px"; 
    timestampsDiv.style.borderRadius = "5px"; // Example border radius
    timestampsDiv.style.fontSize = "20px";
  } else {
    timestampsDiv.innerText = "";
    timestampsDiv.style.display = "none"; // Hide the timestamps
  }
});
