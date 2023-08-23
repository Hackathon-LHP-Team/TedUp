// Get the audio element by id
var myAudio = document.getElementById('myAudio');
var playButton = document.getElementById('play-button');
var pauseButton = document.getElementById('pause-button');
var currentTimeContainer = document.getElementById('current-time');
var totalTimeContainer = document.getElementById('total-time');
var seekSlider = document.getElementById("seekslider");
var volUpButton = document.getElementById('vol-up-btn');
var volDownButton = document.getElementById('vol-down-btn');
var volMuteButton = document.getElementById('vol-mute-btn');
let volumeSlider = document.getElementById("volume-slider");

// Define a function to play podcast
playButton.addEventListener("click", function(){
  myAudio.play();
  playButton.classList.add('display-none');
  pauseButton.classList.remove('display-none');
});

// Define a function to pause podcast
pauseButton.addEventListener("click", function(){
    myAudio.pause();
    pauseButton.classList.add('display-none');
    playButton.classList.remove('display-none');
});

// Convert seconds into correct format
function convertElapsedTime(inputSeconds) {
  var seconds = Math.floor(inputSeconds % 60)
  if (seconds < 10) {
      seconds = "0" + seconds
  }
  var minutes = Math.floor(inputSeconds / 60)
    return minutes + ":" + seconds
}

// Loadedmetadata Event Listener
myAudio.addEventListener('loadedmetadata', function() {
  totalTimeContainer.innerHTML = convertElapsedTime(myAudio.duration);
  currentTimeContainer.innerHTML = convertElapsedTime(myAudio.currentTime);
  seekSlider.max= myAudio.duration;
  seekSlider.setAttribute("value", myAudio.currentTime);
});

// Slider Event Listener -> Change
seekSlider.addEventListener("change", function () {
  myAudio.currentTime = seekSlider.value;
});

// Slider Event Listener -> Update
myAudio.addEventListener('timeupdate', function() {
  currentTimeContainer.innerHTML = convertElapsedTime(myAudio.currentTime);
  seekSlider.setAttribute("value", myAudio.currentTime);
  seekSlider.value = myAudio.currentTime;

  // When the audio ends, we need to hide the pause button and show the play button
  if (myAudio.ended) {
     pauseButton.classList.add('display-none');
     playButton.classList.remove('display-none');
  }
});

// Volumn Slider Control
function setvolume(){
  myAudio.volume = volumeSlider.value;
}
function setvolumeSlider(){
      volumeSlider.value = myAudio.volume;
}
volumeSlider.addEventListener("mousemove", setvolume);

volUpButton.addEventListener("click", function(){
  myAudio.volume+=0.1;
  setvolumeSlider();
});
volDownButton.addEventListener("click", function(){
      myAudio.volume-=0.1;
      setvolumeSlider();
});
volMuteButton.addEventListener("click", function(){
      myAudio.muted = !myAudio.muted;
});
