document.addEventListener(
    "DOMContentLoaded",
    function () {
        initializeForms();
    }
);
/*INITIALIZE FORMS*/
function initializeForms() {
    const forms =
        document.querySelectorAll(
            "form"
        );
    forms.forEach(
        function (form) {
            form.addEventListener(
                "submit",
                function (event) {
                    if (
                        !validateForm(form)
                    ) {
                        event.preventDefault();
                        return false;
                    }
                    console.log(
                        "Form submitted:",
                        form.action
                    );
                }
            );
        }
    );
}
/*FORM VALIDATION*/
function validateForm(form) {
    let valid = true;
    const requiredFields =
        form.querySelectorAll(
            "[required]"
        );
    requiredFields.forEach(
        function (field) {
            removeError(field);
            if (
                field.value.trim() === ""
            ) {
                showError(
                    field,
                    "This field is required."
                );
                valid = false;
            }
        }
    );
    validateNumbers(
        form
    );
    return valid;
}
/*NUMBER VALIDATION*/
function validateNumbers(form) {
    const numbers =
        form.querySelectorAll(
            'input[type="number"]'
        );
    numbers.forEach(
        function (input) {
            if (
                input.value < 0
            ) {
                input.value = 0;
            }
        }
    );
}
/*FIELD ERROR*/
function showError(
    field,
    message
) {
    field.style.borderColor =
        "#ef4444";
    field.setAttribute(
        "title",
        message
    );
}
function removeError(field) {
    field.style.borderColor =
        "";
    field.removeAttribute(
        "title"
    );
}
/*CONFIRM DELETE*/
function confirmDelete(message) {
    return confirm(
        message ||
        "Are you sure you want to delete this record?");
}
