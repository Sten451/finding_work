console.log('Starting');

const message_b = document.querySelector('#check_status');
const message_s = document.querySelector('#screen');
message_b.addEventListener('click', () => {
  show_message();
});

function show_message() {
  console.log(message_b, message_s);
  message_s.style.display = 'block';
}
