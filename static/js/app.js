let step = 0;
const exercises = document.querySelectorAll('.exercise');
const overlay = document.getElementById('transition-overlay');
const msgEl = document.getElementById('transition-message');
const messages = [
  "Great job! Ready for the next exercise?",
  "You're almost there! Just one more!",
  "Congratulations! You’ve finished all exercises!"
];

function showTransition() {
  msgEl.textContent = messages[step];
  overlay.classList.add('show');
  setTimeout(() => {
    overlay.classList.remove('show');
    goNext();
  }, 1000);
}

function goNext() {
  exercises[step].classList.remove('active');
  exercises[step].classList.add('inactive-left');
  step++;
  if (step < exercises.length) {
    exercises[step].classList.remove('inactive-right');
    exercises[step].classList.add('active');
  } else {
      // after finishing a session, go straight back to dashboard
      window.location.href = '/home';
    }
}

document.querySelectorAll('.done-btn').forEach(btn => {
  btn.addEventListener('click', showTransition);
});

// Initialize first exercise
exercises.forEach((ex, idx) => {
  if (idx === 0) ex.classList.add('active');
});
