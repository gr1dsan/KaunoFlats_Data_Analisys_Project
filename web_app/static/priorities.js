let instance = null;
    const priority1 = document.getElementById('priority1');
    const priority2 = document.getElementById('priority2');

    priority1.addEventListener('change', function() {
        const selectedValue = this.value;

        priority2.disabled = !this.value;

        for (let option of priority2.options) {
            option.disabled = option.value === selectedValue;
        }

       if (priority2.value === selectedValue) {
           priority2.value = '';
        }
    });