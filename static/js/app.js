/*
==================================================
YPTSC IMS
APPLICATION CORE
ENTERPRISE SYSTEM
==================================================
*/


document.addEventListener(
    "DOMContentLoaded",
    function () {


        console.log(
            "YPTSC IMS Loaded"
        );



        initializeApplication();



    }
);







/*
==================================================
APPLICATION INITIALIZATION
==================================================
*/


function initializeApplication() {



    initializeGlobalEvents();


    initializeFlashMessages();


    initializeDeleteConfirmation();


    initializeLoadingState();



}









/*
==================================================
GLOBAL EVENTS
==================================================
*/


function initializeGlobalEvents() {



    console.log(
        "Global modules initialized"
    );



}









/*
==================================================
FLASH MESSAGE HANDLER
==================================================
*/


function initializeFlashMessages() {



    const alerts =
        document.querySelectorAll(
            ".alert"
        );



    alerts.forEach(
        function (alert) {



            setTimeout(
                function () {


                    alert.style.opacity =
                        "0";



                    setTimeout(
                        function () {

                            alert.remove();

                        },
                        300
                    );



                },
                4000
            );



        }
    );



}









/*
==================================================
DELETE CONFIRMATION
==================================================
*/


function initializeDeleteConfirmation() {



    const deleteLinks =
        document.querySelectorAll(
            "[data-confirm]"
        );



    deleteLinks.forEach(
        function (link) {



            link.addEventListener(
                "click",
                function (event) {



                    const message =
                        link.dataset.confirm;



                    if (
                        !confirm(
                            message
                        )
                    ) {

                        event.preventDefault();

                    }



                }
            );



        }
    );



}









/*
==================================================
GLOBAL LOADING STATE
==================================================
*/


function initializeLoadingState() {



    const forms =
        document.querySelectorAll(
            "form"
        );



    forms.forEach(
        function (form) {



            form.addEventListener(
                "submit",
                function () {



                    const button =
                        form.querySelector(
                            'button[type="submit"]'
                        );



                    if (button) {


                        button.disabled =
                            true;



                        button.innerHTML =
                            `
                            <i class="fa-solid fa-spinner fa-spin"></i>
                            Processing...
                            `;


                    }



                }
            );



        }
    );



}