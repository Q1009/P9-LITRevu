document.addEventListener('DOMContentLoaded', function() {
    var pendingForm = null;

    function openModal(form) {
        pendingForm = form;
        document.getElementById('modal-overlay').classList.add('modal-visible');
    }

    function closeModal() {
        pendingForm = null;
        document.getElementById('modal-overlay').classList.remove('modal-visible');
    }

    document.getElementById('modal-cancel').addEventListener('click', closeModal);
    document.getElementById('modal-overlay').addEventListener('click', function(e) {
        if (e.target === this) { closeModal(); }
    });
    document.getElementById('modal-confirm').addEventListener('click', function() {
        if (pendingForm) {
            pendingForm.removeEventListener('submit', pendingForm._guardHandler);
            pendingForm.submit();
        }
        closeModal();
    });

    document.querySelectorAll('form.delete-form').forEach(function(form) {
        function handler(e) {
            e.preventDefault();
            openModal(form);
        }
        form._guardHandler = handler;
        form.addEventListener('submit', handler);
    });

    // ── File input label update ────────────────────────────
    document.querySelectorAll('input[type="file"]').forEach(function(input) {
        input.addEventListener('change', function() {
            var nameSpan = document.getElementById(this.id + '_name');
            if (nameSpan) {
                nameSpan.textContent = this.files.length > 0 ? this.files[0].name : '';
            }
        });
    });
});