document.addEventListener("DOMContentLoaded", function () {
    const durationElement = document.getElementById("exam-duration");
    const examDuration = parseInt(durationElement.dataset.duration);

    console.log("Exam Duration Loaded:", examDuration, "minutes");

    let timeLeft = examDuration * 60; // convert minutes to seconds

    function updateTimer() {
        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;

        document.getElementById("timer-display").textContent =
            `${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;

        if (timeLeft <= 0) {
            document.getElementById("exam-form").submit();
        } else {
            timeLeft--;
        }
    }

    setInterval(updateTimer, 1000);
});
