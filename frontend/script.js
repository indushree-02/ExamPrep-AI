async function askQuestion() {
  const question = document.getElementById('question').value;
  const output = document.getElementById('output');

  output.textContent = 'Loading...';

  try {
    const response = await fetch('http://localhost:8000/');
    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    output.textContent = 'Error: ' + error.message;
  }
}
