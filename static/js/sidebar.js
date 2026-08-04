/*
==================================================
YPTSC IMS
SIDEBAR CONTROLLER
ENTERPRISE NAVIGATION
==================================================
*/


document.addEventListener(
    "DOMContentLoaded",
    function () {


        initializeSidebar();


    }
);







/*
==================================================
INITIALIZE SIDEBAR
==================================================
*/


function initializeSidebar() {


    const toggleButton =
        document.getElementById(
            "sidebarToggle"
        );


    const sidebar =
        document.querySelector(
            ".sidebar"
        );



    const overlay =
        document.querySelector(
            ".sidebar-overlay"
        );





    if (
        !sidebar
    ) {

        return;

    }







    /*
    ==============================================
    TOGGLE SIDEBAR
    ==============================================
    */


    if (toggleButton) {


        toggleButton.addEventListener(
            "click",
            function () {


                toggleSidebar(
                    sidebar,
                    overlay
                );


            }
        );


    }







    /*
    ==============================================
    CLOSE OUTSIDE CLICK
    ==============================================
    */


    if (overlay) {


        overlay.addEventListener(
            "click",
            function () {


                closeSidebar(
                    sidebar,
                    overlay
                );


            }
        );


    }








    /*
    ==============================================
    ACTIVE MENU
    ==============================================
    */


    setActiveMenu();








    /*
    ==============================================
    KEYBOARD SUPPORT
    ==============================================
    */


    document.addEventListener(
        "keydown",
        function (event) {


            if (
                event.key === "Escape"
            ) {


                closeSidebar(
                    sidebar,
                    overlay
                );


            }


        }
    );



}









/*
==================================================
OPEN / CLOSE
==================================================
*/


function toggleSidebar(
    sidebar,
    overlay
) {



    sidebar.classList.toggle(
        "active"
    );



    if (overlay) {


        overlay.classList.toggle(
            "active"
        );


    }



}






function closeSidebar(
    sidebar,
    overlay
) {


    sidebar.classList.remove(
        "active"
    );


    if (overlay) {


        overlay.classList.remove(
            "active"
        );


    }



}









/*
==================================================
ACTIVE NAVIGATION
==================================================
*/


function setActiveMenu() {



    const currentPath =
        window.location.pathname;



    const links =
        document.querySelectorAll(
            ".sidebar a"
        );



    links.forEach(
        function (link) {



            const href =
                link.getAttribute(
                    "href"
                );



            if (
                href &&
                currentPath === href
            ) {


                link.classList.add(
                    "active"
                );


            }



        }
    );



}