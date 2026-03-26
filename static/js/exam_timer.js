document.addEventListener("DOMContentLoaded", function () {
    const timerDisplay = document.getElementById("timer-display");
    const examForm = document.getElementById("exam-form");
    const durationDiv = document.getElementById("exam-duration");

    if (!timerDisplay || !examForm || !durationDiv) return;

    let remainingTime = parseInt(durationDiv.dataset.duration) * 60;

    function updateTimer() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;

        timerDisplay.textContent =
            String(minutes).padStart(2, "0") +
            ":" +
            String(seconds).padStart(2, "0");

        if (remainingTime <= 0) {
            examForm.submit();
            return;
        }
        if (remainingTime === 300 && !warningShown) {
            warningBanner.style.display = "block";
            warningShown = true;
        }


        remainingTime--;
    }

    updateTimer();
    setInterval(updateTimer, 1000);
});

window.addEventListener("beforeunload", function (e) {
    e.preventDefault();
    e.returnValue = "";
});


history.pushState(null, null, location.href);
window.onpopstate = function () {
    history.go(1);
};

const warningBanner = document.createElement("div");
warningBanner.id = "time-warning";
warningBanner.textContent = "⚠️ 5 minutes remaining";
document.body.appendChild(warningBanner);

let warningShown = false;
