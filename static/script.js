// Navigation Buttons
const btnHome = document.getElementById("btn-home");
const btnWorkouts = document.getElementById("btn-workouts");
const btnJourney = document.getElementById("btn-journey");

const backButton1 = document.getElementById("back1");
const backButton2 = document.getElementById("back2");
const backButton3 = document.getElementById("back3");

// Gym toggle
const gymToggle = document.querySelector('.toggle');

// Sections
const homeSection = document.getElementById("home-section");
const workoutsSection = document.getElementById("workouts-section");
const journeySection = document.getElementById("journey-section");
const progressSection = document.getElementById("progress-section");
const achievementsSection = document.getElementById("achievements-section");
const gymbuddySection = document.getElementById("gymbuddy-section");
const goalsSection = document.getElementById("goals-section");

const atHome = document.getElementById("at-home");
const atGym = document.getElementById("at-gym");

// My Journey Options
const progressButton = document.getElementById("progress");
const achievementsButton = document.getElementById("achievements");
const mygoalsButton = document.getElementById("goals");

// Sign-Up Modal
const signupModal = document.getElementById("signup-modal");
const openSignupBtn = document.getElementById("open-signup");
const closeSignupBtn = document.getElementById("close-signup");

// Survey Modal
const surveyModal = document.getElementById("survey-modal");
const openSurveyBtn = document.getElementById("open-survey");
const closeSurveyBtn = document.getElementById("close-survey");

// Helper function to show/hide sections
function showSection(section) {
  // Hide all sections
  homeSection.classList.add("hidden-section");
  workoutsSection.classList.add("hidden-section");
  journeySection.classList.add("hidden-section");
  progressSection.classList.add("hidden-section");
  achievementsSection.classList.add("hidden-section");
  gymbuddySection.classList.add("hidden-section");
  goalsSection.classList.add("hidden-section");

  // Remove 'active-section' from all
  homeSection.classList.remove("active-section");
  workoutsSection.classList.remove("active-section");
  journeySection.classList.remove("active-section");
  progressSection.classList.remove("active-section");
  achievementsSection.classList.remove("active-section");
  gymbuddySection.classList.remove("active-section");
  goalsSection.classList.remove("active-section");

  // Show the requested section
  section.classList.remove("hidden-section");
  section.classList.add("active-section");
}

// Helper function to activate/deactivate nav buttons
function activateButton(button) {
  btnHome.classList.remove("active");
  btnWorkouts.classList.remove("active");
  btnJourney.classList.remove("active");
  progressButton.classList.remove("active");
  achievementsButton.classList.remove("active");
  mygoalsButton.classList.remove("active");
  backButton1.classList.remove("active");
  backButton2.classList.remove("active");
  backButton3.classList.remove("active");

  button.classList.add("active");
}

// Gym Toggle
gymToggle.addEventListener("click", () => {
  gymToggle.classList.toggle('active');
  if (gymToggle.className == "toggle active") {
    atGym.classList.remove("hidden-section");
    atGym.classList.add("active-section");
    atHome.classList.remove("active-section");
    atHome.classList.add("hidden-section");
  } else {
    atGym.classList.remove("active-section");
    atGym.classList.add("hidden-section");
    atHome.classList.remove("hidden-section");
    atHome.classList.add("active-section");
  }
});

// Home Button
btnHome.addEventListener("click", () => {
  showSection(homeSection);
  activateButton(btnHome);
});

// Workouts Button
btnWorkouts.addEventListener("click", () => {
  showSection(workoutsSection);
  activateButton(btnWorkouts);
});

// My Journey Button
btnJourney.addEventListener("click", () => {
  showSection(journeySection);
  activateButton(btnJourney);
});

// Progress Button
progressButton.addEventListener("click", () => {
  showSection(progressSection);
  activateButton(progressButton);
});

// Achievements Button
achievementsButton.addEventListener("click", () => {
  showSection(achievementsSection);
  activateButton(achievementsButton);
});

mygoalsButton.addEventListener("click", () => {
  showSection(goalsSection);
  activateButton(mygoalsButton);
});

backButton1.addEventListener("click", () => {
  showSection(journeySection);
  activateButton(backButton1);
});

backButton2.addEventListener("click", () => {
  showSection(journeySection);
  activateButton(backButton2);
});

backButton3.addEventListener("click", () => {
  showSection(journeySection);
  activateButton(backButton3);
});

// Open/Close Sign-Up Modal
// openSignupBtn.addEventListener("click", () => {
//   signupModal.classList.add("show");
// });
closeSignupBtn.addEventListener("click", () => {
  signupModal.classList.remove("show");
});

// Open/Close Survey Modal
// openSurveyBtn.addEventListener("click", () => {
//   surveyModal.classList.add("show");
// });

closeSurveyBtn.addEventListener("click", () => {
  surveyModal.classList.remove("show");
});

// Optional: Close modal by clicking outside of it
window.addEventListener("click", (e) => {
  if (e.target === signupModal) {
    signupModal.classList.remove("show");
  }
  if (e.target === surveyModal) {
    surveyModal.classList.remove("show");
  }
});


// Toggle the dropdown list when the button is clicked
document.querySelector('.dropdown-btn').addEventListener('click', function() {
  document.querySelector('.dropdown-list').classList.toggle('show');
});

// When a list item is clicked, update the button text and hide the dropdown
document.querySelectorAll('.dropdown-list li').forEach(function(item) {
  item.addEventListener('click', function() {
    const selectedText = item.innerText;
    const selectedValue = item.getAttribute('data-value');
    document.querySelector('.dropdown-btn').innerText = selectedText;
    document.querySelector('.dropdown-list').classList.remove('show');
    
    // Log the selected workout for further processing
    console.log('Selected workout:', selectedValue);
    
    // Check if the "Generated Workout" option is selected
    if(selectedValue === 'generatedWork'){
      // Show the generated workout question form
      document.getElementById('generated-workout-form').style.display = 'block';
    } else {
      // Hide the generated workout form if any other option is selected
      document.getElementById('generated-workout-form').style.display = 'none';
      document.getElementById("generated-workout-response").style.display = 'none';
    }
  });
});

// Example handler for the submit button of the generated workout form
document.getElementById('submit-question').addEventListener('click', async function() {
  const question = document.getElementById('muscle-question').value;

  const response = await fetch('/generate-workout', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question: question })
  });

  const data = await response.json();
  console.log('Workout Plan:', data.response);

  // Display the response on the page
  document.getElementById('generated-workout-response').innerText = data.response;
});





// Profile dropdown 
document.addEventListener('DOMContentLoaded', () => {
  const profileDropdownBtn = document.querySelector('.profile-dropdown-btn');
  const profileDropdownList = document.querySelector('.profile-dropdown-list');

  // Toggle the dropdown list when the profile button is clicked
  profileDropdownBtn.addEventListener('click', () => {
    profileDropdownList.classList.toggle('show');
  });

  // Optionally, if you want the dropdown to hide when clicking outside:
  document.addEventListener('click', (event) => {
    if (!profileDropdownBtn.contains(event.target) && !profileDropdownList.contains(event.target)) {
      profileDropdownList.classList.remove('show');
    }
  });
});







document.addEventListener('DOMContentLoaded', () => {
  const logoutLink = document.getElementById('logout-link');
  logoutLink.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "/";
  });
});





