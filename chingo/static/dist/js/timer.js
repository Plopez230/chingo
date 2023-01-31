function startTimer(duration) {
var timer = duration;
var max_time = timer;
setInterval(function () {
    var test_timer = document.getElementById('test-timer');
    var timer_form = document.getElementById('time-over');
    test_timer.style.width = `${(100*timer/max_time)}%`;
    if (timer > -1) {
        timer --;
    } else {
        timer_form.submit();
    }
}, 1000);
}