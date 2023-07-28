const otpInputs = document.querySelectorAll('.otp-input');

console.log('Working')
otpInputs.forEach((input, index) => {
  input.addEventListener('input', (e) => {
    const currentInput = e.target;

    if (currentInput.value) {
      if (index < otpInputs.length - 1) {
        otpInputs[index + 1].focus();
      } else {
        // Focus on the first input if the last one is filled
        otpInputs[0].focus();
      }
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace' && !input.value && index > 0) {
      // Move focus to the previous input when Backspace is pressed
      otpInputs[index - 1].focus();
    }
  });
});