const btn = document.querySelector(".btn-cost");
const costBlock = document.querySelector(".cost__inputs");
const inputs = document.querySelectorAll(".input__cost");

btn.addEventListener("click", function() {
    costBlock.classList.toggle("valid");

    inputs.forEach(input => {
        input.value = "";
    });
});
document.querySelector("#formget").addEventListener("submit", function(e){

    let start = document.querySelector("input[name='priceStart']");
    let end = document.querySelector("input[name='priceEnd']");

    let startVal = start.value.trim();
    let endVal = end.value.trim();

    if (startVal && isNaN(startVal)) {
        alert("Начальная цена должна быть числом");
        e.preventDefault();
        return;
    }

    if (endVal && isNaN(endVal)) {
        alert("Конечная цена должна быть числом");
        e.preventDefault();
        return;
    }

    if (startVal && endVal && Number(startVal) > Number(endVal)) {
        alert("Начальная цена не может быть больше конечной");
        e.preventDefault();
        return;
    }

});
