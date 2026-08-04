// ==================================================
// UNIT INVENTORY
// SEARCH + CATEGORY + STATUS FILTER
// ==================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        // ==================================================
        // GET ELEMENTS
        // ==================================================

        const searchInput =
            document.getElementById(
                "unitSearch"
            );


        const categoryFilter =
            document.getElementById(
                "categoryFilter"
            );


        const statusFilter =
            document.getElementById(
                "statusFilter"
            );


        const unitRows =
            document.querySelectorAll(
                ".unit-row"
            );


        const noFilterResults =
            document.getElementById(
                "noFilterResults"
            );


        const unitCount =
            document.getElementById(
                "unitCount"
            );


        // ==================================================
        // STOP IF THE PAGE ELEMENTS DO NOT EXIST
        // ==================================================

        if (
            !searchInput
            ||
            !categoryFilter
            ||
            !statusFilter
        ) {

            return;

        }


        // ==================================================
        // FILTER UNITS
        // ==================================================

        function filterUnits() {

            // ==============================================
            // SEARCH VALUE
            // ==============================================

            const searchValue =

                (
                    searchInput.value
                    ||
                    ""
                )
                .trim()
                .toLowerCase();


            // ==============================================
            // CATEGORY VALUE
            // ==============================================

            const selectedCategory =

                (
                    categoryFilter.value
                    ||
                    ""
                )
                .trim()
                .toLowerCase();


            // ==============================================
            // STATUS VALUE
            // ==============================================

            const selectedStatus =

                (
                    statusFilter.value
                    ||
                    ""
                )
                .trim()
                .toLowerCase();


            // ==============================================
            // VISIBLE UNIT COUNTER
            // ==============================================

            let visibleCount = 0;


            // ==============================================
            // CHECK EVERY UNIT ROW
            // ==============================================

            unitRows.forEach(
                function (row) {

                    // ======================================
                    // GET ROW TEXT
                    // ======================================

                    const rowText =

                        (
                            row.textContent
                            ||
                            ""
                        )
                        .toLowerCase();


                    // ======================================
                    // GET CATEGORY
                    // ======================================

                    const unitCategory =

                        (
                            row.dataset.category
                            ||
                            ""
                        )
                        .trim()
                        .toLowerCase();


                    // ======================================
                    // GET STATUS
                    // ======================================

                    const unitStatus =

                        (
                            row.dataset.status
                            ||
                            ""
                        )
                        .trim()
                        .toLowerCase();


                    // ======================================
                    // SEARCH MATCH
                    // ======================================

                    const matchesSearch =

                        rowText.includes(
                            searchValue
                        );


                    // ======================================
                    // CATEGORY MATCH
                    // ======================================

                    const matchesCategory =

                        selectedCategory === ""

                        ||

                        unitCategory ===
                        selectedCategory;


                    // ======================================
                    // STATUS MATCH
                    // ======================================

                    const matchesStatus =

                        selectedStatus === ""

                        ||

                        unitStatus ===
                        selectedStatus;


                    // ======================================
                    // SHOW OR HIDE ROW
                    // ======================================

                    if (

                        matchesSearch

                        &&

                        matchesCategory

                        &&

                        matchesStatus

                    ) {

                        row.style.display =
                            "";

                        visibleCount++;

                    }

                    else {

                        row.style.display =
                            "none";

                    }

                }
            );


            // ==============================================
            // SHOW NO RESULTS MESSAGE
            // ==============================================

            if (
                noFilterResults
            ) {

                noFilterResults.style.display =

                    visibleCount === 0

                    ?

                    ""

                    :

                    "none";

            }


            // ==============================================
            // UPDATE UNIT COUNT
            // ==============================================

            if (
                unitCount
            ) {

                unitCount.textContent =

                    "Showing "

                    +

                    visibleCount

                    +

                    " registered unit"

                    +

                    (
                        visibleCount === 1

                        ?

                        ""

                        :

                        "s"
                    );

            }

        }


        // ==================================================
        // SEARCH WHILE TYPING
        // ==================================================

        searchInput.addEventListener(
            "input",
            filterUnits
        );


        // ==================================================
        // FILTER BY CATEGORY
        // ==================================================

        categoryFilter.addEventListener(
            "change",
            filterUnits
        );


        // ==================================================
        // FILTER BY STATUS
        // ==================================================

        statusFilter.addEventListener(
            "change",
            filterUnits
        );


        // ==================================================
        // RUN ON PAGE LOAD
        // ==================================================

        filterUnits();

    }
);

    // ==================================================
    // DELETE UNIT CONFIRMATION MODAL
    // ==================================================

    const deleteUnitModal =
        document.getElementById(
            "deleteUnitModal"
        );


    const deleteUnitName =
        document.getElementById(
            "deleteUnitName"
        );


    const cancelDeleteUnit =
        document.getElementById(
            "cancelDeleteUnit"
        );


    const confirmDeleteUnit =
        document.getElementById(
            "confirmDeleteUnit"
        );


    const deleteUnitButtons =
        document.querySelectorAll(
            ".delete-unit-btn"
        );


    let selectedDeleteForm =
        null;


    // ==================================================
    // OPEN MODAL
    // ==================================================

    deleteUnitButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    selectedDeleteForm =
                        button.closest(
                            ".delete-unit-form"
                        );


                    const unitName =

                        button.dataset.unitName

                        ||

                        "this unit";


                    deleteUnitName.textContent =
                        unitName;


                    deleteUnitModal.classList.add(
                        "show"
                    );


                    deleteUnitModal.setAttribute(
                        "aria-hidden",
                        "false"
                    );

                }
            );

        }
    );


    // ==================================================
    // CLOSE MODAL
    // ==================================================

    function closeDeleteUnitModal() {

        deleteUnitModal.classList.remove(
            "show"
        );


        deleteUnitModal.setAttribute(
            "aria-hidden",
            "true"
        );


        selectedDeleteForm =
            null;

    }


    // ==================================================
    // CANCEL BUTTON
    // ==================================================

    if (
        cancelDeleteUnit
    ) {

        cancelDeleteUnit.addEventListener(
            "click",
            closeDeleteUnitModal
        );

    }


    // ==================================================
    // CLICK OVERLAY TO CLOSE
    // ==================================================

    const deleteUnitOverlay =
        deleteUnitModal.querySelector(
            ".delete-modal-overlay"
        );


    if (
        deleteUnitOverlay
    ) {

        deleteUnitOverlay.addEventListener(
            "click",
            closeDeleteUnitModal
        );

    }


    // ==================================================
    // CONFIRM DELETE
    // ==================================================

    if (
        confirmDeleteUnit
    ) {

        confirmDeleteUnit.addEventListener(
            "click",
            function () {

                if (
                    !selectedDeleteForm
                ) {

                    return;

                }


                confirmDeleteUnit.disabled =
                    true;


                confirmDeleteUnit.innerHTML =

                    `
                    <i class="fa-solid fa-spinner fa-spin"></i>

                    Deleting...
                    `;


                selectedDeleteForm.submit();

            }
        );

    }


    // ==================================================
    // ESCAPE KEY
    // ==================================================

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape"
                &&
                deleteUnitModal.classList.contains(
                    "show"
                )
            ) {

                closeDeleteUnitModal();

            }

        }
    );