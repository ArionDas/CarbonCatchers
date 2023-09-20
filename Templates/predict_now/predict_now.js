const datePicker = document.getElementById("datePicker");
const selectedDate = document.getElementById("selectedDate");

datePicker.addEventListener("change", function () {
  const selectedValue = datePicker.value;
  selectedDate.textContent = `Selected Date: ${selectedValue}`;
});
const timePicker = document.getElementById("timePicker");
const selectedTime = document.getElementById("selectedTime");

timePicker.addEventListener("change", function () {
  const selectedValue = timePicker.value;
  selectedTime.textContent = `Selected Time: ${selectedValue}`;
});

const predict = document.querySelector(".predict");
const data_to_show = document.querySelector(
  ".predicted--data .current--data .pm2"
);

const data = document.querySelector(".current--data h1");
predict.addEventListener("click", (e) => {
  e.preventDefault();
  const date = datePicker.value;
  const time = timePicker.value;
  const timeParts = time.split(":");
  const hours = timeParts[0];
  const dateString = `${date} ${hours}`;
  console.log(dateString);
  async function add() {
    try {
      console.log(1);
      const response = await fetch(`http://127.0.0.1:8000/${dateString}`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      console.log(2);
      const data = await response.json();
      data_to_show.textContent = data.predicted_data.toFixed(2);
    } catch (error) {
      console.error("Error:", error);
    }
  }
  add();
});
