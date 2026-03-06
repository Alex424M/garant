document.getElementById("applicationForm").addEventListener("submit", function(e) {
    let error_phone = document.querySelector(".phone__error p");
    let error_comment = document.querySelector(".comment__error p");
    let phone = document.querySelector("input[name='phone']").value.trim();
    let comment = document.querySelector("textarea[name='message']").value.trim();

    let phoneRegex = /^\+?\d{10,15}$/;
    if (!phoneRegex.test(phone)) {
        error_phone.textContent='Введите корректный номер телефона (10–15 цифр)';
        e.preventDefault();
        return;
    }

    if (comment.length > 500) {
        error_comment.textContent='Комментарий не должен превышать 500 символов';
        e.preventDefault();
        return;
    }

});