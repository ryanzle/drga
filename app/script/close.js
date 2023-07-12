//shit doesnt work lol
//https://stackoverflow.com/questions/10706070/how-to-detect-when-a-page-exits-fullscreen
if (document.addEventListener)
{
 document.addEventListener('fullscreenchange', exitHandler, false);
 document.addEventListener('mozfullscreenchange', exitHandler, false);
 document.addEventListener('MSFullscreenChange', exitHandler, false);
 document.addEventListener('webkitfullscreenchange', exitHandler, false);
}

function exitHandler()
{
    console.log("exitHandler fired");
 if (document.webkitIsFullScreen === false)
 {
  ///fire your event
 }
 else if (document.mozFullScreen === false)
 {
  ///fire your event
 }
 else if (document.msFullscreenElement === false)
 {
  ///fire your event
 }
}  