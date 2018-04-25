window.onload = function() {}

changeImageSize = function(value){
{
  var images = document.getElementsByTagName('img'),
      imagesArr = Array.prototype.slice.call(images);

  console.log(value)

  imagesArr.forEach(function(img) {
    img.style.width = value + 'px';
    img.style.height = value + 'px';
  })
}
}
