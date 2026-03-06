document.querySelector("#regg']").addEventListener("submit", function(e){

    e.preventDefault();

    let first = document.querySelector("input[name='first_name']");
    let last = document.querySelector("input[name='last_name']");
    let pass = document.querySelector("input[name='password']");
    let pass2 = document.querySelector("input[name='password2']");

    let russian = /^[А-Яа-яЁё-]+$/;
    let hasError = false;

    document.querySelectorAll(".error").forEach(e => e.textContent = "");

    if (!russian.test(first.value.trim())) {
        first.previousElementSibling.textContent = "Имя должно быть на русском.";
        hasError = true;
    }

    if (!russian.test(last.value.trim())) {
        last.previousElementSibling.textContent = "Фамилия должна быть на русском.";
        hasError = true;
    }

    if (pass.value.length < 8) {
        pass.previousElementSibling.textContent = "Минимум 8 символов.";
        hasError = true;
    }

    if (!/[A-Z]/.test(pass.value)) {
        pass.previousElementSibling.textContent = "Нужна заглавная буква.";
        hasError = true;
    }

    if (pass.value !== pass2.value) {
        pass2.previousElementSibling.textContent = "Пароли не совпадают.";
        hasError = true;
    }

    if (!hasError) {
        this.submit();
    }

});