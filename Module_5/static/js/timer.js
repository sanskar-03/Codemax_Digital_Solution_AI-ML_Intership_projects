document.addEventListener("DOMContentLoaded", () => {
    const timer = document.getElementById("timer");
    const pauseButton = document.getElementById("pauseButton");

    if (!timer) return;

    let totalSeconds =
        Number(timer.dataset.minutes || 25) * 60;

    let running = true;

    function render() {
        const minutes =
            Math.floor(totalSeconds / 60);

        const seconds =
            totalSeconds % 60;

        timer.textContent =
            String(minutes).padStart(2, "0")
            + ":"
            + String(seconds).padStart(2, "0");
    }

    const interval = setInterval(() => {
        if (!running) return;

        if (totalSeconds <= 0) {
            clearInterval(interval);

            timer.textContent = "00:00";

            if (pauseButton) {
                pauseButton.textContent =
                    "Session finished";
                pauseButton.disabled = true;
            }

            return;
        }

        totalSeconds -= 1;
        render();

    }, 1000);

    if (pauseButton) {
        pauseButton.addEventListener("click", () => {
            running = !running;

            pauseButton.textContent =
                running
                    ? "Pause"
                    : "Resume";
        });
    }

    render();
});
