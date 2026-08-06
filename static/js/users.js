// DELETE USER MODAL
document.addEventListener(
    "DOMContentLoaded",
    function () {
        // GET ELEMENTS
        const deleteModal = document.getElementById(
            "deleteUserModal"
        );
        const deleteUserName = document.getElementById(
            "deleteUserName"
        );
        const cancelDeleteUser = document.getElementById(
            "cancelDeleteUser"
        );
        const confirmDeleteUser = document.getElementById(
            "confirmDeleteUser"
        );
        const deleteButtons = document.querySelectorAll(
            ".delete-user-btn"
        );
        // SELECTED DELETE FORM
        let selectedDeleteForm = null;
        // OPEN DELETE MODAL
        deleteButtons.forEach(
            function (button) {
                button.addEventListener(
                    "click",
                    function () {
                        selectedDeleteForm =
                            button.closest(
                                ".delete-user-form"
                            );
                        const userName =
                            button.dataset.userName;
                        deleteUserName.textContent =
                            userName;
                        // Reset button
                        confirmDeleteUser.disabled =
                            false;
                        confirmDeleteUser.innerHTML = `
                            <i class="fa-solid fa-trash"></i>
                            Delete User
                        `;
                        // Show modal
                        deleteModal.classList.add(
                            "show"
                        );
                        deleteModal.setAttribute(
                            "aria-hidden",
                            "false"
                        );
                    }
                );
            }
        );
        // CANCEL DELETE
        cancelDeleteUser.addEventListener(
            "click",
            function () {
                deleteModal.classList.remove(
                    "show"
                );
                deleteModal.setAttribute(
                    "aria-hidden",
                    "true"
                );
                selectedDeleteForm = null;
            }
        );
        // CONFIRM DELETE
        confirmDeleteUser.addEventListener(
            "click",
            function () {
                if (
                    selectedDeleteForm === null
                ) {
                    return;
                }
                // SHOW LOADING
                confirmDeleteUser.disabled =
                    true;
                cancelDeleteUser.disabled =
                    true;
                confirmDeleteUser.innerHTML = `
                    <i
                        class="
                            fa-solid
                            fa-spinner
                            fa-spin
                        "
                    ></i>
                    Deleting...
                `;
                // SUBMIT DELETE FORM
                selectedDeleteForm.submit();
            }
        );
        // CLOSE WHEN OVERLAY IS CLICKED
        const modalOverlay =
            deleteModal.querySelector(
                ".delete-modal-overlay"
            );
        modalOverlay.addEventListener(
            "click",
            function () {
                if (
                    confirmDeleteUser.disabled
                ) {
                    return;
                }
                deleteModal.classList.remove(
                    "show"
                );
                deleteModal.setAttribute(
                    "aria-hidden",
                    "true"
                );
                selectedDeleteForm = null;
            }
        );
    }
);
