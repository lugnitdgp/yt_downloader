window.addEventListener(
  "load",
  function() {
    video = document.getElementById("video");
    play - button = document.getElementById("play-button");
    play - button.addEventListener("click", playOrPause, false);
  },
  false
);
function playOrPause() {
  if (video.paused) {
    video.play();
  } else {
    video.pause();
  }
}
