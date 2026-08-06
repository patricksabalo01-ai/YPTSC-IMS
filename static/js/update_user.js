document.addEventListener(
    "DOMContentLoaded",
    function () {
        const passwordButtons =
            document.querySelectorAll(
                ".password-toggle"
            );
        passwordButtons.forEach(
            function (button) {
                button.addEventListener(
                    "click",
                    function () {
                        const inputId =
                            button.dataset.target;
                        const passwordInput =
                            document.getElementById(
                                inputId
                            );
                        const icon =
                            button.querySelector(
                                "i"
                            );
                        if (
                            passwordInput.type
                            ===
                            "password"
                        ) {
                            passwordInput.type =
                                "text";
                            icon.classList.remove(
                                "fa-eye"
                            );
                            icon.classList.add(
                                "fa-eye-slash"
                            );
                        } else {
                            passwordInput.type =
                                "password";
                            icon.classList.remove(
                                "fa-eye-slash"
                            );
                            icon.classList.add(
                                "fa-eye"
                            );
                        }
                    }
                );
            }
        );
    }
);
