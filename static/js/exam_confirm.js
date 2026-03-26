document.addEventListener("DOMContentLoaded", function () {
    const examForm = document.getElementById("exam-form");

    if (!examForm) return;

    examForm.addEventListener("submit", function (e) {
        const confirmSubmit = confirm(
            "⚠️ Are you sure you want to submit this exam?\n\nYou will NOT be able to change your answers again."
        );

        if (!confirmSubmit) {
            e.preventDefault();
        }
    });
});
