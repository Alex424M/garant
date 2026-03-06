const entr = document.querySelectorAll(".entr");
const reg = document.querySelectorAll(".reg");

const btn = document.querySelector(".header__btn");
btn.onclick = function () {
    document.getElementById('entryForm').style.display = 'block';
    reg[0].classList.add("notActive");
    entr[0].classList.remove("notActive");
}

const closeBtn = document.querySelectorAll(".close");
closeBtn.forEach(element => {
    element.onclick = function () {
        document.getElementById('entryForm').style.display = 'none';
        document.getElementById('regForm').style.display = 'none';
    }
});


entr[1].onclick = function () {
    document.getElementById('entryForm').style.display = 'block';
    document.getElementById('regForm').style.display = 'none';
    reg[0].classList.add("notActive");
    entr[0].classList.remove("notActive");
}

reg[0].onclick = function () {
    document.getElementById('regForm').style.display = 'block';
    document.getElementById('entryForm').style.display = 'none';
    entr[1].classList.add("notActive");
    reg[1].classList.remove("notActive");
}

window.addEventListener("click", function(event) {
    if (event.target == document.getElementById('entryForm')) {
        document.getElementById('entryForm').style.display = "none";
    }

    if (event.target == document.getElementById('regForm')) {
        document.getElementById('regForm').style.display = "none";
    }
});

function noDigits(event) {
    if ("1234567890".indexOf(event.key) != -1)
        event.preventDefault();
}