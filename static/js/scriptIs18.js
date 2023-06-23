document.addEventListener("DOMContentLoaded", function() {
  var dataUrodzeniaInput = document.getElementById("dataUrodzenia");
  var daneOpiekunaContainer = document.getElementById("daneOpiekunaContainer");

  dataUrodzeniaInput.addEventListener("change", function() {
    var dataUrodzenia = new Date(this.value);
    var dzisiejszaData = new Date();
    var roznicaWiekow = dzisiejszaData.getFullYear() - dataUrodzenia.getFullYear();

    if (roznicaWiekow < 18) {
      daneOpiekunaContainer.style.display = "block";
      document.getElementById("daneOpiekuna").required = true;
    } else {
      daneOpiekunaContainer.style.display = "none";
      document.getElementById("daneOpiekuna").required = false;
    }
  });
});