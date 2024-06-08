// Declare questionInput globally
let questionInput;

// Example POST method implementation:
async function postData(url = "", data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), 
    });
    return response.json(); 
  }

// Add event listener to sendButton
sendButton.addEventListener("click", async () => {
    // Alert when button is clicked
    // alert("Hey you clicked");
    
    // Get value of question input field
    questionInput = document.getElementById("questionInput").value;
    // alert(questionInput);
    
    // Clear question input field
    document.getElementById("questionInput").value = "";
    
    // Show right2 and hide right1
    document.querySelector(".right2").style.display = "block";
    document.querySelector(".right1").style.display = "none";

    // Set question inner HTML to the value of questionInput
    // document.getElementById("question").innerHTML = questionInput;
    document.getElementById("questionUser").innerHTML = questionInput;

    // Get answer and populate
    let result = await postData("/api", {"question" : questionInput})
    document.getElementById("solution").innerHTML = result.answer;
},

// sendButton2.addEventListener("click", async () => {
//   // Alert when button is clicked
//   // alert("Hey you clicked");
  
//   // Get value of question input field
//   questionInput = document.getElementById("questionInput2").value;
//   // alert(questionInput);
  
//   // Clear question input field
//   document.getElementById("questionInput2").value = "";
  
//   // Show right2 and hide right1
//   document.querySelector(".right2").style.display = "block";
//   document.querySelector(".right1").style.display = "none";

//   // Set question inner HTML to the value of questionInput
//   document.getElementById("question").innerHTML = questionInput;
//   document.getElementById("questionUser").innerHTML = questionInput;

//   // Get answer and populate
//   let result = await postData("/api", {"question" : questionInput})
//   document.getElementById("solution").innerHTML = result.answer;
// },

// sendButton2.addEventListener("click", async () => {
//   // Alert when button is clicked
//   // alert("Hey you clicked");
  
//   // Get value of question input field
//   questionInput = document.getElementById("questionInput").value;
//   // alert(questionInput);
  
//   // Clear question input field
//   document.getElementById("questionInput").value = "";
  
//   // Show right2 and hide right1
//   document.querySelector(".right2").style.display = "block";
//   document.querySelector(".right1").style.display = "none";

//   // Set question inner HTML to the value of questionInput
//   document.getElementById("question").innerHTML = questionInput;
//   document.getElementById("questionUser").innerHTML = questionInput;

//   // Get answer and populate
//   let result = await postData("/api", {"question" : questionInput})
//   document.getElementById("solution").innerHTML = result.answer;
// },

  workoutPlanButton.addEventListener("click", async () => {
    // Alert when button is clicked
    // alert("Hey you clicked");
    
    // Get value of question input field
    questionInput = "Make a workout plan for me";
    
    // Clear question input field
    document.getElementById("questionInput").value = "";
    
    // Show right2 and hide right1
    document.querySelector(".right2").style.display = "block";
    document.querySelector(".right1").style.display = "none";

    // Set question inner HTML to the value of questionInput
    // document.getElementById("question").innerHTML = questionInput;
    document.getElementById("questionUser").innerHTML = questionInput;

    // Get answer and populate
    let result = await postData("/api", {"question" : questionInput})
    document.getElementById("solution").innerHTML = result.answer;
  },

  dietButton.addEventListener("click", async () => {
    // Alert when button is clicked
    // alert("Hey you clicked");
    
    // Get value of question input field
    questionInput = "Help me with my diet";
    
    // Clear question input field
    document.getElementById("questionInput").value = "";
    
    // Show right2 and hide right1
    document.querySelector(".right2").style.display = "block";
    document.querySelector(".right1").style.display = "none";

    // Set question inner HTML to the value of questionInput
    // document.getElementById("question").innerHTML = questionInput;
    document.getElementById("questionUser").innerHTML = questionInput;

    // Get answer and populate
    let result = await postData("/api", {"question" : questionInput})
    document.getElementById("solution").innerHTML = result.answer;
  },

  compoundButton.addEventListener("click", async () => {
    // Alert when button is clicked
    // alert("Hey you clicked");
    
    // Get value of question input field
    questionInput = "Best compound movement exercises";
    
    // Clear question input field
    document.getElementById("questionInput").value = "";
    
    // Show right2 and hide right1
    document.querySelector(".right2").style.display = "block";
    document.querySelector(".right1").style.display = "none";

    // Set question inner HTML to the value of questionInput
    // document.getElementById("question").innerHTML = questionInput;
    document.getElementById("questionUser").innerHTML = questionInput;

    // Get answer and populate
    let result = await postData("/api", {"question" : questionInput})
    document.getElementById("solution").innerHTML = result.answer;
  },

  powerLiftingButton.addEventListener("click", async () => {
    // Alert when button is clicked
    // alert("Hey you clicked");
    
    // Get value of question input field
    questionInput = "How to grow in powerlifting";
    
    // Clear question input field
    document.getElementById("questionInput").value = "";
    
    // Show right2 and hide right1
    document.querySelector(".right2").style.display = "block";
    document.querySelector(".right1").style.display = "none";

    // Set question inner HTML to the value of questionInput
    // document.getElementById("question").innerHTML = questionInput;
    document.getElementById("questionUser").innerHTML = questionInput;

    // Get answer and populate
    let result = await postData("/api", {"question" : questionInput})
    document.getElementById("solution").innerHTML = result.answer;
  },

  // document.getElementById('sendButton2').addEventListener('click', function() {
  //   // Clone box1
  //   var clonedBox1 = document.querySelector('.box1').cloneNode(true);
    
  //   // Clone box2
  //   var clonedBox2 = document.querySelector('.box2').cloneNode(true);
    
  //   // Append cloned boxes under the existing ones
  //   document.querySelector('.conversation').appendChild(clonedBox1);
  //   document.querySelector('.conversation').appendChild(clonedBox2);
    
  // }
  document.getElementById('sendButton2').addEventListener('click', async function() {
    // Clone box1
    var clonedBox1 = document.querySelector('.box1').cloneNode(true);
    
    // Clone box2
    var clonedBox2 = document.querySelector('.box2').cloneNode(true);
    
    // Get value of question input field
    var questionInput = document.getElementById("questionInput2").value;
  
    // Clear question input field
    document.getElementById("questionInput2").value = "";
  
    // Show right2 and hide right1
    document.querySelector(".right2").style.display = "block";
    document.querySelector(".right1").style.display = "none";
  
    // Set question inner HTML to the value of questionInput
    document.getElementById("questionUser").innerHTML = questionInput;
  
    // Display "loading..." in solution
    document.getElementById("solution").innerHTML = "loading...";
  
    // Get answer and populate
    let result = await postData("/api", {"question" : questionInput});
    document.getElementById("solution").innerHTML = result.answer;
  
    // Append cloned boxes at the top of the conversation div
    var conversationDiv = document.querySelector('.conversation');
    document.getElementById('conversation').appendChild(conversationDiv); // Append clonedBox1
},

document.getElementById('questionInput').addEventListener('keypress', function(event) {
  if (event.key == 'Enter') {
    event.preventDefault(); // Prevent form submission
    document.getElementById('sendButton').click(); // Trigger button click
  }
},

document.getElementById('questionInput2').addEventListener('keypress', function(event) {
  if (event.key == 'Enter') {
    event.preventDefault(); // Prevent form submission
    document.getElementById('sendButton2').click(); // Trigger button click
  }
}



  // Your postData function goes here
  
  

))))))));
